"""Tests for the UCCSD ansatz."""

import pytest
from vqe_bench.ansatze.uccsd import UCCSDAnsatz

def test_uccsd_initialization(simple_hamiltonian):
    ansatz = UCCSDAnsatz(simple_hamiltonian)
    
    assert ansatz.num_qubits == 2
    assert ansatz.num_parameters > 0
    assert ansatz.circuit is not None

def test_uccsd_fallback_without_chemistry():
    # Mocking a Hamiltonian data dict without Qiskit Nature dependencies
    mock_data = {
        "qubit_op": SparsePauliOp.from_list([("II", 1.0)]),
        "num_particles": None,
        "num_spatial": None,
    }
    import numpy as np
    from qiskit.quantum_info import SparsePauliOp
    
    ansatz = UCCSDAnsatz(mock_data)
    assert ansatz.num_parameters >= 2