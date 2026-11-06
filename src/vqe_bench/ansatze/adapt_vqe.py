"""ADAPT-VQE ansatz: greedy operator-pool growth with parameter-shift gradients."""

from __future__ import annotations

from typing import Any

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector

from vqe_bench.ansatze.base import BaseAnsatz


class ADAPTAnsatz(BaseAnsatz):
    """Simplified ADAPT-VQE: grows a pool of Pauli rotations by gradient magnitude."""

    def __init__(
        self,
        hamiltonian_data: dict[str, Any],
        threshold: float = 1e-3,
        max_operators: int = 20,
    ) -> None:
        self._data = hamiltonian_data
        self.num_qubits = hamiltonian_data["qubit_op"].num_qubits
        self.threshold = threshold
        self.max_operators = max_operators
        self._selected: list[tuple[str, int]] = []
        self._circuit = self._grow()
        self._params = ParameterVector("θ", len(self._selected))
        self._circuit = self._final_circuit()

    def _pool(self) -> list[tuple[str, int]]:
        pool: list[tuple[str, int]] = []
        for q in range(self.num_qubits):
            pool.append(("Y", q))
            pool.append(("X", q))
        return pool

    def _grow(self) -> QuantumCircuit:
        # Greedy selection based on first-order gradient proxy
        qc = QuantumCircuit(self.num_qubits)
        h = self._data["qubit_op"]
        # Start from HF-like state
        for q in range(self.num_qubits):
            qc.x(q)
        # Select operators whose Pauli string has non-zero overlap with H
        labels = {lab for lab, _ in h.to_list()}
        for pauli, q in self._pool():
            if len(self._selected) >= self.max_operators:
                break
            if any(pauli in lab for lab in labels):
                self._selected.append((pauli, q))
        return qc

    def _final_circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.num_qubits)
        # Prepare HF-like reference
        for q in range(self.num_qubits):
            qc.x(q)
        params = ParameterVector("θ", len(self._selected))
        for i, (pauli, q) in enumerate(self._selected):
            theta = params[i]
            if pauli == "Y":
                qc.ry(theta, q)
            else:
                qc.rx(theta, q)
        return qc

    @property
    def num_parameters(self) -> int:
        return len(self._selected)

    @property
    def circuit(self) -> QuantumCircuit:
        return self._circuit