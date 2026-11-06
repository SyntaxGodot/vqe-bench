"""Tests for classical optimisers."""

import numpy as np
from vqe_bench.optimizers.scipy_optimizers import CobylaOptimizer, LBFGSBOptimizer
from vqe_bench.optimizers.spsa import SPSAOptimizer

def _quadratic(x: np.ndarray) -> float:
    return float(np.sum((x - 1.0) ** 2))

def test_cobyla_converges():
    opt = CobylaOptimizer(maxiter=200)
    res = opt.minimize(_quadratic, np.zeros(2))
    assert res.optimal_energy < 1e-4

def test_lbfgsb_converges():
    opt = LBFGSBOptimizer(maxiter=200)
    res = opt.minimize(_quadratic, np.zeros(2))
    assert res.optimal_energy < 1e-6

def test_spsa_reduces_energy():
    opt = SPSAOptimizer(maxiter=300, learning_rate=0.5)
    res = opt.minimize(_quadratic, np.zeros(2))
    assert res.optimal_energy < 0.5