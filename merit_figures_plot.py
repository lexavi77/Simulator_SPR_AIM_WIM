import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.font_manager import FontProperties

# Caminho para a fonte Times New Roman
TNR = FontProperties(fname="/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf")

def plot_figures_of_merit(results, metal_thicknesses_nm, save_dir=None):
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

    # Cores no estilo MATLAB
    color_palette = [
        (0, 0.5, 0),       # green
        (0, 0, 1),         # blue
        (0.93, 0.11, 0.14),# red
        (0, 0.75, 0.75),   # cyan
        (0.75, 0, 0.75),   # magenta
        (0.75, 0.75, 0)    # yellow
    ]

    for metric in metrics:
        metric_data = results.get(metric, {})
        if not metric_data:
            print(f"[INFO] No data found for metric: {metric}")
            continue

        has_valid_data = False
        plt.figure(figsize=(8, 5))

        keys = sorted(metric_data.keys())[:6]  # limitar a 6 curvas
        for idx, key in enumerate(keys):
            y = metric_data[key]
            x = metal_thicknesses_nm
            if all(np.isnan(y)):
                print(f"[INFO] Skipping {metric} for {key}: all values are NaN.")
                continue

            has_valid_data = True
            label = str(key)

            # Pontos
            plt.plot(x, y, 'ko', markersize=5, markerfacecolor='black')

            # Curva suavizada
            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fine = np.linspace(min(x), max(x), 500)
                y_smooth = spline(x_fine)
                color = color_palette[idx % len(color_palette)]
                plt.plot(x_fine, y_smooth, linewidth=1.5, label=label, color=color)
            else:
                plt.plot(x, y, 'k--', linewidth=1.0, label=label)

        if has_valid_data:
            ylabel, xlabel = titles[metric]
            plt.xlabel(xlabel, fontsize=14, fontproperties=TNR)
            plt.ylabel(ylabel, fontsize=14, fontproperties=TNR)
            plt.title(f"{ylabel} vs {xlabel}", fontsize=15, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.grid(True)
            plt.legend(fontsize=10, loc="best", prop=TNR)
            plt.tight_layout()

            if save_dir:
                base_filename = f"{metric}"
                plt.savefig(f"{save_dir}/{base_filename}.png", dpi=300, bbox_inches='tight')
                plt.savefig(f"{save_dir}/{base_filename}.eps", format='eps', bbox_inches='tight')
                print(f"[INFO] Saved: {save_dir}/{base_filename}.png and .eps")

            plt.show()
        else:
            print(f"[INFO] Skipping plot for {metric}: no valid data to display.")
