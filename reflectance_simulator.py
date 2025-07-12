import numpy as np
import matplotlib.pyplot as plt
import os
from fresnel_utils import getFresnelAIM
from performance_metrics import (
    calculate_theta_res_smooth, calculate_fwhm
)
from plot_utils import save_figure
from matplotlib.font_manager import FontProperties

# Fonte Times New Roman (se disponível)
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None

def restrict_range(theta_deg, Rp, window=(40, 80)):
    """Restricts reflectance data to a specific angular window."""
    mask = (theta_deg >= window[0]) & (theta_deg <= window[1])
    return theta_deg[mask], Rp[mask]

def run_reflectance_simulation(
    substrate, metal, analytes_dict,
    materials, lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, metal_thicknesses_nm,
    theta_window=(40, 80)
):
    """
    Simulates the SPR reflectance response for a set of metal thicknesses
    and two analytes (typically analyte_01 and analyte_02).
    """

    results = {
        "theta_res": {},
        "fwhm": {},
        "reflectance": {},
        "theta_deg": theta_deg,
        "substrate": substrate
    }

    os.makedirs("figures", exist_ok=True)
    name_map = {"analyte_01": "positive", "analyte_02": "negative"}

    for analyte_key, n_analyte in analytes_dict.items():
        label = name_map.get(analyte_key, analyte_key)
        print(f"[INFO] Simulating {metal} | {label} | Substrate: {substrate}")

        theta_res_list = []
        fwhm_list = []
        reflectance_list = []

        plt.figure(figsize=(10, 6))

        for i, d_metal_nm in enumerate(metal_thicknesses_nm):
            d_metal = d_metal_nm * 1e-9
            d = np.array([d_cr, d_metal])
            n = np.array([
                materials[substrate],
                materials["Cr"],
                materials[metal],
                n_analyte + 0j
            ])

            # Reflectance vs angle
            Rp = np.array([getFresnelAIM(n, d, angle, lambda0)[2] for angle in theta_rad])

            # Process results
            theta_deg_windowed, Rp_windowed = restrict_range(theta_deg, Rp, theta_window)
            theta_res = calculate_theta_res_smooth(theta_deg_windowed, Rp_windowed)
            fwhm = calculate_fwhm(Rp, theta_deg)

            theta_res_list.append(theta_res)
            fwhm_list.append(fwhm)
            reflectance_list.append(Rp)

            # Plot each curve
            color = plt.cm.tab10(i % 10)
            plt.plot(theta_deg, Rp, color=color, linewidth=1.5,
                     label=f'{d_metal_nm} nm | θres ≈ {theta_res:.2f}°')

            if not np.isnan(theta_res):
                Rp_res = np.interp(theta_res, theta_deg, Rp)
                plt.plot(theta_res, Rp_res, 'ko', markersize=5, markerfacecolor='black')

        results["theta_res"][(metal, analyte_key)] = theta_res_list
        results["fwhm"][(metal, analyte_key)] = fwhm_list
        results["reflectance"][(metal, analyte_key)] = reflectance_list

        # Plot settings
        if TNR:
            plt.xlabel("Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (a.u.)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(fontsize=9, loc="best", prop=TNR)
        else:
            plt.xlabel("Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (a.u.)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=9, loc="best")

        if theta_res_list:
            plt.xlim(min(theta_res_list) - 1.5, max(theta_res_list) + 1.5)

        plt.ylim(0, 1)
        plt.grid(True)
        plt.tight_layout()

        base = f"figures/reflectance_{substrate.lower()}_{metal.lower()}_{label}"
        save_figure(base)
        plt.close()

    return results
