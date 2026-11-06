from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Callable, Optional, Any

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector

from vqe_bench.ansatze.base import BaseAnsatz
from vqe_bench.optimizers.base import BaseOptimizer
from vqe_bench.utils.logger import setup_logger
from vqe_bench.utils.validation import validate_hamiltonian, validate_ansatz_compatibility, validate_parameters
from vqe_bench.utils.telemetry import track_resources
from vqe_bench.metrics.quantum import gradient_norm, landscape_ruggedness

logger = setup_logger("VQE")


@dataclass
class VQEResult:
    optimal_energy: float
    optimal_params: np.ndarray
    error_vs_fci: float
    num_function_evaluations: int
    wall_time: float
    converged: bool
    history: list[float] = field(default_factory=list)
    gradient_norms: list[float] = field(default_factory=list)
    ansatz_params: int = 0
    ansatz_depth: int = 0
    two_qubit_gates: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


def _statevector_energy(qc: QuantumCircuit, op: SparsePauliOp, params: np.ndarray) -> float:
    bound = qc.assign_parameters(dict(zip(qc.parameters, params, strict=True)))
    sv = Statevector.from_instruction(bound)
    return float(np.real(sv.expectation_value(op)))


@track_resources
def run_vqe(
    hamiltonian_data: dict,
    ansatz: BaseAnsatz,
    optimizer: BaseOptimizer,
    seed: int = 42,
    callback: Optional[Callable[[int, np.ndarray, float], None]] = None,
) -> VQEResult:
    """Run VQE with full validation, telemetry, and landscape tracking."""
    op: SparsePauliOp = hamiltonian_data["qubit_op"]
    reference: float = hamiltonian_data["fci_energy"]
    qc = ansatz.circuit

    validate_hamiltonian(op)
    validate_ansatz_compatibility(qc, op)
    
    n_params = ansatz.num_parameters
    if n_params == 0:
        raise ValueError("Ansatz has no trainable parameters.")
        
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(-np.pi, np.pi, size=n_params)
    validate_parameters(x0, n_params)

    logger.info(f"Starting VQE | Params: {n_params} | Qubits: {qc.num_qubits} | Seed: {seed}")

    eval_count = 0
    history: list[float] = []
    grad_norms: list[float] = []

    # We wrap the callback to track gradient norms periodically
    def tracked_cost(params: np.ndarray) -> float:
        nonlocal eval_count
        energy = _statevector_energy(qc, op, params)
        history.append(energy)
        eval_count += 1
        
        if eval_count % 10 == 0 or eval_count == 1:
            g_norm = gradient_norm(qc, op, params)
            grad_norms.append(g_norm)
            
        if callback:
            callback(eval_count, params, energy)
        return energy

    t0 = time.perf_counter()
    try:
        opt_result = optimizer.minimize(tracked_cost, x0)
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        raise
    wall = time.perf_counter() - t0

    error = abs(opt_result.optimal_energy - reference)
    
    # Advanced Landscape Analysis
    ruggedness = landscape_ruggedness(history)
    
    logger.info(
        f"VQE finished: E = {opt_result.optimal_energy:.6f} Ha | "
        f"Error = {error:.2e} Ha | Land. Ruggedness = {ruggedness:.4f}"
    )

    return VQEResult(
        optimal_energy=opt_result.optimal_energy,
        optimal_params=opt_result.optimal_params,
        error_vs_fci=error,
        num_function_evaluations=eval_count,
        wall_time=wall,
        converged=opt_result.converged,
        history=history,
        gradient_norms=grad_norms,
        ansatz_params=ansatz.num_parameters,
        ansatz_depth=ansatz.depth,
        two_qubit_gates=ansatz.two_qubit_gate_count,
        metadata={
            "seed": seed, 
            "optimizer": optimizer.__class__.__name__,
            "ruggedness": ruggedness,
        },
    )