import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from fresnel_utils import getFresnelAIM
from performance_metrics import calculate_theta_res_smooth
from matplotlib.font_manager import FontProperties

# Try to load Times New Roman; fallback to default
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    print("[WARNING] Times New Roman not found. Using default font.")
    TNR = None

def plot_angular_response_for_sensitive_structure_and_export_csv(
    materials, lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, substrate, metals,
    save_dir="output_sensitive_structure"
):
    os.makedirs(save_dir, exist_ok=True)

    n_neg_base = 1.3481
    n_pos_base = 1.3492

    analyte_list = [
        (n_neg_base - 0.001, "negative", "low"),
        (n_neg_base,         "negative", "center"),
        (n_neg_base + 0.001, "negative", "high"),
        (n_pos_base - 0.001, "positive", "low"),
        (n_pos_base,         "positive", "center"),
        (n_pos_base + 0.001, "positive", "high")
    ]

    d_metal = 55e-9
    all_data = []

    for metal in metals:
        plt.figure(figsize=(10, 6))
        color_map = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        all_thetas = {"positive": [], "negative": []}
        legend_items = []

        for i, (n_analyte, group, n_type) in enumerate(analyte_list):
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
                "n_type": n_type,
                "n_analyte (RIU)": f"{n_analyte:.4f}",
                "Theta_res (deg)": theta_res
            })

            label = f"n = {n_analyte:.4f}"
            line = plt.plot(theta_deg, Rp, label=label, color=color_map[i])[0]
            legend_items.append((n_analyte, line, label))

            x_min = max(theta_res - 2, theta_deg[0])
            x_max = min(theta_res + 2, theta_deg[-1])
            y_min = max(0, np.min(Rp) - 0.05)
            y_max = min(1, np.max(Rp) + 0.05)

            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)

        for group in ["positive", "negative"]:
            thetas = all_thetas[group]
            mean_theta = np.mean(thetas)
            std_theta = np.std(thetas)

            print(f"{metal} - {group.upper()} group:")
            print(f"  Mean θ_res: {mean_theta:.4f}°")
            print(f"  Std  θ_res: {std_theta:.4f}°\n")

            all_data.extend([
                {
                    "Metal": metal,
                    "Group": group,
                    "n_type": "mean",
                    "n_analyte (RIU)": "-",
                    "Theta_res (deg)": mean_theta
                },
                {
                    "Metal": metal,
                    "Group": group,
                    "n_type": "std",
                    "n_analyte (RIU)": "-",
                    "Theta_res (deg)": std_theta
                }
            ])

        legend_items.sort(key=lambda x: x[0])
        handles = [item[1] for item in legend_items]
        labels = [item[2] for item in legend_items]

        if TNR:
            plt.title(f"Reflectance Curves\nSubstrate: {substrate}, Metal: {metal}, d = 55 nm",
                      fontsize=15, fontproperties=TNR)
            plt.xlabel("Incident Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (Rp)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(handles, labels, loc="best", fontsize=9, prop=TNR)
        else:
            plt.title(f"Reflectance Curves\nSubstrate: {substrate}, Metal: {metal}, d = 55 nm",
                      fontsize=15)
            plt.xlabel("Incident Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (Rp)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(handles, labels, loc="best", fontsize=9)

        plt.grid(True)
        plt.tight_layout()

        fname = os.path.join(save_dir, f"reflectance_curves_{metal}_55nm")
        plt.savefig(f"{fname}.png", dpi=300)
        plt.savefig(f"{fname}.eps", format="eps", bbox_inches="tight")
        print(f"[INFO] Saved: {fname}.eps and .png")
        plt.close()

    df_all = pd.DataFrame(all_data)
    csv_path = os.path.join(save_dir, "theta_res_stats_all_metals_55nm.csv")
    df_all.to_csv(csv_path, index=False)
    print(f"[INFO] CSV saved: {csv_path}")
