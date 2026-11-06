"""Tests for molecular Hamiltonian builders."""

import pytest
from vqe_bench.hamiltonians.molecules import build_molecule_hamiltonian

@pytest.mark.skipif(
    not pytest.importorskip("qiskit_nature", reason="qiskit-nature not installed"),
    reason="Requires chemistry extras"
)
def test_h2_hamiltonian_builds():
    ham = build_molecule_hamiltonian(
        name="H2",
        basis="sto-3g",
        geometry=[("H", (0, 0, 0)), ("H", (0, 0, 0.735))],
        mapping="jordan_wigner"
    )
    assert "qubit_op" in ham
    assert ham["fci_energy"] < 0