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

def calculate_sensitivity(theta_res_high, theta_res_low, n_high, n_low):
    delta_theta = theta_res_high - theta_res_low
    delta_n = n_high - n_low
    return delta_theta / delta_n if delta_n != 0 else np.nan

def calculate_chi(sensitivity, fwhm):
    return sensitivity / fwhm if fwhm != 0 else np.nan

def calculate_q(theta_res, fwhm):
    return theta_res / fwhm if fwhm != 0 else np.nan
