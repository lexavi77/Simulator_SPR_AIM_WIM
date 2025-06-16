import pandas as pd

def save_results_to_csv(results, metal, filename="results_spr.csv"):
    """
    Salva as figuras de mérito para um determinado metal em um arquivo CSV.

    Parâmetros:
    - results: dicionário com os resultados (como 'results' ou 'comparison_results')
    - metal: string com o nome do metal (ex: 'Au')
    - filename: nome do arquivo de saída
    """
    thicknesses = results.get("metal_thicknesses_nm", list(range(45, 45 + len(results["theta_res"][metal]))))

    df = pd.DataFrame({
        "Metal_Thickness_nm": thicknesses,
        "Theta_res_deg": results["theta_res"].get(metal),
        "FWHM_deg": results["fwhm"].get(metal),
        "FWHM_nm": results.get("fwhm_nm", {}).get(metal),
        "Sensitivity_deg_per_RIU": results.get("sensitivity", {}).get(metal),
        "Sensitivity_nm_per_RIU": results.get("s_lambda", {}).get(metal),
        "Chi_deg": results.get("chi", {}).get(metal),
        "Chi_lambda": results.get("chi_lambda", {}).get(metal),
        "Q_factor": results.get("q", {}).get(metal),
    })

    df.to_csv(filename, index=False)
    print(f"[INFO] Resultados salvos em: {filename}")
