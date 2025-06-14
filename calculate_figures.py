from performance_metrics import calculate_sensitivity, calculate_chi, calculate_q

def calculate_all_figures_of_merit(results, materials, metal):
    if "sensitivity" not in results:
        results["sensitivity"] = {}
    if "chi" not in results:
        results["chi"] = {}
    if "q" not in results:
        results["q"] = {}

    theta_low = results["theta_res"][(metal, "H2O_low")]
    theta_high = results["theta_res"][(metal, "H2O_high")]
    theta_central = results["theta_res"][(metal, "H2O_central")]
    fwhm_central = results["fwhm"][(metal, "H2O_central")]

    delta_n = materials["H2O_high"].real - materials["H2O_low"].real

    sensitivity = [
        calculate_sensitivity(th, tl, materials["H2O_high"].real, materials["H2O_low"].real)
        for th, tl in zip(theta_high, theta_low)
    ]
    chi = [calculate_chi(s, f) for s, f in zip(sensitivity, fwhm_central)]
    q = [calculate_q(t, f) for t, f in zip(theta_central, fwhm_central)]

    results["sensitivity"][metal] = sensitivity
    results["chi"][metal] = chi
    results["q"][metal] = q
