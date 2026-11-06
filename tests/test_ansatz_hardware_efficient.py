"""Tests for the Hardware-Efficient ansatz."""

from vqe_bench.ansatze.hardware_efficient import HardwareEfficientAnsatz

def test_he_parameter_count():
    ansatz = HardwareEfficientAnsatz(num_qubits=4, depth=2, entanglement="linear")
    # (depth + 1) layers * num_qubits
    assert ansatz.num_parameters == 4 * 3

def test_he_linear_entanglement_gates():
    ansatz = HardwareEfficientAnsatz(num_qubits=4, depth=1, entanglement="linear")
    # n-1 CX gates per layer
    assert ansatz.two_qubit_gate_count == 3

def test_he_circular_entanglement_gates():
    ansatz = HardwareEfficientAnsatz(num_qubits=4, depth=1, entanglement="circular")
    # n CX gates per layer
    assert ansatz.two_qubit_gate_count == 4

def test_he_full_entanglement_gates():
    ansatz = HardwareEfficientAnsatz(num_qubits=3, depth=1, entanglement="full")
    # n*(n-1)/2 CX gates
    assert ansatz.two_qubit_gate_count == 3