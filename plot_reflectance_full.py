import matplotlib.pyplot as plt
import numpy as np

def plot_reflectance_22_curves(results, metal_thicknesses_nm):
    """
    Plots 3 graphs (one for each metal: Ag, Au, Cu), each with 22 reflectance curves:
    - 11 curves with analyte_01 (solid line)
    - 11 curves with analyte_02 (dashed line)

    Legend includes only 2 entries: one for analyte_01 and one for analyte_02,
    with thickness range.
    """
    analytes = ["analyte_01", "analyte_02"]
    linestyles = {
        "analyte_01": "-",   # solid line
        "analyte_02": "--"   # dashed line
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

                # Only first curve of each analyte group gets a label
                label = None
                if i == 0:
                    range_str = f"{metal_thicknesses_nm[0]}–{metal_thicknesses_nm[-1]} nm"
                    label = f"{analyte.replace('_', ' ').capitalize()} - {range_str}"

                plt.plot(theta_deg, Rp,
                         linestyle=linestyles[analyte],
                         linewidth=1.2,
                         color=color,
                         alpha=0.8,
                         label=label)

        # Adjust x-axis based on resonance angle range
        if (metal, "analyte_01") in results["theta_res"] and (metal, "analyte_02") in results["theta_res"]:
            all_theta = results["theta_res"][(metal, "analyte_01")] + results["theta_res"][(metal, "analyte_02")]
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
