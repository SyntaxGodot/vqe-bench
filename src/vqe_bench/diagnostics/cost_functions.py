"""Cost functions for barren plateau diagnostics."""

from __future__ import annotations
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector


def global_cost(qc: QuantumCircuit, op: SparsePauliOp, params: np.ndarray) -> float:
    """Expectation value of the full Hamiltonian (global cost function)."""
    bound = qc.assign_parameters(dict(zip(qc.parameters, params, strict=True)))
    sv = Statevector.from_instruction(bound)
    return float(np.real(sv.expectation_value(op)))


def local_cost(qc: QuantumCircuit, op: SparsePauliOp, params: np.ndarray, qubit_idx: int = 0) -> float:
    """Expectation value of a single-qubit Z operator (local cost function)."""
    bound = qc.assign_parameters(dict(zip(qc.parameters, params, strict=True)))
    sv = Statevector.from_instruction(bound)
    
    # Build local Z operator for the specified qubit
    label = ["I"] * qc.num_qubits
    label[qubit_idx] = "Z"
    local_op = SparsePauliOp.from_list([("".join(label), 1.0)])
    
    return float(np.real(sv.expectation_value(local_op)))