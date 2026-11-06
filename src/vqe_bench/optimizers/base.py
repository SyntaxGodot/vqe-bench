"""Enhanced base optimizer with early stopping and gradient tracking."""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Optional
import numpy as np


@dataclass
class OptimizerResult:
    optimal_energy: float
    optimal_params: np.ndarray
    num_function_evaluations: int
    wall_time: float
    converged: bool
    history: list[float] = field(default_factory=list)
    gradient_norms: list[float] = field(default_factory=list)


class BaseOptimizer(ABC):
    """Abstract classical optimiser with early stopping support."""

    def __init__(self, maxiter: int = 500, tol: float = 1e-6, early_stopping: bool = False) -> None:
        self.maxiter = maxiter
        self.tol = tol
        self.early_stopping = early_stopping

    @abstractmethod
    def minimize(
        self,
        cost_fn: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
    ) -> OptimizerResult:
        ...