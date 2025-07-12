import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.font_manager import FontProperties
from plot_utils import save_figure

# Fonte Times New Roman (opcional)
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None

def plot_figures_of_merit(results, metal_thicknesses_nm, save_dir="outputs/figures_of_merit"):
    os.makedirs(save_dir, exist_ok=True)

    # Métricas esperadas
    metrics = [
        "theta_res", "fwhm",
        "sensitivity_empirical", "sensitivity_theoretical",
        "chi_empirical", "chi_theoretical",
        "q_empirical", "q_theoretical"
    ]

    # Títulos e rótulos
    titles = {
        "theta_res": (r"Resonance Angle (°)", "Metal Thickness (nm)"),
        "fwhm": (r"FWHM (°)", "Metal Thickness (nm)"),
        "sensitivity_empirical": (r"Sensitivity (°/RIU)", "Metal Thickness (nm)"),
        "sensitivity_theoretical": (r"Sensitivity (°/RIU)", "Metal Thickness (nm)"),
        "chi_empirical": (r"$\chi$ (RIU$^{-1}$)", "Metal Thickness (nm)"),
        "chi_theoretical": (r"$\chi$ (RIU$^{-1}$)", "Metal Thickness (nm)"),
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

        for metal in ["Ag", "Au", "Cu"]:
            key = (metal, "analyte_02")  # Usar apenas o analyte positivo
            if key not in metric_data:
                continue

            y = metric_data[key]
            x = metal_thicknesses_nm

            if all(np.isnan(y)):
                continue

            has_valid_data = True
            plt.plot(x, y, 'ko', markersize=5, markerfacecolor='black', zorder=3)

            # Curva suavizada (spline)
            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fine = np.linspace(min(x), max(x), 500)
                y_smooth = spline(x_fine)
                plt.plot(x_fine, y_smooth, linewidth=1.5, label=metal)
            else:
                plt.plot(x, y, 'k--', linewidth=1.0, label=metal)

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

            plt.grid(True)
            plt.tight_layout()

            fname = os.path.join(save_dir, metric)
            save_figure(fname)
            plt.close()
