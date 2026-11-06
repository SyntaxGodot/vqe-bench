# vqe-bench Documentation

Welcome to the documentation for **vqe-bench** — a reproducible, publication-quality framework for comparing Variational Quantum Eigensolver (VQE) ansätze, optimisers, and error-mitigation strategies.

## Table of Contents
- [Ansätze](ansatze.md)
- [Configuration Reference](config_reference.md)
- [Error Mitigation](mitigations.md)

## Overview
`vqe-bench` is designed to answer practical questions that VQE practitioners face daily:
1. **Which ansatz is best?** (Hardware-efficient vs. UCCSD vs. ADAPT-VQE)
2. **Which classical optimiser converges fastest?** (COBYLA / SPSA / L-BFGS-B)
3. **Do barren plateaus kill my ansatz at this scale?**
4. **How much does zero-noise extrapolation help under realistic noise?**

## Quick Start
To run a benchmark, use the command-line interface:
```bash
vqe-bench run --config configs/h2_uccsd.yaml