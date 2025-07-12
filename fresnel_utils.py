import numpy as np
from scipy.constants import pi

def getFresnelAIM(n, d, theta, wavelength):

    epsilon = np.sqrt(n**2 - (n[0] * np.sin(theta))**2)
    beta = (2 * pi / wavelength) * np.array(d) * epsilon[1:-1]
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


def restrict_range(theta_deg, Rp, window=(40, 80)):
  
    mask = (theta_deg >= window[0]) & (theta_deg <= window[1])
    return theta_deg[mask], Rp[mask]
