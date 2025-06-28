import numpy as np

lambda0 = 850e-9  # wavelength
theta_deg = np.linspace(40, 80, 4001)
theta_rad = np.radians(theta_deg)

d_cr = 2e-9  # chromium adhesion layer thickness (if used)
d_analyte = 1000e-9  # analyte layer thickness

metal_thicknesses_nm = np.arange(45, 56, 1)  # in nanometers

# Only two analytes are used; central value is computed dynamically where needed
analytes = ["analyte_01", "analyte_02"]

