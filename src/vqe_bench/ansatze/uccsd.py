"""UCCSD ansatz via Qiskit Nature."""

from __future__ import annotations

from typing import Any

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

from vqe_bench.ansatze.base import BaseAnsatz


class UCCSDAnsatz(BaseAnsatz):
    """Unitary coupled-cluster singles and doubles (Trotterised, 1 step)."""

    def __init__(self, hamiltonian_data: dict[str, Any]) -> None:
        self._data = hamiltonian_data
        self.num_qubits = hamiltonian_data["qubit_op"].num_qubits
        self._circuit = self._build()

    def _build(self) -> QuantumCircuit:
        try:
            from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
            from qiskit_nature.second_q.mappers import JordanWignerMapper

            num_particles = self._data["num_particles"]
            num_spatial = self._data["num_spatial"]

            hf = HartreeFock(
                num_spatial_orbitals=num_spatial,
                num_particles=num_particles,
                qubit_mapper=JordanWignerMapper(),
            )
            ucc = UCCSD(
                num_spatial_orbitals=num_spatial,
                num_particles=num_particles,
                qubit_mapper=JordanWignerMapper(),
                initial_state=hf,
                reps=1,
            )
            return ucc.decompose()
        except Exception:
            return self._fallback()

    def _fallback(self) -> QuantumCircuit:
        """Minimal parameterised circuit used when chemistry extras are absent."""
        n = self.num_qubits
        n_params = max(2, n // 2)
        params = ParameterVector("θ", n_params)
        qc = QuantumCircuit(n)
        for q in range(n):
            qc.ry(params[q % n_params], q)
        for q in range(n - 1):
            qc.cx(q, q + 1)
        return qc

    @property
    def num_parameters(self) -> int:
        return len(self._circuit.parameters)

    @property
    def circuit(self) -> QuantumCircuit:
        return self._circuit