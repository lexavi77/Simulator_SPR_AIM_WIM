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

    theta_low = results["theta_res"][(metal, "H2O_low")]
    theta_high = results["theta_res"][(metal, "H2O_high")]
    theta_central = results["theta_res"][(metal, "H2O_central")]
    fwhm_central = results["fwhm"][(metal, "H2O_central")]

    delta_n = materials["H2O_high"].real - materials["H2O_low"].real

    # --- Sensibilidade empírica e figuras de mérito associadas
    sensitivity_empirical = [
        calculate_sensitivity(th, tl, materials["H2O_high"].real, materials["H2O_low"].real)
        for th, tl in zip(theta_high, theta_low)
    ]
    chi_empirical = [calculate_chi(s, f) for s, f in zip(sensitivity_empirical, fwhm_central)]
    q_empirical = [calculate_q(t, f) for t, f in zip(theta_central, fwhm_central)]

    results["sensitivity_empirical"][metal] = sensitivity_empirical
    results["chi_empirical"][metal] = chi_empirical
    results["q_empirical"][metal] = q_empirical

    # --- Sensibilidade teórica e figuras de mérito associadas
    n_eff_s = materials["H2O_high"].real  # conforme especificado nas orientações
    n2 = materials[results["substrate"]].real

    eps_metal = materials[metal] ** 2
    eps_mr = eps_metal.real

    sensitivity_theoretical = [
        calculate_theoretical_sensitivity(eps_mr, n_eff_s, n2)
        for _ in theta_central  # uma vez por espessura
    ]
    chi_theoretical = [calculate_chi(s, f) for s, f in zip(sensitivity_theoretical, fwhm_central)]
    q_theoretical = [calculate_q(t, f) for t, f in zip(theta_central, fwhm_central)]

    results["sensitivity_theoretical"][metal] = sensitivity_theoretical
    results["chi_theoretical"][metal] = chi_theoretical
    results["q_theoretical"][metal] = q_theoretical
