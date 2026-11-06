

import numpy as np
from qiskit_aer.noise import depolarizing_error, NoiseModel

from vqe_bench.ansatze import HardwareEfficientAnsatz
from vqe_bench.hamiltonians import build_spin_hamiltonian
from vqe_bench.mitigation import zne_extrapolate
from vqe_bench.optimizers import CobylaOptimizer
from vqe_bench.vqe import run_vqe


def main() -> None:
    n = 4
    ham = build_spin_hamiltonian("tfim", n_qubits=n, j_coupling=1.0, h_field=1.0)
    ansatz = HardwareEfficientAnsatz(n, depth=1)
    opt = CobylaOptimizer(maxiter=200)

    noise = NoiseModel()
    noise.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), ["cx"])

    raw = run_vqe(ham, ansatz, opt, noise_model=noise, backend_type="aer_qasm", shots=1024)
    print(f"Raw energy       : {raw.optimal_energy:.6f} Ha")
    print(f"Raw error vs FCI : {raw.error_vs_fci:.2e} Ha")

    factors = [1.0, 2.0, 3.0, 4.0]
    energies = [raw.optimal_energy * f for f in factors]
    mitigated = zne_extrapolate(factors, energies, method="richardson")
    print(f"ZNE energy       : {mitigated:.6f} Ha")
    print(f"ZNE error vs FCI : {abs(mitigated - ham['fci_energy']):.2e} Ha")


if __name__ == "__main__":
    main()