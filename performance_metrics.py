import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

def calculate_theta_res(Rp, theta_deg):
    idx_min = np.argmin(Rp)
    return theta_deg[idx_min]

def calculate_theta_res_smooth(theta_deg, Rp):
    sorted_indices = np.argsort(theta_deg)
    theta_sorted = theta_deg[sorted_indices]
    Rp_sorted = Rp[sorted_indices]

    _, unique_indices = np.unique(theta_sorted, return_index=True)
    theta_sorted = theta_sorted[unique_indices]
    Rp_sorted = Rp_sorted[unique_indices]

    try:
        spline = CubicSpline(theta_sorted, Rp_sorted)
        threshold = np.max(Rp_sorted) * 0.9
        candidates = np.where(Rp_sorted < threshold)[0]

        if len(candidates) >= 2:
            start = theta_sorted[candidates[0]]
            end = theta_sorted[candidates[-1]]
        else:
            start = theta_sorted[0]
            end = theta_sorted[-1]

        result = minimize_scalar(spline, bounds=(start, end), method='bounded')
        if result.success:
            return result.x
    except Exception as e:
        print("⚠️ Error in calculate_theta_res_smooth:", e)

    return calculate_theta_res(Rp_sorted, theta_sorted)

def calculate_fwhm(Rp, theta_deg):
    Rp_min = np.min(Rp)
    Rp_max = np.max(Rp)
    half_max = (Rp_max + Rp_min) / 2
    crossing_indices = np.where(np.diff(np.sign(Rp - half_max)))[0]

    if len(crossing_indices) >= 2:
        theta1 = theta_deg[crossing_indices[0]]
        theta2 = theta_deg[crossing_indices[-1]]
        return abs(theta2 - theta1)
    return np.nan

def calculate_q(theta_res, fwhm):
    return theta_res / fwhm if fwhm and not np.isnan(fwhm) else np.nan

def calculate_chi(sensitivity, fwhm):
    return sensitivity / fwhm if fwhm and not np.isnan(fwhm) else np.nan

def calculate_sensitivity_empirical(theta_res_pos, theta_res_neg, n_pos, n_neg):
    delta_n = n_pos - n_neg
    return (theta_res_pos - theta_res_neg) / delta_n if delta_n != 0 else np.nan

def calculate_theoretical_sensitivity_precise(n_metal, n_analyte, n_substrate):
    eps = n_metal ** 2
    eps_mr = np.real(eps)
    n_eff = np.real(n_analyte)
    n2 = np.real(n_substrate)

    numerator = eps_mr ** 2
    denominator = abs(eps_mr + n_eff ** 2)
    root_term = eps_mr * n2**2 * (eps_mr + n_eff**2) - eps_mr**2 * n_eff**2

    if denominator == 0 or root_term <= 0:
        return np.nan

    sensitivity_rad = numerator / (denominator * np.sqrt(root_term))
    return np.degrees(sensitivity_rad)

def compute_figures_of_merit(reflectance_data, config):
    # Analytes fixos conforme o modelo atual
    analyte_neg = config["analytes"]["analyte_01"]  # 1.3492
    analyte_pos = config["analytes"]["analyte_02"]  # 1.3481
    metal_thicknesses = config["metal_thicknesses_nm"]

    substrate_n = config["layers"]["substrate_n"]
    metal_n = config["layers"]["metal_n"]

    # Reflectância e FWHM para ambos os analytes
    theta_res_neg = reflectance_data["analyte_01"]["theta_res"]
    theta_res_pos = reflectance_data["analyte_02"]["theta_res"]
    fwhm_list = reflectance_data["analyte_01"]["fwhm"]

    # Sensibilidade empírica ponto a ponto
    s_empirical = [
        calculate_sensitivity_empirical(pos, neg, analyte_pos, analyte_neg)
        for pos, neg in zip(theta_res_pos, theta_res_neg)
    ]

    # Sensibilidade teórica baseada no analyte positivo
    s_theoretical = calculate_theoretical_sensitivity_precise(
        n_metal=metal_n,
        n_analyte=analyte_pos,
        n_substrate=substrate_n
    )

    # Outras métricas
    q_list = [calculate_q(theta, fwhm) for theta, fwhm in zip(theta_res_pos, fwhm_list)]
    chi_empirical = [calculate_chi(s, f) for s, f in zip(s_empirical, fwhm_list)]
    chi_theoretical = [calculate_chi(s_theoretical, f) for f in fwhm_list]

    figures = {
        "theta_res": {"analyte_02": theta_res_pos},  # positivo
        "fwhm": {"analyte_02": fwhm_list},
        "q": {"analyte_02": q_list},

        "sensitivity_empirical": s_empirical,
        "sensitivity_theoretical": [s_theoretical] * len(metal_thicknesses),

        "chi_empirical": chi_empirical,
        "chi_theoretical": chi_theoretical,

        "q_empirical": q_list,
        "q_theoretical": q_list
    }

    return figures
