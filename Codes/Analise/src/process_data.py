import os
import glob
import numpy as np
import pandas as pd
from pathlib import Path

# =============================================================================
# 1. CONFIGURAÇÃO DE DIRETÓRIOS E LOGS
# =============================================================================
output_dir = Path("../../Output")
analysis_dir = Path("..")
log_dir = analysis_dir / "logs"
data_dir = analysis_dir / "processed_data"

log_dir.mkdir(parents=True, exist_ok=True)
data_dir.mkdir(parents=True, exist_ok=True)

log_path = log_dir / "validacao_analise.log"
log_file = open(log_path, "w", encoding="utf-8")

def log_print(texto):
    """Escreve no console e no arquivo de log simultaneamente."""
    print(texto)
    log_file.write(texto + "\n")

log_print("=" * 80)
log_print("INICIANDO PROCESSAMENTO, LIMPEZA E TESTES DE SANIDADE DOS DADOS DO PYTHIA")
log_print("=" * 80)

# =============================================================================
# 2. VARREDURA E PROCESSAMENTO DOS ARQUIVOS .DAT
# =============================================================================
registros = []

# Encontra todos os arquivos .dat recursivamente na pasta Output
arquivos_dat = list(output_dir.glob("**/*.dat"))
log_print(f"Total de arquivos .dat encontrados: {len(arquivos_dat)}\n")

for arq in arquivos_dat:
    # Exemplo de caminho: ../Output/pO/Hard_pO/eCM_13000_GeV/histcharmTotal0.dat
    partes = arq.relative_to(output_dir).parts
    
    if len(partes) < 4:
        continue
        
    sistema = partes[0]          # pO ou pPb
    dinamica_path = partes[1]    # Hard_pO, Soft_pPb, etc.
    dinamica = "Hard" if "Hard" in dinamica_path else "Soft"
    ecm_str = partes[2]          # eCM_13000_GeV ou eCM_13000GeV
    
    # Extrai apenas o número da energia em GeV
    ecm = int(''.join(filter(str.isdigit, ecm_str)))
    
    nome_arquivo = arq.name      # ex: histcharmTotal0.dat
    
    # Identifica o observável e o corte de eta/canal
    if "charmTotal" in nome_arquivo:
        observavel = "charmTotal"
    elif "cFinalPartonLevel" in nome_arquivo:
        observavel = "cFinalPartonLevel"
    elif "Dmeson" in nome_arquivo:
        observavel = "Dmeson"
    else:
        continue
        
    # Extrai o sufixo (número do corte de eta ou 'Asym')
    sufixo = nome_arquivo.replace("histcharmTotal", "").replace("histcFinalPartonLevel", "").replace("histDmeson", "").replace(".dat", "")

    # -------------------------------------------------------------------------
    # Leitura e Tratamento do Arquivo .dat (Remoção do Underflow)
    # -------------------------------------------------------------------------
    try:
        dados = np.loadtxt(arq)
    except Exception as e:
        log_print(f"[ERRO] Falha ao ler {arq}: {e}")
        continue
        
    if dados.ndim == 1:
        dados = dados.reshape(1, -1)
        
    # Remove o underflow (primeira linha do Hist do Pythia)
    if len(dados) > 1:
        dados = dados[1:]
        
    N_vals = dados[:, 0]
    counts = dados[:, 1]
    
    total_eventos = np.sum(counts)
    if total_eventos == 0:
        status = "ZERO_EVENTOS"
        P_N = np.zeros_like(counts)
        media_N = 0.0
        soma_prob = 0.0
    else:
        P_N = counts / total_eventos
        media_N = np.sum(N_vals * P_N)
        soma_prob = np.sum(P_N)
        
        # Teste de Sanidade para a normalização da probabilidade
        if np.isclose(soma_prob, 1.0, atol=1e-3):
            status = "OK"
        else:
            status = "ERRO_NORMALIZACAO"

    # Log individual resumido
    log_print(f"Sistema: {sistema:<4} | Din: {dinamica:<4} | eCM: {ecm:<5} GeV | Obs: {observavel:<18} | Corte: {sufixo:<5} | <N>: {media_N:<7.2f} | Status: {status}")

    # -------------------------------------------------------------------------
    # Armazenamento dos dados bin a bin para o DataFrame consolidado
    # -------------------------------------------------------------------------
    for n, c, pn in zip(N_vals, counts, P_N):
        registros.append({
            "sistema": sistema,
            "dinamica": dinamica,
            "ecm": ecm,
            "observavel": observavel,
            "corte_eta": sufixo,
            "N": int(n),
            "counts": c,
            "P_N": pn,
            "media_N": media_N
        })

# =============================================================================
# 3. CONSOLIDAÇÃO E SALVAMENTO DO DATAFRAME
# =============================================================================
df_analise = pd.DataFrame(registros)

caminho_saida_pkl = data_dir / "df_analise_consolidado.pkl"
df_analise.to_pickle(caminho_saida_pkl)

log_print("\n" + "=" * 80)
log_print(f"Processamento concluído com sucesso!")
log_print(f"DataFrame consolidado salvo em: {caminho_saida_pkl}")
log_print(f"Total de registros armazenados: {len(df_analise)}")
log_print("=" * 80)

log_file.close()