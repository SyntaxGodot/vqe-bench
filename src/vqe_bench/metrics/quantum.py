import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from vqe_bench.diagnostics.parameter_shift import parameter_shift_gradient

def gradient_norm(qc: QuantumCircuit, op: SparsePauliOp, params: np.ndarray) -> float:
    """Calculate the L2 norm of the gradient vector."""
    grads = [
        parameter_shift_gradient(qc, op, params, i)
        for i in range(len(params))
    ]
    return float(np.linalg.norm(grads))

def parameter_variance(params: np.ndarray) -> float:
    """Measure how spread out the parameters are (indicates plateau)."""
    return float(np.var(params))

def landscape_ruggedness(history: list[float]) -> float:
    """Measure the standard deviation of energy changes during optimization."""
    if len(history) < 2:
        return 0.0
    diffs = np.diff(history)
    return float(np.std(diffs))