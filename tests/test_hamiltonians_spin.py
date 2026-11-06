"""Tests for spin model Hamiltonians."""

import pytest
import numpy as np
from vqe_bench.hamiltonians.spins import build_spin_hamiltonian, exact_ground_state

def test_tfim_ground_state_analytical():
    # For n=2, J=1, h=1, H = -Z0Z1 - X0 - X1. Ground energy = -2.0
    ham = build_spin_hamiltonian("tfim", n_qubits=2, j_coupling=1.0, h_field=1.0)
    assert np.isclose(ham["fci_energy"], -2.0, atol=1e-6)

def test_heisenberg_xxz_builds():
    ham = build_spin_hamiltonian("heisenberg_xxz", n_qubits=4)
    assert ham["qubit_op"].num_qubits == 4
    assert isinstance(ham["fci_energy"], float)