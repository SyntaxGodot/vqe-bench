"""Tests for Zero-Noise Extrapolation."""

import pytest
from vqe_bench.mitigation.zne import zne_extrapolate
from vqe_bench.mitigation.folding import fold_circuit_global, fold_circuit_local
from qiskit import QuantumCircuit

def test_zne_linear():
    factors = [1.0, 3.0, 5.0]
    noisy_energies = [0.05, 0.15, 0.25] # linear with slope 0.05
    mitigated = zne_extrapolate(factors, noisy_energies, method="linear")
    assert pytest.approx(mitigated, abs=1e-6) == 0.0

def test_zne_richardson():
    factors = [1.0, 3.0, 5.0]
    noisy_energies = [0.06, 0.2, 0.42] # quadratic curve
    mitigated = zne_extrapolate(factors, noisy_energies, method="richardson")
    assert pytest.approx(mitigated, abs=1e-6) == 0.05

def test_fold_global_depth_increases():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    folded = fold_circuit_global(qc, scale_factor=3.0)
    assert folded.depth() > qc.depth()

def test_fold_local_depth_increases():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    folded = fold_circuit_local(qc, scale_factor=3.0)
    assert folded.depth() > qc.depth()