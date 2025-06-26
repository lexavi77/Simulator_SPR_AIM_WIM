from performance_metrics import (
    calculate_sensitivity,
    calculate_chi,
    calculate_q,
    calculate_theoretical_sensitivity
)

def calculate_all_figures_of_merit(results, materials, metal):
    if "sensitivity_empirical" not in results:
        results["sensitivity_empirical"] = {}
    if "chi_empirical" not in results:
        results["chi_empirical"] = {}
    if "q_empirical" not in results:
        results["q_empirical"] = {}

    if "sensitivity_theoretical" not in results:
        results["sensitivity_theoretical"] = {}
    if "chi_theoretical" not in results:
        results["chi_theoretical"] = {}
    if "q_theoretical" not in results:
        results["q_theoretical"] = {}

    # Extract angles for both analytes
    theta_low = results["theta_res"][(metal, "analyte_01")]
    theta_high = results["theta_res"][(metal, "analyte_02")]
    fwhm_low = results["fwhm"][(metal, "analyte_01")]
    fwhm_high = results["fwhm"][(metal, "analyte_02")]

    # Use average FWHM and theta for chi and Q
    fwhm_avg = [(fl + fh) / 2 for fl, fh in zip(fwhm_low, fwhm_high)]
    theta_avg = [(tl + th) / 2 for tl, th in zip(theta_low, theta_high)]

    n1 = materials["analyte_01"].real
    n2 = materials["analyte_02"].real
    delta_n = n2 - n1

    # --- Empirical sensitivity and figures of merit
    sensitivity_empirical = [
        calculate_sensitivity(th, tl, n2, n1)
        for th, tl in zip(theta_high, theta_low)
    ]
    chi_empirical = [calculate_chi(s, f) for s, f in zip(sensitivity_empirical, fwhm_avg)]
    q_empirical = [calculate_q(t, f) for t, f in zip(theta_avg, fwhm_avg)]

    results["sensitivity_empirical"][metal] = sensitivity_empirical
    results["chi_empirical"][metal] = chi_empirical
    results["q_empirical"][metal] = q_empirical

    # --- Theoretical sensitivity and figures of merit
    n_eff_s = n2  # Use the higher analyte index
    n_substrate = materials[results["substrate"]].real
    eps_metal = materials[metal] ** 2
    eps_mr = eps_metal.real

    sensitivity_theoretical = [
        calculate_theoretical_sensitivity(eps_mr, n_eff_s, n_substrate)
        for _ in theta_avg
    ]
    chi_theoretical = [calculate_chi(s, f) for s, f in zip(sensitivity_theoretical, fwhm_avg)]
    q_theoretical = [calculate_q(t, f) for t, f in zip(theta_avg, fwhm_avg)]

    results["sensitivity_theoretical"][metal] = sensitivity_theoretical
    results["chi_theoretical"][metal] = chi_theoretical
    results["q_theoretical"][metal] = q_theoretical
