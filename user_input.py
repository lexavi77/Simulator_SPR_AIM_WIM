def select_materials():
    name_map = {
        "pmma": "PMMA",
        "pc": "PC",
        "topas": "TOPAS",
        "ag": "Ag",
        "au": "Au",
        "cu": "Cu"
    }

    print("Choose the substrate: PMMA, PC, or TOPAS")
    substrate_input = input("Substrate: ").strip().lower()
    print("Choose the metal: Ag, Au, or Cu")
    metal_input = input("Metal: ").strip().lower()

    if substrate_input not in name_map or metal_input not in name_map:
        raise ValueError("Invalid material.")

    return name_map[substrate_input], name_map[metal_input]
