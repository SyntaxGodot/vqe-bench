"""SciPy-based optimisers (COBYLA, L-BFGS-B)."""

from __future__ import annotations

import time
from typing import Callable

import numpy as np
from scipy.optimize import minimize as scipy_minimize

from vqe_bench.optimizers.base import BaseOptimizer, OptimizerResult


class CobylaOptimizer(BaseOptimizer):
    """COBYLA derivative-free optimiser."""

    def minimize(
        self,
        cost_fn: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
    ) -> OptimizerResult:
        history: list[float] = []

        def wrapped(x: np.ndarray) -> float:
            val = float(cost_fn(x))
            history.append(val)
            return val

        t0 = time.perf_counter()
        res = scipy_minimize(
            wrapped,
            initial_params,
            method="COBYLA",
            options={"maxiter": self.maxiter},
        )
        wall = time.perf_counter() - t0
        return OptimizerResult(
            optimal_energy=float(res.fun),
            optimal_params=np.asarray(res.x),
            num_function_evaluations=int(res.nfev),
            wall_time=wall,
            converged=bool(res.success),
            history=history,
        )


class LBFGSBOptimizer(BaseOptimizer):
    """L-BFGS-B gradient-based optimiser (finite-difference gradients)."""

    def minimize(
        self,
        cost_fn: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
    ) -> OptimizerResult:
        history: list[float] = []

        def wrapped(x: np.ndarray) -> float:
            val = float(cost_fn(x))
            history.append(val)
            return val

        t0 = time.perf_counter()
        res = scipy_minimize(
            wrapped,
            initial_params,
            method="L-BFGS-B",
            options={"maxiter": self.maxiter},
        )
        wall = time.perf_counter() - t0
        return OptimizerResult(
            optimal_energy=float(res.fun),
            optimal_params=np.asarray(res.x),
            num_function_evaluations=int(res.nfev),
            wall_time=wall,
            converged=bool(res.success),
            history=history,
        )