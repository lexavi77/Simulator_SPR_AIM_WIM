import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def plot_figures_of_merit(results, metal_thicknesses_nm):
    metrics = ["theta_res", "fwhm", "sensitivity", "chi", "q"]
    titles = {
        "theta_res": "Resonance Angle (°)",
        "fwhm": "FWHM (°)",
        "sensitivity": "Sensitivity (°/RIU)",
        "chi": "Chi Parameter (χ)",
        "q": "Q Factor"
    }

    for metric in metrics:
        plt.figure(figsize=(8, 5))
        for key in results[metric]:
            x = metal_thicknesses_nm
            y = results[metric][key]

            # Only interpolate if there are enough data points and no NaNs
            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fine = np.linspace(min(x), max(x), 500)
                y_smooth = spline(x_fine)
                plt.plot(x_fine, y_smooth, label=str(key))
            else:
                plt.plot(x, y, 'o-', label=str(key))  # fallback without smoothing

        plt.xlabel("Metal Thickness (nm)")
        plt.ylabel(titles[metric])
        plt.title(f"Figure of Merit: {titles[metric]}")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
