import numpy as np

materials = {
    "PMMA": 1.4835 + 0j,
    "PC": 1.5688 + 0j,
    "TOPAS": 1.52564 + 0j,
    "Cr": 3.2408 + 3.4963j,
    "Ag": 0.040 + 5.9655j,
    "Au": 0.16408 + 5.3194j,
    "Cu": 0.27630 + 5.4197j,
    "analyte_01": 1.3492,
    "analyte_02": 1.3481
}

# =========================
# Simulation Configuration
# =========================

lambda0 = 850e-9
theta_deg = np.linspace(40, 80, 4001)
theta_rad = np.radians(theta_deg)
d_cr = 2e-9
d_analyte = 445e-9
metal_thicknesses_nm = np.arange(45, 56, 1)