"""Tests for exact parameter-shift gradients."""

import numpy as np
from qiskit.quantum_info import SparsePauliOp
from vqe_bench.diagnostics.gradients import parameter_shift_gradient
from vqe_bench.ansatze.hardware_efficient import HardwareEfficientAnsatz

def test_parameter_shift_exact_identity():
    # Gradient of <Z> w.r.t Ry(θ) is -sin(θ)
    ans = HardwareEfficientAnsatz(num_qubits=1, depth=0)
    qc = ans.circuit
    op = SparsePauliOp.from_list([("Z", 1.0)])
    
    theta0 = 0.5
    grad = parameter_shift_gradient(qc, op, np.array([theta0]), 0)
    
    assert np.isclose(grad, -np.sin(theta0), atol=1e-9)