import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi

def getReflectivity(n, d, theta, wavelength):
    """
    Calcula a reflectância e o coeficiente de reflexão usando o método das matrizes de Abeles.
    
    Parâmetros:
    - n: índices de refração das camadas (array complexo)
    - d: espessuras das camadas (em metros)
    - theta: ângulo de incidência (em radianos)
    - wavelength: comprimento de onda (em metros)

    Retorna:
    - Reflectância (módulo ao quadrado de r)
    - Coeficiente de reflexão r (complexo)
    """
    mu = np.ones(len(n))
    k0 = 2 * pi / wavelength
    kz = k0 * np.sqrt(n**2 - (n[0] * np.sin(theta))**2)
    delta = d * kz

    q = kz / (mu * n**2)

    M_tot = np.array([[1, 0], [0, 1]], dtype=complex)
    for k in range(1, len(n) - 1):
        M_k = np.array([
            [np.cos(delta[k]), -1j / q[k] * np.sin(delta[k])],
            [-1j * q[k] * np.sin(delta[k]), np.cos(delta[k])]
        ])
        M_tot = M_tot @ M_k

    numerator = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] - (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    denominator = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] + (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    r = numerator / denominator

    return np.abs(r)**2, r

def field_distribution(theta_res, n, d, wavelength, z_range):
    """
    Calcula o perfil do campo magnético Hy² ao longo da profundidade, normalizado.
    
    Parâmetros:
    - theta_res: ângulo de ressonância (em radianos)
    - n: índices de refração
    - d: espessuras
    - wavelength: comprimento de onda (m)
    - z_range: vetor de profundidade (m)

    Retorna:
    - Perfil normalizado da intensidade do campo magnético ao longo de z_range
    """
    k0 = 2 * np.pi / wavelength
    kx = k0 * n[0] * np.sin(theta_res)

    kz = np.sqrt(n**2 * k0**2 - kx**2 + 0j)
    q = kz / (n**2)

    Hy_inc = 1
    _, r = getReflectivity(n, d, theta_res, wavelength)

    delta = d * kz
    M_tot = np.array([[1, 0], [0, 1]], dtype=complex)
    for k in range(1, len(n) - 1):
        M_k = np.array([
            [np.cos(delta[k]), -1j / q[k] * np.sin(delta[k])],
            [-1j * q[k] * np.sin(delta[k]) , np.cos(delta[k])]
        ])
        M_tot = M_tot @ M_k

    t = 2 * q[0] / ((M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] + (M_tot[1, 0] + M_tot[1, 1] * q[-1]))

    field_profile = []
    z_layer_total = 0
    for j in range(1, len(n) - 1):
        z_start = z_layer_total
        z_end = z_start + d[j]
        z_local = z_range[(z_range >= z_start) & (z_range < z_end)]
        if len(z_local) == 0:
            z_layer_total += d[j]
            continue
        dz = z_local - z_start
        Hyj = Hy_inc * (np.exp(1j * kz[j] * dz) + r * np.exp(-1j * kz[j] * dz))
        field_profile.append(np.abs(Hyj)**2)
        z_layer_total += d[j]

    z_ana = z_range[z_range >= z_layer_total]
    dz_ana = z_ana - z_layer_total
    HyN = t * np.exp(1j * kz[-1] * dz_ana)
    field_profile.append(np.abs(HyN)**2)

    full_profile = np.concatenate(field_profile)
    return full_profile / np.max(full_profile)

# Parâmetros do artigo
wavelength = 633e-9
n = np.array([1.732, 0.1325 + 4.0203j, 1.335])  # Prisma, Prata, Analito
d = np.array([0, 43e-9, 0])

theta_deg = np.arange(40, 80.1, 0.1)
theta_rad = np.radians(theta_deg)

Rp, r_values = np.array([getReflectivity(n, d, angle, wavelength) for angle in theta_rad]).T

theta_res = theta_rad[np.argmin(Rp)]
z_range = np.linspace(0, 200e-9, 1000)
field_profile = field_distribution(theta_res, n, d, wavelength, z_range)

plt.figure(figsize=(10, 5))
plt.plot(theta_deg, Rp, label='Reflectância')
plt.axvline(np.degrees(theta_res), color='r', linestyle='--', label=f'Ângulo de ressonância ≈ {np.degrees(theta_res):.2f}°')
plt.xlabel('Ângulo de Incidência (°)')
plt.ylabel('Reflectância')
plt.title('Reflectância vs Ângulo de Incidência (Camada Única de Prata)')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(z_range * 1e9, field_profile, label='|Hy(z)|²')
plt.xlabel('Distância da Interface (nm)')
plt.ylabel('Intensidade Normalizada')
plt.title('Distribuição do Campo Magnético Hy')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
