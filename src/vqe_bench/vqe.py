"""VQE driver loop."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import SparsePauliOp, Statevector

try:
    from qiskit_aer import AerSimulator
    from qiskit_aer.primitives import Estimator as AerEstimator
    _HAS_AER = True
except Exception:
    _HAS_AER = False

from vqe_bench.ansatze.base import BaseAnsatz
from vqe_bench.optimizers.base import BaseOptimizer


@dataclass
class VQEResult:
    optimal_energy: float
    optimal_params: np.ndarray
    error_vs_fci: float
    num_function_evaluations: int
    wall_time: float
    converged: bool
    history: list[float] = field(default_factory=list)
    ansatz_params: int = 0
    ansatz_depth: int = 0
    two_qubit_gates: int = 0


def _statevector_energy(qc: QuantumCircuit, op: SparsePauliOp, params: np.ndarray) -> float:
    bound = qc.assign_parameters(dict(zip(qc.parameters, params, strict=True)))
    sv = Statevector.from_instruction(bound)
    return float(np.real(sv.expectation_value(op)))


def run_vqe(
    hamiltonian_data: dict,
    ansatz: BaseAnsatz,
    optimizer: BaseOptimizer,
    seed: int = 42,
    backend_type: str = "aer_statevector",
    shots: int | None = None,
    noise_model=None,
) -> VQEResult:
    """Run VQE and return a structured result."""
    op: SparsePauliOp = hamiltonian_data["qubit_op"]
    reference: float = hamiltonian_data["fci_energy"]
    qc = ansatz.circuit

    rng = np.random.default_rng(seed)
    n_params = ansatz.num_parameters
    x0 = rng.uniform(-np.pi, np.pi, size=n_params)

    if backend_type == "aer_qasm" and _HAS_AER and shots is not None:
        simulator = AerSimulator(noise_model=noise_model)
        estimator = AerEstimator(
            backend_options={"method": "statevector", "noise_model": noise_model},
            run_options={"shots": shots},
        )

        def cost_fn(params: np.ndarray) -> float:
            bound = qc.assign_parameters(dict(zip(qc.parameters, params, strict=True)))
            bound = transpile(bound, simulator, optimization_level=0)
            try:
                result = estimator.run([(bound, op)]).result()
                return float(result[0].data.evs)
            except Exception:
                return _statevector_energy(qc, op, params)

    else:

        def cost_fn(params: np.ndarray) -> float:
            return _statevector_energy(qc, op, params)

    t0 = time.perf_counter()
    opt_result = optimizer.minimize(cost_fn, x0)
    wall = time.perf_counter() - t0

    return VQEResult(
        optimal_energy=opt_result.optimal_energy,
        optimal_params=opt_result.optimal_params,
        error_vs_fci=abs(opt_result.optimal_energy - reference),
        num_function_evaluations=opt_result.num_function_evaluations,
        wall_time=wall,
        converged=opt_result.converged,
        history=opt_result.history,
        ansatz_params=ansatz.num_parameters,
        ansatz_depth=ansatz.depth,
        two_qubit_gates=ansatz.two_qubit_gate_count,
    )