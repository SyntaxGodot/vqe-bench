"""Molecular Hamiltonians via PySCF + Qiskit Nature."""

from __future__ import annotations

from typing import Any

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer


def build_molecule_hamiltonian(
    name: str,
    basis: str,
    geometry: list[tuple[str, tuple[float, float, float]]],
    charge: int = 0,
    multiplicity: int = 1,
    mapping: str = "jordan_wigner",
    tapering: bool = False,
) -> dict[str, Any]:
    """Build a qubit Hamiltonian for a small molecule.

    Returns a dict with keys: ``qubit_op``, ``num_particles``, ``num_spatial``,
    ``fci_energy``, ``mapper``.
    """
    geom_str = "; ".join(
        f"{sym} {x} {y} {z}" for sym, (x, y, z) in geometry
    )
    driver = PySCFDriver(
        atom=geom_str,
        basis=basis,
        charge=charge,
        multiplicity=multiplicity,
    )
    problem = driver.run()
    fci_energy = problem.reference_energy  # FCI in active space

    mapper_cls = ParityMapper if mapping == "parity" else JordanWignerMapper
    mapper = mapper_cls(num_particles=problem.num_particles) if mapping == "parity" else mapper_cls()

    if tapering and mapping == "parity":
        from qiskit_nature.second_q.transformers import FreezeCoreTransformer

        transformer = FreezeCoreTransformer()
        problem = transformer.transform(problem)

    qubit_op = mapper.map(problem.second_q_ops()[0])

    if tapering and mapping == "parity":
        from qiskit_nature.second_q.mappers import QubitConverter

        converter = QubitConverter(mapper=mapper, two_qubit_reduction=True, z2symmetry_reduction="auto")
        qubit_op = converter.convert(problem.second_q_ops()[0])

    return {
        "qubit_op": qubit_op,
        "num_particles": problem.num_particles,
        "num_spatial": problem.num_spatial_orbitals,
        "fci_energy": fci_energy,
        "mapper": mapper,
        "name": name,
    }