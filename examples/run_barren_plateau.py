"""Gradient variance vs. qubit count (global cost function)."""

import numpy as np
from vqe_bench.ansatze import HardwareEfficientAnsatz
from vqe_bench.diagnostics import gradient_variance
from vqe_bench.hamiltonians import build_spin_hamiltonian
from vqe_bench.visualization import plot_gradient_variance


def main() -> None:
    qubit_counts = [2, 3, 4, 5, 6]
    variances: list[float] = []
    
    for n in qubit_counts:
        ham = build_spin_hamiltonian("tfim", n_qubits=n, j_coupling=1.0, h_field=1.0)
        op = ham["qubit_op"]

        def builder(num_qubits: int, depth: int):
            return HardwareEfficientAnsatz(num_qubits, depth=depth, entanglement="linear").circuit

        var = gradient_variance(builder, op, n, depth=1, num_samples=30, seed=0)
        variances.append(var)
        print(f"n={n}  Var[grad] = {var:.3e}")

    plot_gradient_variance(qubit_counts, variances, "barren_plateau.png")
    coeffs = np.polyfit(qubit_counts, np.log(variances), 1)
    print(f"Decay rate b ≈ {np.exp(-coeffs[0]):.2f}")


if __name__ == "__main__":
    main()