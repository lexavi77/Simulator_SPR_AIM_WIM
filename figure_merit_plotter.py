import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.font_manager import FontProperties
from plot_style import apply_plot_style
from plot_utils import save_figure

# Font
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None
    print("[WARNING] Times New Roman not found. Using default font.")

# MATLAB-like colors
color_palette = [
    (0, 0.5, 0), (0, 0, 1), (0.93, 0.11, 0.14),
    (0, 0.75, 0.75), (0.75, 0, 0.75), (0.75, 0.75, 0)
]

name_map = {
    "analyte_01": "negative",
    "analyte_02": "positive"
}


def plot_figures_of_merit(results, metal_thicknesses_nm, save_dir="outputs/figures_of_merit"):
    apply_plot_style()
    os.makedirs(save_dir, exist_ok=True)

    metrics = [
        "theta_res", "fwhm",
        "sensitivity_empirical", "sensitivity_theoretical",
        "chi_empirical", "chi_theoretical",
        "q_empirical", "q_theoretical"
    ]

    titles = {
        "theta_res": (r"Resonance Angle (°)", "Metal Thickness (nm)"),
        "fwhm": (r"FWHM (°)", "Metal Thickness (nm)"),
        "sensitivity_empirical": (r"Sensitivity (°/RIU)", "Metal Thickness (nm)"),
        "sensitivity_theoretical": (r"Sensitivity (°/RIU)", "Metal Thickness (nm)"),
        "chi_empirical": (r"$\chi$ (RIU$^{-1})$", "Metal Thickness (nm)"),
        "chi_theoretical": (r"$\chi$ (RIU$^{-1})$", "Metal Thickness (nm)"),
        "q_empirical": (r"$Q$ (a.u.)", "Metal Thickness (nm)"),
        "q_theoretical": (r"$Q$ (a.u.)", "Metal Thickness (nm)")
    }




    for metric in metrics:
        metric_data = results.get(metric, {})
        if not metric_data:
            print(f"[INFO] No data found for metric: {metric}")
            continue

        has_valid_data = False
        plt.figure(figsize=(8, 5))

        # Suporte a diferentes chaves (com ou sem analyte)
        keys = sorted(metric_data.keys())

        for idx, key in enumerate(keys):
            y = metric_data[key]
            x = metal_thicknesses_nm

            if all(np.isnan(y)):
                print(f"[INFO] Skipping {metric} for {key}: all values are NaN.")
                continue

            has_valid_data = True

            # Rótulo da curva
            if isinstance(key, tuple) and len(key) == 2:
                metal_name, analyte_key = key
                analyte_label = name_map.get(analyte_key, analyte_key)
                label = f"{metal_name} – {analyte_label}"
            else:
                label = str(key)

            color = color_palette[idx % len(color_palette)]
            plt.plot(x, y, 'ko', markersize=5, markerfacecolor='black')

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
                plt.xticks(fontsize=12, fontproperties=TNR)
                plt.yticks(fontsize=12, fontproperties=TNR)
                plt.legend(fontsize=10, loc="best", prop=TNR)
            else:
                plt.xlabel(xlabel, fontsize=14)
                plt.ylabel(ylabel, fontsize=14)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.legend(fontsize=10, loc="best")

            plt.title("")  # sem título no topo
            plt.grid(True)
            plt.tight_layout()

            fname = os.path.join(save_dir, metric)
            save_figure(fname)
            plt.show()
            plt.close()
        else:
            print(f"[INFO] Skipping plot for {metric}: no valid data to display.")
