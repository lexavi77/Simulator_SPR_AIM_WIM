import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import warnings
from scipy.constants import pi
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from matplotlib.font_manager import FontProperties

# =========================
# Optical Constants
# =========================

materials = {
    "PMMA": 1.4835 + 0j,
    "PC": 1.5688 + 0j,
    "TOPAS": 1.52564 + 0j,
    "Cr": 3.2408 + 3.4963j,
    "Ag": 0.040 + 5.9655j,
    "Au": 0.16408 + 5.3194j,
    "Cu": 0.27630 + 5.4197j,
    "analyte_01": 1.3492,
    "analyte_02": 1.3481
}

# =========================
# Simulation Configuration
# =========================

lambda0 = 850e-9
theta_deg = np.linspace(40, 80, 4001)
theta_rad = np.radians(theta_deg)
d_cr = 2e-9
d_analyte = 445e-9
metal_thicknesses_nm = np.arange(45, 56, 1)

# =========================
# Plot Style and Font
# =========================

warnings.filterwarnings("ignore", category=UserWarning, message=".*transparency.*")
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None

def save_figure(filename_base: str, dpi_eps: int = 600, dpi_png: int = 300, show: bool = False):
    if not plt.get_fignums():
        print("[WARNING] No active figure to save.")
        return
    os.makedirs(os.path.dirname(filename_base), exist_ok=True)
    try:
        plt.tight_layout()
    except Exception as e:
        print(f"[WARNING] Could not apply tight_layout(): {e}")
    try:
        plt.savefig(f"{filename_base}.png", format="png", dpi=dpi_png)
        print(f"[INFO] Saved: {filename_base}.png")
    except Exception as e:
        print(f"[ERROR] Failed to save PNG: {e}")
    try:
        plt.savefig(f"{filename_base}.eps", format="eps", bbox_inches="tight", dpi=dpi_eps)
        print(f"[INFO] Saved: {filename_base}.eps")
    except Exception as e:
        print(f"[WARNING] Failed to save EPS (ignored): {e}")
    if show:
        try:
            plt.show()
        except Exception as e:
            print(f"[WARNING] Could not display figure: {e}")

def getFresnelAIM(n, d, theta, wavelength):
    mu = np.ones(len(n))
    epsilon = np.sqrt(n**2 - (n[0] * np.sin(theta))**2)
    beta = (2 * pi / wavelength) * np.array(d) * np.array(epsilon[1:-1])
    q = epsilon / n**2
    M_tot = np.identity(2, dtype=complex)
    for k in range(1, len(n) - 1):
        M_k = np.array([
            [np.cos(beta[k-1]), -1j / q[k] * np.sin(beta[k-1])],
            [-1j * q[k] * np.sin(beta[k-1]), np.cos(beta[k-1])]
        ])
        M_tot = M_tot @ M_k
    num = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] - (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    den = (M_tot[0, 0] + M_tot[0, 1] * q[-1]) * q[0] + (M_tot[1, 0] + M_tot[1, 1] * q[-1])
    r = num / den
    t = 2 * q[0] / den
    Rp = np.abs(r) ** 2
    return r, t, Rp


def calculate_theta_res(Rp, theta_deg):
    return theta_deg[np.argmin(Rp)]

def calculate_theta_res_smooth(theta_deg, Rp, threshold_ratio=0.98, min_angle=50, max_angle=80):
    """
    Robust estimation of the resonance angle (theta_res) using cubic spline interpolation.
    """
    try:
        # Filter valid range
        mask = (theta_deg >= min_angle) & (theta_deg <= max_angle)
        theta_filtered = theta_deg[mask]
        Rp_filtered = Rp[mask]

        if len(theta_filtered) < 5:
            print("[WARNING] Not enough data in selected range. Falling back to minimum Rp.")
            return theta_deg[np.argmin(Rp)]

        # Create spline
        spline = CubicSpline(theta_filtered, Rp_filtered)

        # Define threshold and candidates
        threshold = np.max(Rp_filtered) * threshold_ratio
        candidates = np.where(Rp_filtered < threshold)[0]

        if len(candidates) < 2:
            print("[WARNING] No clear resonance dip found. Falling back to minimum Rp.")
            return theta_deg[np.argmin(Rp)]

        start = theta_filtered[candidates[0]]
        end = theta_filtered[candidates[-1]]

        # Minimize reflectance in window
        result = minimize_scalar(spline, bounds=(start, end), method='bounded')
        if result.success:
            return result.x
        else:
            print("[WARNING] Minimization failed. Falling back to minimum Rp.")
    except Exception as e:
        print(f"[ERROR] Exception in theta_res estimation: {e}")

    return theta_deg[np.argmin(Rp)]


def calculate_fwhm(Rp, theta_deg):
    Rp_min = np.min(Rp)
    Rp_max = np.max(Rp)
    half_max = (Rp_max + Rp_min) / 2
    crossings = np.where(np.diff(np.sign(Rp - half_max)))[0]
    if len(crossings) >= 2:
        return abs(theta_deg[crossings[-1]] - theta_deg[crossings[0]])
    return np.nan

def calculate_q(theta_res, fwhm):
    return theta_res / fwhm if fwhm and not np.isnan(fwhm) else np.nan

def calculate_chi(sensitivity, fwhm):
    return sensitivity / fwhm if fwhm and not np.isnan(fwhm) else np.nan

def calculate_sensitivity_empirical(theta_res_pos, theta_res_neg, n_pos, n_neg):
    delta_n = n_pos - n_neg
    return (theta_res_pos - theta_res_neg) / delta_n if delta_n != 0 else np.nan

def calculate_theoretical_sensitivity_precise(n_metal, n_analyte, n_substrate):
    eps = n_metal ** 2
    eps_mr = np.real(eps)
    n_eff = np.real(n_analyte)
    n2 = np.real(n_substrate)
    numerator = eps_mr ** 2
    denominator = abs(eps_mr + n_eff ** 2)
    root_term = eps_mr * n2**2 * (eps_mr + n_eff**2) - eps_mr**2 * n_eff**2
    if denominator == 0 or root_term <= 0:
        return np.nan
    sensitivity_rad = numerator / (denominator * np.sqrt(root_term))
    return np.degrees(sensitivity_rad)


def restrict_range(theta_deg, Rp, window=(40, 80)):
    mask = (theta_deg >= window[0]) & (theta_deg <= window[1])
    return theta_deg[mask], Rp[mask]

def run_reflectance_simulation(substrate, metal, analytes, theta_window=(40, 80)):
    results = {
        "theta_res": {},
        "fwhm": {},
        "substrate": substrate,
        "theta_deg": theta_deg,
        "reflectance": {}
    }

    os.makedirs("figures", exist_ok=True)
    name_map = {"analyte_01": "positive", "analyte_02": "negative"}

    for analyte in analytes:
        label_analyte = name_map.get(analyte, analyte)
        print(f"\nSimulating for {label_analyte}...")

        plt.figure(figsize=(10, 6))
        theta_res_list = []
        fwhm_list = []
        reflectance_list = []

        for i, d_metal_nm in enumerate(metal_thicknesses_nm):
            d_metal = d_metal_nm * 1e-9
            d = np.array([d_cr, d_metal])
            n = np.array([
                materials[substrate],
                materials["Cr"],
                materials[metal],
                materials[analyte]
            ])

            Rp = np.array([
                getFresnelAIM(n, d, angle, lambda0)[2]
                for angle in theta_rad
            ])

            theta_deg_windowed, Rp_windowed = restrict_range(theta_deg, Rp, theta_window)
            theta_res = calculate_theta_res_smooth(theta_deg_windowed, Rp_windowed)
            fwhm = calculate_fwhm(Rp, theta_deg)

            theta_res_list.append(theta_res)
            fwhm_list.append(fwhm)
            reflectance_list.append(Rp)

            color = plt.cm.tab10(i % 10)
            plt.plot(theta_deg, Rp, linewidth=1.5, color=color,
                     label=f'{d_metal_nm} nm | θres ≈ {theta_res:.2f}°', zorder=1.5)

            if not np.isnan(theta_res):
                Rp_res = np.interp(theta_res, theta_deg, Rp)
                plt.plot(theta_res, Rp_res, 'ko', markersize=5, markerfacecolor='black', zorder=3)

        results["theta_res"][(metal, analyte)] = theta_res_list
        results["fwhm"][(metal, analyte)] = fwhm_list
        results["reflectance"][(metal, analyte)] = reflectance_list

        if TNR:
            plt.xlabel("Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (a.u.)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(fontsize=9, prop=TNR, loc="best")
        else:
            plt.xlabel("Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (a.u.)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=9, loc="best")

        if theta_res_list:
            plt.xlim(min(theta_res_list) - 1.5, max(theta_res_list) + 1.5)

        plt.ylim(0, 1)
        plt.grid(True)
        plt.tight_layout()
        base = f"figures/reflectance_{substrate.lower()}_{metal.lower()}_{label_analyte.lower()}"
        save_figure(base)
        plt.close()

    return results


def save_results_to_csv(results, metal_thicknesses_nm, analytes_dict, filename="results_spr.csv"):
    """
    Saves all empirical and theoretical figures of merit for each metal-analyte pair to a CSV file
    using semicolon (;) as the delimiter for compatibility with Excel in regional settings.
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

    # Use semicolon as separator for Excel compatibility in PT-BR systems
    df.to_csv(filename, index=False, sep=';')
    print(f"[INFO] Results saved to: {filename}")


# =========================
# Plotting Function
# =========================

def plot_figures_of_merit(results, metal_thicknesses_nm, save_dir="outputs/figures_of_merit"):
    os.makedirs(save_dir, exist_ok=True)
    metrics = [
        "theta_res", "fwhm",
        "sensitivity_empirical", "sensitivity_theoretical",
        "chi_empirical", "chi_theoretical",
        "q_empirical", "q_theoretical"
    ]
    titles = {
        "theta_res": (r"Resonance Angle (°)", "Metal Thickness (nm)"),
        "fwhm": (r"FWHM (°)", "Metal Thickness (nm)"),
        "sensitivity_empirical": (r"Sensitivity (°/RIU)", "Metal Thickness (nm)"),
        "sensitivity_theoretical": (r"Sensitivity (°/RIU)", "Metal Thickness (nm)"),
        "chi_empirical": (r"$\chi$ (RIU$^{-1})$", "Metal Thickness (nm)"),
        "chi_theoretical": (r"$\chi$ (RIU$^{-1})$", "Metal Thickness (nm)"),
        "q_empirical": (r"$Q$ (a.u.)", "Metal Thickness (nm)"),
        "q_theoretical": (r"$Q$ (a.u.)", "Metal Thickness (nm)")
    }
    for metric in metrics:
        metric_data = results.get(metric, {})
        if not metric_data:
            print(f"[INFO] No data found for metric: {metric}")
            continue
        has_valid_data = False
        plt.figure(figsize=(8, 5))
        for idx, metal in enumerate(["Ag", "Au", "Cu"]):
            key = (metal, "analyte_02")
            if key not in metric_data:
                continue
            y = metric_data[key]
            x = metal_thicknesses_nm
            if all(np.isnan(y)):
                continue
            has_valid_data = True
            plt.plot(x, y, 'ko', markersize=5, markerfacecolor='black', zorder=3)
            if len(x) >= 4 and not np.any(np.isnan(y)):
                spline = CubicSpline(x, y)
                x_fine = np.linspace(min(x), max(x), 500)
                y_smooth = spline(x_fine)
                plt.plot(x_fine, y_smooth, linewidth=1.5, label=metal)
            else:
                plt.plot(x, y, 'k--', linewidth=1.0, label=metal)
        if has_valid_data:
            ylabel, xlabel = titles[metric]
            if TNR:
                plt.xlabel(xlabel, fontsize=14, fontproperties=TNR)
                plt.ylabel(ylabel, fontsize=14, fontproperties=TNR)
                plt.xticks(fontsize=12, fontproperties=TNR)
                plt.yticks(fontsize=12, fontproperties=TNR)
                plt.legend(fontsize=10, loc="best", prop=TNR)
            else:
                plt.xlabel(xlabel, fontsize=14)
                plt.ylabel(ylabel, fontsize=14)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                plt.legend(fontsize=10, loc="best")
            plt.grid(True)
            plt.tight_layout()
            fname = os.path.join(save_dir, metric)
            save_figure(fname)
            plt.close()


def run_mode_1():
    print("[MODE 1] Compare Ag, Au, Cu for a selected substrate using analyte_01 and analyte_02")
    available_substrates = ["PMMA", "PC", "TOPAS"]
    for i, s in enumerate(available_substrates, 1):
        print(f"{i} - {s}")
    try:
        index = int(input("Select substrate (1-3): ").strip())
        substrate = available_substrates[index - 1]
    except (ValueError, IndexError):
        print("[ERROR] Invalid option.")
        return

    analytes = {
        "analyte_01": materials["analyte_01"],  # negative
        "analyte_02": materials["analyte_02"]   # positive
    }

    results = {
        "theta_deg": theta_deg,
        "substrate": substrate,
        "theta_res": {},
        "fwhm": {},
        "reflectance": {},
    }

    for metal in ["Ag", "Au", "Cu"]:
        res = run_reflectance_simulation(
            substrate, metal, analytes
        )
        results["reflectance"].update(res["reflectance"])
        results["theta_res"].update(res["theta_res"])
        results["fwhm"].update(res["fwhm"])

        key = (metal, "analyte_02")
        theta_res_neg = res["theta_res"][(metal, "analyte_01")]
        theta_res_pos = res["theta_res"][(metal, "analyte_02")]
        fwhm_list = res["fwhm"][(metal, "analyte_02")]

        s_empirical = [
            calculate_sensitivity_empirical(pos, neg, analytes["analyte_02"], analytes["analyte_01"])
            for pos, neg in zip(theta_res_pos, theta_res_neg)
        ]
        s_theoretical = calculate_theoretical_sensitivity_precise(
            n_metal=materials[metal],
            n_analyte=analytes["analyte_02"],
            n_substrate=materials[substrate]
        )
        q_list = [calculate_q(theta, fwhm) for theta, fwhm in zip(theta_res_pos, fwhm_list)]
        chi_empirical = [calculate_chi(s, f) for s, f in zip(s_empirical, fwhm_list)]
        chi_theoretical = [calculate_chi(s_theoretical, f) for f in fwhm_list]

        results.setdefault("sensitivity_empirical", {})[metal] = s_empirical
        results.setdefault("sensitivity_theoretical", {})[key] = [s_theoretical] * len(fwhm_list)
        results.setdefault("chi_empirical", {})[key] = chi_empirical
        results.setdefault("chi_theoretical", {})[key] = chi_theoretical
        results.setdefault("q_empirical", {})[key] = q_list
        results.setdefault("q_theoretical", {})[key] = q_list

    plot_figures_of_merit(results, metal_thicknesses_nm)
    save_results_to_csv(results, metal_thicknesses_nm, analytes)


if __name__ == "__main__":
    run_mode_1()