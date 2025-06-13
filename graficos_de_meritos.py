import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def plotar_figuras_de_merito(resultados, espessuras_metal_nm):
    foms = ["theta_res", "fwhm", "sensibilidade", "chi", "q"]
    titulos = {
        "theta_res": "Ângulo de Ressonância (°)",
        "fwhm": "FWHM (°)",
        "sensibilidade": "Sensibilidade (°/RIU)",
        "chi": "Parâmetro χ",
        "q": "Fator Q"
    }

    for metrica in foms:
        plt.figure(figsize=(8, 5))
        for chave in resultados[metrica]:
            x = espessuras_metal_nm
            y = resultados[metrica][chave]

            # Só interpola se houver dados suficientes e não forem NaN
            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fino = np.linspace(min(x), max(x), 500)
                y_suave = spline(x_fino)
                plt.plot(x_fino, y_suave, label=str(chave))
            else:
                plt.plot(x, y, 'o-', label=str(chave))  # fallback sem suavização

        plt.xlabel("Espessura do Metal (nm)")
        plt.ylabel(titulos[metrica])
        plt.title(f"Figura de Mérito: {titulos[metrica]}")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
