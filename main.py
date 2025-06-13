import numpy as np
import matplotlib.pyplot as plt

from fresnel_utils import getFresnelAIM
from dados_opticos import materials
from config_simulacao import (
    lambda0, theta_deg, theta_rad,
    d_cr, d_analito, espessuras_metal_nm, analitos
)
from entrada_usuario import selecionar_materiais
from figuras_de_merito import calcular_q
from calculo_figuras import calcular_todas_figuras_de_merito
from graficos_de_meritos import plotar_figuras_de_merito
from simulador_reflectancia import executar_simulacao_reflectancia

# ------------------- Lógica de Execução -------------------

print("Escolha o modo de simulação:")
print("1 - Análise de um material específico")
print("2 - Comparar metais com analito fixo (H2O_central)")
modo = input("Modo (1 ou 2): ").strip()

if modo == "1":
    substrato, metal = selecionar_materiais()
    resultados = executar_simulacao_reflectancia(
        substrato, metal, analitos,
        materials, lambda0, theta_deg, theta_rad,
        d_cr, d_analito, espessuras_metal_nm
    )
    calcular_todas_figuras_de_merito(resultados, materials, metal)
    plotar_figuras_de_merito(resultados, espessuras_metal_nm)

elif modo == "2":
    print("\nModo comparação entre metais selecionado.")
    print("Escolha o substrato fixo: PMMA, PC ou TOPAS")
    substrato_input = input("Substrato: ").strip().upper()
    mapa_nomes = {"PMMA": "PMMA", "PC": "PC", "TOPAS": "TOPAS"}
    if substrato_input not in mapa_nomes:
        raise ValueError("Substrato inválido.")
    substrato = mapa_nomes[substrato_input]

    resultados_comp = {
        "theta_res": {},
        "fwhm": {},
        "sensibilidade": {},
        "chi": {},
        "q": {}
    }

    for metal in ["Ag", "Au", "Cu"]:
        print(f"\nSimulando para metal: {metal}")
        resultados_metal = executar_simulacao_reflectancia(
            substrato, metal, ["H2O_central"],
            materials, lambda0, theta_deg, theta_rad,
            d_cr, d_analito, espessuras_metal_nm
        )

        theta = resultados_metal["theta_res"][(metal, "H2O_central")]
        fwhm = resultados_metal["fwhm"][(metal, "H2O_central")]

        resultados_comp["theta_res"][metal] = theta
        resultados_comp["fwhm"][metal] = fwhm
        resultados_comp["sensibilidade"][metal] = [np.nan] * len(theta)
        resultados_comp["chi"][metal] = [np.nan] * len(theta)
        resultados_comp["q"][metal] = [calcular_q(t, f) for t, f in zip(theta, fwhm)]

    print("\nPlotando comparações entre metais...")
    plotar_figuras_de_merito(resultados_comp, espessuras_metal_nm)

else:
    print("Opção inválida. Finalizando programa.")
