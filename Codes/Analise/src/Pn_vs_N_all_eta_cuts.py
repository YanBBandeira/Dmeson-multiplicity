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
    "pO": r"$\mathrm{pO}$",
    "pPb": r"$\mathrm{pPb}$",
}

pt_labels = {
    "pt_gt_0GeV": r"$p_{\mathrm{T}} > 0\;\mathrm{GeV}/c$",
    "pt_gt_5GeV": r"$p_{\mathrm{T}} > 5\;\mathrm{GeV}/c$",
    "pt_gt_10GeV": r"$p_{\mathrm{T}} > 10\;\mathrm{GeV}/c$",
}

eta_labels_clean = {
    "0": r"|\eta| < 0.5",
    "0.5": r"|\eta| < 0.5",
    "1": r"|\eta| < 1.0",
    "1.0": r"|\eta| < 1.0",
    "2": r"|\eta| < 2.0",
    "2.0": r"|\eta| < 2.0",
    "3": r"|\eta| < 3.0",
    "3.0": r"|\eta| < 3.0",
    "4": r"|\eta| < 4.0",
    "4.0": r"|\eta| < 4.0",
    "5": r"|\eta| < 5.0",
    "5.0": r"|\eta| < 5.0",
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
    "5": 10,
    "5.0": 10,
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
    "pO": "--",  # Tracejada
    "pPb": "-.",  # Traço-ponto
}

# Diferentes marcadores para cada sistema
markers_sistemas = {
    "pp": "o",  # Círculo
    "pO": "s",  # Quadrado
    "pPb": "^",  # Triângulo
}

obs = {"charm": "cFinalPartonLevel", "Dmeson": "Dmeson"}
dinamica = "Soft"
pt_cut = "pt_gt_0GeV"

ecms = sorted(df["ecm"].unique())

for ecm in ecms:
    sub_ecm_dmeson = df[
        (df["ecm"] == ecm)
        & (df["dinamica"] == dinamica)
        & (df["observavel"] == obs["Dmeson"])
        & (df["pt_cut"] == pt_cut)
    ].copy()

    if sub_ecm_dmeson.empty:
        continue

    sub_ecm_dmeson["corte_str"] = sub_ecm_dmeson["corte_eta"].astype(str)
    sub_ecm_dmeson = sub_ecm_dmeson[sub_ecm_dmeson["corte_str"].isin(fatores_m.keys())]

    ecm_d = ecm / 1000.0 if ecm >= 1000 else ecm
    unit_d = "TeV" if ecm >= 1000 else "GeV"
    pt_str = pt_labels.get(pt_cut, str(pt_cut))

    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    global_ymin, global_ymax = 1e99, 0.0
    max_x_global = 0

    cortes_disponiveis = [
        c for c in sub_ecm_dmeson["corte_str"].unique() if c in fatores_m.keys()
    ]
    for corte in cortes_disponiveis:
        m = fatores_m[corte]
        print(corte, m)

        ultimo_x = 0
        ultimo_y = 0

        # 1. Sistema pp (Cor azul, linha cheia)
        sub_pp = sub_ecm_dmeson[
            (sub_ecm_dmeson["sistema"] == "pp") & (sub_ecm_dmeson["corte_str"] == corte)
        ].copy()
        if not sub_pp.empty:
            sub_pp["y_scaled"] = sub_pp["P_N"] * (10.0**m)
            gp = sub_pp.sort_values("N")
            xp, yp = gp["N"].values, gp["y_scaled"].values
            valid = yp > 0
            xp, yp = xp[valid], yp[valid]
            if len(yp) > 0:
                ax.step(
                    xp,
                    yp,
                    where="mid",
                    color=cores_sistemas["pp"],
                    linestyle=styles_sistemas["pp"],
                    alpha=0.9,
                )
                ax.plot(
                    xp,
                    yp,
                    marker=markers_sistemas["pp"],
                    linestyle="none",
                    color=cores_sistemas["pp"],
                    markersize=5,
                )
                max_x_global = max(max_x_global, xp[-1])
                global_ymin, global_ymax = min(global_ymin, np.min(yp)), max(
                    global_ymax, np.max(yp)
                )
                ultimo_x, ultimo_y = xp[-1], yp[-1]

        # 2. Sistema pO (Cor verde, linha cheia)
        sub_po = sub_ecm_dmeson[
            (sub_ecm_dmeson["sistema"] == "pO") & (sub_ecm_dmeson["corte_str"] == corte)
        ].copy()

        if not sub_po.empty:
            sub_po["y_scaled"] = sub_po["P_N"] * (10.0**m)
            gp = sub_po.sort_values("N")
            xp, yp = gp["N"].values, gp["y_scaled"].values
            valid = yp > 0
            xp, yp = xp[valid], yp[valid]
            if len(yp) > 0:
                ax.step(
                    xp,
                    yp,
                    where="mid",
                    color=cores_sistemas["pO"],
                    linestyle=styles_sistemas["pO"],
                    alpha=0.9,
                )
                ax.plot(
                    xp,
                    yp,
                    marker=markers_sistemas["pO"],
                    linestyle="none",
                    color=cores_sistemas["pO"],
                    markersize=5,
                )
                max_x_global = max(max_x_global, xp[-1])
                global_ymin, global_ymax = min(global_ymin, np.min(yp)), max(
                    global_ymax, np.max(yp)
                )
                ultimo_x, ultimo_y = max(ultimo_x, xp[-1]), yp[-1]

        # 3. Sistema pPb (Cor vermelha, linha cheia)
        sub_ppb = sub_ecm_dmeson[
            (sub_ecm_dmeson["sistema"] == "pPb")
            & (sub_ecm_dmeson["corte_str"] == corte)
        ].copy()
        if not sub_ppb.empty:
            sub_ppb["y_scaled"] = sub_ppb["P_N"] * (10.0**m)
            gp = sub_ppb.sort_values("N")
            xp, yp = gp["N"].values, gp["y_scaled"].values
            valid = yp > 0
            xp, yp = xp[valid], yp[valid]
            if len(yp) > 0:
                ax.step(
                    xp,
                    yp,
                    where="mid",
                    color=cores_sistemas["pPb"],
                    linestyle=styles_sistemas["pPb"],
                    alpha=0.9,
                )
                ax.plot(
                    xp,
                    yp,
                    marker=markers_sistemas["pPb"],
                    linestyle="none",
                    color=cores_sistemas["pPb"],
                    markersize=5,
                )
                max_x_global = max(max_x_global, xp[-1])
                global_ymin, global_ymax = min(global_ymin, np.min(yp)), max(
                    global_ymax, np.max(yp)
                )
                ultimo_x, ultimo_y = max(ultimo_x, xp[-1]), yp[-1]

        # Texto descritivo em PRETO ao lado da curva
        if ultimo_x > 0:
            ax.text(
                ultimo_x + max(0.5, max_x_global * 0.05),
                ultimo_y,
                f"$ {eta_labels_clean[corte]} \\ , \mathrm{{m}} = {m} $",
                color="black",
                fontsize=14,
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

    # Informações gerais da simulação no canto inferior direito
    info_titulo = (
            f"PYTHIA 8 / Angantyr\n"
            f"$\\sqrt{{s_{{NN}}}} = {ecm_d:g}\\;\\mathrm{{{unit_d}}}$"
      )

    ax.legend(
        title=info_titulo,
        handles=legend_elements,
        loc="upper right",
        bbox_to_anchor=(0.975, 0.975),
        frameon=False,
        fontsize = 13,
        title_fontsize = 12,
        labelspacing=0.3,
        handlelength=2.5,
        alignment="right",
     )

    # ax.text(0.95, 0.08, info_text, transform=ax.transAxes, fontsize=11, va="bottom", ha="right", bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='lightgray'))

    ax.set_yscale("log")
    ax.minorticks_on()

    ax.grid(linestyle=':', linewidth=0.6, alpha=0.7)

    ax.set_yscale("log")
    ax.set_xlabel(r"$N_{\mathrm{D}}$")                     
    ax.set_ylabel(r"$P(N_{\mathrm{D}}) \times 10^{\mathrm{m}}$")
    ax.set_xlim(-0.8, max_x_global * 1.65 if max_x_global > 0 else 20)

    if global_ymax > 0 and global_ymin < 1e99:
        ax.set_ylim(global_ymin * 0.1, global_ymax * 30)

    # Salvando 1 arquivo PDF para cada energia
    output_path = figures_dir / f"Pn_vs_N_all_eta_cuts_ecm_{ecm}.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

print(
    "Gráficos gerados com sucesso com o novo layout limpo, cores por sistema e texto no canto inferior direito!"
)
