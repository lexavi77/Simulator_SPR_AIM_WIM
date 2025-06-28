from user_input import select_materials
from fresnel_utils import getFresnelAIM
from reflectance_simulator import run_reflectance_simulation
from calculate_figures import calculate_all_figures_of_merit
from merit_figures_plot import plot_figures_of_merit
from save_results import save_results_to_csv
from plot_reflectance_full import plot_reflectance_22_curves
from plot_style import apply_plot_style
from plot_sensitive_structure import plot_angular_response_for_sensitive_structure_and_export_csv
from optical_data import materials
from simulation_config import (
    lambda0, theta_deg, theta_rad,
    d_cr, d_analyte, metal_thicknesses_nm, analytes
)

def run_mode_1():
    apply_plot_style()  # Aplica o estilo MATLAB-like

    substrate, metal = select_materials()

    # Simula para analyte_01 e analyte_02
    results = run_reflectance_simulation(
        substrate, metal, analytes,
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analyte, metal_thicknesses_nm
    )

    results["theta_deg"] = theta_deg
    results["substrate"] = substrate

    # Calcula figuras de mérito
    calculate_all_figures_of_merit(results, materials, metal)

    # Plota e salva gráficos das figuras de mérito
    plot_figures_of_merit(results, metal_thicknesses_nm)

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

        # Merge reflectance and performance metrics
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

    # Plot and save the 22 reflectance curves per metal
    plot_reflectance_22_curves(results, metal_thicknesses_nm)


def run_mode_3():
    print("\n[MODE 3] Plotting sensitive structures (TOPAS + d=55nm) for Ag, Au, Cu")
    substrate = "TOPAS"
    metals = ["Ag", "Au", "Cu"]
    plot_angular_response_for_sensitive_structure_and_export_csv(
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analyte, substrate, metals
    )
