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
figures_dir = Path("../Figures/Multiplicity")
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

# Dicionário completo e centralizado para todos os cortes em eta (em padrão LaTeX estrito)
eta_labels = {
    "0.5": r"$|\eta| < 0.5$",
    "1.0": r"$|\eta| < 1.0$",
    "1.5": r"$|\eta| < 1.5$",
    "2.0": r"$|\eta| < 2.0$",
    "2.4": r"$|\eta| < 2.4$",
    "5.0": r"$|\eta| < 5.0$",
    "asym": r"$-3.1 < \eta < 5.0$",
    "assymetric": r"$-3.1 < \eta < 5.0$",
    "-3.1_5.0": r"$-3.1 < \eta < 5.0$",
    "asymmetric": r"$-3.1 < \eta < 5.0$",
}

def format_eta_cut(corte):
    """Retorna o rótulo em LaTeX correspondente ao corte em eta."""
    corte_key = str(corte).strip().lower()
    # Busca no dicionário; se não encontrar, aplica o formato padrão em LaTeX dinamicamente
    return eta_labels.get(corte_key, f"$|\\eta| < {corte}$")

# Paletas de cores para diferentes modos
cores_ecm = {
    5020: "crimson",
    9620: "forestgreen",
    13000: "royalblue",
    5.02: "crimson",
    9.62: "forestgreen",
    13.0: "royalblue",
}
cores_sistemas = {"pp": "black", "pO": "royalblue", "pPb": "crimson"}


def plot_helper(
    df_sub, group_col, color_dict, label_formatter, title_info, output_path
):
    """Função auxiliar genérica utilizando plt.step com eixo x expandido para 2x."""
    fig, ax = plt.subplots(figsize=(8, 6))
    max_x_global = 0
    max_y_global = 0

    for val in sorted(df_sub[group_col].unique()):
        df_group = df_sub[df_sub[group_col] == val].sort_values("N")

        x_vals = df_group["N"].values
        y_vals = df_group["P_N"].values

        if len(x_vals) == 0:
            return

        valid_mask = y_vals > 0
        x_plot = x_vals[valid_mask]
        y_plot = y_vals[valid_mask]

        if len(y_plot) == 0:
            continue

        # Plot limpo e direto com plt.step
        ax.step(
            x_plot,
            y_plot,
            where="mid",
            label=label_formatter(val, df_group),
            color=color_dict.get(val, "gray"),
            linewidth=1.8
        )

        if x_plot[-1] > max_x_global:
            max_x_global = x_plot[-1]
        if np.max(y_plot) > max_y_global:
            max_y_global = np.max(y_plot)

    ax.set_yscale("log")
    if max_y_global > 0:
        ax.set_ylim(1e-5, max_y_global * 50)
    
    # Eixo x esticado para o dobro (2x) do último ponto válido
    ax.set_xlim(-0.5, max_x_global * 2.0 if max_x_global > 0 else 20)

    ax.set_xlabel(r"$N$", fontsize=14)
    ax.set_ylabel(r"$P(N)$", fontsize=14)

    ax.text(
        0.05,
        0.95,
        title_info,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="none", alpha=0.8),
    )

    ax.legend(loc="upper right", fontsize=10, frameon=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


# =============================================================================
# 2. EXECUÇÃO PROCEDURAL DOS DIFERENTES COMPARATIVOS
# =============================================================================
sistemas = df["sistema"].unique()
observaveis = df["observavel"].unique()
cortes = df["corte_eta"].unique()
ecms = df["ecm"].unique()

for dinamica in ["Hard", "Soft"]:
    for obs in observaveis:

        # --- TIPO 1: Variação de eCM (Mantém sistema e corte fixos) ---
        for sys in sistemas:
            for corte in cortes:
                sub = df[
                    (df["sistema"] == sys)
                    & (df["dinamica"] == dinamica)
                    & (df["observavel"] == obs)
                    & (df["corte_eta"] == corte)
                ]
                if sub.empty:
                    continue

                ecm_val_display = lambda e: e / 1000.0 if e >= 1000 else e
                ecm_unit = lambda e: "TeV" if e >= 1000 else "GeV"

                fmt = (
                    lambda e, d: f"$\\sqrt{{s}} = {ecm_val_display(e):g}\\;\\mathrm{{{ecm_unit(e)}}}$ ($\\langle N \\rangle = {d['media_N'].iloc[0]:.2f}$)"
                )
                eta_str = format_eta_cut(corte)
                title = f"PYTHIA 8 / Angantyr\nSystem: {sistema_labels.get(sys, sys)} ({dinamica})\nObs: {obs_labels.get(obs, obs)}\n{eta_str}"

                out = (
                    figures_dir
                    / "ecm_comparison"
                    / sys
                    / dinamica
                    / obs
                    / f"PN_ecm_{sys}_eta_{corte}.pdf"
                )
                plot_helper(sub, "ecm", cores_ecm, fmt, title, out)

        # --- TIPO 2: Variação de Sistemas (Mantém eCM e corte fixos) ---
        for ecm in ecms:
            for corte in cortes:
                sub = df[
                    (df["ecm"] == ecm)
                    & (df["dinamica"] == dinamica)
                    & (df["observavel"] == obs)
                    & (df["corte_eta"] == corte)
                ]
                if sub.empty:
                    continue

                ecm_d = ecm / 1000.0 if ecm >= 1000 else ecm
                unit_d = "TeV" if ecm >= 1000 else "GeV"

                fmt = (
                    lambda s, d: f"{sistema_labels.get(s, s)} ($\\langle N \\rangle = {d['media_N'].iloc[0]:.2f}$)"
                )
                eta_str = format_eta_cut(corte)
                title = f"PYTHIA 8 / Angantyr\n$\\sqrt{{s}} = {ecm_d:g}\\;\\mathrm{{{unit_d}}}$ ({dinamica})\nObs: {obs_labels.get(obs, obs)}\n{eta_str}"

                out = (
                    figures_dir
                    / "system_comparison"
                    / f"ecm_{ecm}"
                    / dinamica
                    / obs
                    / f"PN_system_eta_{corte}.pdf"
                )
                plot_helper(sub, "sistema", cores_sistemas, fmt, title, out)

print("Todos os comparativos de P(N) gerados com sucesso com eta_labels abrangente e eixo x expandido!")