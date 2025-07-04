from performance_metrics import (
    calculate_theta_res_smooth,
    calculate_fwhm,
    calculate_sensitivity_empirical,
    calculate_theoretical_sensitivity_precise,
    calculate_chi,
    calculate_q
)
import numpy as np

def calculate_all_figures_of_merit(results, materials, metal):
    substrate_index = materials[results["substrate"]].real

    for analyte in ["analyte_01", "analyte_02"]:
        theta_res = results["theta_res"][(metal, analyte)]
        fwhm = results["fwhm"][(metal, analyte)]

        # --- Empirical Q
        q_values = [calculate_q(t, f) for t, f in zip(theta_res, fwhm)]
        results.setdefault("q_empirical", {})[(metal, analyte)] = q_values

        # --- Theoretical sensitivity, chi, Q
        n_analyte = materials[analyte].real

        sensitivity_theoretical = [
            calculate_theoretical_sensitivity_precise(
                n_metal=materials[metal],
                n_analyte=n_analyte,
                n_substrate=substrate_index
            )
        ] * len(theta_res)  # valor fixo para todas as espessuras

        chi_theoretical = [calculate_chi(s, f) for s, f in zip(sensitivity_theoretical, fwhm)]
        q_theoretical = [calculate_q(t, f) for t, f in zip(theta_res, fwhm)]

        results.setdefault("sensitivity_theoretical", {})[(metal, analyte)] = sensitivity_theoretical
        results.setdefault("chi_theoretical", {})[(metal, analyte)] = chi_theoretical
        results.setdefault("q_theoretical", {})[(metal, analyte)] = q_theoretical

    # --- Sensibilidade empírica (Δθ / Δn) entre analyte_01 (negativo) e analyte_02 (positivo)
    theta_neg = results["theta_res"][(metal, "analyte_01")]
    theta_pos = results["theta_res"][(metal, "analyte_02")]

    fwhm_neg = results["fwhm"][(metal, "analyte_01")]
    fwhm_pos = results["fwhm"][(metal, "analyte_02")]

    n_neg = materials["analyte_01"].real
    n_pos = materials["analyte_02"].real

    sensitivity_empirical = [
        calculate_sensitivity_empirical(tp, tn, n_pos, n_neg)
        for tp, tn in zip(theta_pos, theta_neg)
    ]

    results.setdefault("sensitivity_empirical", {})[metal] = sensitivity_empirical

    # --- χ empíricos para cada analyte usando mesma sensibilidade empírica
    chi_empirical_pos = [calculate_chi(s, f) for s, f in zip(sensitivity_empirical, fwhm_pos)]
    chi_empirical_neg = [calculate_chi(s, f) for s, f in zip(sensitivity_empirical, fwhm_neg)]

    results.setdefault("chi_empirical", {})[(metal, "analyte_02")] = chi_empirical_pos
    results.setdefault("chi_empirical", {})[(metal, "analyte_01")] = chi_empirical_neg
