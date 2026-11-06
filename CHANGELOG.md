# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Qiskit 2.x support
- Clifford Data Regression (CDR) mitigation
- ADAPT-VQE with qubit-excitation pool

## [0.2.0] - 2024-05-20

### Added
- **Telemetry tracking** (`vqe_bench.utils.telemetry`) — CPU time, wall time, and peak memory for every VQE run.
- **Disk-based Hamiltonian caching** (`vqe_bench.utils.caching`) — speeds up repeated bond-length scans.
- **Automated HTML reports** (`vqe_bench.reporting`) — stakeholder-ready dashboards.
- **Advanced quantum metrics** (`vqe_bench.metrics.quantum`) — gradient norm and landscape ruggedness tracking.
- **Validation utilities** (`vqe_bench.utils.validation`) — prevents shape mismatches at runtime.
- **Structured logging** (`vqe_bench.utils.logger`).
- `CONTRIBUTORS.md`, `Makefile`, `.pre-commit-config.yaml`, `CHANGELOG.md`.

### Changed
- `run_vqe()` now returns a `VQEResult` with `metadata["telemetry"]` populated.
- `pyproject.toml` now depends on `psutil` and `diskcache`.
- README updated with enterprise feature overview.

### Fixed
- Broken GitHub links in README (`ZitouniNidhal` → `SyntaxGodot`).
- Molecule builder now caches results with `lru_cache`.

## [0.1.0] - 2024-04-01

### Added
- Initial release: VQE driver, 3 ansätze, 3 optimizers, ZNE mitigation.
- H₂ / LiH / BeH₂ molecular Hamiltonians (via PySCF).
- TFIM / Heisenberg XXZ spin models.
- Comprehensive pytest suite.