import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def plot_figures_of_merit(results, metal_thicknesses_nm):
    metrics = [
        "theta_res",
        "fwhm",
        "sensitivity_empirical",
        "sensitivity_theoretical",
        "chi_empirical",
        "chi_theoretical",
        "q_empirical",
        "q_theoretical"
    ]

    titles = {
        "theta_res": "Resonance Angle (°)",
        "fwhm": "FWHM (°)",
        "sensitivity_empirical": "Empirical Sensitivity (°/RIU)",
        "sensitivity_theoretical": "Theoretical Sensitivity (°/RIU)",
        "chi_empirical": "Empirical χ (°⁻¹)",
        "chi_theoretical": "Theoretical χ (°⁻¹)",
        "q_empirical": "Empirical Q",
        "q_theoretical": "Theoretical Q"
    }

    for metric in metrics:
        has_valid_data = False

        for key in results.get(metric, {}):
            x = metal_thicknesses_nm
            y = results[metric][key]

            if all(np.isnan(y)):
                print(f"[INFO] Skipping {metric} for {key}: all values are NaN.")
                continue

            if not has_valid_data:
                plt.figure(figsize=(8, 5))

            has_valid_data = True

            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fine = np.linspace(min(x), max(x), 500)
                y_smooth = spline(x_fine)
                plt.plot(x_fine, y_smooth, label=str(key))
            else:
                plt.plot(x, y, 'o-', label=str(key))  # fallback sem suavização

        if has_valid_data:
            plt.xlabel("Metal Thickness (nm)")
            plt.ylabel(titles[metric])
            plt.title(f"Figure of Merit: {titles[metric]}")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print(f"[INFO] Skipping plot for {metric}: no valid data to display.")
