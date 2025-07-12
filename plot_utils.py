import os
import matplotlib.pyplot as plt
import warnings

# Suprimir warning conhecido de transparência ao salvar EPS
warnings.filterwarnings("ignore", category=UserWarning, message=".*transparency.*")

def save_figure(filename_base: str, dpi_eps: int = 600, dpi_png: int = 300, show: bool = False):
    """
    Saves the current Matplotlib figure as both .eps and .png and optionally shows it.

    Parameters:
        filename_base (str): Full path without extension (e.g., "outputs/figure_name").
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

    try:
        plt.savefig(png_path, format="png", dpi=dpi_png)
        print(f"[INFO] Saved: {png_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save PNG: {e}")

    try:
        plt.savefig(eps_path, format="eps", dpi=dpi_eps, bbox_inches="tight")
        print(f"[INFO] Saved: {eps_path}")
    except Exception as e:
        print(f"[WARNING] Failed to save EPS (ignored): {e}")

    if show:
        try:
            plt.show()
        except Exception as e:
            print(f"[WARNING] Could not display figure: {e}")
