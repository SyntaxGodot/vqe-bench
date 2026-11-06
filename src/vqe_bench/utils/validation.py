from __future__ import annotations
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from typing import Any


def validate_hamiltonian(op: SparsePauliOp) -> None:
    """Ensure Hamiltonian has valid properties."""
    if not isinstance(op, SparsePauliOp):
        raise TypeError(f"Expected SparsePauliOp, got {type(op)}")
    if op.num_qubits < 1:
        raise ValueError(f"Hamiltonian must act on at least 1 qubit, got {op.num_qubits}")
    if not np.all(np.isfinite(op.coeffs)):
        raise ValueError("Hamiltonian contains non-finite coefficients.")


def validate_ansatz_compatibility(circuit: QuantumCircuit, op: SparsePauliOp) -> None:
    """Ensure the ansatz and Hamiltonian act on the same number of qubits."""
    if circuit.num_qubits != op.num_qubits:
        raise ValueError(
            f"Ansatz qubit count ({circuit.num_qubits}) does not match "
            f"Hamiltonian qubit count ({op.num_qubits})"
        )


def validate_parameters(params: np.ndarray, expected_length: int) -> None:
    """Check parameter vector shape."""
    if not isinstance(params, np.ndarray):
        raise TypeError("Parameters must be a numpy array.")
    if len(params) != expected_length:
        raise ValueError(f"Expected {expected_length} parameters, got {len(params)}")
    if not np.all(np.isfinite(params)):
        raise ValueError("Parameter vector contains NaN or Inf values.")