import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from pathlib import Path

# Aplica o estilo clássico do ROOT/ALICE
hep.style.use(hep.style.ROOT)

# =============================================================================
# 1. CARREGAMENTO DOS DADOS E CONFIGURAÇÕES
# =============================================================================
data_path = Path("../processed_data/df_analise_consolidado.pkl")
figures_dir = Path("../Figures/Multiplicity")
figures_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_pickle(data_path)

# Dicionário para títulos e rótulos
obs_labels = {
    "charmTotal": r"Total Charm ($c + \bar{c}$)",
    "cFinalPartonLevel": r"Final Parton Level Charm",
    "Dmeson": r"D Mesons ($D^0, D^\pm, D_s$)"
}

sistemas = df["sistema"].unique()
observaveis = df["observavel"].unique()
cortes = df["corte_eta"].unique()

cores_ecm = {5020: "crimson", 9620: "forestgreen", 13000: "royalblue"}

# =============================================================================
# 2. LOOP PROCEDURAL DE PLOTAGEM
# =============================================================================
for sistema in sistemas:
    for dinamica in ["Hard", "Soft"]:
        for obs in observaveis:
            for corte in cortes:
                
                # Filtra os dados no DataFrame
                df_sub = df[
                    (df["sistema"] == sistema) & 
                    (df["dinamica"] == dinamica) & 
                    (df["observavel"] == obs) & 
                    (df["corte_eta"] == corte)
                ]
                
                if df_sub.empty:
                    continue

                plt.figure(figsize=(8, 6))
                max_x_global = 0
                max_y_global = 0

                # Plot das curvas por energia eCM
                for ecm in sorted(df_sub["ecm"].unique()):
                    df_ecm = df_sub[df_sub["ecm"] == ecm].sort_values("N")
                    
                    x_vals = df_ecm["N"].values
                    y_vals = df_ecm["P_N"].values
                    media = df_ecm["media_N"].iloc[0]
                    
                    if len(x_vals) == 0:
                        continue

                    # Converte zeros para limites de log
                    y_vals_plot = np.where(y_vals <= 0, 1e-6, y_vals)

                    # Bins para hep.histplot
                    largura_bin = 1.0
                    bin_edges = np.append(x_vals - largura_bin / 2.0, x_vals[-1] + largura_bin / 2.0)

                    hep.histplot(
                        y_vals_plot,
                        bins=bin_edges,
                        histtype="step",
                        label=f"{ecm} GeV ($\\langle N \\rangle = {media:.2f}$)",
                        color=cores_ecm.get(ecm, "black"),
                        linewidth=1.8
                    )

                    # Ajuste de limites dinâmicos
                    indices_validos = np.where(y_vals > 0)[0]
                    if len(indices_validos) > 0:
                        max_local_x = x_vals[indices_validos[-1]]
                        if max_local_x > max_x_global:
                            max_x_global = max_local_x
                            
                    local_max_y = np.max(y_vals)
                    if local_max_y > max_y_global:
                        max_y_global = local_max_y

                # Formatação estática e eixos
                plt.yscale("log")
                plt.ylim(bottom=1e-5, top=max_y_global * 100 if max_y_global > 0 else 1.0)
                plt.xlim(left=-0.5, right=max_x_global * 1.2 if max_x_global > 0 else 20)

                plt.xlabel("$N$")
                plt.ylabel("$P(N)$")
                
                # Legendas e textos informativos
                corte_txt = f"Corte $\\eta$: {corte}"
                plt.text(0.05, 0.95, f"Pythia 8 Angantyr\n{sistema} ({dinamica})\n{obs_labels.get(obs, obs)}\n{corte_txt}", 
                         transform=plt.gca().transAxes, fontsize=11, verticalalignment="top")

                #plt.grid(True, which="both", linestyle="--", alpha=0.2)
                plt.legend(loc="best", fontsize=10, frameon=False)

                # Salvamento da figura
                subpasta_out = figures_dir / sistema / dinamica / obs
                subpasta_out.mkdir(parents=True, exist_ok=True)
                nome_fig = f"PN_{sistema}_{dinamica}_{obs}_eta_{corte}.pdf"
                
                plt.tight_layout()
                plt.savefig(subpasta_out / nome_fig, bbox_inches="tight")
                plt.close()

print("Plot de distribuições de multiplicidade P(N) concluído!")