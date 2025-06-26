def select_materials():
    valid_substrates = ["PMMA", "PC", "TOPAS"]
    valid_metals = ["Ag", "Au", "Cu"]

    while True:
        substrate = input("Select substrate (PMMA, PC, TOPAS): ").strip().upper()
        if substrate in valid_substrates:
            break
        print("Invalid substrate. Please choose from: PMMA, PC, TOPAS.")

    while True:
        metal = input("Select metal (Ag, Au, Cu): ").strip().capitalize()
        if metal in valid_metals:
            break
        print("Invalid metal. Please choose from: Ag, Au, Cu.")

    return substrate, metal
