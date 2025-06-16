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

# ------------------- Função principal -------------------

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

# ------------------- MODO 1: Material específico -------------------

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

# ------------------- MODO 2: Comparação entre metais -------------------

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

        # Executa as 3 simulações
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

        # Prepara o dicionário com todos os dados para cálculo das métricas
        results = {
            "theta_res": {},
            "fwhm": {},
            "reflectance": {},
            "theta_deg": theta_deg,
            "substrate": substrate
        }

        # Combina os resultados das 3 simulações
        results["theta_res"].update(res_low["theta_res"])
        results["theta_res"].update(res_high["theta_res"])
        results["theta_res"].update(res_central["theta_res"])

        results["fwhm"].update(res_central["fwhm"])
        results["reflectance"].update(res_central["reflectance"])

        # Calcula todas as figuras de mérito
        calculate_all_figures_of_merit(results, materials, metal)

        # Armazena os resultados para esse metal
        comparison_results["theta_res"][metal] = results["theta_res"][(metal, "H2O_central")]
        comparison_results["fwhm"][metal] = results["fwhm"][(metal, "H2O_central")]
        comparison_results["fwhm_nm"][metal] = results["fwhm_nm"][metal]
        comparison_results["sensitivity"][metal] = results["sensitivity"][metal]
        comparison_results["s_lambda"][metal] = results["s_lambda"][metal]
        comparison_results["chi"][metal] = results["chi"][metal]
        comparison_results["chi_lambda"][metal] = results["chi_lambda"][metal]
        comparison_results["q"][metal] = results["q"][metal]

    print("\nPlotting metal comparison...")
    plot_figures_of_merit(comparison_results, metal_thicknesses_nm)

    # Exporta resultados por metal
    for metal in ["Ag", "Au", "Cu"]:
        save_results_to_csv(comparison_results, metal, filename=f"results_{metal}.csv")

# ------------------- Execução -------------------

if __name__ == "__main__":
    main()
