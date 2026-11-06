"""Zero-noise extrapolation factories."""

from __future__ import annotations

import numpy as np


def zne_extrapolate(
    scale_factors: list[float],
    energies: list[float],
    method: str = "richardson",
) -> float:
    """Extrapolate to zero noise from (scale_factor, energy) pairs."""
    x = np.asarray(scale_factors, dtype=float)
    y = np.asarray(energies, dtype=float)

    if method == "linear":
        coeffs = np.polyfit(x, y, 1)
        return float(np.polyval(coeffs, 0.0))

    if method == "richardson":
        # Richardson extrapolation assumes y = a + b*x + c*x^2 + ...
        # Build Vandermonde system and evaluate at x=0
        n = len(x)
        vander = np.vander(x, n, increasing=True)
        coeffs, *_ = np.linalg.lstsq(vander, y, rcond=None)
        return float(coeffs[0])

    if method == "exponential":
        # Fit y = a + b * exp(c*x); fall back to linear if unstable
        try:
            from scipy.optimize import curve_fit

            def model(xx: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
                return a + b * np.exp(c * xx)

            popt, _ = curve_fit(
                model, x, y, p0=[y[-1], y[0] - y[-1], -1.0], maxfev=10000
            )
            return float(popt[0])
        except Exception:
            coeffs = np.polyfit(x, y, 1)
            return float(np.polyval(coeffs, 0.0))

    raise ValueError(f"Unknown extrapolation method: {method}")