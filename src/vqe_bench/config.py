"""Pydantic configuration schema and YAML loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, model_validator


class ExperimentConfig(BaseModel):
    name: str
    seed: int = 42
    output_dir: str = "results"


class MoleculeConfig(BaseModel):
    name: str
    basis: str = "sto-3g"
    geometry: list[tuple[str, tuple[float, float, float]]]
    charge: int = 0
    multiplicity: int = 1
    mapping: Literal["jordan_wigner", "parity"] = "jordan_wigner"
    tapering: bool = False


class SpinConfig(BaseModel):
    model: Literal["tfim", "heisenberg_xxz"]
    n_qubits: int
    j_coupling: float = 1.0
    h_field: float = 1.0
    delta: float = 1.0
    periodic: bool = True


class SystemConfig(BaseModel):
    type: Literal["molecule", "spin"]
    molecule: MoleculeConfig | None = None
    spin: SpinConfig | None = None

    @model_validator(mode="after")
    def _check(self) -> SystemConfig:
        if self.type == "molecule" and self.molecule is None:
            raise ValueError("system.type=molecule requires 'molecule' block")
        if self.type == "spin" and self.spin is None:
            raise ValueError("system.type=spin requires 'spin' block")
        return self


class AnsatzConfig(BaseModel):
    type: Literal["hardware_efficient", "uccsd", "adapt"]
    depth: int = 1
    entanglement: Literal["linear", "circular", "full", "sca"] = "linear"
    adapt_threshold: float = 1e-3
    adapt_max_operators: int = 20


class OptimizerConfig(BaseModel):
    method: Literal["cobyla", "spsa", "lbfgsb"] = "cobyla"
    maxiter: int = 500
    num_restarts: int = 1
    learning_rate: float = 0.1


class BackendConfig(BaseModel):
    type: Literal["aer_statevector", "aer_qasm"] = "aer_statevector"
    noise: dict[str, Any] | None = None
    shots: int | None = None

    @model_validator(mode="after")
    def _check_shots(self) -> BackendConfig:
        if self.type == "aer_qasm" and self.shots is None:
            raise ValueError("backend.shots is required for aer_qasm")
        return self


class MitigationConfig(BaseModel):
    type: Literal["zne"]
    scaling_factors: list[float] = Field(default=[1.0, 3.0, 5.0])
    folding: Literal["global", "local"] = "global"
    extrapolation: Literal["linear", "richardson", "exponential"] = "richardson"

    @model_validator(mode="after")
    def _check_factors(self) -> MitigationConfig:
        if self.scaling_factors[0] != 1.0:
            raise ValueError("mitigation.scaling_factors must start at 1.0")
        if len(self.scaling_factors) < 2:
            raise ValueError("mitigation.scaling_factors must have >= 2 entries")
        return self


class Config(BaseModel):
    experiment: ExperimentConfig
    system: SystemConfig
    ansatz: AnsatzConfig
    optimizer: OptimizerConfig
    backend: BackendConfig = BackendConfig()
    mitigation: MitigationConfig | None = None


def load_config(path: str | Path) -> Config:
    """Load and validate a YAML experiment configuration."""
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config.model_validate(raw)