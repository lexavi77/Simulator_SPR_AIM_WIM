import numpy as np
from optical_data import materials
from simulation_config import (
    lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, metal_thicknesses_nm, analytes
)
from user_input import select_materials
from fresnel_utils import getFresnelAIM
from reflectance_simulator import run_reflectance_simulation
from calculate_figures import calculate_all_figures_of_merit
from merit_figures_plot import plot_figures_of_merit
from save_results import save_results_to_csv
from plot_reflectance_full import plot_reflectance_22_curves
from plot_sensitive_structure import plot_angular_response_for_sensitive_structure_and_export_csv


def main():
    print("Select simulation mode:")
    print("1 - Analyze a specific material")
    print("2 - Compare metals with fixed analyte (H2O_central)")
    print("3 - Plot 22 reflectance curves per metal (final report requirement)")
    print("4 - Plot sensitive structure (TOPAS + d=55nm) for 3 metals (6 analytes)")
    mode = input("Mode (1, 2, 3 or 4): ").strip()

    if mode == "1":
        run_mode_1()
    elif mode == "2":
        run_mode_2()
    elif mode == "3":
        run_mode_3()
    elif mode == "4":
        run_mode_4()
    else:
        print("Invalid option. Exiting program.")


def run_mode_1():
    # Select substrate and metal from user
    substrate, metal = select_materials()

    # Run simulation
    results = run_reflectance_simulation(
        substrate, metal, analytes,
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analyte, metal_thicknesses_nm
    )

    results["theta_deg"] = theta_deg
    results["substrate"] = substrate

    # Compute and plot figures of merit
    calculate_all_figures_of_merit(results, materials, metal)
    plot_figures_of_merit(results, metal_thicknesses_nm)


def run_mode_2():
    print("\n[MODE 2] Metal comparison selected.")
    substrate_input = input("Select substrate (PMMA, PC, TOPAS): ").strip().upper()
    if substrate_input not in {"PMMA", "PC", "TOPAS"}:
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

        results = {
            "theta_res": {},
            "fwhm": {},
            "reflectance": {},
            "theta_deg": theta_deg,
            "substrate": substrate
        }

        results["theta_res"].update(res_low["theta_res"])
        results["theta_res"].update(res_high["theta_res"])
        results["theta_res"].update(res_central["theta_res"])
        results["fwhm"].update(res_central["fwhm"])
        results["reflectance"].update(res_central["reflectance"])

        calculate_all_figures_of_merit(results, materials, metal)

        comparison_results["theta_res"][metal] = results["theta_res"][(metal, "H2O_central")]
        comparison_results["fwhm"][metal] = results["fwhm"][(metal, "H2O_central")]
        comparison_results["sensitivity_empirical"][metal] = results["sensitivity_empirical"][metal]
        comparison_results["sensitivity_theoretical"][metal] = results["sensitivity_theoretical"][metal]
        comparison_results["chi_empirical"][metal] = results["chi_empirical"][metal]
        comparison_results["chi_theoretical"][metal] = results["chi_theoretical"][metal]
        comparison_results["q_empirical"][metal] = results["q_empirical"][metal]
        comparison_results["q_theoretical"][metal] = results["q_theoretical"][metal]

    # Final plotting and export
    plot_figures_of_merit(comparison_results, metal_thicknesses_nm)
    for metal in ["Ag", "Au", "Cu"]:
        save_results_to_csv(comparison_results, metal, filename=f"results_{metal}.csv")


def run_mode_3():
    print("\n[MODE 3] Plotting 22 reflectance curves per metal...")

    substrate_input = input("Select substrate (PMMA, PC, TOPAS): ").strip().upper()
    if substrate_input not in {"PMMA", "PC", "TOPAS"}:
        raise ValueError("Invalid substrate.")
    substrate = substrate_input

    analytes_22 = ["H2O_low", "H2O_high"]

    results = {
        "theta_res": {},
        "fwhm": {},
        "reflectance": {},
        "theta_deg": theta_deg,
        "substrate": substrate
    }

    for metal in ["Ag", "Au", "Cu"]:
        res = run_reflectance_simulation(
            substrate, metal, analytes_22,
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        results["theta_res"].update(res["theta_res"])
        results["fwhm"].update(res["fwhm"])
        results["reflectance"].update(res["reflectance"])

    plot_reflectance_22_curves(results, metal_thicknesses_nm)


def run_mode_4():
    print("\n[MODE 4] Plotting sensitive structures (TOPAS + d=55nm) for Ag, Au, Cu")
    substrate = "TOPAS"
    metals = ["Ag", "Au", "Cu"]
    plot_angular_response_for_sensitive_structure_and_export_csv(
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analyte, substrate, metals
    )


# ------------------- Execution -------------------

if __name__ == "__main__":
    main()
