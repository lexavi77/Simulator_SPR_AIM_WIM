import numpy as np
import matplotlib.pyplot as plt

from fresnel_utils import getFresnelAIM
from optical_data import materials
from simulation_config import (
    lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, metal_thicknesses_nm, analytes
)
from user_input import select_materials
from performance_metrics import calculate_q, calculate_sensitivity, calculate_chi
from calculate_figures import calculate_all_figures_of_merit
from merit_figures_plot import plot_figures_of_merit
from reflectance_simulator import run_reflectance_simulation

# ------------------- Execution Logic -------------------

print("Select simulation mode:")
print("1 - Analyze a specific material")
print("2 - Compare metals with fixed analyte (H2O_central)")
mode = input("Mode (1 or 2): ").strip()

if mode == "1":
    substrate, metal = select_materials()
    results = run_reflectance_simulation(
        substrate, metal, analytes,
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analyte, metal_thicknesses_nm
    )
    calculate_all_figures_of_merit(results, materials, metal)
    plot_figures_of_merit(results, metal_thicknesses_nm)

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
        "sensitivity": {},
        "chi": {},
        "q": {}
    }

    delta_n = materials["H2O_high"].real - materials["H2O_low"].real

    for metal in ["Ag", "Au", "Cu"]:
        print(f"\nSimulating for metal: {metal}")

        # Simula H2O_low
        results_low = run_reflectance_simulation(
            substrate, metal, ["H2O_low"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        # Simula H2O_high
        results_high = run_reflectance_simulation(
            substrate, metal, ["H2O_high"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        # Simula H2O_central para fwhm e q
        results_central = run_reflectance_simulation(
            substrate, metal, ["H2O_central"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        theta_low = results_low["theta_res"][(metal, "H2O_low")]
        theta_high = results_high["theta_res"][(metal, "H2O_high")]
        fwhm = results_central["fwhm"][(metal, "H2O_central")]
        theta_central = results_central["theta_res"][(metal, "H2O_central")]

        sensitivity = [calculate_sensitivity(th, tl, materials["H2O_high"].real, materials["H2O_low"].real)
                       for th, tl in zip(theta_high, theta_low)]
        chi = [calculate_chi(s, f) for s, f in zip(sensitivity, fwhm)]
        q = [calculate_q(t, f) for t, f in zip(theta_central, fwhm)]

        comparison_results["theta_res"][metal] = theta_central
        comparison_results["fwhm"][metal] = fwhm
        comparison_results["sensitivity"][metal] = sensitivity
        comparison_results["chi"][metal] = chi
        comparison_results["q"][metal] = q

    print("\nPlotting metal comparison...")
    plot_figures_of_merit(comparison_results, metal_thicknesses_nm)

else:
    print("Invalid option. Exiting program.")