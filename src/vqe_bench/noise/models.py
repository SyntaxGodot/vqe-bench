"""Configurable Aer noise models."""

from __future__ import annotations

from qiskit_aer.noise import (
    NoiseModel,
    ReadoutError,
    depolarizing_error,
    thermal_relaxation_error,
)


def build_depolarising_noise(
    p_single: float = 0.001,
    p_two: float = 0.01,
    num_qubits: int = 4,
) -> NoiseModel:
    model = NoiseModel()
    err1 = depolarizing_error(p_single, 1)
    err2 = depolarizing_error(p_two, 2)
    model.add_all_qubit_quantum_error(err1, ["u1", "u2", "u3", "rx", "ry", "rz"])
    model.add_all_qubit_quantum_error(err2, ["cx", "cz"])
    return model


def build_thermal_noise(
    t1: float = 50e-6,
    t2: float = 70e-6,
    gate_time_1q: float = 50e-9,
    gate_time_2q: float = 300e-9,
    num_qubits: int = 4,
) -> NoiseModel:
    model = NoiseModel()
    err1 = thermal_relaxation_error(t1, t2, gate_time_1q)
    err2 = thermal_relaxation_error(t1, t2, gate_time_2q).expand(
        thermal_relaxation_error(t1, t2, gate_time_2q)
    )
    model.add_all_qubit_quantum_error(err1, ["u1", "u2", "u3", "rx", "ry", "rz"])
    model.add_all_qubit_quantum_error(err2, ["cx", "cz"])
    return model


def build_readout_noise(
    p0_given_1: float = 0.02,
    p1_given_0: float = 0.02,
    num_qubits: int = 4,
) -> NoiseModel:
    model = NoiseModel()
    readout = ReadoutError([[1 - p1_given_0, p1_given_0], [p0_given_1, 1 - p0_given_1]])
    model.add_all_qubit_readout_error(readout)
    return model