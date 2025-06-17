import numpy as np

lambda0 = 850e-9  # wavelength
theta_deg = np.linspace(40, 80, 4001)
theta_rad = np.radians(theta_deg)

d_cr = 2e-9  # chromium adhesion layer thickness (if used)
d_analyte = 500e-9  # analyte layer thickness

metal_thicknesses_nm = np.arange(45, 56, 1)  # in nanometers
analytes = ["H2O_low", "H2O_central", "H2O_high"]
