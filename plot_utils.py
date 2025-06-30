# plot_utils.py
import os
import matplotlib.pyplot as plt
import warnings

# Suppress known EPS transparency warning
warnings.filterwarnings("ignore", category=UserWarning, message=".*transparency.*")

def save_figure(filename_base: str, dpi_eps: int = 600, dpi_png: int = 300, show: bool = False):
    """
    Saves the current Matplotlib figure as both .eps and .png and optionally shows it.

    Parameters:
        filename_base (str): Full path without extension.
        dpi_eps (int): Resolution for EPS (default: 600).
        dpi_png (int): Resolution for PNG (default: 300).
        show (bool): Whether to display the plot after saving.
    """
    if not plt.get_fignums():
        print("[WARNING] No active figure to save.")
        return

    os.makedirs(os.path.dirname(filename_base), exist_ok=True)

    eps_path = f"{filename_base}.eps"
    png_path = f"{filename_base}.png"

    try:
        plt.tight_layout()
    except Exception as e:
        print(f"[WARNING] Could not apply tight_layout(): {e}")

    # Save PNG (sem backend switch)
    try:
        plt.savefig(png_path, format="png", dpi=dpi_png)
        print(f"[INFO] Saved: {png_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save PNG: {e}")

    # Save EPS
    try:
        plt.savefig(eps_path, format="eps", bbox_inches="tight", dpi=dpi_eps)
        print(f"[INFO] Saved: {eps_path}")
    except Exception as e:
        print(f"[WARNING] Failed to save EPS (ignored): {e}")

    # Optionally show
    if show:
        try:
            plt.show()
        except Exception as e:
            print(f"[WARNING] Could not display figure: {e}")

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
