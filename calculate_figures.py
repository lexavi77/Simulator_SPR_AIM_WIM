from performance_metrics import (
    calculate_sensitivity,
    calculate_chi,
    calculate_q,
    calculate_fwhm_nm,
    calculate_spectral_sensitivity_from_theta  # ⬅️ novo
)

from simulation_config import lambda0  # lambda0 em metros (850e-9)

def calculate_all_figures_of_merit(results, materials, metal):
    if "sensitivity" not in results:
        results["sensitivity"] = {}
    if "chi" not in results:
        results["chi"] = {}
    if "q" not in results:
        results["q"] = {}
    if "fwhm_nm" not in results:
        results["fwhm_nm"] = {}
    if "s_lambda" not in results:
        results["s_lambda"] = {}  # ⬅️ novo
    if "chi_lambda" not in results:
        results["chi_lambda"] = {}  # ⬅️ novo

    theta_low = results["theta_res"][(metal, "H2O_low")]
    theta_high = results["theta_res"][(metal, "H2O_high")]
    theta_central = results["theta_res"][(metal, "H2O_central")]
    fwhm_central = results["fwhm"][(metal, "H2O_central")]

    delta_n = materials["H2O_high"].real - materials["H2O_low"].real
    n_prisma = materials[results["substrate"]].real
    theta_deg = results["theta_deg"]

    # --- FWHM espectral (nm)
    fwhm_nm_list = []
    for Rp_curve in results["reflectance"][(metal, "H2O_central")]:
        fwhm_nm = calculate_fwhm_nm(
            Rp_curve,
            theta_deg,
            lambda0 * 1e9,  # para nm
            n_prisma
        )
        fwhm_nm_list.append(fwhm_nm)

    # --- Sensibilidade angular e figuras de mérito angulares
    sensitivity = [
        calculate_sensitivity(th, tl, materials["H2O_high"].real, materials["H2O_low"].real)
        for th, tl in zip(theta_high, theta_low)
    ]
    chi = [calculate_chi(s, f) for s, f in zip(sensitivity, fwhm_central)]
    q = [calculate_q(t, f) for t, f in zip(theta_central, fwhm_central)]

    # --- Sensibilidade espectral (nm/RIU) e χ espectral
    s_lambda = calculate_spectral_sensitivity_from_theta(
        theta_res_high=theta_high,
        theta_res_low=theta_low,
        lambda0_nm=lambda0 * 1e9,
        n_prisma=n_prisma,
        n_high=materials["H2O_high"].real,
        n_low=materials["H2O_low"].real
    )
    chi_lambda = [
        s / f if f != 0 else np.nan
        for s, f in zip(s_lambda, fwhm_nm_list)
    ]

    # --- Armazenamento dos resultados
    results["sensitivity"][metal] = sensitivity
    results["chi"][metal] = chi
    results["q"][metal] = q
    results["fwhm_nm"][metal] = fwhm_nm_list
    results["s_lambda"][metal] = s_lambda
    results["chi_lambda"][metal] = chi_lambda
