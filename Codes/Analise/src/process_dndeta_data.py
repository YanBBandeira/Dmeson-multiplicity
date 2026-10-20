import os
import numpy as np
import pandas as pd
from pathlib import Path

output_dir = Path("../../Output")
analysis_dir = Path("..")
data_dir = analysis_dir / "processed_data"
log_dir = analysis_dir / "logs"

data_dir.mkdir(parents=True, exist_ok=True)
log_dir.mkdir(parents=True, exist_ok=True)

log_path = log_dir / "processamento_dneta.log"
log_file = open(log_path, "w", encoding="utf-8")

def log_print(texto):
    print(texto)
    log_file.write(texto + "\n")

log_print("="*90)
log_print("INICIANDO PROCESSAMENTO E TESTES DE SANIDADE DE dN/deta (CAMINHO CONDICIONAL)")
log_print("="*90)

# Tenta carregar o DataFrame de multiplicidade para o teste cruzado <N> vs Integral dN/deta
df_mult_path = data_dir / "df_multiplicidade.pkl"
df_mult = pd.read_pickle(df_mult_path) if df_mult_path.exists() else None

if df_mult is not None:
    log_print("DataFrame de multiplicidade carregado com sucesso para validação cruzada.")
else:
    log_print("AVISO: df_multiplicidade.pkl não encontrado. O teste cruzado com <N> será ignorado.")

registros_eta = []
arquivos_eta = list(output_dir.glob("**/pt_gt_*/*dNeta*.dat"))

log_print(f"Total de arquivos .dat de dN/deta encontrados: {len(arquivos_eta)}")
log_print("-" * 90)

for arq in arquivos_eta:
    partes = arq.relative_to(output_dir).parts
    if len(partes) < 5:
        continue
        
    sistema = partes[0]
    dinamica_path = partes[1]
    dinamica = "Hard" if "Hard" in dinamica_path else "Soft"
    ecm_str = partes[2]
    ecm = int(''.join(filter(str.isdigit, ecm_str)))
    pt_folder = partes[3] # ex: pt_gt_0GeV, pt_gt_5GeV, pt_gt_10GeV
    
    nome_arquivo = arq.name
    
    if "charmTotal" in nome_arquivo:
        observavel = "charmTotal"
        prefixo_mult = "histcharmTotal"
    elif "cFinalPartonLevel" in nome_arquivo:
        observavel = "cFinalPartonLevel"
        prefixo_mult = "histcFinalPartonLevel"
    elif "Dmeson" in nome_arquivo:
        observavel = "Dmeson"
        prefixo_mult = "histDmeson"
    else:
        continue
        
    sufixo = nome_arquivo.replace("dNeta_charmTotal", "").replace("dNeta_cFinalPartonLevel", "").replace("dNeta_Dmeson", "").replace(".dat", "")

    # 1. Localizar o arquivo de multiplicidade correspondente para extrair N_efetivos (N > 0)
    pasta_caso = arq.parent
    arq_mult = pasta_caso / f"{prefixo_mult}{sufixo}.dat"
    
    n_efetivos = 0
    if arq_mult.exists():
        try:
            dados_mult = np.loadtxt(arq_mult)
            if dados_mult.ndim == 1:
                dados_mult = dados_mult.reshape(1, -1)
            
            # Remove a primeira linha (N = 0) para seguir o caminho condicional
            if len(dados_mult) > 1:
                dados_mult_val = dados_mult[1:]
                n_efetivos = np.sum(dados_mult_val[:, 1]) # Soma das contagens de eventos com N >= 1
        except Exception as e:
            log_print(f"AVISO: Erro ao ler multiplicidade para {arq.name}: {e}")

    try:
        dados = np.loadtxt(arq)
    except Exception as e:
        log_print(f"ERRO ao ler {arq.name}: {e}")
        continue
        
    if dados.ndim == 1:
        dados = dados.reshape(1, -1)
        
    if len(dados) > 1:
        dados = dados[1:] # Remove underflow do dN/deta bruto
        
    eta_vals = dados[:, 0]
    conteudos_brutos = dados[:, 1] # Soma acumulada do eta das partículas nos eventos

    # 2. Normalização Condicional do dN/deta
    bin_width = eta_vals[1] - eta_vals[0] if len(eta_vals) > 1 else 1.0
    
    if n_efetivos > 0:
        # Divide pelo número de eventos efetivos (N > 0) e pela largura do bin
        dneta_vals = conteudos_brutos / (n_efetivos * bin_width)
    else:
        dneta_vals = np.zeros_like(conteudos_brutos)

    # TESTE DE SANIDADE: Integral do dN/deta normalizado vs <N> condicional
    integral_dneta = np.sum(dneta_vals * bin_width)
    
    comparacao_str = "N/A"
    if df_mult is not None:
        sub_mult = df_mult[
            (df_mult["sistema"] == sistema) & 
            (df_mult["dinamica"] == dinamica) & 
            (df_mult["ecm"] == ecm) & 
            (df_mult["pt_cut"] == pt_folder) & 
            (df_mult["observavel"] == observavel) & 
            (df_mult["corte_eta"] == sufixo)
        ]
        if not sub_mult.empty:
            media_n_ref = sub_mult["media_N"].iloc[0]
            
            # Tolerância pequena para lidar com precisão de ponto flutuante
            tolerancia = 1e-2 
            sao_iguais = abs(media_n_ref - integral_dneta) < tolerancia
            
            status_ok = " [OK]" if sao_iguais else ""
            comparacao_str = f"<N>={media_n_ref:.2f} | Int={integral_dneta:.2f}{status_ok}"

    log_print(f"Sistema: {sistema:<3} | Din: {dinamica:<4} | eCM: {ecm:<5} GeV | Pt: {pt_folder:<12} | Obs: {observavel:<18} | Eta: {sufixo:<5} | {comparacao_str}")

    for eta, val in zip(eta_vals, dneta_vals):
        registros_eta.append({
            "sistema": sistema,
            "dinamica": dinamica,
            "ecm": ecm,
            "pt_cut": pt_folder,
            "observavel": observavel,
            "corte_eta_ref": sufixo,
            "eta": eta,
            "dN_deta": val
        })

df_eta = pd.DataFrame(registros_eta)
df_eta.to_pickle(data_dir / "df_dneta.pkl")

log_print("="*90)
log_print(f"Processamento condicional de dN/deta concluído com sucesso!")
log_print(f"DataFrame consolidado salvo em: {data_dir / 'df_dneta.pkl'}")
log_print(f"Total de registros armazenados: {len(df_eta)}")
log_print("="*90)

log_file.close()