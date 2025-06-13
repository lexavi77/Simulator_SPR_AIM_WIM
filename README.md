# Simulator_SPR_AIM_WIM

A computational simulator developed in Python for the analysis of optical sensors based on the Surface Plasmon Resonance (SPR) phenomenon, using the **Angular Interrogation Method (AIM)** — where the incidence angle is varied — and the **Wavelength Interrogation Mode** — where the angle is fixed and the wavelength is swept, implemented using a **Wave Interference Method** approach, also known as the **Transfer Matrix Method (TMM)**.

This project aims to provide a precise, modular, and reproducible platform for investigating the optical properties of multilayer structures applied to biosensors.

## 📌 General Description

The `Simulator_SPR_AIM_WIM` project integrates fundamental concepts from electrical engineering, optics, and scientific computing to simulate electromagnetic phenomena in SPR sensors. The focus lies in modeling light interaction with metallic and dielectric structures, considering material properties, layer thicknesses, and variations in the refractive index of the sensing medium.

This simulator serves as a support tool for scientific research in the context of biomolecular detection, especially in hybrid systems combining **Loop-Mediated Isothermal Amplification (LAMP)** with SPR.

> 🔧 **Note:** This project is still under development. The Wave Interference Method (WIM) has not yet been fully implemented, and dispersion effects have not been incorporated into WIM calculations. In addition, the user interface and documentation are currently in Portuguese and are planned to be translated into English in future versions.

## 🎓 Academic and Scientific Applications

- Simulation of SPR reflectance curves for various material configurations
- Calculation of figures of merit: angular sensitivity, FWHM, figure of merit (FoM)
- Performance evaluation of SPR-based optical sensors
- Visualization of the evanescent electric field distribution
- Comparison between AIM and WIM methods
- Validation of numerical models using commercial software (e.g., COMSOL)

## 🧱 Project Structure

```
Simulator_SPR_AIM_WIM/
├── main.py                    
├── fresnel_utils.py          
├── getFresnelWIM.py          
├── calculo_figuras.py       
├── dados_opticos.py          
├── config_simulacao.py       
├── entrada_usuario.py        
├── graficos_de_meritos.py    
├── figuras_de_merito.py     
├── .gitignore                
├── README.md                 
└── __pycache__/              
```

## 🧰 Software Requirements

- Python 3.10+
- Libraries:
  - NumPy
  - Matplotlib
  - SciPy

To install:

```bash
pip install numpy matplotlib scipy
```

## ⚙️ Execution

Run the main script with:

```bash
python3 main.py
```

The user must choose:

1. Simulation method (AIM or, in development, WIM)
2. Optical substrate (PMMA, PC, TOPAS)
3. Metal layer (Au, Ag, Cu)
4. Analyte (fixed or variable refractive index)

Results include angular reflectance curves, sensitivity, and figure of merit.

## 📊 Output Results

- SPR reflectance curves
- Spectral analysis by varying incidence angle
- Sensitivity vs. analyte refractive index
- Material and substrate comparison
- Evanescent field distribution (in development)
- Exportable data for validation (e.g., COMSOL)

## 👨‍💼 Technical Lead

**Alex Armênio Xavier Ramos**  
Electrical Engineering Student – Federal University of Campina Grande (UFCG)  
PIBIC Researcher – Project: *Hybrid LAMP-SPR sensors for point-of-care diagnostics*  
Contact: lexavi779910@gmail.com

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
