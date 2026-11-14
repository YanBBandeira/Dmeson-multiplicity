import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from pathlib import Path

plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "figure.figsize": (7.5, 6.5),
        "figure.dpi": 300,
        "font.size": 15,
        "axes.labelsize": 18,
        "axes.titlesize": 18,
        "xtick.labelsize": 15,
        "ytick.labelsize": 15,
        "legend.fontsize": 12,
        "axes.linewidth": 2.0,
        "xtick.major.width": 2.0,
        "ytick.major.width": 2.0,
        "xtick.minor.width": 1.5,
        "ytick.minor.width": 1.5,
        "xtick.major.size": 7.0,
        "ytick.major.size": 7.0,
        "xtick.minor.size": 4.0,
        "ytick.minor.size": 4.0,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "axes.formatter.limits": [-2, 3],
        "axes.formatter.use_mathtext": True,
        "grid.linestyle": ":",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.7,
        "grid.color": "gray",
        "lines.linewidth": 2.5,
        "legend.handlelength": 2.0,
        "legend.labelspacing": 0.05,
        "legend.borderaxespad": 0.1,
    }
)

# 1. Carregamento dos dados e configurações
data_file = Path("../processed_data/df_multiplicidade.pkl")
figures_dir = Path("../Figures/Article_figs")
figures_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_pickle(data_file)

sistema_labels = {
    "pp": r"$\mathrm{pp}$",
    "pO": r"$\mathrm{pO}$",
    "pPb": r"$\mathrm{pPb}$",
}

eta_labels_clean = {
    "0": r"$|\eta| < 0.5$",
    "0.5": r"$|\eta| < 0.5$",
    "1": r"$|\eta| < 1.0$",
    "1.0": r"$|\eta| < 1.0$",
    "2": r"$|\eta| < 2.0$",
    "2.0": r"$|\eta| < 2.0$",
    "3": r"$|\eta| < 3.0$",
    "3.0": r"$|\eta| < 3.0$",
    "4": r"$|\eta| < 4.0$",
    "4.0": r"$|\eta| < 4.0$",
    "5": r"$|\eta| < 5.0$",
    "5.0": r"$|\eta| < 5.0$",
}

fatores_m = {
    "0": 0,
    "0.5": 0,
    "1": 2,
    "1.0": 2,
    "2": 4,
    "2.0": 4,
    "3": 6,
    "3.0": 6,
    "4": 8,
    "4.0": 8,
    "5": 10,
    "5.0": 10,
}

# Cores, estilos e marcadores seguindo rigorosamente o padrão do código legado
cores_sistemas = {
    "pp": "#1f77b4",  # Azul profissional
    "pO": "#ff7f0e",  # Laranja elegante
    "pPb": "#9467bd", # Roxo sofisticado
}

styles_sistemas = {
    "pp": "-",
    "pO": "--",
    "pPb": "-.",
}

markers_sistemas = {
    "pp": "o",
    "pO": "s",
    "pPb": "^",
}

obs = {"charm": "cFinalPartonLevel", "Dmeson": "Dmeson"}
dinamica = "Soft"
pt_cut = "pt_gt_0GeV"

cortes_alvo = ["0.5", "1.0", "2.0", "3.0", "4.0", "5.0"]


fig, ax = plt.subplots(figsize=(7.5, 6.5))
for corte in cortes_alvo:
    global_ymin, global_ymax = 1e99, 0.0
    max_x_global = 0
    plot_gerado = False
    
    ultimo_x = 0
    ultimo_y = 0
    
    # Recupera o fator m para o corte de eta atual
    m = fatores_m.get(corte, 1)
    print(m)

    # Filtra dados gerais do corte de eta atual para otimizar
    sub_df = df[
        (df["dinamica"] == dinamica)
        & (df["observavel"] == obs["Dmeson"])
        & (df["pt_cut"] == pt_cut)
    ].copy()

    sub_df["corte_str"] = sub_df["corte_eta"].astype(str)
    
    if corte in ["0", "0.5"]:
        sub_corte_eta = sub_df[sub_df["corte_str"].isin(["0", "0.5", "0.0"])]
    else:
        sub_corte_eta = sub_df[sub_df["corte_str"].isin([corte, f"{float(corte):.1f}", f"{int(float(corte))}"])]

    # 1. Sistema pp
    sub_pp = sub_corte_eta[sub_corte_eta["sistema"] == "pp"].copy()
    if not sub_pp.empty:
        agg_pp = sub_pp.groupby("ecm")["media_N"].first().reset_index().sort_values("ecm")
        x_vals, y_vals = agg_pp["ecm"].values /1000, agg_pp["media_N"].values + m
        print(x_vals, y_vals)
        valid = y_vals > 0
        x_vals, y_vals = x_vals[valid], y_vals[valid]
        if len(y_vals) > 0:
            plot_gerado = True
            ax.plot(
                x_vals, y_vals,
                marker=markers_sistemas["pp"],
                color=cores_sistemas["pp"],
                linestyle=styles_sistemas["pp"],
                linewidth=2.0, markersize=6, alpha=0.9
            )
            max_x_global = max(max_x_global, x_vals[-1])
            global_ymin, global_ymax = min(global_ymin, np.min(y_vals)), max(global_ymax, np.max(y_vals))
            ultimo_x, ultimo_y = x_vals[-1], y_vals[-1]

    # 2. Sistema pO
    sub_po = sub_corte_eta[sub_corte_eta["sistema"] == "pO"].copy()
    if not sub_po.empty:
        agg_po = sub_po.groupby("ecm")["media_N"].first().reset_index().sort_values("ecm")
        x_vals, y_vals = agg_po["ecm"].values / 1000, agg_po["media_N"].values + m
        valid = y_vals > 0
        x_vals, y_vals = x_vals[valid], y_vals[valid]
        if len(y_vals) > 0:
            plot_gerado = True
            ax.plot(
                x_vals, y_vals,
                marker=markers_sistemas["pO"],
                color=cores_sistemas["pO"],
                linestyle=styles_sistemas["pO"],
                linewidth=2.0, markersize=6, alpha=0.9
            )
            max_x_global = max(max_x_global, x_vals[-1])
            global_ymin, global_ymax = min(global_ymin, np.min(y_vals)), max(global_ymax, np.max(y_vals))
            ultimo_x, ultimo_y = max(ultimo_x, x_vals[-1]), y_vals[-1]

    # 3. Sistema pPb
    sub_ppb = sub_corte_eta[sub_corte_eta["sistema"] == "pPb"].copy()
    if not sub_ppb.empty:
        agg_ppb = sub_ppb.groupby("ecm")["media_N"].first().reset_index().sort_values("ecm")
        x_vals, y_vals = agg_ppb["ecm"].values / 1000, agg_ppb["media_N"].values + m
        valid = y_vals > 0
        x_vals, y_vals = x_vals[valid], y_vals[valid]
        if len(y_vals) > 0:
            plot_gerado = True
            ax.plot(
                x_vals, y_vals,
                marker=markers_sistemas["pPb"],
                color=cores_sistemas["pPb"],
                linestyle=styles_sistemas["pPb"],
                linewidth=2.0, markersize=6, alpha=0.9
            )
            max_x_global = max(max_x_global, x_vals[-1])
            global_ymin, global_ymax = min(global_ymin, np.min(y_vals)), max(global_ymax, np.max(y_vals))
            ultimo_x, ultimo_y = max(ultimo_x, x_vals[-1]), y_vals[-1]

    if not plot_gerado:
        plt.close(fig)
        continue

    # Texto descritivo em PRETO ao lado da última curva (exatamente como no modelo legado)
    eta_str = eta_labels_clean.get(corte, f"$|\\eta| < {corte}$")
    if ultimo_x > 0:
        ax.text(
            ultimo_x * 1.02,
            ultimo_y * 0.95,
            f"{eta_str} $\\ , \\, \\mathrm{{m}} = {m}$",
            color="black",
            fontsize=14,
            va="center",
            ha="left",
        )

# Legenda com as cores exatas de cada sistema
legend_elements = [
    Line2D([0], [0], color=cores_sistemas["pp"], linestyle=styles_sistemas["pp"], marker=markers_sistemas["pp"], linewidth=2.5, label=r"$\mathrm{pp}$"),
    Line2D([0], [0], color=cores_sistemas["pO"], linestyle=styles_sistemas["pO"], marker=markers_sistemas["pO"], linewidth=2.5, label=r"$\mathrm{p-O}$"),
    Line2D([0], [0], color=cores_sistemas["pPb"], linestyle=styles_sistemas["pPb"], marker=markers_sistemas["pPb"], linewidth=2.5, label=r"$\mathrm{p-Pb}$"),
]

info_titulo = "PYTHIA 8 / Angantyr"

ax.legend(
    title=info_titulo,
    handles=legend_elements,
    loc="upper right",
    bbox_to_anchor=(0.975, 0.975),
    frameon=False,
    fontsize=13,
    title_fontsize=12,
    labelspacing=0.3,
    handlelength=2.5,
    alignment="right",
)

ax.set_xlim(4,18)
ax.set_ylim(0,16)
ax.minorticks_on()
ax.grid(linestyle=":", linewidth=0.6, alpha=0.7)

ax.set_xlabel(r"$\sqrt{s_{\mathrm{NN}}}\;(\mathrm{TeV})$")
ax.set_ylabel(r"$\langle N_{\mathrm{D}} \rangle = \sum N_{\mathrm{D}}P(N_{\mathrm{D}})  + {\mathrm{m}}$")


# Salvando 1 arquivo PDF para cada corte de eta
output_path = figures_dir / f"MeanN_vs_ecm_all_eta_cuts.pdf"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print("Gráficos de $\\langle N_{\\mathrm{D}} \\rangle$ vs $\\sqrt{s_{\\mathrm{NN}}}$ gerados com sucesso com blocos separados `sub_pp`, `sub_pO` e `sub_pPb` e texto lateral alinhado!")