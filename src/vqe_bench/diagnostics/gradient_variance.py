"""Exact parameter-shift gradients and gradient-variance scans."""

from __future__ import annotations

from typing import Callable

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp, Statevector


def _expectation(qc: QuantumCircuit, op: SparsePauliOp, params: np.ndarray) -> float:
    bound = qc.assign_parameters(dict(zip(qc.parameters, params, strict=True)))
    sv = Statevector.from_instruction(bound)
    return float(np.real(sv.expectation_value(op)))


def parameter_shift_gradient(
    qc: QuantumCircuit,
    op: SparsePauliOp,
    params: np.ndarray,
    param_index: int,
) -> float:
    """Exact gradient of <ψ(θ)|H|ψ(θ)> w.r.t. one parameter via parameter-shift."""
    param = list(qc.parameters)[param_index]
    shift = np.pi / 2.0

    plus = params.copy()
    plus[param_index] += shift
    minus = params.copy()
    minus[param_index] -= shift

    return 0.5 * (_expectation(qc, op, plus) - _expectation(qc, op, minus))


def gradient_variance(
    ansatz_builder: Callable[[int, int], QuantumCircuit],
    op: SparsePauliOp,
    num_qubits: int,
    depth: int,
    num_samples: int = 50,
    seed: int = 0,
) -> float:
    """Variance of the gradient of the first parameter over random inits."""
    rng = np.random.default_rng(seed)
    qc = ansatz_builder(num_qubits, depth)
    n_params = len(qc.parameters)
    if n_params == 0:
        return 0.0
    grads: list[float] = []
    for _ in range(num_samples):
        params = rng.uniform(0, 2 * np.pi, size=n_params)
        grads.append(parameter_shift_gradient(qc, op, params, 0))
    return float(np.var(grads))