import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.font_manager import FontProperties
from plot_style import apply_plot_style
from plot_utils import save_figure  # Utilitário de salvamento centralizado

# Font configuration
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None
    print("[WARNING] Times New Roman not found. Using default font.")

# MATLAB-style colors
color_palette = [
    (0, 0.5, 0), (0, 0, 1), (0.93, 0.11, 0.14),
    (0, 0.75, 0.75), (0.75, 0, 0.75), (0.75, 0.75, 0)
]

# Mapping analyte names
name_map = {"analyte_01": "positive", "analyte_02": "negative"}
linestyles = {"analyte_01": "-", "analyte_02": "--"}

def plot_reflectance_22_curves(results, metal_thicknesses_nm, save_dir="outputs/reflectance_curves"):
    apply_plot_style()
    analytes = ["analyte_01", "analyte_02"]
    colors = [(0, 0.5, 0), (0, 0, 1), (0.93, 0.11, 0.14)]

    os.makedirs(save_dir, exist_ok=True)

    for idx, metal in enumerate(["Ag", "Au", "Cu"]):
        plt.figure(figsize=(10, 6))
        color = colors[idx]

        for analyte in analytes:
            key = (metal, analyte)
            Rp_list = results["reflectance"].get(key)
            theta_deg = results["theta_deg"]

            if not Rp_list:
                continue

            for i, Rp in enumerate(Rp_list):
                label = name_map[analyte] if i == 0 else None
                plt.plot(theta_deg, Rp,
                         linestyle=linestyles[analyte],
                         linewidth=1.5,
                         color=color,
                         alpha=0.9,
                         label=label)
                plt.plot(theta_deg, Rp, 'ko', markersize=5, markerfacecolor='black', alpha=0.6)

        # Ajusta limites do eixo x
        if (metal, "analyte_01") in results["theta_res"] and (metal, "analyte_02") in results["theta_res"]:
            all_theta = results["theta_res"][(metal, "analyte_01")] + results["theta_res"][(metal, "analyte_02")]
            if all_theta:
                plt.xlim(min(all_theta) - 1.5, max(all_theta) + 1.5)

        plt.ylim(0, 1)

        if TNR:
            plt.xlabel("Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (a.u.)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(fontsize=10, loc="lower left", prop=TNR)
        else:
            plt.xlabel("Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (a.u.)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=10, loc="lower left")

        plt.title("")  # Garantir ausência de título
        plt.grid(True)
        plt.tight_layout()

        fname = os.path.join(save_dir, f"reflectance_{metal.lower()}")
        save_figure(fname)
        plt.show()
        plt.close()

def plot_figures_of_merit(results, metal_thicknesses_nm, save_dir="outputs/figures_of_merit"):
    apply_plot_style()
    os.makedirs(save_dir, exist_ok=True)

    metrics = ["theta_res", "fwhm", "chi_empirical", "q_empirical"]

    titles = {
        "theta_res": (r"Resonance Angle (°)", "Metal Thickness (nm)"),
        "fwhm": (r"FWHM (°)", "Metal Thickness (nm)"),
        "chi_empirical": (r"$\chi\ (\mathrm{RIU}^{-1})$", "Metal Thickness (nm)"),
        "q_empirical": (r"$Q\ (\mathrm{a.u.})$", "Metal Thickness (nm)")
    }

    for metric in metrics:
        metric_data = results.get(metric, {})
        if not metric_data:
            print(f"[INFO] No data found for metric: {metric}")
            continue

        has_valid_data = False
        plt.figure(figsize=(8, 5))
        keys = sorted(metric_data.keys())[:6]  # Ag, Au, Cu × 2 analytes

        for idx, key in enumerate(keys):
            y = metric_data[key]
            x = metal_thicknesses_nm

            if all(np.isnan(y)):
                print(f"[INFO] Skipping {metric} for {key}: all values are NaN.")
                continue

            has_valid_data = True

            metal_name, analyte_key = key
            analyte_label = name_map.get(analyte_key, analyte_key)
            label_key = f"{metal_name} – {analyte_label}"

            color = color_palette[idx % len(color_palette)]

            plt.plot(x, y, 'ko', markersize=5, markerfacecolor='black')

            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fine = np.linspace(min(x), max(x), 500)
                y_smooth = spline(x_fine)
                plt.plot(x_fine, y_smooth, linewidth=1.5, label=label_key, color=color)
            else:
                plt.plot(x, y, 'k--', linewidth=1.0, label=label_key)

        if has_valid_data:
            ylabel, xlabel = titles[metric]

            if TNR:
                plt.xlabel(xlabel, fontsize=14, fontproperties=TNR)
                plt.ylabel(ylabel, fontsize=14, fontproperties=TNR)
                plt.xticks(fontsize=12, fontproperties=TNR)
                plt.yticks(fontsize=12, fontproperties=TNR)
                plt.legend(fontsize=10, loc="best", prop=TNR)
            else:
                plt.xlabel(xlabel, fontsize=14)
                plt.ylabel(ylabel, fontsize=14)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.legend(fontsize=10, loc="best")

            plt.title("")  # Remoção explícita de qualquer título
            plt.grid(True)
            plt.tight_layout()

            fname = os.path.join(save_dir, metric)
            save_figure(fname)
            plt.show()
            plt.close()
        else:
            print(f"[INFO] Skipping plot for {metric}: no valid data to display.")
