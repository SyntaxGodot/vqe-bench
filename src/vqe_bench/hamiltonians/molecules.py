"""Robust molecular Hamiltonian builders."""

from __future__ import annotations
import functools
from typing import Any

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper

from vqe_bench.utils.logger import setup_logger

logger = setup_logger("Molecules")


@functools.lru_cache(maxsize=32)
def build_molecule_hamiltonian(
    name: str,
    basis: str,
    geometry: tuple[tuple[str, tuple[float, float, float]], ...],
    charge: int = 0,
    multiplicity: int = 1,
    mapping: str = "jordan_wigner",
    tapering: bool = False,
) -> dict[str, Any]:
    """Build a qubit Hamiltonian with caching and error handling."""
    geom_str = "; ".join(
        f"{sym} {x} {y} {z}" for sym, (x, y, z) in geometry
    )
    
    try:
        driver = PySCFDriver(
            atom=geom_str,
            basis=basis,
            charge=charge,
            multiplicity=multiplicity,
        )
        problem = driver.run()
        fci_energy = problem.reference_energy
    except Exception as e:
        logger.error(f"PySCF failed for {name}: {e}")
        raise RuntimeError(f"Molecular Hamiltonian build failed for {name}") from e

    mapper = ParityMapper(num_particles=problem.num_particles) if mapping == "parity" else JordanWignerMapper()
    qubit_op = mapper.map(problem.second_q_ops()[0])

    if tapering and mapping == "parity":
        from qiskit_nature.second_q.mappers import QubitConverter
        converter = QubitConverter(mapper=mapper, two_qubit_reduction=True, z2symmetry_reduction="auto")
        qubit_op = converter.convert(problem.second_q_ops()[0])

    logger.info(f"Built {name} | Qubits: {qubit_op.num_qubits} | FCI: {fci_energy:.6f} Ha")
    
    return {
        "qubit_op": qubit_op,
        "num_particles": problem.num_particles,
        "num_spatial": problem.num_spatial_orbitals,
        "fci_energy": fci_energy,
        "mapper": mapper,
        "name": name,
    }