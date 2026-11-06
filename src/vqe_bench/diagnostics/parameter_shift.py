"""Exact parameter-shift gradients."""

from __future__ import annotations
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector


def _expectation(qc: QuantumCircuit, op: SparsePauliOp, params: np.ndarray) -> float:
    bound = qc.assign_parameters(dict(zip(qc.parameters, params, strict=True)))
    return float(np.real(Statevector.from_instruction(bound).expectation_value(op)))


def parameter_shift_gradient(
    qc: QuantumCircuit, 
    op: SparsePauliOp, 
    params: np.ndarray, 
    param_index: int
) -> float:
    """Exact gradient of <ψ(θ)|H|ψ(θ)> w.r.t. one parameter via parameter-shift."""
    shift = np.pi / 2.0
    
    plus = params.copy()
    plus[param_index] += shift
    minus = params.copy()
    minus[param_index] -= shift

    return 0.5 * (_expectation(qc, op, plus) - _expectation(qc, op, minus))