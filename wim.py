import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi

def getFresnelWIM_TM(n, d, theta, wavelength):
    mu = np.ones(len(n))
    epsilon = np.sqrt(n**2 - (np.real(n[0]) * np.sin(theta))**2)
    beta = (2 * pi / wavelength) * d * epsilon
    q = epsilon / n**2  # para modo TM

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

# Parâmetros de entrada fixos
theta_deg = 72
theta = np.radians(theta_deg)

# Varredura espectral: 600 a 900 nm
wavelengths = np.linspace(300e-9, 1500e-9, 50)
lambda_nm = wavelengths * 1e9

# Índices fornecidos
n_p = 1.4874
n_m = 0.13544 + 3.8820j
n_s = 1.3310 + 2.4540e-8j
n = np.array([n_p, n_m, n_s])

# Espessuras fornecidas — mas o prisma idealmente é semi-infinito
d = np.array([0, 50e-9, 500e-9])  # d_p = 0

# Cálculo da refletância espectral
Rp = np.zeros_like(wavelengths)

for i, wl in enumerate(wavelengths):
    _, _, Rp[i] = getFresnelWIM_TM(n, d, theta, wl)

# Encontrar comprimento de onda de ressonância
lambda_res = lambda_nm[np.argmin(Rp)]

# Plot
plt.figure(figsize=(8, 6))
plt.plot(lambda_nm, Rp, color='blue', label='Reflectância (TM)')
plt.axvline(lambda_res, color='red', linestyle='--', label=f'λ ressonância: {lambda_res:.1f} nm')
plt.xlabel('Comprimento de onda (nm)', fontsize=12)
plt.ylabel('Reflectância', fontsize=12)
plt.title(f'Response SPR (modo WIM) para θ = {theta_deg}°', fontsize=14)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Exibe o comprimento de onda de ressonância
print(f"Comprimento de onda de ressonância: {lambda_res:.1f} nm")