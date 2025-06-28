# Simulator_SPR_AIM_WIM

A modular and extensible Python simulator for **Surface Plasmon Resonance (SPR)** sensors, supporting both **Angular Interrogation Method (AIM)** and upcoming **Wavelength Interrogation Mode (WIM)**. Designed for scientific research, especially in biosensing applications using **Loop-Mediated Isothermal Amplification (LAMP)**.

The simulator enables precise modeling of multilayer structures (prism/metal/analyte), offering tools for visualization, sensitivity analysis, and performance benchmarking of SPR-based sensors.

---

## 📌 Overview

The project integrates principles of optics, electromagnetism, and scientific computing to model the interaction between light and nanostructured surfaces, providing:

- Angular reflectance simulations using Fresnel equations (AIM)
- Exportable results and figure of merit analysis (θ_res, FWHM, χ, Q)
- Automated plotting with a MATLAB-like aesthetic (Times New Roman, color palette)
- Modular architecture for easy experimentation with different materials

> ⚠️ **Note:** The **Wavelength Interrogation Mode (WIM)** is under development. Dispersion models for optical materials are partially implemented but not yet integrated into WIM.

---

## 🎯 Key Features

✅ Angular interrogation with Fresnel-based reflectance  
✅ Multiple substrates (PMMA, PC, TOPAS) and metals (Au, Ag, Cu)  
✅ Analyte variation: both positive and negative groups (RIU shift)  
✅ Performance metrics: Sensitivity (empirical & theoretical), FWHM, χ, Q  
✅ Mode-specific outputs:  
  - `run_mode_1`: θres & metrics per configuration  
  - `run_mode_2`: 22 reflectance curves per metal  
  - `run_mode_3`: sensitive structure (fixed metal thickness) scan  
✅ CSV exports for θres and merit figures  
✅ Publication-ready plots (.png and .eps)

---

## 🧪 Academic Applications

- Design and optimization of SPR biosensors
- Integration studies of SPR and LAMP for point-of-care diagnostics
- Theoretical and empirical analysis of sensor performance
- Comparison between different metals and substrates
- Validation of numerical results via tools like COMSOL

---

## 📁 Project Structure

```
Simulator_SPR_AIM_WIM/
├── main.py                         # Execution entry point
├── fresnel_utils.py               # Fresnel reflectance core
├── reflectance_simulator.py       # AIM simulation logic
├── calculate_figures.py           # Sensitivity, chi, Q computation
├── performance_metrics.py         # Theta_res, FWHM, helper formulas
├── optical_data.py                # Refractive index dictionary
├── simulation_config.py           # Global parameters (λ, θ, d, analytes)
├── plot_style.py                  # Style definitions (fonts, grids)
├── plot_utils.py                  # Centralized figure export (.eps/.png)
├── plot_reflectance_full.py       # 22 curves plotting (mode 2)
├── plot_sensitive_structure.py    # Fixed-thickness analyte variation (mode 3)
├── merit_figures_plot.py          # Plotting metrics vs metal thickness
├── save_results.py                # CSV export of computed values
├── user_input.py                  # CLI input for substrate/metal
└── README.md
```

---

## 💻 Requirements

- Python 3.10+
- Dependencies:
  ```bash
  pip install numpy matplotlib scipy pandas
  ```

---

## ⚙️ How to Run

```bash
python3 main.py
```

You will be prompted to select:

1. Simulation mode (1, 2, or 3)
2. Substrate (PMMA, PC, TOPAS)
3. Metal (Ag, Au, Cu)

Results will be saved in structured folders (`/outputs/...`) including:
- Angular reflectance curves
- Figures of merit (θres, FWHM, χ, Q)
- CSV export for reproducibility

---

## 🔭 Next Steps

- 🔄 Integration of Wavelength Interrogation Mode (WIM)
- 🌐 Web-based frontend using WIM interface (HTML/JS)
- 📈 Real-time plot updates via ESP32 web server (for embedded use)
- 🧠 Material dispersion support (spectral refractive indices)

---

## 👨‍🔬 Author

**Alex Armênio Xavier Ramos**  
Undergraduate Researcher (PIBIC)  
Electrical Engineering – Federal University of Campina Grande (UFCG)  
Email: [lexavi779910@gmail.com](mailto:lexavi779910@gmail.com)

Project: *Hybrid LAMP-SPR sensors for point-of-care diagnostics*

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
