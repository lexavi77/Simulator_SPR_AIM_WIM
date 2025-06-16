import numpy as np
import matplotlib.pyplot as plt

from fresnel_utils import getFresnelAIM
from optical_data import materials
from simulation_config import (
    lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, metal_thicknesses_nm, analytes
)
from user_input import select_materials
from performance_metrics import (
    calculate_q, calculate_sensitivity, calculate_chi,
    calculate_fwhm_nm, calculate_spectral_sensitivity_from_theta
)
from calculate_figures import calculate_all_figures_of_merit
from merit_figures_plot import plot_figures_of_merit
from reflectance_simulator import run_reflectance_simulation
from save_results import save_results_to_csv

# ------------------- Execução principal -------------------

print("Select simulation mode:")
print("1 - Analyze a specific material")
print("2 - Compare metals with fixed analyte (H2O_central)")
mode = input("Mode (1 or 2): ").strip()

# ------------------- MODO 1: Simulação para material específico -------------------

if mode == "1":
    substrate, metal = select_materials()
    results = run_reflectance_simulation(
        substrate, metal, analytes,
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analyte, metal_thicknesses_nm
    )

    # Calcula figuras de mérito incluindo FWHM espectral
    calculate_all_figures_of_merit(results, materials, metal)

    # Plota todas as métricas
    plot_figures_of_merit(results, metal_thicknesses_nm)

# ------------------- MODO 2: Comparação entre metais -------------------

elif mode == "2":
    print("\nComparison mode selected.")
    print("Select fixed substrate: PMMA, PC, or TOPAS")
    substrate_input = input("Substrate: ").strip().upper()
    name_map = {"PMMA": "PMMA", "PC": "PC", "TOPAS": "TOPAS"}

    if substrate_input not in name_map:
        raise ValueError("Invalid substrate.")
    substrate = name_map[substrate_input]

    comparison_results = {
        "theta_res": {},
        "fwhm": {},
        "fwhm_nm": {},
        "sensitivity": {},
        "s_lambda": {},
        "chi": {},
        "chi_lambda": {},
        "q": {},
        "metal_thicknesses_nm": metal_thicknesses_nm
    }

    for metal in ["Ag", "Au", "Cu"]:
        print(f"\nSimulating for metal: {metal}")

        results_low = run_reflectance_simulation(
            substrate, metal, ["H2O_low"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )
        results_high = run_reflectance_simulation(
            substrate, metal, ["H2O_high"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )
        results_central = run_reflectance_simulation(
            substrate, metal, ["H2O_central"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        theta_low = results_low["theta_res"][(metal, "H2O_low")]
        theta_high = results_high["theta_res"][(metal, "H2O_high")]
        theta_central = results_central["theta_res"][(metal, "H2O_central")]
        fwhm = results_central["fwhm"][(metal, "H2O_central")]

        fwhm_nm = [
            calculate_fwhm_nm(
                Rp, theta_deg,
                lambda0 * 1e9,
                materials[substrate].real
            )
            for Rp in results_central["reflectance"][(metal, "H2O_central")]
        ]

        sensitivity = [
            calculate_sensitivity(th, tl, materials["H2O_high"].real, materials["H2O_low"].real)
            for th, tl in zip(theta_high, theta_low)
        ]
        chi = [calculate_chi(s, f) for s, f in zip(sensitivity, fwhm)]
        q = [calculate_q(t, f) for t, f in zip(theta_central, fwhm)]

        s_lambda = calculate_spectral_sensitivity_from_theta(
            theta_res_high=theta_high,
            theta_res_low=theta_low,
            lambda0_nm=lambda0 * 1e9,
            n_prisma=materials[substrate].real,
            n_high=materials["H2O_high"].real,
            n_low=materials["H2O_low"].real
        )

        chi_lambda = [
            s / f if f != 0 else np.nan
            for s, f in zip(s_lambda, fwhm_nm)
        ]

        comparison_results["theta_res"][metal] = theta_central
        comparison_results["fwhm"][metal] = fwhm
        comparison_results["fwhm_nm"][metal] = fwhm_nm
        comparison_results["sensitivity"][metal] = sensitivity
        comparison_results["s_lambda"][metal] = s_lambda
        comparison_results["chi"][metal] = chi
        comparison_results["chi_lambda"][metal] = chi_lambda
        comparison_results["q"][metal] = q

    print("\nPlotting metal comparison...")
    plot_figures_of_merit(comparison_results, metal_thicknesses_nm)

    # Exporta resultados para CSVs separados
    for metal in ["Ag", "Au", "Cu"]:
        save_results_to_csv(comparison_results, metal, filename=f"results_{metal}.csv")

else:
    print("Invalid option. Exiting program.")
