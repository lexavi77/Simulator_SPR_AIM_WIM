import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi

# Função de cálculo da refletância usando matriz de transferência
def getFresnelAIM(n, d, theta, wavelength):
    mu = np.ones(len(n))
    epsilon = np.sqrt(n**2 - (np.real(n[0]) * np.sin(theta))**2)
    beta = (2 * pi / wavelength) * d * epsilon
    q = np.sqrt(mu) * epsilon / n**2

    M_tot = np.array([[1, 0], [0, 1]], dtype=complex)

    for k in range(1, len(n) - 1):
        M_k = np.array([
            [np.cos(beta[k]), -1j / q[k] * np.sin(beta[k])],
            [-1j * q[k] * np.sin(beta[k]), np.cos(beta[k])]
        ])
        M_tot = M_tot @ M_k

    den = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] + (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    r = ((M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] - (M_tot[1, 0] + M_tot[1, 1] * q[-1])) / den
    t = 2 * q[0] / den
    Rp = np.abs(r)**2
    return r, t, Rp

# Parâmetros
wavelength = 850e-9  # 850 nm
theta = np.radians(np.arange(60, 85.1, 0.1))
theta_ang = np.degrees(theta)

# Índices de refração
n_p = 1.5548                   
n_cr = 3.2408 + 3.4963j            # Cromo
n_m = 0.27630 + 5.4197j
n_s = 1.3481          
n = np.array([n_p, n_cr, n_m, n_s])

# Espessuras
d_p = 500e-9   #
d_cr = 2e-9    # Cromo
d_m = 55e-9    # 
d_s = 443e-9   # 
d = np.array([d_p, d_cr, d_m, d_s])

# Cálculo da refletância
Rp = np.zeros_like(theta)
for i, angle in enumerate(theta):
    _, _, Rp[i] = getFresnelAIM(n, d, angle, wavelength)

# Ângulo de ressonância
theta_res = theta_ang[np.argmin(Rp)]

# Plot
plt.figure(figsize=(8, 6))
plt.plot(theta_ang, Rp, label='Reflectance', color='green', linewidth=1.5)
plt.axvline(theta_res, color='red', linestyle='--', label=f'Resonance Angle: {theta_res:.2f}°')
plt.xlabel('Angle (°)', fontsize=12)
plt.ylabel('Reflectance (a. u.)', fontsize=12)
plt.title('Reflectance vs Incidence Angle with 2 nm Cr Layer', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.show()

theta_res
