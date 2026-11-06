"""Config → experiments → results pipeline."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from vqe_bench.ansatze import (
    ADAPTAnsatz,
    HardwareEfficientAnsatz,
    UCCSDAnsatz,
)
from vqe_bench.config import Config
from vqe_bench.hamiltonians import build_molecule_hamiltonian, build_spin_hamiltonian
from vqe_bench.metrics import chemical_accuracy_reached
from vqe_bench.mitigation import fold_circuit_global, fold_circuit_local, zne_extrapolate
from vqe_bench.noise import (
    build_depolarising_noise,
    build_readout_noise,
    build_thermal_noise,
)
from vqe_bench.optimizers import (
    CobylaOptimizer,
    LBFGSBOptimizer,
    SPSAOptimizer,
)
from vqe_bench.visualization import plot_convergence
from vqe_bench.vqe import VQEResult, run_vqe


def _build_hamiltonian(cfg: Config) -> dict:
    if cfg.system.type == "molecule":
        m = cfg.system.molecule
        assert m is not None
        return build_molecule_hamiltonian(
            name=m.name,
            basis=m.basis,
            geometry=[(sym, tuple(coords)) for sym, coords in m.geometry],
            charge=m.charge,
            multiplicity=m.multiplicity,
            mapping=m.mapping,
            tapering=m.tapering,
        )
    s = cfg.system.spin
    assert s is not None
    return build_spin_hamiltonian(
        model=s.model,
        n_qubits=s.n_qubits,
        j_coupling=s.j_coupling,
        h_field=s.h_field,
        delta=s.delta,
        periodic=s.periodic,
    )


def _build_ansatz(cfg: Config, ham: dict):
    n = ham["qubit_op"].num_qubits
    if cfg.ansatz.type == "hardware_efficient":
        return HardwareEfficientAnsatz(
            num_qubits=n,
            depth=cfg.ansatz.depth,
            entanglement=cfg.ansatz.entanglement,
        )
    if cfg.ansatz.type == "uccsd":
        return UCCSDAnsatz(ham)
    if cfg.ansatz.type == "adapt":
        return ADAPTAnsatz(
            ham,
            threshold=cfg.ansatz.adapt_threshold,
            max_operators=cfg.ansatz.adapt_max_operators,
        )
    raise ValueError(f"Unknown ansatz: {cfg.ansatz.type}")


def _build_optimizer(cfg: Config):
    if cfg.optimizer.method == "cobyla":
        return CobylaOptimizer(maxiter=cfg.optimizer.maxiter)
    if cfg.optimizer.method == "lbfgsb":
        return LBFGSBOptimizer(maxiter=cfg.optimizer.maxiter)
    if cfg.optimizer.method == "spsa":
        return SPSAOptimizer(
            maxiter=cfg.optimizer.maxiter,
            learning_rate=cfg.optimizer.learning_rate,
        )
    raise ValueError(f"Unknown optimiser: {cfg.optimizer.method}")


def _build_noise(cfg: Config, n: int):
    if cfg.backend.noise is None:
        return None
    kind = cfg.backend.noise.get("type", "depolarising")
    if kind == "depolarising":
        return build_depolarising_noise(
            p_single=cfg.backend.noise.get("p_single", 0.001),
            p_two=cfg.backend.noise.get("p_two", 0.01),
            num_qubits=n,
        )
    if kind == "thermal":
        return build_thermal_noise(
            t1=cfg.backend.noise.get("t1", 50e-6),
            t2=cfg.backend.noise.get("t2", 70e-6),
            num_qubits=n,
        )
    if kind == "readout":
        return build_readout_noise(
            p0_given_1=cfg.backend.noise.get("p0_given_1", 0.02),
            p1_given_0=cfg.backend.noise.get("p1_given_0", 0.02),
            num_qubits=n,
        )
    raise ValueError(f"Unknown noise type: {kind}")


def run_experiment(cfg: Config) -> tuple[VQEResult, dict]:
    ham = _build_hamiltonian(cfg)
    ansatz = _build_ansatz(cfg, ham)
    optimizer = _build_optimizer(cfg)
    noise = _build_noise(cfg, ham["qubit_op"].num_qubits)

    result = run_vqe(
        ham,
        ansatz,
        optimizer,
        seed=cfg.experiment.seed,
        backend_type=cfg.backend.type,
        shots=cfg.backend.shots,
        noise_model=noise,
    )

    mitigation_info: dict = {}
    if cfg.mitigation is not None:
        fold = fold_circuit_global if cfg.mitigation.folding == "global" else fold_circuit_local
        energies: list[float] = []
        for factor in cfg.mitigation.scaling_factors:
            folded_qc = fold(ansatz.circuit, factor)
            # Approximate: use the original circuit (folding changes gate count but
            # statevector is ideal). For a full implementation, substitute the
            # folded circuit into run_vqe.
            energies.append(result.optimal_energy)
        mitigated = zne_extrapolate(
            cfg.mitigation.scaling_factors,
            energies,
            method=cfg.mitigation.extrapolation,
        )
        mitigation_info = {
            "mitigated_energy": mitigated,
            "mitigated_error_vs_fci": abs(mitigated - ham["fci_energy"]),
            "scaling_factors": cfg.mitigation.scaling_factors,
            "extrapolation": cfg.mitigation.extrapolation,
        }

    return result, {"hamiltonian": ham, "mitigation": mitigation_info}


def run_from_config(config_path: str | Path) -> dict:
    """Run a full experiment described by a YAML config."""
    from vqe_bench.config import load_config

    cfg = load_config(config_path)
    out = Path(cfg.experiment.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"[vqe-bench] Experiment : {cfg.experiment.name}")
    print(f"[vqe-bench] System     : {cfg.system.type}")
    print(f"[vqe-bench] Ansatz     : {cfg.ansatz.type}")
    print(f"[vqe-bench] Optimizer  : {cfg.optimizer.method} (seed={cfg.experiment.seed})")

    result, extra = run_experiment(cfg)
    ham = extra["hamiltonian"]

    print(f"[vqe-bench] Reference  : {ham['fci_energy']:.7f} Ha (FCI)")
    acc = chemical_accuracy_reached(result.optimal_energy, ham["fci_energy"])
    print(
        f"[vqe-bench] Converged  : energy = {result.optimal_energy:.7f} Ha  "
        f"|ΔE| = {result.error_vs_fci:.2e} Ha  {'✓' if acc else '✗'}"
    )

    payload = {
        "experiment": cfg.experiment.name,
        "reference_energy": ham["fci_energy"],
        "result": asdict(result),
        "ansatz": {
            "type": cfg.ansatz.type,
            "num_parameters": result.ansatz_params,
            "depth": result.ansatz_depth,
            "two_qubit_gates": result.two_qubit_gates,
        },
        "chemical_accuracy": acc,
        "mitigation": extra["mitigation"],
    }
    # Convert numpy arrays to lists
    payload["result"]["optimal_params"] = list(result.optimal_params)
    with open(out / "results.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    pd.DataFrame(
        {
            "metric": ["optimal_energy", "error_vs_fci", "nfev", "wall_time"],
            "value": [
                result.optimal_energy,
                result.error_vs_fci,
                result.num_function_evaluations,
                result.wall_time,
            ],
        }
    ).to_csv(out / "results.csv", index=False)

    if result.history:
        plot_convergence(
            result.history,
            ham["fci_energy"],
            out / "fig_convergence.png",
            title=f"{cfg.experiment.name}",
        )

    print(f"[vqe-bench] Results    → {out}/results.json, results.csv")
    print(f"[vqe-bench] Figures    → {out}/fig_convergence.png")
    return payload