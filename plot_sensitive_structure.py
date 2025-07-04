import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import numpy as np
import pandas as pd
from fresnel_utils import getFresnelAIM
from performance_metrics import calculate_theta_res_smooth
from plot_utils import save_figure
from plot_style import apply_plot_style

# Font
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None

# Cores por metal
METAL_COLORS = {
    "Ag": "#2ca02c",  # Verde
    "Au": "#1f77b4",  # Azul
    "Cu": "#d62728"   # Vermelho
}

def plot_figures_of_merit_comparative(results_dict, thicknesses_nm, save_dir):
    apply_plot_style()
    os.makedirs(save_dir, exist_ok=True)

    metrics = ["theta_res", "fwhm", "sensitivity_empirical", "sensitivity_theoretical", "chi", "Q"]
    ylabels = {
        "theta_res": "θres (°)",
        "fwhm": "FWHM (°)",
        "sensitivity_empirical": "Sensitivity (emp.) (°/RIU)",
        "sensitivity_theoretical": "Sensitivity (theor.) (°/RIU)",
        "chi": "χ (RIU⁻¹)",
        "Q": "Q (RIU⁻¹)"
    }

    for metric in metrics:
        plt.figure(figsize=(10, 6))

        for metal in ["Ag", "Au", "Cu"]:
            values = results_dict[metal][metric]
            color = METAL_COLORS[metal]

            # Curva com cor do metal (abaixo)
            plt.plot(thicknesses_nm, values,
                     color=color,
                     label=metal,
                     linewidth=1.8,
                     zorder=1.5)

            # Pontos pretos por cima
            plt.scatter(thicknesses_nm, values,
                        color='black',
                        s=30,
                        zorder=3)

        if TNR:
            plt.xlabel("Metal thickness (nm)", fontsize=14, fontproperties=TNR)
            plt.ylabel(ylabels[metric], fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(fontsize=10, prop=TNR)
        else:
            plt.xlabel("Metal thickness (nm)", fontsize=14)
            plt.ylabel(ylabels[metric], fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=10)

        plt.grid(True)
        plt.tight_layout()

        filename = os.path.join(save_dir, f"{metric}_vs_thickness")
        save_figure(filename)
        plt.close()

def plot_angular_response_for_sensitive_structure_and_export_csv(
    materials, lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, substrate, metals,
    save_dir="outputs/sensitive_structure"
):
    apply_plot_style()
    os.makedirs(save_dir, exist_ok=True)

    # Analyte definitions
    n_analyte_negative = 1.3492  # analyte_01
    n_analyte_positive = 1.3481  # analyte_02

    analyte_list = [
        (n_analyte_negative - 0.001, "negative", "low"),
        (n_analyte_negative,         "negative", "center"),
        (n_analyte_negative + 0.001, "negative", "high"),
        (n_analyte_positive - 0.001, "positive", "low"),
        (n_analyte_positive,         "positive", "center"),
        (n_analyte_positive + 0.001, "positive", "high")
    ]

    d_metal = 55e-9
    all_data = []

    for metal in metals:
        plt.figure(figsize=(10, 6))
        color_map = ["#1f77b4", "#1f77b4", "#1f77b4", "#d62728", "#d62728", "#d62728"]
        all_thetas = {"positive": [], "negative": []}
        legend_handles = []

        for i, (n_analyte, group, n_type) in enumerate(analyte_list):
            n = np.array([
                materials[substrate],
                materials["Cr"],
                materials[metal],
                n_analyte + 0j
            ])
            d = np.array([d_cr, d_metal])

            Rp = np.array([
                getFresnelAIM(n, d, theta, lambda0)[2]
                for theta in theta_rad
            ])

            theta_res = calculate_theta_res_smooth(theta_deg, Rp)
            all_thetas[group].append(theta_res)

            all_data.append({
                "Metal": metal,
                "Group": group,
                "n_type": n_type,
                "n_analyte (RIU)": f"{n_analyte:.4f}",
                "Theta_res (deg)": theta_res
            })

            label = f"n = {n_analyte:.4f}"
            line, = plt.plot(theta_deg, Rp, color=color_map[i], linewidth=1.5, label=label)

            idx_res = np.argmin(np.abs(np.array(theta_deg) - theta_res))
            plt.plot(theta_deg[idx_res], Rp[idx_res], 'ko', markersize=6, markerfacecolor='black', zorder=3)

            legend_handles.append(line)

        if TNR:
            plt.xlabel("Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (a.u.)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(handles=legend_handles, loc="best", fontsize=9, prop=TNR)
        else:
            plt.xlabel("Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (a.u.)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(handles=legend_handles, loc="best", fontsize=9)

        plt.grid(True)
        plt.tight_layout()

        fname = os.path.join(save_dir, f"spr_reflectance_{substrate.lower()}_{metal.lower()}_55nm")
        save_figure(fname)
        plt.show()
        plt.close()

    df_all = pd.DataFrame(all_data)
    csv_path = os.path.join(save_dir, "theta_res_stats_all_metals_55nm.csv")
    df_all.to_csv(csv_path, index=False)
    print(f"[INFO] CSV saved: {csv_path}")
