"""Minimal end-to-end VQE on H2."""

from vqe_bench.ansatze import UCCSDAnsatz
from vqe_bench.hamiltonians import build_molecule_hamiltonian
from vqe_bench.optimizers import CobylaOptimizer
from vqe_bench.vqe import run_vqe


def main() -> None:
    h2 = build_molecule_hamiltonian(
        name="H2",
        basis="sto-3g",
        geometry=[("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, 0.735))],
        mapping="parity",
        tapering=True,
    )
    ansatz = UCCSDAnsatz(h2)
    result = run_vqe(h2, ansatz, CobylaOptimizer(maxiter=500), seed=42)
    print(f"FCI reference : {h2['fci_energy']:.8f} Ha")
    print(f"VQE energy    : {result.optimal_energy:.8f} Ha")
    print(f"|ΔE|          : {result.error_vs_fci:.2e} Ha")
    print(f"Converged     : {result.converged}")


if __name__ == "__main__":
    main()