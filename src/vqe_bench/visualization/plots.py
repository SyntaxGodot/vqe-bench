"""Matplotlib figures for benchmark results."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def plot_convergence(
    history: list[float],
    reference: float,
    output_path: str | Path,
    title: str = "VQE convergence",
) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
    ax.plot(np.arange(len(history)), np.array(history) - reference, lw=1.5)
    ax.axhline(0.0, color="grey", ls="--", lw=0.8)
    ax.axhline(1.6e-3, color="red", ls=":", lw=0.8, label="chem. accuracy")
    ax.set_xlabel("Function evaluation")
    ax.set_ylabel("Energy error (Ha)")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_energy_vs_depth(
    depths: list[int],
    energies: list[float],
    reference: float,
    output_path: str | Path,
) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    ax.plot(depths, np.abs(np.array(energies) - reference), "o-")
    ax.set_xlabel("Circuit depth")
    ax.set_ylabel("|E - E_FCI| (Ha)")
    ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_gradient_variance(
    qubit_counts: list[int],
    variances: list[float],
    output_path: str | Path,
    title: str = "Gradient variance",
) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    ax.plot(qubit_counts, variances, "s-", label="measured")
    if len(qubit_counts) >= 2:
        coeffs = np.polyfit(qubit_counts, np.log(variances), 1)
        fit = np.exp(np.polyval(coeffs, np.array(qubit_counts)))
        ax.plot(qubit_counts, fit, "--", label=f"exp fit (b={np.exp(-coeffs[0]):.2f})")
    ax.set_xlabel("Number of qubits")
    ax.set_ylabel("Var[∂C/∂θ]")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)