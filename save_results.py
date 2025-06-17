import pandas as pd

def save_results_to_csv(results, metal, filename="results_spr.csv"):
    """
    Salva as figuras de mérito empíricas e teóricas para um determinado metal em um arquivo CSV.

    Parâmetros:
    - results: dicionário com os resultados (como 'results' ou 'comparison_results')
    - metal: string com o nome do metal (ex: 'Au')
    - filename: nome do arquivo de saída
    """
    thicknesses = results.get("metal_thicknesses_nm", list(range(45, 45 + len(results["theta_res"][(metal, "H2O_central")]))))

    df = pd.DataFrame({
        "Metal_Thickness_nm": thicknesses,
        "Theta_res_deg": results["theta_res"][(metal, "H2O_central")],
        "FWHM_deg": results["fwhm"][(metal, "H2O_central")],
        
        # Empirical metrics
        "Sensitivity_Empirical_deg_per_RIU": results.get("sensitivity_empirical", {}).get(metal),
        "Chi_Empirical": results.get("chi_empirical", {}).get(metal),
        "Q_Empirical": results.get("q_empirical", {}).get(metal),

        # Theoretical metrics
        "Sensitivity_Theoretical_deg_per_RIU": results.get("sensitivity_theoretical", {}).get(metal),
        "Chi_Theoretical": results.get("chi_theoretical", {}).get(metal),
        "Q_Theoretical": results.get("q_theoretical", {}).get(metal),
    })

    df.to_csv(filename, index=False)
    print(f"[INFO] Resultados salvos em: {filename}")
