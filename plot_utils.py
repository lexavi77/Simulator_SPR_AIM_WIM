# plot_utils.py
import os
import matplotlib.pyplot as plt

def save_figure(filename_base: str, dpi_eps: int = 600, dpi_png: int = 300):
    """
    Saves the current Matplotlib figure as both .eps and .png.

    Parameters:
        filename_base (str): Full path without extension.
        dpi_eps (int): Resolution for EPS (default: 600).
        dpi_png (int): Resolution for PNG (default: 300).
    """
    if not plt.get_fignums():
        print("[WARNING] No active figure to save.")
        return

    os.makedirs(os.path.dirname(filename_base), exist_ok=True)

    plt.tight_layout()

    eps_path = f"{filename_base}.eps"
    png_path = f"{filename_base}.png"

    plt.savefig(eps_path, format="eps", bbox_inches="tight", dpi=dpi_eps)
    plt.savefig(png_path, format="png", dpi=dpi_png)
    print(f"[INFO] Saved: {eps_path} and {png_path}")


def get_matlab_colors(n):
    """
    Returns a list of n distinct colors in the MATLAB/Tableau style.
    
    Parameters:
        n (int): Number of colors requested.

    Returns:
        List of hex color codes.
    """
    base_colors = [
        "#1f77b4",  # Blue
        "#ff7f0e",  # Orange
        "#2ca02c",  # Green
        "#d62728",  # Red
        "#9467bd",  # Purple
        "#8c564b",  # Brown
        "#e377c2",  # Pink
        "#7f7f7f",  # Gray
        "#bcbd22",  # Olive
        "#17becf"   # Cyan
    ]
    return [base_colors[i % len(base_colors)] for i in range(n)]
