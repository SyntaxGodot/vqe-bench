"""Base optimiser interface and result dataclass."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable

import numpy as np


@dataclass
class OptimizerResult:
    optimal_energy: float
    optimal_params: np.ndarray
    num_function_evaluations: int
    wall_time: float
    converged: bool
    history: list[float] = field(default_factory=list)


class BaseOptimizer(ABC):
    """Abstract classical optimiser."""

    def __init__(self, maxiter: int = 500) -> None:
        self.maxiter = maxiter

    @abstractmethod
    def minimize(
        self,
        cost_fn: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
    ) -> OptimizerResult:
        ...