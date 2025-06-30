import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from fresnel_utils import getFresnelAIM
from performance_metrics import calculate_theta_res_smooth
from matplotlib.font_manager import FontProperties
from plot_style import apply_plot_style
from plot_utils import save_figure, get_matlab_colors

# Load Times New Roman if available
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    print("[WARNING] Times New Roman not found. Using default font.")
    TNR = None


def calculate_theoretical_sensitivity_precise(n_metal, n_analyte, n_substrate):
    """
    Sensitivity (°/RIU) via Thirstrup Eq. (3), no approximations.
    """
    eps = n_metal ** 2
    eps_mr = np.real(eps)
    n_eff = np.real(n_analyte)
    n2 = np.real(n_substrate)

    numerator = eps_mr ** 2
    denominator = abs(eps_mr + n_eff ** 2)
    root_term = eps_mr * n2**2 * (eps_mr + n_eff**2) - eps_mr**2 * n_eff**2

    if denominator == 0 or root_term <= 0:
        return np.nan

    sensitivity_rad = numerator / (denominator * np.sqrt(root_term))
    return np.degrees(sensitivity_rad)


def plot_angular_response_for_sensitive_structure_and_export_csv(
    materials, lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, substrate, metals,
    save_dir="outputs/sensitive_structure"
):
    apply_plot_style()
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
        color_map = get_matlab_colors(6)
        all_thetas = {"positive": [], "negative": []}
        legend_handles = []

        for i, (n_analyte, group, n_type) in enumerate(analyte_list):
            n = np.array([
                materials[substrate],
                materials["Cr"],
                materials[metal],
                n_analyte + 0j
            ])
            d = np.array([d_cr, d_metal])

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
            line, = plt.plot(theta_deg, Rp, color=color_map[i], linewidth=1.5, label=label)

            idx_res = np.argmin(np.abs(np.array(theta_deg) - theta_res))
            plt.plot(theta_deg[idx_res], Rp[idx_res], 'ko', markersize=6, markerfacecolor='black')

            legend_handles.append(line)

        # Métricas para cada grupo (positivo/negativo)
        for group in ["positive", "negative"]:
            thetas = all_thetas[group]
            mean_theta = np.mean(thetas)
            std_theta = np.std(thetas)
            theta_low = thetas[0]
            theta_high = thetas[2]

            n_base = n_pos_base if group == "positive" else n_neg_base
            n_low = n_base - 0.001
            n_high = n_base + 0.001

            sensitivity_empirical = (theta_high - theta_low) / (n_high - n_low)

            sensitivity_theoretical = calculate_theoretical_sensitivity_precise(
                n_metal=materials[metal],
                n_analyte=n_base + 0j,
                n_substrate=materials[substrate]
            )

            print(f"{metal} - {group.upper()} group:")
            print(f"  Mean θ_res: {mean_theta:.4f}°")
            print(f"  Std  θ_res: {std_theta:.4f}°")
            print(f"  Sensitivity (empirical):  {sensitivity_empirical:.4f} °/RIU")
            print(f"  Sensitivity (theoretical): {sensitivity_theoretical:.4f} °/RIU\n")

            all_data.extend([
                {"Metal": metal, "Group": group, "n_type": "mean", "n_analyte (RIU)": "-", "Theta_res (deg)": mean_theta},
                {"Metal": metal, "Group": group, "n_type": "std", "n_analyte (RIU)": "-", "Theta_res (deg)": std_theta},
                {"Metal": metal, "Group": group, "n_type": "sensitivity_empirical", "n_analyte (RIU)": "-", "Theta_res (deg)": sensitivity_empirical},
                {"Metal": metal, "Group": group, "n_type": "sensitivity_theoretical", "n_analyte (RIU)": "-", "Theta_res (deg)": sensitivity_theoretical}
            ])

        # Finalização dos gráficos
        if TNR:
            plt.xlabel("Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (a.u.)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(handles=legend_handles, loc="best", fontsize=9, prop=TNR)
        else:
            plt.xlabel("Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (a.u.)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(handles=legend_handles, loc="best", fontsize=9)

        plt.grid(True)
        plt.tight_layout()

        fname = os.path.join(save_dir, f"spr_reflectance_{substrate.lower()}_{metal.lower()}_55nm")
        save_figure(fname)
        plt.show()
        plt.close()

    df_all = pd.DataFrame(all_data)
    csv_path = os.path.join(save_dir, "theta_res_stats_all_metals_55nm.csv")
    df_all.to_csv(csv_path, index=False)
    print(f"[INFO] CSV saved: {csv_path}")
