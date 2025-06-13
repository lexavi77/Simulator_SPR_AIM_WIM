# simulador_reflectancia.py

import numpy as np
import matplotlib.pyplot as plt
from fresnel_utils import getFresnelAIM
from figuras_de_merito import calcular_theta_res, calcular_fwhm

def executar_simulacao_reflectancia(substrato, metal, analitos, materials,
                                     lambda0, theta_deg, theta_rad,
                                     d_cr, d_analito, espessuras_metal_nm):
    resultados = {
        "theta_res": {},
        "fwhm": {}
    }

    for analito in analitos:
        print(f"\nSimulando para analito: {analito}")
        plt.figure(figsize=(10, 6))

        theta_res_lista = []
        fwhm_lista = []

        for d_metal_nm in espessuras_metal_nm:
            d_metal = d_metal_nm * 1e-9
            d = np.array([d_cr, d_metal, d_analito])
            n = np.array([
                materials[substrato],
                materials["Cr"],
                materials[metal],
                materials[analito]
            ])

            Rp = np.zeros_like(theta_rad)
            for i, angle in enumerate(theta_rad):
                _, _, Rp[i] = getFresnelAIM(n, d, angle, lambda0)

            theta_res = calcular_theta_res(Rp, theta_deg)
            fwhm = calcular_fwhm(Rp, theta_deg)

            theta_res_lista.append(theta_res)
            fwhm_lista.append(fwhm)

            plt.plot(theta_deg, Rp, label=f'{d_metal_nm} nm | θres ≈ {theta_res:.2f}°')

        resultados["theta_res"][(metal, analito)] = theta_res_lista
        resultados["fwhm"][(metal, analito)] = fwhm_lista

        plt.title(f"SPR - Substrato: {substrato}, Metal: {metal}, Analito: {analito}")
        plt.xlabel("Ângulo de Incidência (°)")
        plt.ylabel("Reflectância")
        plt.grid(True)
        plt.legend(fontsize=9)
        plt.tight_layout()
        plt.show()

    return resultados
