# plot_style.py
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from matplotlib import font_manager

def apply_plot_style():
    # Tenta localizar Times New Roman
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
    if os.path.exists(font_path):
        font_entry = font_manager.FontProperties(fname=font_path)
        mpl.rcParams["font.family"] = font_entry.get_name()
    else:
        print("[WARNING] Times New Roman not found. Using default serif font.")
        mpl.rcParams["font.family"] = "serif"

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
