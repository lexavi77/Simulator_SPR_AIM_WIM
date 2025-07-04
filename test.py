import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi

def getFresnelAIM(n, d, theta, wavelength):
    n = np.array(n)
    d = np.array(d)
    epsilon = np.sqrt(n**2 - (np.real(n[0]) * np.sin(theta))**2)
    beta = (2 * pi / wavelength) * d * epsilon[1:-1]
    q = epsilon / n**2

    M_tot = np.identity(2, dtype=complex)
    for k in range(1, len(n) - 1):
        M_k = np.array([
            [np.cos(beta[k - 1]), -1j / q[k] * np.sin(beta[k - 1])],
            [-1j * q[k] * np.sin(beta[k - 1]), np.cos(beta[k - 1])]
        ])
        M_tot = M_tot @ M_k

    den = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] + (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    r = ((M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] - (M_tot[1, 0] + M_tot[1, 1] * q[-1])) / den
    t = 2 * q[0] / den
    Rp = np.abs(r) ** 2
    return r, t, Rp

# === Parâmetros ===
wavelength = 850e-9
theta = np.radians(np.arange(40, 85.1, 0.1))
theta_deg = np.degrees(theta)

# Índices de refração (6 camadas: entrada, 4 internas, saída)
n_air = 1.0 + 0j           # entrada (ex: ar)
n_topas = 1.5548 + 0j
n_cr = 3.2408 + 3.4963j
n_au = 0.16408 + 5.3194j
n_analyte = 1.3481 + 0j
n_substrate = 1.0 + 0j     # saída (ex: ar)

n = [n_air, n_topas, n_cr, n_au, n_analyte, n_substrate]

# Espessuras das 4 camadas internas (TOPAS, Cr, Au, Analyte)
d = [500e-9, 2e-9, 55e-9, 445e-9]  # len(d) == len(n) - 2

# Calcula reflectância
Rp = np.zeros_like(theta)
for i, angle in enumerate(theta):
    _, _, Rp[i] = getFresnelAIM(n, d, angle, wavelength)

theta_res = theta_deg[np.argmin(Rp)]

# === Plot ===
plt.plot(theta_deg, Rp, label='Reflectance', color='blue')
plt.axvline(theta_res, color='red', linestyle='--', label=f'Resonance: {theta_res:.2f}°')
plt.xlabel('Angle (°)')
plt.ylabel('Reflectance (a.u.)')
plt.title('SPR Reflectance for 4-layer stack')
plt.grid(True)
plt.legend()
plt.show()

print(f"Resonance angle: {theta_res:.2f}°")
