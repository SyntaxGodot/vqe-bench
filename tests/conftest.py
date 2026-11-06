"""Shared pytest fixtures."""

import pytest
import numpy as np
from qiskit.quantum_info import SparsePauliOp

@pytest.fixture
def simple_hamiltonian():
    """A simple 2-qubit Hamiltonian for testing (e.g., H2 minimal basis)."""
    return {
        "qubit_op": SparsePauliOp.from_list([
            ("II", -1.0523732),
            ("IZ", 0.39793742),
            ("ZI", -0.39793742),
            ("ZZ", -0.0112801),
            ("XX", 0.18093119)
        ]),
        "num_particles": (1, 1),
        "num_spatial": 2,
        "fci_energy": -1.8517,
        "name": "Test_H2"
    }

@pytest.fixture
def random_params():
    """Generate deterministic random parameters for ansatz testing."""
    rng = np.random.default_rng(42)
    return rng.uniform(-np.pi, np.pi, size=10)