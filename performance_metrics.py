import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

def calculate_theta_res(Rp, theta_deg):
    idx_min = np.argmin(Rp)
    return theta_deg[idx_min]

def calculate_theta_res_smooth(Rp, theta_deg):
    spline = CubicSpline(theta_deg, Rp)
    result = minimize_scalar(spline, bounds=(theta_deg[0], theta_deg[-1]), method='bounded')
    if result.success:
        return result.x
    else:
        # Fallback to basic method if smoothing fails
        return calculate_theta_res(Rp, theta_deg)

def calculate_fwhm(Rp, theta_deg):
    Rp_min = np.min(Rp)
    Rp_max = np.max(Rp)
    half_max = (Rp_max + Rp_min) / 2

    crossing_indices = np.where(np.diff(np.sign(Rp - half_max)))[0]

    if len(crossing_indices) >= 2:
        theta1 = theta_deg[crossing_indices[0]]
        theta2 = theta_deg[crossing_indices[-1]]
        return abs(theta2 - theta1)
    else:
        return np.nan  # Unable to compute FWHM
def calculate_fwhm_nm(Rp, theta_deg, lambda0_nm, n_prisma):
    """
    Calcula a largura espectral aproximada (em nm) com base na curva R(θ),
    convertendo a FWHM angular usando aproximação local.

    Parâmetros:
    - Rp: vetor de reflectância
    - theta_deg: vetor de ângulos em graus
    - lambda0_nm: comprimento de onda da luz em nm
    - n_prisma: índice de refração real do substrato/prisma

    Retorna:
    - fwhm_nm: largura espectral estimada em nm
    """
    Rp_min = np.min(Rp)
    Rp_max = np.max(Rp)
    half_max = (Rp_max + Rp_min) / 2

    crossing_indices = np.where(np.diff(np.sign(Rp - half_max)))[0]

    if len(crossing_indices) >= 2:
        theta1 = theta_deg[crossing_indices[0]]
        theta2 = theta_deg[crossing_indices[-1]]
        fwhm_deg = abs(theta2 - theta1)

        theta_center_deg = (theta1 + theta2) / 2
        theta_center_rad = np.deg2rad(theta_center_deg)
        fwhm_rad = np.deg2rad(fwhm_deg)

        d_lambda_d_theta = lambda0_nm / np.tan(theta_center_rad)
        fwhm_nm = abs(d_lambda_d_theta * fwhm_rad)

        return fwhm_nm
    else:
        return np.nan


def calculate_sensitivity(theta_res_high, theta_res_low, n_high, n_low):
    delta_theta = theta_res_high - theta_res_low
    delta_n = n_high - n_low
    return delta_theta / delta_n if delta_n != 0 else np.nan

def calculate_chi(sensitivity, fwhm):
    return sensitivity / fwhm if fwhm != 0 else np.nan

def calculate_q(theta_res, fwhm):
    return theta_res / fwhm if fwhm != 0 else np.nan
def calculate_spectral_sensitivity_from_theta(
    theta_res_high, theta_res_low,
    lambda0_nm, n_prisma, n_high, n_low
):
    """
    Calcula a sensibilidade espectral (nm/RIU) com base na variação do ângulo de ressonância
    entre dois analitos com índices diferentes.

    A relação usada é:
    λ_res ≈ λ0 / tan(θ_res)

    Parâmetros:
    - theta_res_high: lista com θ_res para n_high (graus)
    - theta_res_low:  lista com θ_res para n_low  (graus)
    - lambda0_nm: comprimento de onda da luz (nm)
    - n_prisma: índice de refração do substrato (real)
    - n_high, n_low: índices de refração dos analitos

    Retorna:
    - Lista com S_lambda em nm/RIU para cada espessura
    """
    delta_n = n_high - n_low
    if delta_n == 0:
        return [np.nan] * len(theta_res_high)

    theta_high_rad = np.deg2rad(theta_res_high)
    theta_low_rad = np.deg2rad(theta_res_low)

    # Aproximação da posição espectral da ressonância
    lambda_res_high = lambda0_nm / np.tan(theta_high_rad)
    lambda_res_low = lambda0_nm / np.tan(theta_low_rad)

    delta_lambda = lambda_res_high - lambda_res_low
    s_lambda = delta_lambda / delta_n

    return s_lambda
