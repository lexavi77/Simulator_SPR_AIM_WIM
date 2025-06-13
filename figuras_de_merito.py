import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar


def calcular_theta_res(Rp, theta_deg):
    """Retorna o ângulo de ressonância (mínimo da curva de reflectância - método simples)."""
    idx_min = np.argmin(Rp)
    return theta_deg[idx_min]


def calcular_theta_res_suave(Rp, theta_deg):
    """Retorna o ângulo de ressonância minimizando uma spline de Rp(θ) para maior precisão."""
    spline = CubicSpline(theta_deg, Rp)
    resultado = minimize_scalar(spline, bounds=(theta_deg[0], theta_deg[-1]), method='bounded')
    if resultado.success:
        return resultado.x
    else:
        # Fallback para o método simples se a suavização falhar
        return calcular_theta_res(Rp, theta_deg)


def calcular_fwhm(Rp, theta_deg):
    """Calcula a largura à meia altura (FWHM) da curva de reflectância."""
    Rp_min = np.min(Rp)
    Rp_max = np.max(Rp)
    half_max = (Rp_max + Rp_min) / 2

    crossing_indices = np.where(np.diff(np.sign(Rp - half_max)))[0]

    if len(crossing_indices) >= 2:
        theta1 = theta_deg[crossing_indices[0]]
        theta2 = theta_deg[crossing_indices[-1]]
        return abs(theta2 - theta1)
    else:
        return np.nan  # Não foi possível calcular FWHM


def calcular_sensibilidade(theta_res_high, theta_res_low, n_high, n_low):
    """Calcula a sensibilidade angular (S)."""
    delta_theta = theta_res_high - theta_res_low
    delta_n = n_high - n_low
    return delta_theta / delta_n if delta_n != 0 else np.nan


def calcular_chi(sensibilidade, fwhm):
    """Calcula o parâmetro chi (χ), razão entre sensibilidade e FWHM."""
    return sensibilidade / fwhm if fwhm != 0 else np.nan


def calcular_q(theta_res, fwhm):
    """Calcula o fator de qualidade Q."""
    return theta_res / fwhm if fwhm != 0 else np.nan
