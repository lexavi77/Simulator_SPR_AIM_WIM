import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.font_manager import FontProperties

# Font configuration
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None
    print("[WARNING] Times New Roman not found. Using default font.")

# MATLAB-style colors
color_palette = [
    (0, 0.5, 0),        # green
    (0, 0, 1),          # blue
    (0.93, 0.11, 0.14), # red
    (0, 0.75, 0.75),    # cyan
    (0.75, 0, 0.75),    # magenta
    (0.75, 0.75, 0)     # yellow
]

def plot_reflectance_22_curves(results, metal_thicknesses_nm, save_dir="outputs/reflectance_curves"):
    from matplotlib.font_manager import FontProperties

    try:
        font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
        TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
    except Exception:
        TNR = None

    analytes = ["analyte_01", "analyte_02"]
    linestyles = {"analyte_01": "-", "analyte_02": "--"}
    colors = [(0, 0.5, 0), (0, 0, 1), (0.93, 0.11, 0.14)]  # Green, Blue, Red

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
                label = f"{analyte.replace('_', ' ').capitalize()}" if i == 0 else None
                plt.plot(theta_deg, Rp,
                         linestyle=linestyles[analyte],
                         linewidth=1.5,
                         color=color,
                         alpha=0.9,
                         label=label)
                plt.plot(theta_deg, Rp, 'ko', markersize=5, markerfacecolor='black', alpha=0.6)

        if (metal, "analyte_01") in results["theta_res"] and (metal, "analyte_02") in results["theta_res"]:
            all_theta = results["theta_res"][(metal, "analyte_01")] + results["theta_res"][(metal, "analyte_02")]
            if all_theta:
                plt.xlim(min(all_theta) - 1.5, max(all_theta) + 1.5)

        plt.ylim(0, 1)
        title = f"Reflectance Curves - {metal}"
        xlabel = "Incidence Angle (°)"
        ylabel = "Reflectance"

        if TNR:
            plt.title(title, fontsize=15, fontproperties=TNR)
            plt.xlabel(xlabel, fontsize=14, fontproperties=TNR)
            plt.ylabel(ylabel, fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(fontsize=10, loc="lower left", prop=TNR)
        else:
            plt.title(title, fontsize=15)
            plt.xlabel(xlabel, fontsize=14)
            plt.ylabel(ylabel, fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=10, loc="lower left")

        plt.grid(True)
        plt.tight_layout()

        path_eps = os.path.join(save_dir, f"reflectance_{metal.lower()}.eps")
        path_png = os.path.join(save_dir, f"reflectance_{metal.lower()}.png")
        plt.savefig(path_eps, format='eps', bbox_inches='tight')
        plt.savefig(path_png, format='png', dpi=300, bbox_inches='tight')
        print(f"[INFO] Saved: {path_eps} and {path_png}")

        plt.show()
        plt.close()


def plot_figures_of_merit(results, metal_thicknesses_nm, save_dir="outputs/figures_of_merit"):
    os.makedirs(save_dir, exist_ok=True)

    metrics = [
        "theta_res",
        "fwhm",
        "chi_empirical",
        "q_empirical"
    ]

    titles = {
        "theta_res": ("Resonance Angle (°)", "Metal Thickness (nm)"),
        "fwhm": ("FWHM (°)", "Metal Thickness (nm)"),
        "chi_empirical": ("Empirical χ (°⁻¹)", "Metal Thickness (nm)"),
        "q_empirical": ("Empirical Q", "Metal Thickness (nm)")
    }

    for metric in metrics:
        metric_data = results.get(metric, {})
        if not metric_data:
            print(f"[INFO] No data found for metric: {metric}")
            continue

        has_valid_data = False
        plt.figure(figsize=(8, 5))
        keys = sorted(metric_data.keys())[:6]  # Limit to 6 curves

        for idx, key in enumerate(keys):
            y = metric_data[key]
            x = metal_thicknesses_nm

            if all(np.isnan(y)):
                print(f"[INFO] Skipping {metric} for {key}: all values are NaN.")
                continue

            has_valid_data = True
            label = str(key)
            color = color_palette[idx % len(color_palette)]

            # Black markers
            plt.plot(x, y, 'ko', markersize=5, markerfacecolor='black')

            # Smoothed curve
            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fine = np.linspace(min(x), max(x), 500)
                y_smooth = spline(x_fine)
                plt.plot(x_fine, y_smooth, linewidth=1.5, label=label, color=color)
            else:
                plt.plot(x, y, 'k--', linewidth=1.0, label=label)

        if has_valid_data:
            ylabel, xlabel = titles[metric]

            if TNR:
                plt.xlabel(xlabel, fontsize=14, fontproperties=TNR)
                plt.ylabel(ylabel, fontsize=14, fontproperties=TNR)
                plt.title(f"{ylabel} vs {xlabel}", fontsize=15, fontproperties=TNR)
                plt.xticks(fontsize=12, fontproperties=TNR)
                plt.yticks(fontsize=12, fontproperties=TNR)
                plt.legend(fontsize=10, loc="best", prop=TNR)
            else:
                plt.xlabel(xlabel, fontsize=14)
                plt.ylabel(ylabel, fontsize=14)
                plt.title(f"{ylabel} vs {xlabel}", fontsize=15)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.legend(fontsize=10, loc="best")

            plt.grid(True)
            plt.tight_layout()

            base_filename = f"{metric}"
            path_eps = os.path.join(save_dir, f"{base_filename}.eps")
            path_png = os.path.join(save_dir, f"{base_filename}.png")
            plt.savefig(path_eps, format='eps', bbox_inches='tight')
            plt.savefig(path_png, format='png', dpi=300, bbox_inches='tight')
            print(f"[INFO] Saved: {path_eps} and {path_png}")

            # Show the plot on screen
            plt.show()

            # Close it afterwards to release memory
            plt.close()
        else:
            print(f"[INFO] Skipping plot for {metric}: no valid data to display.")
