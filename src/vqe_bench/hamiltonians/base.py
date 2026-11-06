"""Base class and utilities for Hamiltonian builders."""

from __future__ import annotations
from typing import Any
import numpy as np
from qiskit.quantum_info import SparsePauliOp


def exact_ground_state(op: SparsePauliOp) -> float:
    """Compute the exact ground-state energy via dense diagonalisation."""
    mat = op.to_matrix(sparse=False)
    eigvals = np.linalg.eigvalsh(mat)
    return float(eigvals[0])


def validate_hamiltonian_data(data: dict[str, Any]) -> None:
    """Validate that a Hamiltonian data dict contains the required keys."""
    required_keys = {"qubit_op", "fci_energy"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(f"Hamiltonian data is missing keys: {missing}")
    if not isinstance(data["qubit_op"], SparsePauliOp):
        raise TypeError("qubit_op must be a SparsePauliOp")