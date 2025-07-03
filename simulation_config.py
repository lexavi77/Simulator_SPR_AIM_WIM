import numpy as np

# Constants and sweep parameters
lambda0 = 850e-9  # wavelength in meters
theta_deg = np.linspace(40, 80, 4001)
theta_rad = np.radians(theta_deg)

# Fixed layer thicknesses
d_cr = 2e-9        # chromium adhesion layer (optional, in meters)
d_analyte = 445e-9  # analyte layer thickness (in meters)

# Metal thickness range in nanometers
metal_thicknesses_nm = np.arange(45, 56, 1)  # 45 to 55 nm

analytes = {
    "analyte_01": 1.3492,
    "analyte_02": 1.3481
}

# Global config dictionary (used in mode_compare_metals)
config = {
    "lambda0": lambda0,
    "theta_deg": theta_deg,
    "theta_rad": theta_rad,
    "d_cr": d_cr,
    "d_analyte": d_analyte,
    "metal_thicknesses_nm": metal_thicknesses_nm,
    "analytes": analytes,
    "metal": "Au"  # default metal
}
