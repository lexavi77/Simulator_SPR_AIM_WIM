from simulador_reflectancia import executar_simulacao_reflectancia

def selecionar_materiais():
    mapa_nomes = {
        "PMMA": "PMMA",
        "PC": "PC",
        "TOPAS": "TOPAS",
        "AG": "Ag",
        "AU": "Au",
        "CU": "Cu"
    }

    print("Escolha o substrato: PMMA, PC ou TOPAS")
    substrato_input = input("Substrato: ").strip().upper()
    print("Escolha o metal: Ag, Au ou Cu")
    metal_input = input("Metal: ").strip().upper()

    if substrato_input not in mapa_nomes or metal_input not in mapa_nomes:
        raise ValueError("Material inválido.")

    return mapa_nomes[substrato_input], mapa_nomes[metal_input]
