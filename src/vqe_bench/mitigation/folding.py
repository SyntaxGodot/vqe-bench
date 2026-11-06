"""Global and local unitary folding."""

from __future__ import annotations

from qiskit import QuantumCircuit


def fold_circuit_global(circuit: QuantumCircuit, scale_factor: float) -> QuantumCircuit:
    """Fold the whole circuit: append U†U^k copies."""
    if scale_factor < 1.0:
        raise ValueError("scale_factor must be >= 1.0")
    n_folds = int(round((scale_factor - 1.0) / 2.0))
    folded = circuit.copy()
    for _ in range(n_folds):
        folded = folded.compose(circuit.inverse()).compose(circuit)
    return folded


def fold_circuit_local(circuit: QuantumCircuit, scale_factor: float) -> QuantumCircuit:
    """Fold individual gates (simplified: treat each gate as a layer)."""
    if scale_factor < 1.0:
        raise ValueError("scale_factor must be >= 1.0")
    n_folds = int(round((scale_factor - 1.0) / 2.0))
    folded = QuantumCircuit(*circuit.qregs)
    for inst in circuit.data:
        folded.append(inst.operation, inst.qubits, inst.clbits)
        if inst.operation.num_qubits == 2:
            for _ in range(n_folds):
                folded.append(inst.operation.inverse(), inst.qubits, inst.clbits)
                folded.append(inst.operation, inst.qubits, inst.clbits)
    return folded