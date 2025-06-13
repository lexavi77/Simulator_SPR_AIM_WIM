import numpy as np

lambda0 = 850e-9  # comprimento de onda
theta_deg = np.linspace(40, 80, 1000)
theta_rad = np.radians(theta_deg)
d_cr = 2e-9
d_analito = 500e-9
espessuras_metal_nm = np.arange(45, 56, 1)
analitos = ["H2O_low", "H2O_central", "H2O_high"]