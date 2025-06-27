import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

def calculate_theta_res(Rp, theta_deg):
    idx_min = np.argmin(Rp)
    return theta_deg[idx_min]

def calculate_theta_res_smooth(theta_deg, Rp):
    """
    Calculates the resonance angle from a smoothed reflectance curve
    using cubic interpolation and minimum search.
    """
    # Ensures the data is in ascending order
    sorted_indices = np.argsort(theta_deg)
    theta_sorted = theta_deg[sorted_indices]
    Rp_sorted = Rp[sorted_indices]

    # Additional check: if there are repeated values, remove them
    unique_indices = np.unique(theta_sorted, return_index=True)[1]
    theta_sorted = theta_sorted[unique_indices]
    Rp_sorted = Rp_sorted[unique_indices]

    # Interpolation and minimum search
    try:
        spline = CubicSpline(theta_sorted, Rp_sorted)
        result = minimize_scalar(spline, bounds=(theta_sorted[0], theta_sorted[-1]), method='bounded')
        if result.success:
            return result.x
    except Exception as e:
        print("⚠️ Error applying CubicSpline:", e)

    # Fallback in case of error
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


def calculate_theoretical_sensitivity(eps_mr, n_eff_s, n2):
    """
    Calculates the angular sensitivity S (in degrees/RIU) based on equation (3)
    from the article "Diffractive optical coupling element for surface plasmon resonance sensors".
    
    Parameters:
        eps_mr   : Real part of the metal permittivity (ε_mr)
        n_eff_s  : Effective refractive index of the analyte (n_s^eff)
        n2       : Refractive index of the substrate (n2)

    Returns:
        S_in_degrees_per_RIU : Angular sensitivity (degrees/RIU)
    """
    numerator = eps_mr**2
    denominator = abs(eps_mr + n_eff_s**2)

    root_term = eps_mr * n2**2 * (eps_mr + n_eff_s**2) - (eps_mr**2) * (n_eff_s**2)

    if root_term <= 0:
        return np.nan  # Avoids complex or undefined result

    sensitivity_rad = numerator / (denominator * np.sqrt(root_term))
    sensitivity_deg = sensitivity_rad * (180 / np.pi)
    
    return sensitivity_deg
