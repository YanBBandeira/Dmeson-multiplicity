import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
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

obs_labels = {
    "charmTotal": r"Total Charm ($\mathrm{c} + \bar{\mathrm{c}}$)",
    "cFinalPartonLevel": r"Charm",
    "Dmeson": r"D Mesons ($D^0, D^\pm, D_s$)",
}

sistema_labels = {
    "pp": r"$\mathrm{pp}$",
    "pO": r"$\mathrm{p-O}$",
    "pPb": r"$\mathrm{p-Pb}$",
}

pt_labels = {
    "pt_gt_0GeV": r"$p_{\mathrm{T}} > 0\;\mathrm{GeV}/c$",
    "pt_gt_5GeV": r"$p_{\mathrm{T}} > 5\;\mathrm{GeV}/c$",
    "pt_gt_10GeV": r"$p_{\mathrm{T}} > 10\;\mathrm{GeV}/c$",
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

# Fator m de 0 até 5
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
    "5": 4,
    "5.0": 4,
}

# Cores fixas e distintas para cada sistema
# Cores de publicação para os sistemas
cores_sistemas = {
    "pp": "#1f77b4",  # Azul profissional
    "pO": "#ff7f0e",  # Laranja elegante
    "pPb": "#9467bd",  # Roxo sofisticado
}

# Diferentes estilos de linha para cada sistema
styles_sistemas = {
    "pp": "-",  # Linha cheia
    "pO": "-",  # Tracejada
    "pPb": "-",  # Traço-ponto
}

# Diferentes marcadores para cada sistema
markers_sistemas = {
    "pp": "o",  # Círculo
    "pO": "s",  # Quadrado
    "pPb": "^",  # Triângulo
}

cores_pt = {"pt_gt_0GeV": "#1f77b4", "pt_gt_5GeV": "#ff7f0e", "pt_gt_10GeV": "#9467bd"}
styles_pt = {"pt_gt_0GeV": "-", "pt_gt_5GeV": "--", "pt_gt_10GeV": "-."}
markers_pt = {"pt_gt_0GeV": "o", "pt_gt_5GeV": "s", "pt_gt_10GeV": "^"}

obs = {"charm": "cFinalPartonLevel", "Dmeson": "Dmeson"}
dinamica = "Soft"

sistemas = ["pp", "pO", "pPb"]
cortes_alvo = ["0", "5"]  # ou "0" e "5" conforme seu dataframe
pt_cuts_disponiveis = ["pt_gt_0GeV", "pt_gt_5GeV", "pt_gt_10GeV"]

for sistema in sistemas:
    fig, ax = plt.subplots()

    global_ymin, global_ymax = 1e99, 0.0
    max_x_global = 0

    # Percorre os cortes de eta (0.5 e 5.0)
    for corte in cortes_alvo:
        m = fatores_m.get(corte, 0)
        # Percorre os diferentes cortes de pT para gerar as curvas no mesmo gráfico
        for pt_c in pt_cuts_disponiveis:
            sub_df = df[
                (df["sistema"] == sistema)
                & (df["ecm"] == 13000)
                & (df["dinamica"] == dinamica)
                & (df["observavel"] == obs["Dmeson"])
                & (df["pt_cut"] == pt_c)
            ].copy()

            sub_df["corte_str"] = sub_df["corte_eta"].astype(str)
            sub_sub = sub_df[sub_df["corte_str"] == corte].copy()

            if sub_sub.empty:
                continue

            sub_sub["y_scaled"] = sub_sub["P_N"] * (10.0**m)
            gp = sub_sub.sort_values("N")
            xp, yp = gp["N"].values, gp["y_scaled"].values
            valid = yp > 0
            xp, yp = xp[valid], yp[valid]

            if len(yp) > 0:
                # Adiciona o label apenas na primeira passada para evitar itens duplicados na legenda (3 itens no total)
                label_name = pt_labels.get(pt_c, pt_c) if corte == cortes_alvo[0] else None

                ax.step(
                    xp, yp,
                    where="mid",
                    alpha=0.9,
                    color=cores_pt[pt_c],
                    linestyle=styles_pt[pt_c],
                    label=label_name
                )
                ax.plot(
                    xp, yp,
                    marker=markers_pt[pt_c],
                    linestyle="none",
                    color=cores_pt[pt_c],
                    markersize=4
                )

                max_x_global = max(max_x_global, xp[-1])
                global_ymin, global_ymax = min(global_ymin, np.min(yp)), max(global_ymax, np.max(yp))
                if pt_c == "pt_gt_0GeV":
                    ultimo_x, ultimo_y = xp[-1], yp[-1]

        # Texto ao lado da curva indicando o eta e o m daquele painel
        if ultimo_x > 0:
            ax.text(
                ultimo_x + max(0.5, max_x_global * 0.05),
                ultimo_y,
                f" {eta_labels_clean[corte]} $\\ , \mathrm{{m}} = {m} $",
                color="black",
                fontsize=12,
                va="center",
                ha="left",
        )
    # Legenda com as cores exatas de cada sistema
    legend_elements = [
        Line2D(
            [0],
            [0],
            color=cores_sistemas["pp"],
            linestyle=styles_sistemas["pp"],
            marker=markers_sistemas["pp"],
            linewidth=2.5,
            label=r"$\mathrm{pp}$",
        ),
        Line2D(
            [0],
            [0],
            color=cores_sistemas["pO"],
            linestyle=styles_sistemas["pO"],
            marker=markers_sistemas["pO"],
            linewidth=2.5,
            label=r"$\mathrm{p-O}$",
        ),
        Line2D(
            [0],
            [0],
            color=cores_sistemas["pPb"],
            linestyle=styles_sistemas["pPb"],
            marker=markers_sistemas["pPb"],
            linewidth=2.5,
            label=r"$\mathrm{p-Pb}$",
        ),
    ]                           

    # Título da legenda indicando o gerador e o sistema atual
    info_titulo = (
        f"PYTHIA 8 / Angantyr\n" f"{sistema_labels.get(sistema, sistema)} collision"
    )

    ax.legend(
        title=info_titulo,
        loc="upper right",
        bbox_to_anchor=(0.975, 0.975),
        frameon=False,
        fontsize=13,
        title_fontsize=12,
        labelspacing=0.3,
        handlelength=2.5,
        alignment="right",
    )

    # ax.text(0.95, 0.08, info_text, transform=ax.transAxes, fontsize=11, va="bottom", ha="right", bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='lightgray'))

    ax.set_yscale("log")
    ax.minorticks_on()

    ax.grid(linestyle=":", linewidth=0.6, alpha=0.7)

    ax.set_yscale("log")
    ax.set_xlabel(r"$N_{\mathrm{D}}$")
    ax.set_ylabel(r"$P(N_{\mathrm{D}}) \times 10^{\mathrm{m}}$")
    ax.set_xlim(-0.8, max_x_global * 1.65 if max_x_global > 0 else 20)

    if global_ymax > 0 and global_ymin < 1e99:
        ax.set_ylim(global_ymin * 0.1, global_ymax * 30)

    # Salvando 1 arquivo PDF para cada energia
    # Salvando 1 arquivo PDF para cada sistema
    output_path = figures_dir / f"Pn_vs_N_{sistema}_diff_eta_all_ptcuts.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

print(
    "Gráficos gerados com sucesso com o novo layout limpo, cores por sistema e texto no canto inferior direito!"
)
