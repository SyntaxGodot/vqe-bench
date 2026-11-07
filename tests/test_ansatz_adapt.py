"""Tests for the ADAPT-VQE ansatz."""

import pytest
from vqe_bench.ansatze.adapt_vqe import ADAPTAnsatz

def test_adapt_initialization(simple_hamiltonian):
    ansatz = ADAPTAnsatz(simple_hamiltonian, threshold=1e-2, max_operators=5)
    
    assert ansatz.num_qubits == 2
    assert ansatz.num_parameters <= 5
    assert ansatz.num_parameters > 0
    assert "θ" in str(ansatz.circuit.parameters)

def test_adapt_circuit_depth(simple_hamiltonian):
    ansatz = ADAPTAnsatz(simple_hamiltonian)
    assert ansatz.depth > 0