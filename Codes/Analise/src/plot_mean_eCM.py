from pathlib import Path
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import pandas as pd

# Aplica o estilo clássico do ROOT/ALICE
hep.style.use(hep.style.ROOT)

# =============================================================================
# 1. CARREGAMENTO DOS DADOS E CONFIGURAÇÕES
# =============================================================================
data_path = Path("../processed_data/df_multiplicidade.pkl")
figures_dir = Path("../Figures/Mean_Multiplicity")
figures_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_pickle(data_path)

obs_labels = {
    "charmTotal": r"Total Charm ($\mathrm{c} + \bar{\mathrm{c}}$)",
    "cFinalPartonLevel": r"Final Parton Level Charm",
    "Dmeson": r"D Mesons ($D^0, D^\pm, D_s$)",
}

sistema_labels = {
    "pp": r"$\mathrm{pp}$",
    "pO": r"$\mathrm{pO}$",
    "pPb": r"$\mathrm{pPb}$",
}

eta_labels = {
    "0": r"$|\eta| < 0.5$",
    "1": r"$|\eta| < 1.0$",
    "2": r"$|\eta| < 2.0$",
    "3": r"$|\eta| < 3.0$",
    "4": r"$|\eta| < 4.0$",
    "5": r"$|\eta| < 5.0$",
    "6": r"$|\eta| < 6.0$",
    "7": r"$|\eta| < 7.0$",
    "asym": r"$-3.1 < \eta < 5.0$",
    "assymetric": r"$-3.1 < \eta < 5.0$",
    "-3.1_5.0": r"$-3.1 < \eta < 5.0$",
    "asymmetric": r"$-3.1 < \eta < 5.0$",
}

pt_labels = {
    "pt_gt_0GeV": r"$p_{\mathrm{T}} > 0\;\mathrm{GeV}/c$",
    "pt_gt_5GeV": r"$p_{\mathrm{T}} > 5\;\mathrm{GeV}/c$",
    "pt_gt_10GeV": r"$p_{\mathrm{T}} > 10\;\mathrm{GeV}/c$"
}

# Cores, estilos de linha e marcadores distintos para os sistemas
cores_sistemas = {"pp": "black", "pO": "royalblue", "pPb": "crimson"}
styles_sistemas = {"pp": "-", "pO": "--", "pPb": "-."}
markers_sistemas = {"pp": "o", "pO": "s", "pPb": "^"}

# =============================================================================
# 2. EXECUÇÃO PROCEDURAL DE PLOTAGEM (<N> vs eCM)
# =============================================================================
sistemas = df["sistema"].unique()
observaveis = df["observavel"].unique()
cortes = df["corte_eta"].unique()
pt_cuts = df["pt_cut"].unique()

for dinamica in ["Hard", "Soft"]:
    for obs in observaveis:
        for pt_cut in pt_cuts:
            for corte in cortes:
                
                fig, ax = plt.subplots(figsize=(8, 6))
                plot_gerado = False

                for sistema in sistemas:
                    # Filtra dados para o sistema, dinâmica, observável, corte de pT e eta atuais
                    sub = df[
                        (df["sistema"] == sistema)
                        & (df["dinamica"] == dinamica)
                        & (df["observavel"] == obs)
                        & (df["pt_cut"] == pt_cut)
                        & (df["corte_eta"] == corte)
                    ].sort_values("ecm")

                    if sub.empty:
                        continue

                    # Extrai os valores únicos de ecm e media_N correspondentes
                    agg_sub = sub.groupby("ecm")["media_N"].first().reset_index()

                    x_vals = agg_sub["ecm"].values
                    y_vals = agg_sub["media_N"].values

                    if len(x_vals) == 0:
                        continue

                    plot_gerado = True
                    ax.plot(
                        x_vals,
                        y_vals,
                        marker=markers_sistemas.get(sistema, "o"),
                        linestyle=styles_sistemas.get(sistema, "-"),
                        linewidth=1.8,
                        markersize=6,
                        color=cores_sistemas.get(sistema, "black"),
                        label=sistema_labels.get(sistema, sistema)
                    )

                if not plot_gerado:
                    plt.close(fig)
                    continue

                # Formatação estática rigorosa em LaTeX
                ax.set_xlabel(r"$\sqrt{s}\;(\mathrm{GeV})$", fontsize=14)
                ax.set_ylabel(r"$\langle N \rangle$", fontsize=14)

                eta_str = eta_labels.get(str(corte).strip().lower(), f"$|\\eta| < {corte}$")
                pt_str_label = pt_labels.get(pt_cut, str(pt_cut))
                
                title_info = (
                    f"PYTHIA 8 / Angantyr\n"
                    f"Dynamics: {dinamica}\n"
                    f"Obs: {obs_labels.get(obs, obs)}\n"
                    f"{eta_str} | {pt_str_label}"
                )
                
                ax.text(
                    0.05,
                    0.95,
                    title_info,
                    transform=ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="none", alpha=0.8),
                )

                ax.legend(loc="upper left", fontsize=10, frameon=False)
                ax.grid(True, which="both", linestyle=":", alpha=0.4)

                # Salvamento estruturado em subpastas organizadas por pT
                subpasta_out = figures_dir / dinamica / obs / pt_cut
                subpasta_out.mkdir(parents=True, exist_ok=True)
                nome_fig = f"MeanN_vs_eCM_eta_{corte}.pdf"

                plt.tight_layout()
                plt.savefig(subpasta_out / nome_fig, dpi=300, bbox_inches="tight")
                plt.close()

print("Todos os plots de $\\langle N \\rangle$ vs $\\sqrt{s}$ gerados com sucesso!")