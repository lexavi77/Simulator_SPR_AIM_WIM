import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from numpy import pi
import warnings

def calculate_theta_res(Rp, theta_deg):
    """Returns the angle at which reflectance is minimum."""
    return theta_deg[np.argmin(Rp)]

def calculate_theta_res_smooth(theta_deg, Rp, threshold_ratio=0.98, min_angle=50, max_angle=80):
    """
    Robust estimation of the resonance angle using cubic spline interpolation.

    Parameters:
        theta_deg (np.ndarray): Array of incidence angles in degrees.
        Rp (np.ndarray): Reflectance array.
        threshold_ratio (float): Ratio to define resonance dip window.
        min_angle, max_angle (float): Angle bounds for the fitting.

    Returns:
        theta_res (float): Estimated resonance angle.
    """
    try:
        mask = (theta_deg >= min_angle) & (theta_deg <= max_angle)
        theta_filtered = theta_deg[mask]
        Rp_filtered = Rp[mask]

        if len(theta_filtered) < 5:
            warnings.warn("Insufficient data in selected range. Falling back to simple minimum.")
            return calculate_theta_res(Rp, theta_deg)

        spline = CubicSpline(theta_filtered, Rp_filtered)
        threshold = np.max(Rp_filtered) * threshold_ratio
        candidates = np.where(Rp_filtered < threshold)[0]

        if len(candidates) < 2:
            warnings.warn("No valid resonance dip found. Using fallback.")
            return calculate_theta_res(Rp, theta_deg)

        start = theta_filtered[candidates[0]]
        end = theta_filtered[candidates[-1]]
        result = minimize_scalar(spline, bounds=(start, end), method='bounded')

        return result.x if result.success else calculate_theta_res(Rp, theta_deg)

    except Exception as e:
        warnings.warn(f"Exception in resonance estimation: {e}")
        return calculate_theta_res(Rp, theta_deg)

def calculate_fwhm(Rp, theta_deg):
    """Calculates the Full Width at Half Maximum (FWHM) of the reflectance dip."""
    Rp_min = np.min(Rp)
    Rp_max = np.max(Rp)
    half_max = (Rp_max + Rp_min) / 2
    crossings = np.where(np.diff(np.sign(Rp - half_max)))[0]

    if len(crossings) >= 2:
        return abs(theta_deg[crossings[-1]] - theta_deg[crossings[0]])
    return np.nan

def calculate_q(theta_res, fwhm):
    """Calculates the quality factor Q = θres / FWHM."""
    return theta_res / fwhm if fwhm and not np.isnan(fwhm) else np.nan

def calculate_chi(sensitivity, fwhm):
    """Calculates χ = Sensitivity / FWHM."""
    return sensitivity / fwhm if fwhm and not np.isnan(fwhm) else np.nan

def calculate_sensitivity_empirical(theta_res_pos, theta_res_neg, n_pos, n_neg):
    """Estimates sensitivity using empirical θres shift over Δn."""
    delta_n = n_pos - n_neg
    return (theta_res_pos - theta_res_neg) / delta_n if delta_n != 0 else np.nan

def calculate_theoretical_sensitivity_precise(n_metal, n_analyte, n_substrate):
    """
    Calculates theoretical angular sensitivity from SPR dispersion relation.

    Reference:
        Based on model from [Thirstrup, 2004] and adapted for angular SPR systems.
    """
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
