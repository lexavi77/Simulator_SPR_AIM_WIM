import numpy as np
import matplotlib.pyplot as plt

from fresnel_utils import getFresnelAIM
from optical_data import materials
from simulation_config import (
    lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, metal_thicknesses_nm, analytes
)
from user_input import select_materials
from calculate_figures import calculate_all_figures_of_merit
from merit_figures_plot import plot_figures_of_merit
from reflectance_simulator import run_reflectance_simulation
from save_results import save_results_to_csv

# ------------------- Main Function -------------------

for metal in ["Ag", "Au", "Cu"]:
    n_complex = materials[metal]
    eps = n_complex ** 2
    print(f"{metal}: n = {n_complex}, ε = {eps}, ε_real = {eps.real}")

def main():
    print("Select simulation mode:")
    print("1 - Analyze a specific material")
    print("2 - Compare metals with fixed analyte (H2O_central)")
    mode = input("Mode (1 or 2): ").strip()

    if mode == "1":
        run_mode_1()
    elif mode == "2":
        run_mode_2()
    else:
        print("Invalid option. Exiting program.")

# ------------------- MODE 1: Specific Material -------------------

def run_mode_1():
    substrate, metal = select_materials()

    results = run_reflectance_simulation(
        substrate, metal, analytes,
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analyte, metal_thicknesses_nm
    )

    results["theta_deg"] = theta_deg
    results["substrate"] = substrate

    calculate_all_figures_of_merit(results, materials, metal)
    plot_figures_of_merit(results, metal_thicknesses_nm)

# ------------------- MODE 2: Metal Comparison -------------------

def run_mode_2():
    print("\nComparison mode selected.")
    substrate_input = input("Select fixed substrate (PMMA, PC, TOPAS): ").strip().upper()
    valid_substrates = {"PMMA", "PC", "TOPAS"}

    if substrate_input not in valid_substrates:
        raise ValueError("Invalid substrate.")
    substrate = substrate_input

    comparison_results = {
        "theta_res": {},
        "fwhm": {},
        "sensitivity_empirical": {},
        "sensitivity_theoretical": {},
        "chi_empirical": {},
        "chi_theoretical": {},
        "q_empirical": {},
        "q_theoretical": {},
        "metal_thicknesses_nm": metal_thicknesses_nm
    }

    for metal in ["Ag", "Au", "Cu"]:
        print(f"\nSimulating for metal: {metal}")

        # Executes the 3 simulations
        res_low = run_reflectance_simulation(
            substrate, metal, ["H2O_low"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )
        res_high = run_reflectance_simulation(
            substrate, metal, ["H2O_high"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )
        res_central = run_reflectance_simulation(
            substrate, metal, ["H2O_central"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        # Prepares the dictionary with all data for metric calculations
        results = {
            "theta_res": {},
            "fwhm": {},
            "reflectance": {},
            "theta_deg": theta_deg,
            "substrate": substrate
        }

        # Combines the results of the 3 simulations
        results["theta_res"].update(res_low["theta_res"])
        results["theta_res"].update(res_high["theta_res"])
        results["theta_res"].update(res_central["theta_res"])

        results["fwhm"].update(res_central["fwhm"])
        results["reflectance"].update(res_central["reflectance"])

        # Calculates all figures of merit
        calculate_all_figures_of_merit(results, materials, metal)

        # Stores the results for this metal
        comparison_results["theta_res"][metal] = results["theta_res"][(metal, "H2O_central")]
        comparison_results["fwhm"][metal] = results["fwhm"][(metal, "H2O_central")]
        comparison_results["sensitivity_empirical"][metal] = results["sensitivity_empirical"][metal]
        comparison_results["sensitivity_theoretical"][metal] = results["sensitivity_theoretical"][metal]
        comparison_results["chi_empirical"][metal] = results["chi_empirical"][metal]
        comparison_results["chi_theoretical"][metal] = results["chi_theoretical"][metal]
        comparison_results["q_empirical"][metal] = results["q_empirical"][metal]
        comparison_results["q_theoretical"][metal] = results["q_theoretical"][metal]

    print("\nPlotting metal comparison...")
    plot_figures_of_merit(comparison_results, metal_thicknesses_nm)

    # Exports results for each metal
    for metal in ["Ag", "Au", "Cu"]:
        save_results_to_csv(comparison_results, metal, filename=f"results_{metal}.csv")

# ------------------- Execution -------------------

if __name__ == "__main__":
    main()
