import os
import pandas as pd

def save_results_to_csv(results, metal_thicknesses_nm, analytes_dict, filename="results_spr.csv"):
    """
    Export all figures of merit to a CSV file using semicolon (;) for Excel compatibility.

    Parameters:
        results (dict): Dictionary containing all metrics calculated in the simulation.
        metal_thicknesses_nm (array): Array of metal thicknesses used in the simulation.
        analytes_dict (dict): Dictionary with analyte names and refractive index values.
        filename (str): Name of the output CSV file.
    """
    all_rows = []

    for metal in ["Ag", "Au", "Cu"]:
        for analyte_key, analyte_value in analytes_dict.items():
            key = (metal, analyte_key)
            row_count = len(results["theta_res"].get(key, []))
            thicknesses = metal_thicknesses_nm[:row_count]

            for i in range(row_count):
                row = {
                    "Metal": metal,
                    "Analyte": analyte_key,
                    "Metal_Thickness_nm": thicknesses[i],
                    "Theta_res_deg": results["theta_res"].get(key, [None]*row_count)[i],
                    "FWHM_deg": results["fwhm"].get(key, [None]*row_count)[i],
                    "Sensitivity_Empirical_deg_per_RIU": results.get("sensitivity_empirical", {}).get(metal, [None]*row_count)[i],
                    "Chi_Empirical": results.get("chi_empirical", {}).get(key, [None]*row_count)[i],
                    "Q_Empirical": results.get("q_empirical", {}).get(key, [None]*row_count)[i],
                    "Sensitivity_Theoretical_deg_per_RIU": results.get("sensitivity_theoretical", {}).get(key, [None]*row_count)[i],
                    "Chi_Theoretical": results.get("chi_theoretical", {}).get(key, [None]*row_count)[i],
                    "Q_Theoretical": results.get("q_theoretical", {}).get(key, [None]*row_count)[i],
                }
                all_rows.append(row)

    df = pd.DataFrame(all_rows)

    # Use semicolon for PT-BR Excel compatibility
    os.makedirs(os.path.dirname(filename), exist_ok=True) if os.path.dirname(filename) else None
    df.to_csv(filename, index=False, sep=';')
    print(f"[INFO] CSV export completed: {filename}")
