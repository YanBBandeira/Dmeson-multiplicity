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
data_path = Path("../processed_data/df_dneta.pkl")
figures_dir = Path("../Figures/DnEta")
figures_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_pickle(data_path)

# Normaliza o nome da coluna caso tenha sido salva como corte_eta_ref
if "corte_eta_ref" in df.columns and "corte_eta" not in df.columns:
    df = df.rename(columns={"corte_eta_ref": "corte_eta"})


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

# Dicionários de Estilos Distintos (Cores, Marcadores e Estilos de Linha)
cores_ecm = {5020: "crimson", 9620: "forestgreen", 13000: "royalblue", 5.02: "crimson", 9.62: "forestgreen", 13.0: "royalblue"}
styles_ecm = {5020: "-", 9620: "--", 13000: "-.", 5.02: "-", 9.62: "--", 13.0: "-."}
markers_ecm = {5020: "o", 9620: "s", 13000: "^", 5.02: "o", 9.62: "s", 13.0: "^"}

cores_sistemas = {"pp": "black", "pO": "royalblue", "pPb": "crimson"}
styles_sistemas = {"pp": "-", "pO": "--", "pPb": "-."}
markers_sistemas = {"pp": "o", "pO": "s", "pPb": "^"}

cores_pt = {"pt_gt_0GeV": "black", "pt_gt_5GeV": "darkorange", "pt_gt_10GeV": "firebrick"}
styles_pt = {"pt_gt_0GeV": "-", "pt_gt_5GeV": "--", "pt_gt_10GeV": ":"}
markers_pt = {"pt_gt_0GeV": "o", "pt_gt_5GeV": "s", "pt_gt_10GeV": "D"}


def plot_dndeta_helper(
    df_sub, group_col, color_dict, style_dict, marker_dict, label_formatter, title_info, output_path
):
    """Função auxiliar para gerar os perfis dN/deta usando plt.step com traços e marcadores distintos."""
    fig, ax = plt.subplots(figsize=(8, 6))
    max_y_global = 0

    for val in sorted(df_sub[group_col].unique()):
        df_group = df_sub[df_sub[group_col] == val].sort_values("eta")

        x_vals = df_group["eta"].values
        y_vals = df_group["dN_deta"].values

        if len(x_vals) == 0:
            continue

        valid_mask = ~np.isnan(y_vals)
        x_plot = x_vals[valid_mask]
        y_plot = y_vals[valid_mask]

        if len(y_plot) == 0:
            continue

        ax.step(
            x_plot,
            y_plot,
            where="mid",
            label=label_formatter(val, df_group),
            color=color_dict.get(val, "gray"),
            linestyle=style_dict.get(val, "-"),
            linewidth=1.8
        )
        
        ax.plot(
            x_plot,
            y_plot,
            marker=marker_dict.get(val, "o"),
            linestyle="none",
            color=color_dict.get(val, "gray"),
            markersize=4
        )

        if np.max(y_plot) > max_y_global:
            max_y_global = np.max(y_plot)

    ax.set_xlim(-10.0, 10.0)
    if max_y_global > 0:
        ax.set_ylim(0, max_y_global * 1.35)

    ax.set_xlabel(r"$\eta$", fontsize=14)
    ax.set_ylabel(r"$\mathrm{d}N/\mathrm{d}\eta$", fontsize=14)

    ax.text(
        0.05,
        0.95,
        title_info,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="none", alpha=0.8),
    )

    ax.legend(loc="best", fontsize=10, frameon=False)
    ax.grid(True, which="both", linestyle=":", alpha=0.4)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


# =============================================================================
# 2. EXECUÇÃO PROCEDURAL DOS DIFERENTES COMPARATIVOS (dN/deta)
# =============================================================================
sistemas = df["sistema"].unique()
observaveis = df["observavel"].unique()
cortes = df["corte_eta"].unique()
ecms = df["ecm"].unique()
pt_cuts = df["pt_cut"].unique()

for dinamica in ["Hard", "Soft"]:
    for obs in observaveis:
        for pt_cut in pt_cuts:
            pt_str_label = pt_labels.get(pt_cut, str(pt_cut))

            # --- TIPO 1: Variação de eCM ---
            for sys in sistemas:
                for corte in cortes:
                    sub = df[
                        (df["sistema"] == sys)
                        & (df["dinamica"] == dinamica)
                        & (df["observavel"] == obs)
                        & (df["corte_eta"] == corte)
                        & (df["pt_cut"] == pt_cut)
                    ]
                    if sub.empty:
                        continue

                    ecm_val_display = lambda e: e / 1000.0 if e >= 1000 else e
                    ecm_unit = lambda e: "TeV" if e >= 1000 else "GeV"

                    fmt = lambda e, d: f"$\\sqrt{{s}} = {ecm_val_display(e):g}\\;\\mathrm{{{ecm_unit(e)}}}$"
                    eta_str = eta_labels.get(str(corte).strip().lower(), f"$|\\eta| < {corte}$")
                    title = f"PYTHIA 8 / Angantyr\nSystem: {sistema_labels.get(sys, sys)} ({dinamica})\nObs: {obs_labels.get(obs, obs)}\nCut ID: {eta_str} | {pt_str_label}"

                    out = figures_dir / "ecm_comparison" / sys / dinamica / obs / pt_cut / f"DnEta_ecm_{sys}_eta_{corte}.pdf"
                    plot_dndeta_helper(sub, "ecm", cores_ecm, styles_ecm, markers_ecm, fmt, title, out)

            # --- TIPO 2: Variação de Sistemas ---
            for ecm in ecms:
                for corte in cortes:
                    sub = df[
                        (df["ecm"] == ecm)
                        & (df["dinamica"] == dinamica)
                        & (df["observavel"] == obs)
                        & (df["corte_eta"] == corte)
                        & (df["pt_cut"] == pt_cut)
                    ]
                    if sub.empty:
                        continue

                    ecm_d = ecm / 1000.0 if ecm >= 1000 else ecm
                    unit_d = "TeV" if ecm >= 1000 else "GeV"

                    fmt = lambda s, d: f"{sistema_labels.get(s, s)}"
                    eta_str = eta_labels.get(str(corte).strip().lower(), f"$|\\eta| < {corte}$")
                    title = f"PYTHIA 8 / Angantyr\n$\\sqrt{{s}} = {ecm_d:g}\\;\\mathrm{{{unit_d}}}$ ({dinamica})\nObs: {obs_labels.get(obs, obs)}\nCut ID: {eta_str} | {pt_str_label}"

                    out = figures_dir / "system_comparison" / f"ecm_{ecm}" / dinamica / obs / pt_cut / f"DnEta_system_eta_{corte}.pdf"
                    plot_dndeta_helper(sub, "sistema", cores_sistemas, styles_sistemas, markers_sistemas, fmt, title, out)

            # --- TIPO 3: Variação de Cortes em pT ---
            for sys in sistemas:
                for ecm in ecms:
                    for corte in cortes:
                        sub = df[
                            (df["sistema"] == sys)
                            & (df["ecm"] == ecm)
                            & (df["dinamica"] == dinamica)
                            & (df["observavel"] == obs)
                            & (df["corte_eta"] == corte)
                        ]
                        if sub.empty:
                            continue

                        ecm_d = ecm / 1000.0 if ecm >= 1000 else ecm
                        unit_d = "TeV" if ecm >= 1000 else "GeV"

                        fmt = lambda pt, d: f"{pt_labels.get(pt, pt)}"
                        eta_str = eta_labels.get(str(corte).strip().lower(), f"$|\\eta| < {corte}$")
                        title = f"PYTHIA 8 / Angantyr\n{sistema_labels.get(sys, sys)} | $\\sqrt{{s}} = {ecm_d:g}\\;\\mathrm{{{unit_d}}}$ ({dinamica})\nObs: {obs_labels.get(obs, obs)}\nCut ID: {eta_str}"

                        out = figures_dir / "pt_comparison" / sys / f"ecm_{ecm}" / dinamica / obs / f"DnEta_pt_eta_{corte}.pdf"
                        plot_dndeta_helper(sub, "pt_cut", cores_pt, styles_pt, markers_pt, fmt, title, out)

print("Todos os comparativos de $\\mathrm{d}N/\\mathrm{d}\\eta$ gerados com sucesso!")