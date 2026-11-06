import numpy as np
import pytest
from qiskit.quantum_info import SparsePauliOp

from vqe_bench.ansatze import HardwareEfficientAnsatz
from vqe_bench.hamiltonians import build_spin_hamiltonian
from vqe_bench.optimizers import CobylaOptimizer
from vqe_bench.vqe import run_vqe


def test_vqe_validates_mismatched_qubits():
    ham = build_spin_hamiltonian("tfim", n_qubits=2)
    ansatz = HardwareEfficientAnsatz(num_qubits=3, depth=1)  # Wrong number of qubits
    with pytest.raises(ValueError, match="qubit count"):
        run_vqe(ham, ansatz, CobylaOptimizer(maxiter=10))


def test_vqe_callback_is_called():
    ham = build_spin_hamiltonian("tfim", n_qubits=2)
    ansatz = HardwareEfficientAnsatz(num_qubits=2, depth=1)
    opt = CobylaOptimizer(maxiter=10)
    
    calls = []
    def my_callback(iteration, params, energy):
        calls.append((iteration, energy))

    run_vqe(ham, ansatz, opt, callback=my_callback)
    assert len(calls) > 0
    assert calls[0][0] == 1


def test_vqe_result_metadata():
    ham = build_spin_hamiltonian("tfim", n_qubits=2)
    ansatz = HardwareEfficientAnsatz(num_qubits=2, depth=1)
    result = run_vqe(ham, ansatz, CobylaOptimizer(maxiter=5))
    
    assert "seed" in result.metadata
    assert result.metadata["optimizer"] == "CobylaOptimizer"
    assert result.num_function_evaluations > 0