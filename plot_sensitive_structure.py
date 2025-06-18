import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fresnel_utils import getFresnelAIM
from performance_metrics import calculate_theta_res_smooth

def plot_angular_response_for_sensitive_structure_and_export_csv(
    materials, lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, substrate, metals
):
    analyte_groups = {
        "positive": [1.3492 - 0.001, 1.3492, 1.3492 + 0.001],
        "negative": [1.3481 - 0.001, 1.3481, 1.3481 + 0.001]
    }

    d_metal = 55e-9
    all_data = []

    for metal in metals:
        plt.figure(figsize=(10, 6))
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        all_thetas = {"positive": [], "negative": []}

        for idx, (group, analytes) in enumerate(analyte_groups.items()):
            for i, n_analyte in enumerate(analytes):
                n = np.array([
                    materials[substrate],
                    materials["Cr"],
                    materials[metal],
                    n_analyte + 0j
                ])
                d = np.array([10e-9, d_metal])

                Rp = np.array([
                    getFresnelAIM(n, d, theta, lambda0)[2]
                    for theta in theta_rad
                ])

                theta_res = calculate_theta_res_smooth(theta_deg, Rp)
                all_thetas[group].append(theta_res)

                all_data.append({
                    "Metal": metal,
                    "Group": group,
                    "n_analyte": f"{n_analyte:.4f}",
                    "Theta_res (deg)": theta_res
                })

                label = f"{group}: n = {n_analyte:.4f}"
                plt.plot(theta_deg, Rp, label=label, color=colors[idx * 3 + i])

                x_min = max(theta_res - 2, theta_deg[0])
                x_max = min(theta_res + 2, theta_deg[-1])
                y_min = max(0, np.min(Rp) - 0.05)
                y_max = min(1, np.max(Rp) + 0.05)

                plt.xlim(x_min, x_max)
                plt.ylim(y_min, y_max)

        # estatistics for each group
        for group in ["positive", "negative"]:
            mean_theta = np.mean(all_thetas[group])
            std_theta = np.std(all_thetas[group])

            print(f"{metal} - {group.upper()} group:")
            print(f"  Mean θ_res: {mean_theta:.4f}°")
            print(f"  Std  θ_res: {std_theta:.4f}°\n")

            all_data.append({
                "Metal": metal,
                "Group": group,
                "n_analyte": "mean",
                "Theta_res (deg)": mean_theta
            })
            all_data.append({
                "Metal": metal,
                "Group": group,
                "n_analyte": "std",
                "Theta_res (deg)": std_theta
            })

        plt.title(f"Reflectance Curves\nSubstrate: {substrate}, Metal: {metal}, d = 55 nm")
        plt.xlabel("Incident Angle (°)")
        plt.ylabel("Reflectance (Rp)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"reflectance_curves_{metal}_55nm.png", dpi=300)
        plt.show()

    # cvs data export
    df_all = pd.DataFrame(all_data)
    df_all.to_csv("theta_res_stats_all_metals_55nm.csv", index=False)
    print("Consolidated CSV file saved: theta_res_stats_all_metals_55nm.csv")
    print("Reflectance curves and associated statistics have been saved successfully.")
