import numpy as np
from scipy.constants import pi

def getFresnelWIM_TM(n, d, theta, wavelength):
    """
    Calcula a refletância TM usando a matriz característica (modo WIM).

    Parâmetros:
    - n: array com índices de refração (complexos)
    - d: array com espessuras das camadas (em metros)
    - theta: ângulo de incidência (em rad)
    - wavelength: comprimento de onda (em metros)

    Retorna:
    - r: coeficiente de reflexão complexo
    - t: coeficiente de transmissão complexo
    - Rp: refletância (|r|^2)
    """
    mu = np.ones(len(n))  # permeabilidade relativa (μ ≈ 1)
    epsilon = np.sqrt(n**2 - (np.real(n[0]) * np.sin(theta))**2)
    beta = (2 * pi / wavelength) * d * epsilon
    q = epsilon / n**2  # modo TM

    M_tot = np.array([[1, 0], [0, 1]], dtype=complex)

    for k in range(1, len(n) - 1):
        M_k = np.array([
            [np.cos(beta[k]), -1j / q[k] * np.sin(beta[k])],
            [-1j * q[k] * np.sin(beta[k]), np.cos(beta[k])]
        ])
        M_tot = M_tot @ M_k

    num = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] - (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    den = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] + (M_tot[1, 0] + M_tot[1, 1] * q[-1])

    r = num / den
    t = 2 * q[0] / den
    Rp = np.abs(r)**2

    return r, t, Rp
