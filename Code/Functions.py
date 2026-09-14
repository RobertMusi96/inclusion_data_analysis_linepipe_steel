import numpy as np
from scipy.special import iv  # modified Bessel function
import matplotlib as mpl

def setup_matplotlib_parameter():
    # ── Wong B. (2011) Nature Methods 8, 441 ──────────────────────────────────
    # "Points of view: Color blindness"
    # Safe for deuteranopia, protanopia, and tritanopia

    WONG = {
        "black": "#000000",
        "orange": "#E69F00",
        "sky_blue": "#56B4E9",
        "bluish_green": "#009E73",
        "yellow": "#F0E442",
        "blue": "#0072B2",
        "vermillion": "#D55E00",
        "reddish_purple": "#CC79A7",
    }

    # Recommended order: avoid yellow early (low contrast on white)
    WONG_CYCLE = [
        WONG["blue"],
        WONG["orange"],
        WONG["bluish_green"],
        WONG["vermillion"],
        WONG["sky_blue"],
        WONG["reddish_purple"],
        WONG["yellow"],
        WONG["black"],
    ]

    # ── Apply globally ─────────────────────────────────────────────────────────

    mpl.rcParams.update({
        "axes.prop_cycle": mpl.cycler(color=WONG_CYCLE),
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "sans-serif"],
        "font.size": 10,
        "axes.labelsize": 12,
        "axes.labelweight": "bold",
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.edgecolor": "#222222",
        "axes.linewidth": 0.8,
        "axes.facecolor": "#ffffff",
        "figure.facecolor": "#ffffff",
        "grid.color": "#dddddd",
        "grid.linewidth": 0.6,
        "axes.grid": True,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "legend.labelcolor": "#444444",
    })

    return WONG_CYCLE

# -------------------------- KDE -------------------------
def cartesian_to_ternary(x, y):
    """
    Convert grid points to ternary coordinates.
    """
    B = x - 0.5 * y / (np.sqrt(3) / 2)
    C = y / (np.sqrt(3) / 2)
    A = 1 - B - C
    return np.column_stack((A, B, C))


def vmf_kde(X_sphere, query_points, bandwidth, normalize: bool = True,
            scaling: str = "linear" or "log" or "None"):
    """
    Sqrt transformation.
    Von Mises-Fisher KDE on the unit hypersphere.
    """
    X = sqrt_transform(X_sphere)

    d = X.shape[1]       # dimensionality (3 for ternary)
    kappa = 1.0 / bandwidth**2  # concentration parameter

    # Normalization constant for vMF in d dimensions
    p = d / 2
    C = kappa**(p - 1) / ((2 * np.pi)**p * iv(p - 1, kappa))

    # Compute density at each query point
    densities = np.zeros(len(query_points))
    for i, q in enumerate(query_points):
        dot_products = X @ q          # cosine similarities, shape (n,)
        densities[i] = np.mean(C * np.exp(kappa * dot_products))

    if scaling == "log":
        Z = np.log10(densities + 1e-300)
    elif scaling == "linear":
        Z = densities
    else:
        raise ValueError(f"Invalid scaling option: {scaling}")

    if normalize:
        return (Z - Z.min()) / (Z.max() - Z.min())
    else:
        return Z


# ── 1. Square root transformation (simplex → hypersphere) ──────────────────
def sqrt_transform(X):
    """Map compositions to the positive orthant of the unit hypersphere."""
    X = X / X.sum(axis=1, keepdims=True)  # ensure normalization
    return np.sqrt(X)  # each row now has L2 norm = 1


def sqrt_inverse(Y):
    """Map back from hypersphere to simplex."""
    return Y ** 2  # squaring recovers compositions (already normalized)