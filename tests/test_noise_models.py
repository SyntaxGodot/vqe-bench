"""Tests for Aer noise models."""

from vqe_bench.noise.models import (
    build_depolarising_noise, build_thermal_noise, build_readout_noise
)

def test_depolarising_noise_model():
    model = build_depolarising_noise(p_single=0.01, p_two=0.02)
    assert model is not None
    assert "cx" in model.noise_instructions

def test_thermal_noise_model():
    model = build_thermal_noise()
    assert model is not None

def test_readout_noise_model():
    model = build_readout_noise()
    assert model is not None