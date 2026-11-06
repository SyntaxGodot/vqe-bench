"""Tests for barren plateau gradient variance diagnostics."""

import numpy as np
from vqe_bench.diagnostics.gradients import gradient_variance
from vqe_bench.ansatze.hardware_efficient import HardwareEfficientAnsatz
from vqe_bench.hamiltonians.spins import build_spin_hamiltonian

def test_gradient_variance_returns_float():
    ham = build_spin_hamiltonian("tfim", n_qubits=2)
    
    def builder(n, d):
        return HardwareEfficientAnsatz(n, depth=d).circuit
        
    var = gradient_variance(builder, ham["qubit_op"], num_qubits=2, depth=1, num_samples=5)
    assert isinstance(var, float)
    assert var >= 0.0