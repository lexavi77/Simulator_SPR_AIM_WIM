import matplotlib.pyplot as plt
import numpy as np

def plot_reflectance_22_curves(results, metal_thicknesses_nm):
    """
    Plots 3 graphs (one for each metal: Ag, Au, Cu), each with 22 reflectance curves:
    - 11 curves with negative analyte (solid line)
    - 11 curves with positive analyte (dashed line)

    Parameters:
    - results: dictionary returned by run_reflectance_simulation
    - metal_thicknesses_nm: list with simulated thicknesses (e.g., range(45, 56))
    """
    analytes = ["H2O_low", "H2O_high"]
    linestyles = {
        "H2O_low": "-",   # solid line (negative)
        "H2O_high": "--"  # dashed line (positive)
    }
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",
              "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan", "black"]

    for metal in ["Ag", "Au", "Cu"]:
        plt.figure(figsize=(10, 6))

        for analyte in analytes:
            key = (metal, analyte)
            reflectances = results["reflectance"].get(key)
            theta_deg = results["theta_deg"]

            if reflectances is None:
                print(f"[WARNING] No reflectance data for {metal} - {analyte}")
                continue

            for i, Rp in enumerate(reflectances):
                color = colors[i % len(colors)]
                label = f"{analyte.replace('H2O_', '').capitalize()} - {metal_thicknesses_nm[i]} nm" if i == 0 else None
                plt.plot(theta_deg, Rp,
                         linestyle=linestyles[analyte],
                         linewidth=1.2,
                         color=color,
                         alpha=0.8,
                         label=label)

        # Automatic adjustment of the X-axis based on simulated θres
        if (metal, "H2O_low") in results["theta_res"] and (metal, "H2O_high") in results["theta_res"]:
            all_theta = results["theta_res"][(metal, "H2O_low")] + results["theta_res"][(metal, "H2O_high")]
            if all_theta:
                theta_min = min(all_theta)
                theta_max = max(all_theta)
                padding = 1.5
                plt.xlim(theta_min - padding, theta_max + padding)

        plt.title(f"Reflectance Curves - {metal}")
        plt.xlabel("Incidence Angle (°)")
        plt.ylabel("Reflectance")
        plt.grid(True)
        plt.tight_layout()
        plt.legend(fontsize=8, loc="best")
        plt.show()
