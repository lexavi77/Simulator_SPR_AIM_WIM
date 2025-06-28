import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.font_manager import FontProperties
from fresnel_utils import getFresnelAIM
from performance_metrics import calculate_theta_res, calculate_fwhm
from plot_style import apply_plot_style
from plot_utils import save_figure

# Fonte
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None
    print("[WARNING] Times New Roman not found. Using default font.")

# Paleta MATLAB-like
color_palette = [
    (0, 0.5, 0), (0, 0, 1), (0.93, 0.11, 0.14), (0, 0.75, 0.75),
    (0.75, 0, 0.75), (0.75, 0.75, 0), (0.25, 0.25, 0.25), (1, 0.5, 0),
    (0.5, 0, 0), (0, 0.5, 0.5), (0, 0, 0)
]

name_map = {
    "analyte_01": "positive",
    "analyte_02": "negative"
}

def run_reflectance_simulation(substrate, metal, analytes, materials,
                                lambda0, theta_deg, theta_rad,
                                d_cr, d_analyte, metal_thicknesses_nm):
    apply_plot_style()
    results = {
        "theta_res": {},
        "fwhm": {},
        "substrate": substrate,
        "theta_deg": theta_deg,
        "reflectance": {}
    }

    os.makedirs("figures", exist_ok=True)

    for analyte in analytes:
        label_analyte = name_map.get(analyte, analyte)
        print(f"\nSimulating for {label_analyte}...")

        plt.figure(figsize=(10, 6))
        theta_res_list = []
        fwhm_list = []
        reflectance_list = []

        for i, d_metal_nm in enumerate(metal_thicknesses_nm):
            d_metal = d_metal_nm * 1e-9
            d = np.array([d_cr, d_metal])
            n = np.array([
                materials[substrate],
                materials["Cr"],
                materials[metal],
                materials[analyte]
            ])

            Rp = np.array([
                getFresnelAIM(n, d, angle, lambda0)[2]
                for angle in theta_rad
            ])

            theta_res = calculate_theta_res(Rp, theta_deg)
            fwhm = calculate_fwhm(Rp, theta_deg)

            theta_res_list.append(theta_res)
            fwhm_list.append(fwhm)
            reflectance_list.append(Rp)

            color = color_palette[i % len(color_palette)]
            plt.plot(theta_deg, Rp, linewidth=1.5, color=color,
                     label=f'{d_metal_nm} nm | θres ≈ {theta_res:.2f}°')
            if not np.isnan(theta_res):
                Rp_res = np.interp(theta_res, theta_deg, Rp)
                plt.plot(theta_res, Rp_res, 'ko', markersize=5, markerfacecolor='black')

        results["theta_res"][(metal, analyte)] = theta_res_list
        results["fwhm"][(metal, analyte)] = fwhm_list
        results["reflectance"][(metal, analyte)] = reflectance_list

        if TNR:
            plt.xlabel("Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (a.u.)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(fontsize=9, prop=TNR, loc="best")
        else:
            plt.xlabel("Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (a.u.)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=9, loc="best")

        if theta_res_list:
            theta_min = min(theta_res_list)
            theta_max = max(theta_res_list)
            plt.xlim(theta_min - 1.5, theta_max + 1.5)

        plt.ylim(0, 1)
        plt.grid(True)
        plt.tight_layout()

        base = f"figures/reflectance_{substrate.lower()}_{metal.lower()}_{label_analyte.lower()}"
        save_figure(base)
        plt.show()
        plt.close()

    return results
