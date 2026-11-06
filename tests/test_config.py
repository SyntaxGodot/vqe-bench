"""Tests for Pydantic configuration validation."""

import pytest
from pydantic import ValidationError
from vqe_bench.config import (
    BackendConfig, MitigationConfig, SystemConfig, Config
)

def test_backend_requires_shots_for_qasm():
    with pytest.raises(ValidationError):
        BackendConfig(type="aer_qasm")

def test_mitigation_must_start_at_one():
    with pytest.raises(ValidationError):
        MitigationConfig(type="zne", scaling_factors=[2.0, 3.0, 5.0])

def test_mitigation_needs_at_least_two_factors():
    with pytest.raises(ValidationError):
        MitigationConfig(type="zne", scaling_factors=[1.0])

def test_system_molecule_requires_molecule_block():
    with pytest.raises(ValidationError):
        SystemConfig(type="molecule")