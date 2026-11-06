"""Tests for VQE metrics."""

from vqe_bench.metrics.energy import (
    absolute_error, relative_error, chemical_accuracy_reached
)

def test_absolute_error():
    assert absolute_error(-1.0, -1.1) == 0.1

def test_relative_error():
    assert relative_error(-1.0, -2.0) == 0.5

def test_chemical_accuracy():
    assert chemical_accuracy_reached(-1.0, -1.001)
    assert not chemical_accuracy_reached(-1.0, -1.002)