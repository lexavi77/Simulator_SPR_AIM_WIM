import numpy as np
import matplotlib.pyplot as plt
from fresnel_utils import getFresnelAIM
from performance_metrics import calculate_theta_res, calculate_fwhm

def run_reflectance_simulation(substrate, metal, analytes, materials,
                                lambda0, theta_deg, theta_rad,
                                d_cr, d_analyte, metal_thicknesses_nm):
    results = {
        "theta_res": {},
        "fwhm": {},
        "substrate": substrate,
        "theta_deg": theta_deg,
        "reflectance": {}
    }

    for analyte in analytes:
        print(f"\nSimulating for analyte: {analyte}")
        plt.figure(figsize=(10, 6))

        theta_res_list = []
        fwhm_list = []
        reflectance_list = []

        for d_metal_nm in metal_thicknesses_nm:
            d_metal = d_metal_nm * 1e-9
            d = np.array([d_cr, d_metal])
            n = np.array([
                materials[substrate],
                materials["Cr"],
                materials[metal],
                materials[analyte]
            ])

            Rp = np.zeros_like(theta_rad)
            for i, angle in enumerate(theta_rad):
                _, _, Rp[i] = getFresnelAIM(n, d, angle, lambda0)

            theta_res = calculate_theta_res(Rp, theta_deg)
            fwhm = calculate_fwhm(Rp, theta_deg)

            theta_res_list.append(theta_res)
            fwhm_list.append(fwhm)
            reflectance_list.append(Rp)

            plt.plot(theta_deg, Rp, label=f'{d_metal_nm} nm | θres ≈ {theta_res:.2f}°')

        results["theta_res"][(metal, analyte)] = theta_res_list
        results["fwhm"][(metal, analyte)] = fwhm_list
        results["reflectance"][(metal, analyte)] = reflectance_list

        plt.title(f"SPR - Substrate: {substrate}, Metal: {metal}, Analyte: {analyte}")
        plt.xlabel("Incidence Angle (°)")
        plt.ylabel("Reflectance")
        plt.grid(True)
        plt.legend(fontsize=9)
        plt.tight_layout()

        # Ajuste automático do zoom no eixo X
        if theta_res_list:  # evita erro se estiver vazio
            theta_min = min(theta_res_list)
            theta_max = max(theta_res_list)
            padding = 1.5
            plt.xlim(theta_min - padding, theta_max + padding)

        plt.show()

    return results
