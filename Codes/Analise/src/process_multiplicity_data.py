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

log_path = log_dir / "processamento_multiplicidade.log"
log_file = open(log_path, "w", encoding="utf-8")

def log_print(texto):
    print(texto)
    log_file.write(texto + "\n")

log_print("Iniciando processamento dos dados de Multiplicidade...")

registros = []
arquivos_dat = list(output_dir.glob("**/pt_gt_*/*hist*.dat"))

for arq in arquivos_dat:
    partes = arq.relative_to(output_dir).parts
    if len(partes) < 5:
        continue
        
    sistema = partes[0]
    dinamica_path = partes[1]
    dinamica = "Hard" if "Hard" in dinamica_path else "Soft"
    ecm_str = partes[2]
    ecm = int(''.join(filter(str.isdigit, ecm_str)))
    pt_folder = partes[3]
    
    nome_arquivo = arq.name
    
    if "charmTotal" in nome_arquivo:
        observavel = "charmTotal"
    elif "cFinalPartonLevel" in nome_arquivo:
        observavel = "cFinalPartonLevel"
    elif "Dmeson" in nome_arquivo:
        observavel = "Dmeson"
    else:
        continue
        
    sufixo = nome_arquivo.replace("histcharmTotal", "").replace("histcFinalPartonLevel", "").replace("histDmeson", "").replace(".dat", "")

    try:
        dados = np.loadtxt(arq)
    except Exception:
        continue
        
    if dados.ndim == 1:
        dados = dados.reshape(1, -1)
        
    if len(dados) > 1:
        dados = dados[1:] # Remove underflow
        
    N_vals = dados[:, 0]
    counts = dados[:, 1]
    
    total_eventos = np.sum(counts)
    if total_eventos == 0:
        continue
        
    P_N = counts / total_eventos
    soma_probabilidades = np.sum(P_N)
    status_sanidade = "OK" if np.isclose(soma_probabilidades, 1.0, atol=1e-4) else f"FALHA (Soma={soma_probabilidades:.4f})"
    media_N = np.sum(N_vals * P_N)

    # Log detalhado por arquivo processado
    log_print(f"Sistema: {sistema:<3} | Din: {dinamica:<4} | eCM: {ecm:<5} GeV | Pt: {pt_folder:<12} | Obs: {observavel:<18} | Eta: {sufixo:<5} | <N>: {media_N:<6.2f} | Sanidade P(N)=1: {status_sanidade}")

    for n, c, pn in zip(N_vals, counts, P_N):
        registros.append({
            "sistema": sistema,
            "dinamica": dinamica,
            "ecm": ecm,
            "pt_cut": pt_folder,
            "observavel": observavel,
            "corte_eta": sufixo,
            "N": int(n),
            "counts": c,
            "P_N": pn,
            "media_N": media_N
        })

df_mult = pd.DataFrame(registros)
df_mult.to_pickle(data_dir / "df_multiplicidade.pkl")
log_print(f"Processamento concluído! Total de registros: {len(df_mult)}")
log_file.close()