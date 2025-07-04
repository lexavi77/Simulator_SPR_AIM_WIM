from user_input import select_materials
from fresnel_utils import getFresnelAIM
from reflectance_simulator import run_reflectance_simulation
from calculate_figures import calculate_all_figures_of_merit
from merit_figures_plot import plot_figures_of_merit
from save_results import save_results_to_csv
from plot_reflectance_full import plot_reflectance_22_curves
from plot_sensitive_structure import plot_figures_of_merit_comparative
from plot_style import apply_plot_style
from plot_sensitive_structure import plot_angular_response_for_sensitive_structure_and_export_csv
from optical_data import materials
from simulation_config import (
    lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, metal_thicknesses_nm, analytes
)

def run_mode_1():
    """
    Mode 1: User selects a substrate; simulator compares Ag, Au, Cu
    using analyte_01 (negative) and analyte_02 (positive) and calculates figures of merit.
    """
    from simulation_config import analytes

    apply_plot_style()

    available_substrates = ["PMMA", "PC", "TOPAS"]
    print("[MODE 1] Compare Ag, Au, Cu for a selected substrate using analyte_01 and analyte_02")
    print("Select substrate:")
    for i, s in enumerate(available_substrates, 1):
        print(f"{i} - {s}")

    try:
        index = int(input("Option: ").strip())
        substrate = available_substrates[index - 1]
    except (ValueError, IndexError):
        print("[ERROR] Invalid option.")
        return

    analyte = {
        "analyte_01": analytes["analyte_01"],  # negative
        "analyte_02": analytes["analyte_02"]   # positive
    }

    results = {
        "theta_deg": theta_deg,
        "substrate": substrate,
        "theta_res": {},
        "fwhm": {},
        "reflectance": {},
    }

    for metal in ["Ag", "Au", "Cu"]:
        res = run_reflectance_simulation(
            substrate, metal, analyte,
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        results["reflectance"].update(res["reflectance"])
        results["theta_res"].update(res["theta_res"])
        results["fwhm"].update(res["fwhm"])

        calculate_all_figures_of_merit(res, materials, metal)

        for key in [
            "sensitivity_theoretical", "chi_theoretical", "q_theoretical"
        ]:
            if key in res:
                if key not in results:
                    results[key] = {}
                results[key].update(res[key])

    plot_figures_of_merit(results, metal_thicknesses_nm)
    
    # ⚠️ Corrigido: passa o dicionário de analytes corretamente
    save_results_to_csv(results, metal_thicknesses_nm, analyte)


def run_mode_2():
    print("\n[MODE 2] Plotting 22 reflectance curves per metal...")

    substrate_input = input("Select substrate (PMMA, PC, TOPAS): ").strip().upper()
    if substrate_input not in {"PMMA", "PC", "TOPAS"}:
        raise ValueError("Invalid substrate.")
    substrate = substrate_input

    analytes_22 = ["analyte_01", "analyte_02"]

    results = {
        "theta_deg": theta_deg,
        "substrate": substrate,
        "theta_res": {},
        "fwhm": {},
        "reflectance": {},
        "sensitivity": {},
        "chi": {},
        "Q": {},
    }

    for metal in ["Ag", "Au", "Cu"]:
        res = run_reflectance_simulation(
            substrate, metal, analytes_22,
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        results["reflectance"].update(res["reflectance"])
        results["theta_res"].update(res["theta_res"])
        results["fwhm"].update(res["fwhm"])

        calculate_all_figures_of_merit(res, materials, metal)

        for key in ["sensitivity_empirical", "chi_empirical", "q_empirical",
                    "sensitivity_theoretical", "chi_theoretical", "q_theoretical"]:
            if key in res:
                if key not in results:
                    results[key] = {}
                results[key].update(res[key])

    plot_reflectance_22_curves(results, metal_thicknesses_nm, figures=results)


def run_mode_3():
    print("\n[MODE 3] Plotting sensitive structures (TOPAS + d=55nm) for Ag, Au, Cu")

    substrate = "TOPAS"
    analytes_22 = ["analyte_01", "analyte_02"]
    metals = ["Ag", "Au", "Cu"]

    results = {
        "theta_deg": theta_deg,
        "substrate": substrate,
        "theta_res": {},
        "fwhm": {},
        "reflectance": {},
    }

    for metal in metals:
        res = run_reflectance_simulation(
            substrate, metal, analytes_22,
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )

        results["reflectance"].update(res["reflectance"])
        results["theta_res"].update(res["theta_res"])
        results["fwhm"].update(res["fwhm"])

        calculate_all_figures_of_merit(res, materials, metal)

        for key in [
            "sensitivity_empirical", "chi_empirical", "q_empirical",
            "sensitivity_theoretical", "chi_theoretical", "q_theoretical"
        ]:
            if key in res:
                if key not in results:
                    results[key] = {}
                results[key].update(res[key])

    plot_figures_of_merit_comparative(results, metal_thicknesses_nm, save_dir="outputs/sensitive_structure")
