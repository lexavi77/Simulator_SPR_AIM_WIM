from reflectance_simulator import run_reflectance_simulation

def select_materials():
    name_map = {
        "PMMA": "PMMA",
        "PC": "PC",
        "TOPAS": "TOPAS",
        "AG": "Ag",
        "AU": "Au",
        "CU": "Cu"
    }

    print("Choose the substrate: PMMA, PC, or TOPAS")
    substrate_input = input("Substrate: ").strip().upper()
    print("Choose the metal: Ag, Au, or Cu")
    metal_input = input("Metal: ").strip().upper()

    if substrate_input not in name_map or metal_input not in name_map:
        raise ValueError("Invalid material.")

    return name_map[substrate_input], name_map[metal_input]
