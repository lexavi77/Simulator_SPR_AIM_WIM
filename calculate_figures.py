from performance_metrics import (
    calculate_sensitivity,
    calculate_chi,
    calculate_q,
    calculate_theoretical_sensitivity
)

def calculate_all_figures_of_merit(results, materials, metal):
    for analyte in ["analyte_01", "analyte_02"]:
        theta_res = results["theta_res"][(metal, analyte)]
        fwhm = results["fwhm"][(metal, analyte)]

        # --- Empirical Q
        q_values = [calculate_q(t, f) for t, f in zip(theta_res, fwhm)]
        results.setdefault("q_empirical", {})[(metal, analyte)] = q_values

        # --- Theoretical values
        n_eff_s = materials[analyte].real
        n_substrate = materials[results["substrate"]].real
        eps_metal = materials[metal] ** 2
        eps_mr = eps_metal.real

        sensitivity_theoretical = [
            calculate_theoretical_sensitivity(eps_mr, n_eff_s, n_substrate)
            for _ in theta_res
        ]
        chi_theoretical = [
            calculate_chi(s, f) for s, f in zip(sensitivity_theoretical, fwhm)
        ]
        q_theoretical = [
            calculate_q(t, f) for t, f in zip(theta_res, fwhm)
        ]

        results.setdefault("sensitivity_theoretical", {})[(metal, analyte)] = sensitivity_theoretical
        results.setdefault("chi_theoretical", {})[(metal, analyte)] = chi_theoretical
        results.setdefault("q_theoretical", {})[(metal, analyte)] = q_theoretical

    # --- Empirical sensitivity (comparison between the two analytes)
    theta_low = results["theta_res"][(metal, "analyte_01")]
    theta_high = results["theta_res"][(metal, "analyte_02")]
    fwhm_01 = results["fwhm"][(metal, "analyte_01")]
    fwhm_02 = results["fwhm"][(metal, "analyte_02")]

    n1 = materials["analyte_01"].real
    n2 = materials["analyte_02"].real

    sensitivity_empirical = [
        calculate_sensitivity(th, tl, n2, n1)
        for th, tl in zip(theta_high, theta_low)
    ]

    results.setdefault("sensitivity_empirical", {})[metal] = sensitivity_empirical

    # --- Empirical chi for each analyte (using empirical sensitivity)
    chi_empirical_01 = [calculate_chi(s, f) for s, f in zip(sensitivity_empirical, fwhm_01)]
    chi_empirical_02 = [calculate_chi(s, f) for s, f in zip(sensitivity_empirical, fwhm_02)]

    results.setdefault("chi_empirical", {})[(metal, "analyte_01")] = chi_empirical_01
    results.setdefault("chi_empirical", {})[(metal, "analyte_02")] = chi_empirical_02
