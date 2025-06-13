from figuras_de_merito import calcular_sensibilidade, calcular_chi, calcular_q

def calcular_todas_figuras_de_merito(resultados, materials, metal):
    if "sensibilidade" not in resultados:
        resultados["sensibilidade"] = {}
    if "chi" not in resultados:
        resultados["chi"] = {}
    if "q" not in resultados:
        resultados["q"] = {}

    theta_low = resultados["theta_res"][(metal, "H2O_low")]
    theta_high = resultados["theta_res"][(metal, "H2O_high")]
    theta_central = resultados["theta_res"][(metal, "H2O_central")]
    fwhm_central = resultados["fwhm"][(metal, "H2O_central")]

    delta_n = materials["H2O_high"].real - materials["H2O_low"].real

    sensibilidade = [
        calcular_sensibilidade(th, tl, materials["H2O_high"].real, materials["H2O_low"].real)
        for th, tl in zip(theta_high, theta_low)
    ]
    chi = [calcular_chi(s, f) for s, f in zip(sensibilidade, fwhm_central)]
    q = [calcular_q(t, f) for t, f in zip(theta_central, fwhm_central)]

    resultados["sensibilidade"][metal] = sensibilidade
    resultados["chi"][metal] = chi
    resultados["q"][metal] = q
