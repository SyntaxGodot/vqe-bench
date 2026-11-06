"""Barren-plateau diagnostics."""

from vqe_bench.diagnostics.gradients import (
    gradient_variance,
    parameter_shift_gradient,
)

__all__ = ["parameter_shift_gradient", "gradient_variance"]