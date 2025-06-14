import numpy as np
from scipy.constants import pi

def getFresnelAIM(n, d, theta, wavelength):
    mu = np.ones(len(n))
    epsilon = np.sqrt(n**2 - (n[0] * np.sin(theta))**2)
    # Thickness values are specified only for the internal layers (i.e. all
    # layers except the first and the last).  When there are more than four
    # layers ``epsilon[1:]`` would include the external medium and lead to a
    # shape mismatch with ``d``.  Using ``epsilon[1:-1]`` ensures ``beta``
    # matches the number of provided thickness values.
    beta = (2 * pi / wavelength) * np.array(d) * np.array(epsilon[1:-1])
    q = epsilon / n**2

    M_tot = np.identity(2, dtype=complex)

    for k in range(1, len(n) - 1):
        M_k = np.array([
            [np.cos(beta[k-1]), -1j / q[k] * np.sin(beta[k-1])],
            [-1j * q[k] * np.sin(beta[k-1]), np.cos(beta[k-1])]
        ])
        M_tot = M_tot @ M_k

    num = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] - (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    den = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] + (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    r = num / den
    t = 2 * q[0] / den
    Rp = np.abs(r) ** 2
    return r, t, Rp
