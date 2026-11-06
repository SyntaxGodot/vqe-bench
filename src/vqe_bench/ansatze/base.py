"""Common ansatz interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from qiskit import QuantumCircuit


class BaseAnsatz(ABC):
    """Abstract base class for all ansätze."""

    @property
    @abstractmethod
    def num_parameters(self) -> int:
        ...

    @property
    @abstractmethod
    def circuit(self) -> QuantumCircuit:
        ...

    @property
    def depth(self) -> int:
        return self.circuit.depth()

    @property
    def two_qubit_gate_count(self) -> int:
        count = 0
        for inst in self.circuit.data:
            if inst.operation.num_qubits == 2:
                count += 1
        return count