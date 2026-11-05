"""Spin-model Hamiltonians (TFIM, Heisenberg XXZ) and exact diagonalisation."""

from __future__ import annotations

from typing import Any

import numpy as np
from qiskit.quantum_info import SparsePauliOp


def build_spin_hamiltonian(
    model: str,
    n_qubits: int,
    j_coupling: float = 1.0,
    h_field: float = 1.0,
    delta: float = 1.0,
    periodic: bool = True,
) -> dict[str, Any]:
    """Build a qubit Hamiltonian for a 1D spin chain (open or periodic BC)."""
    if model == "tfim":
        op = _tfim(n_qubits, j_coupling, h_field, periodic)
    elif model == "heisenberg_xxz":
        op = _heisenberg_xxz(n_qubits, j_coupling, delta, periodic)
    else:
        raise ValueError(f"Unknown spin model: {model}")
    return {
        "qubit_op": op,
        "fci_energy": exact_ground_state(op),
        "name": f"{model}_n{n_qubits}",
    }


def _bonds(n: int, periodic: bool) -> list[tuple[int, int]]:
    bonds = [(i, i + 1) for i in range(n - 1)]
    if periodic and n > 2:
        bonds.append((n - 1, 0))
    return bonds


def _tfim(n: int, j: float, h: float, periodic: bool) -> SparsePauliOp:
    terms: list[tuple[str, float]] = []
    for i, k in _bonds(n, periodic):
        label = ["I"] * n
        label[i] = "Z"
        label[k] = "Z"
        terms.append(("".join(label), -j))
    for i in range(n):
        label = ["I"] * n
        label[i] = "X"
        terms.append(("".join(label), -h))
    return SparsePauliOp.from_list(terms)


def _heisenberg_xxz(n: int, j: float, delta: float, periodic: bool) -> SparsePauliOp:
    terms: list[tuple[str, float]] = []
    for i, k in _bonds(n, periodic):
        for pauli, coeff in [("X", j), ("Y", j), ("Z", j * delta)]:
            label = ["I"] * n
            label[i] = pauli
            label[k] = pauli
            terms.append(("".join(label), coeff))
    return SparsePauliOp.from_list(terms)


def exact_ground_state(op: SparsePauliOp) -> float:
    """Exact ground-state energy via dense diagonalisation."""
    mat = op.to_matrix(sparse=False)
    eigvals = np.linalg.eigvalsh(mat)
    return float(eigvals[0])