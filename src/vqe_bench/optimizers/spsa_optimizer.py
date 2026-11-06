"""Simultaneous Perturbation Stochastic Approximation (SPSA)."""

from __future__ import annotations

import time
from typing import Callable

import numpy as np

from vqe_bench.optimizers.base import BaseOptimizer, OptimizerResult


class SPSAOptimizer(BaseOptimizer):
    """SPSA with decaying learning rate and perturbation size."""

    def __init__(
        self,
        maxiter: int = 500,
        learning_rate: float = 0.1,
        a: float = 0.602,
        c: float = 0.101,
    ) -> None:
        super().__init__(maxiter)
        self.learning_rate = learning_rate
        self.a = a
        self.c = c

    def minimize(
        self,
        cost_fn: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
    ) -> OptimizerResult:
        x = np.array(initial_params, dtype=float)
        n_params = len(x)
        history: list[float] = [float(cost_fn(x))]
        nfev = 1
        rng = np.random.default_rng(0)
        t0 = time.perf_counter()

        for k in range(1, self.maxiter + 1):
            ak = self.learning_rate / (k ** self.a)
            ck = 1.0 / (k ** self.c)
            delta = rng.choice([-1.0, 1.0], size=n_params)
            x_plus = x + ck * delta
            x_minus = x - ck * delta
            f_plus = float(cost_fn(x_plus))
            f_minus = float(cost_fn(x_minus))
            nfev += 2
            grad = (f_plus - f_minus) / (2.0 * ck * delta)
            x = x - ak * grad
            energy = float(cost_fn(x))
            nfev += 1
            history.append(energy)

        wall = time.perf_counter() - t0
        return OptimizerResult(
            optimal_energy=history[-1],
            optimal_params=x,
            num_function_evaluations=nfev,
            wall_time=wall,
            converged=True,
            history=history,
        )