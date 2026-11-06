"""Energy-error metrics."""

from __future__ import annotations

CHEMICAL_ACCURACY: float = 1.6e-3  # Hartree


def absolute_error(energy: float, reference: float) -> float:
    """Compute the absolute energy error."""
    return abs(energy - reference)


def relative_error(energy: float, reference: float) -> float:
    """Compute the relative energy error."""
    if reference == 0.0:
        return float("inf")
    return abs(energy - reference) / abs(reference)


def chemical_accuracy_reached(energy: float, reference: float) -> bool:
    """Check if the energy is within chemical accuracy (1.6 mHa)."""
    return absolute_error(energy, reference) <= CHEMICAL_ACCURACY