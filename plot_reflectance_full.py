import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from plot_style import apply_plot_style
from plot_utils import save_figure

# Font: Times New Roman se disponível
try:
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    TNR = FontProperties(fname=font_path) if os.path.exists(font_path) else None
except Exception:
    TNR = None
    print("[WARNING] Times New Roman not found. Using default font.")

# Estilo por grupo (corrigido: analyte_01 = negativo, analyte_02 = positivo)
GROUP_LABELS = {"analyte_01": "negative", "analyte_02": "positive"}
GROUP_COLORS = {"analyte_01": "#1f77b4", "analyte_02": "#d62728"}
GROUP_LINES = {"analyte_01": "-", "analyte_02": "--"}

def plot_reflectance_22_curves(results, metal_thicknesses_nm, figures, save_dir="outputs/reflectance_curves"):
    apply_plot_style()
    os.makedirs(save_dir, exist_ok=True)

    analytes = ["analyte_01", "analyte_02"]
    theta_deg = results["theta_deg"]


    for metal in ["Ag", "Au", "Cu"]:
        plt.figure(figsize=(10, 6))

        for analyte in analytes:
            key = (metal, analyte)
            Rp_list = results["reflectance"].get(key, [])
            theta_res_list = results["theta_res"].get(key, [])

            if not Rp_list:
                continue

            for i, Rp in enumerate(Rp_list):
                label = GROUP_LABELS[analyte] if i == 0 else None
                color = GROUP_COLORS[analyte]
                linestyle = GROUP_LINES[analyte]

                plt.plot(theta_deg, Rp,
                         color=color,
                         linestyle=linestyle,
                         linewidth=1.5,
                         alpha=0.9,
                         label=label)

                if len(theta_res_list) > i:
                    theta_res = theta_res_list[i]
                    idx = np.argmin(np.abs(np.array(theta_deg) - theta_res))
                    plt.plot(theta_deg[idx], Rp[idx],
                             'ko', markersize=5, markerfacecolor='black')

        theta_combined = results["theta_res"].get((metal, "analyte_01"), []) + \
                         results["theta_res"].get((metal, "analyte_02"), [])
        if theta_combined:
            plt.xlim(min(theta_combined) - 1.5, max(theta_combined) + 1.5)

        plt.ylim(0, 1)

        # Inserir sensibilidades exatas no gráfico (calculadas com base em analyte_01)
        try:
            s_num = figures["sensitivity_empirical"][0]
            s_theo = figures["sensitivity_theoretical"][0]
            text = f"S_num = {s_num:.6f} °/RIU\nS_theo = {s_theo:.6f} °/RIU"
            plt.text(0.02, 0.02, text, transform=plt.gca().transAxes, fontsize=10,
                     verticalalignment='bottom', horizontalalignment='left',
                     bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))
        except Exception as e:
            print(f"[WARNING] Could not insert sensitivity text: {e}")

        if TNR:
            plt.xlabel("Angle (°)", fontsize=14, fontproperties=TNR)
            plt.ylabel("Reflectance (a.u.)", fontsize=14, fontproperties=TNR)
            plt.xticks(fontsize=12, fontproperties=TNR)
            plt.yticks(fontsize=12, fontproperties=TNR)
            plt.legend(fontsize=10, loc="lower left", prop=TNR)
        else:
            plt.xlabel("Angle (°)", fontsize=14)
            plt.ylabel("Reflectance (a.u.)", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(fontsize=10, loc="lower left")

        plt.grid(True)
        plt.title("")
        plt.tight_layout()

        fname = os.path.join(save_dir, f"reflectance_{metal.lower()}")
        save_figure(fname)
        plt.show()
        plt.close()
