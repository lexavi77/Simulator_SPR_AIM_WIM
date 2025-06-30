# plot_style.py
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from matplotlib import font_manager

def apply_plot_style():
    # Caminho da Times New Roman
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    fallback_font = "DejaVu Serif"

    if os.path.exists(font_path):
        font_entry = font_manager.FontProperties(fname=font_path)
        tnr_name = font_entry.get_name()
        mpl.rcParams["font.family"] = [tnr_name, fallback_font]
        print(f"[INFO] Using font: {tnr_name} with fallback: {fallback_font}")
    else:
        mpl.rcParams["font.family"] = [fallback_font]
        print(f"[WARNING] Times New Roman not found. Using fallback: {fallback_font}")

    mpl.rcParams.update({
        "font.size": 12,
        "axes.labelsize": 14,
        "axes.titlesize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white"
    })
