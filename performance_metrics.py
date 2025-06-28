import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

def calculate_theta_res(Rp, theta_deg):
    """Returns the angle where the reflectance is minimum."""
    idx_min = np.argmin(Rp)
    return theta_deg[idx_min]

def calculate_theta_res_smooth(theta_deg, Rp):
    """
    Calculates the resonance angle using cubic spline interpolation
    and bounded scalar minimization.
    """
    sorted_indices = np.argsort(theta_deg)
    theta_sorted = theta_deg[sorted_indices]
    Rp_sorted = Rp[sorted_indices]

    # Ensure unique x-values for interpolation
    _, unique_indices = np.unique(theta_sorted, return_index=True)
    theta_sorted = theta_sorted[unique_indices]
    Rp_sorted = Rp_sorted[unique_indices]

    try:
        spline = CubicSpline(theta_sorted, Rp_sorted)
        result = minimize_scalar(spline, bounds=(theta_sorted[0], theta_sorted[-1]), method='bounded')
        if result.success:
            return result.x
    except Exception as e:
        print("⚠️ Error in calculate_theta_res_smooth:", e)

    # Fallback
    return calculate_theta_res(Rp_sorted, theta_sorted)

def calculate_fwhm(Rp, theta_deg):
    """Computes the Full Width at Half Maximum (FWHM) of a reflectance dip."""
    Rp_min = np.min(Rp)
    Rp_max = np.max(Rp)
    half_max = (Rp_max + Rp_min) / 2

    crossing_indices = np.where(np.diff(np.sign(Rp - half_max)))[0]

    if len(crossing_indices) >= 2:
        theta1 = theta_deg[crossing_indices[0]]
        theta2 = theta_deg[crossing_indices[-1]]
        return abs(theta2 - theta1)
    return np.nan  # Cannot compute FWHM

def calculate_sensitivity(theta_res_high, theta_res_low, n_high, n_low):
    """Calculates sensitivity in degrees/RIU."""
    delta_n = n_high - n_low
    return (theta_res_high - theta_res_low) / delta_n if delta_n != 0 else np.nan

def calculate_chi(sensitivity, fwhm):
    """Calculates χ = sensitivity / FWHM (in RIU⁻¹)."""
    return sensitivity / fwhm if fwhm != 0 else np.nan

def calculate_q(theta_res, fwhm):
    """Calculates Q = θ_res / FWHM (adimensional)."""
    return theta_res / fwhm if fwhm != 0 else np.nan

def calculate_theoretical_sensitivity(eps_mr, n_eff_s, n2):
    """
    Calculates angular sensitivity S (°/RIU) using Equation (3) from:
    'Diffractive optical coupling element for surface plasmon resonance sensors'.
    """
    numerator = eps_mr**2
    denominator = abs(eps_mr + n_eff_s**2)
    root_term = eps_mr * n2**2 * (eps_mr + n_eff_s**2) - (eps_mr**2) * (n_eff_s**2)

    if root_term <= 0:
        return np.nan

    sensitivity_rad = numerator / (denominator * np.sqrt(root_term))
    return sensitivity_rad * (180 / np.pi)  # Convert to degrees/RIU
