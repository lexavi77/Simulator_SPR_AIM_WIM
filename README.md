# Simulator_SPR_AIM_WIM

A Python-based simulator for **Surface Plasmon Resonance (SPR)** sensors, focused on the **Angular Interrogation Method (AIM)**. It models multilayer structures commonly used in biosensing — particularly for hybrid **LAMP‑SPR** (Loop‑Mediated Isothermal Amplification) applications.

The main goal is to **compute figures of merit** — including resonance angle, FWHM, sensitivity, Q‑factor, and χ — to determine which **metal (Ag, Au, or Cu)** and **film thickness** provide the best sensing performance.  
The simulator performs a sweep over **metal thicknesses from 45 to 55 nm, in 1 nm steps**, enabling a fine-grained evaluation of structural variations.

This tool provides accurate reflectance simulations, exportable performance metrics, and publication-quality plots.  
> 🔬 **Wavelength Interrogation Mode (WIM)** is under active development.


## 📌 Overview

- **AIM support**: Angular reflectance simulations based on Fresnel equations  
- **Performance metrics**: θ<sub>res</sub>, FWHM, χ, Q  
- **Materials library**: Substrates (PMMA, PC, TOPAS), metals (Au, Ag, Cu)  
- **Analyte variation**: Positive/negative refractive index changes (RIU)  
- **Plotting**: High-resolution `.png` / `.eps` exports in scientific style  
- **Exports**: CSV files with all computed values for reproducibility

---

## 🎯 Scientific Use Cases

- ✅ Biosensor design and optimization  
- ✅ Integration of SPR with LAMP for diagnostics  
- ✅ Sensitivity and specificity analysis  
- ✅ Validation via COMSOL or similar tools

---

## 📁 Project Structure

```
Simulator_SPR_AIM_WIM/
├── main.py
├── fresnel_utils.py
├── reflectance_simulator.py
├── calculate_figures.py
├── performance_metrics.py
├── optical_data.py
├── simulation_config.py
├── plot_style.py
├── plot_utils.py
├── plot_reflectance_full.py
├── plot_sensitive_structure.py
├── merit_figures_plot.py
├── save_results.py
├── user_input.py
└── README.md
```

---

## 💻 Requirements & Installation

Python 3.10+ is required. To install dependencies:

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`:**
```
numpy
scipy
pandas
matplotlib
```

---

## ⚙️ How to Run

```bash
python3 main.py
```

Follow these prompts:

1. **Simulation mode:**
   - `1`: θ<sub>res</sub> & metrics per configuration  
   - `2`: Reflectance curves (22 curves per metal)  
   - `3`: Analyte sweep with fixed metal thickness  
2. **Substrate**: choose from PMMA, PC, TOPAS  
3. **Metal**: choose from Au, Ag, Cu  

Outputs are saved in:
- Plots (`.png` & `.eps`)  
- CSV files (θ<sub>res</sub>, FWHM, χ, Q)

---

## 🔭 Next Steps

- 🟡 Add **Wavelength Interrogation Mode (WIM)** — spectral reflectance R(λ)  
- 🧪 Integrate dispersion models for λ-dependence (Sellmeier, Cauchy)  
- 🖥️ Optional GUI or web dashboard (Streamlit, Flask)  
- 🔗 Support ESP32 integration for experimental interfacing

---

## 👨‍🔬 Author

**Alex Armênio Xavier Ramos**  
Undergraduate Researcher (PIBIC)  
Electrical Engineering – Federal University of Campina Grande (UFCG)  
Email: lexavi779910@gmail.com

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
