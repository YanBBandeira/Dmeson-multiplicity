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
figures_dir = Path("../Figures/N_mean")
figures_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_pickle(data_path)

obs_labels = {
    "charmTotal": r"Total Charm ($c + \bar{c}$)",
    "cFinalPartonLevel": r"Final Parton Level Charm",
    "Dmeson": r"D Mesons ($D^0, D^\pm, D_s$)"
}

# Agrupa para obter <N> único por combinação de (sistema, dinamica, ecm, observavel, corte_eta)
df_media = df.groupby(["sistema", "dinamica", "ecm", "observavel", "corte_eta"])["media_N"].first().reset_index()

sistemas = df_media["sistema"].unique()
observaveis = df_media["observavel"].unique()
cortes = df_media["corte_eta"].unique()

# =============================================================================
# 2. LOOP PROCEDURAL DE PLOTAGEM DA MÉDIA <N> vs sqrt(s)
# =============================================================================
for sistema in sistemas:
    for obs in observaveis:
        for corte in cortes:
            
            df_sub = df_media[
                (df_media["sistema"] == sistema) & 
                (df_media["observavel"] == obs) & 
                (df_media["corte_eta"] == corte)
            ]
            
            if df_sub.empty:
                continue

            plt.figure(figsize=(8, 6))

            # Plota Hard e Soft na mesma figura para comparação
            for dinamica, cor, marker in [("Hard", "crimson", "o"), ("Soft", "royalblue", "s")]:
                df_din = df_sub[df_sub["dinamica"] == dinamica].sort_values("ecm")
                
                if df_din.empty:
                    continue

                x_ecm = df_din["ecm"].values
                y_mean = df_din["media_N"].values

                plt.plot(
                    x_ecm, 
                    y_mean, 
                    marker=marker, 
                    color=cor, 
                    linestyle="-", 
                    linewidth=2.0, 
                    markersize=8, 
                    label=f"{dinamica} Process"
                )

            plt.xlabel(r"$\sqrt{s_{\mathrm{NN}}}$ [GeV]")
            plt.ylabel(r"$\langle N \rangle$")
            #plt.xscale("log")
            
            # Ajusta xlim para cobrir de 4000 a 15000 GeV
            plt.xlim(4000, 15000)
            
            # Texto explicativo
            plt.text(0.05, 0.88, f"Pythia 8 Angantyr\nSistema: {sistema}\n{obs_labels.get(obs, obs)}\nCorte $\\eta$: {corte}", 
                     transform=plt.gca().transAxes, fontsize=11, verticalalignment="top")

            #plt.grid(True, which="both", linestyle="--", alpha=0.2)
            plt.legend(loc="best", fontsize=11, frameon=False)

            # Salvamento da figura
            subpasta_out = figures_dir / sistema / obs
            subpasta_out.mkdir(parents=True, exist_ok=True)
            nome_fig = f"MeanN_vs_eCM_{sistema}_{obs}_eta_{corte}.pdf"

            plt.tight_layout()
            plt.savefig(subpasta_out / nome_fig, bbox_inches="tight")
            plt.close()

print("Plot da média <N> vs sqrt(s) concluído com sucesso!")