import numpy as np
import matplotlib.pyplot as plt
import os
from fresnel_utils import getFresnelAIM, restrict_range
from matplotlib.font_manager import FontProperties
from plot_style import apply_plot_style
from plot_utils import save_figure
from reflectance_simulator import run_reflectance_simulation
from performance_metrics import (
    calculate_sensitivity_empirical,
    calculate_theoretical_sensitivity_precise,
    calculate_q,
    calculate_chi
)
from merit_figures_plot import plot_figures_of_merit
from results_export import save_results_to_csv
from optical_data import (
    materials, theta_deg, theta_rad,
    lambda0, d_cr, d_analyte, metal_thicknesses_nm
)

import numpy as np

def run_mode_1():
    print("[MODE 1] Compare Ag, Au, Cu for a selected substrate using analyte_01 and analyte_02")
    available_substrates = ["PMMA", "PC", "TOPAS"]
    for i, s in enumerate(available_substrates, 1):
        print(f"{i} - {s}")
    try:
        index = int(input("Select substrate (1-3): ").strip())
        substrate = available_substrates[index - 1]
    except (ValueError, IndexError):
        print("[ERROR] Invalid option.")
        return

    analytes = {
        "analyte_01": materials["analyte_01"],  # negative
        "analyte_02": materials["analyte_02"]   # positive
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
            substrate, metal, analytes,
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analyte, metal_thicknesses_nm
        )
        results["reflectance"].update(res["reflectance"])
        results["theta_res"].update(res["theta_res"])
        results["fwhm"].update(res["fwhm"])

        key = (metal, "analyte_02")
        theta_res_neg = res["theta_res"][(metal, "analyte_01")]
        theta_res_pos = res["theta_res"][(metal, "analyte_02")]
        fwhm_list = res["fwhm"][(metal, "analyte_02")]

        s_empirical = [
            calculate_sensitivity_empirical(pos, neg, analytes["analyte_02"], analytes["analyte_01"])
            for pos, neg in zip(theta_res_pos, theta_res_neg)
        ]
        s_theoretical = calculate_theoretical_sensitivity_precise(
            n_metal=materials[metal],
            n_analyte=analytes["analyte_02"],
            n_substrate=materials[substrate]
        )
        q_list = [calculate_q(theta, fwhm) for theta, fwhm in zip(theta_res_pos, fwhm_list)]
        chi_empirical = [calculate_chi(s, f) for s, f in zip(s_empirical, fwhm_list)]
        chi_theoretical = [calculate_chi(s_theoretical, f) for f in fwhm_list]

        results.setdefault("sensitivity_empirical", {})[metal] = s_empirical
        results.setdefault("sensitivity_theoretical", {})[key] = [s_theoretical] * len(fwhm_list)
        results.setdefault("chi_empirical", {})[key] = chi_empirical
        results.setdefault("chi_theoretical", {})[key] = chi_theoretical
        results.setdefault("q_empirical", {})[key] = q_list
        results.setdefault("q_theoretical", {})[key] = q_list

    plot_figures_of_merit(results, metal_thicknesses_nm)
    save_results_to_csv(results, metal_thicknesses_nm, analytes)

if __name__ == "__main__":
    run_mode_1()
