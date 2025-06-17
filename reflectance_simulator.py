import numpy as np
import matplotlib.pyplot as plt
from fresnel_utils import getFresnelAIM
from performance_metrics import calculate_theta_res, calculate_fwhm

def run_reflectance_simulation(substrate, metal, analytes, materials,
                                lambda0, theta_deg, theta_rad,
                                d_cr, d_analyte, metal_thicknesses_nm):
    # Initialize a dictionary to store simulation results
    results = {
        "theta_res": {},  # Resonance angles for each metal-analyte combination
        "fwhm": {},       # Full width at half maximum for each metal-analyte combination
        "substrate": substrate,  # Substrate material
        "theta_deg": theta_deg,  # Incidence angles in degrees
        "reflectance": {}  # Reflectance curves for each metal-analyte combination
    }

    # Loop through each analyte to perform simulations
    for analyte in analytes:
        print(f"\nSimulating for analyte: {analyte}")
        plt.figure(figsize=(10, 6))  # Create a new figure for each analyte

        # Initialize lists to store results for the current analyte
        theta_res_list = []  # Resonance angles
        fwhm_list = []       # Full width at half maximum
        reflectance_list = []  # Reflectance curves

        # Loop through each metal thickness
        for d_metal_nm in metal_thicknesses_nm:
            d_metal = d_metal_nm * 1e-9  # Convert thickness from nm to meters
            d = np.array([d_cr, d_metal])  # Layer thicknesses (Cr and metal)
            n = np.array([
                materials[substrate],  # Refractive index of substrate
                materials["Cr"],       # Refractive index of chromium
                materials[metal],      # Refractive index of metal
                materials[analyte]     # Refractive index of analyte
            ])

            # Initialize reflectance array
            Rp = np.zeros_like(theta_rad)
            for i, angle in enumerate(theta_rad):
                # Calculate reflectance using Fresnel equations
                _, _, Rp[i] = getFresnelAIM(n, d, angle, lambda0)

            # Calculate resonance angle and FWHM for the reflectance curve
            theta_res = calculate_theta_res(Rp, theta_deg)
            fwhm = calculate_fwhm(Rp, theta_deg)

            # Store results for the current metal thickness
            theta_res_list.append(theta_res)
            fwhm_list.append(fwhm)
            reflectance_list.append(Rp)

            # Plot the reflectance curve
            plt.plot(theta_deg, Rp, label=f'{d_metal_nm} nm | θres ≈ {theta_res:.2f}°')

        # Store results for the current analyte in the results dictionary
        results["theta_res"][(metal, analyte)] = theta_res_list
        results["fwhm"][(metal, analyte)] = fwhm_list
        results["reflectance"][(metal, analyte)] = reflectance_list

        # Add plot details
        plt.title(f"SPR - Substrate: {substrate}, Metal: {metal}, Analyte: {analyte}")
        plt.xlabel("Incidence Angle (°)")
        plt.ylabel("Reflectance")
        plt.grid(True)
        plt.legend(fontsize=9)
        plt.tight_layout()

        # Automatically adjust the X-axis range based on simulated resonance angles
        theta_min = min(theta_res_list)
        theta_max = max(theta_res_list)
        padding = 1.5  # Add a margin for better visualization
        plt.xlim(theta_min - padding, theta_max + padding)

        # Display the plot
        plt.show()

    # Return the simulation results
    return results
