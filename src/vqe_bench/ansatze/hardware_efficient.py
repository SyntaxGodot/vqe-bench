"""Hardware-efficient ansatz with configurable entanglement."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

from vqe_bench.ansatze.base import BaseAnsatz


class HardwareEfficientAnsatz(BaseAnsatz):
    """Layers of Ry rotations followed by CX entanglement."""

    def __init__(
        self,
        num_qubits: int,
        depth: int = 1,
        entanglement: str = "linear",
    ) -> None:
        self.num_qubits = num_qubits
        self.reps = depth
        self.entanglement = entanglement
        self._params = ParameterVector("θ", num_qubits * (depth + 1))
        self._circuit = self._build()

    def _entangling_pairs(self) -> list[tuple[int, int]]:
        n = self.num_qubits
        if self.entanglement == "linear":
            return [(i, i + 1) for i in range(n - 1)]
        if self.entanglement == "circular":
            pairs = [(i, i + 1) for i in range(n - 1)]
            if n > 2:
                pairs.append((n - 1, 0))
            return pairs
        if self.entanglement == "full":
            return [(i, j) for i in range(n) for j in range(i + 1, n)]
        if self.entanglement == "sca":
            # Shifted circular alternating: even then odd bonds
            pairs = [(i, i + 1) for i in range(0, n - 1, 2)]
            pairs += [(i, i + 1) for i in range(1, n - 1, 2)]
            return pairs
        raise ValueError(f"Unknown entanglement: {self.entanglement}")

    def _build(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.num_qubits)
        p = 0
        for layer in range(self.reps + 1):
            for q in range(self.num_qubits):
                qc.ry(self._params[p], q)
                p += 1
            if layer < self.reps:
                for a, b in self._entangling_pairs():
                    qc.cx(a, b)
        return qc

    @property
    def num_parameters(self) -> int:
        return len(self._params)

    @property
    def circuit(self) -> QuantumCircuit:
        return self._circuit