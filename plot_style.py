import matplotlib.pyplot as plt

def apply_plot_style():
    """
    Applies a consistent MATLAB-like style to all plots.
    This includes grid lines, classic line widths, and LaTeX-style fonts.
    """
    plt.rcParams.update({
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "grid.color": "gray",
        "legend.frameon": False,
        "lines.linewidth": 1.8,
        "lines.markersize": 6,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif", "Palatino"],
        "mathtext.fontset": "cm",
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 5,
        "ytick.major.size": 5,
        "figure.dpi": 100,
        "savefig.dpi": 300
    })
