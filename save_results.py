import pandas as pd

def save_results_to_csv(results, metal_thicknesses_nm, analytes_dict, filename="results_spr.csv"):
    """
    Saves theoretical figures of merit for each metal-analyte pair to a CSV file.
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
                    "Sensitivity_Theoretical_deg_per_RIU": results.get("sensitivity_theoretical", {}).get(key, [None]*row_count)[i],
                    "Chi_Theoretical": results.get("chi_theoretical", {}).get(key, [None]*row_count)[i],
                    "Q_Theoretical": results.get("q_theoretical", {}).get(key, [None]*row_count)[i],
                }
                all_rows.append(row)

    df = pd.DataFrame(all_rows)
    df.to_csv(filename, index=False)
    print(f"[INFO] Results saved to: {filename}")
