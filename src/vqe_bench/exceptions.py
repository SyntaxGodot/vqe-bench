"""Custom exceptions for vqe-bench."""

class VQEBenchError(Exception):
    """Base exception for all vqe-bench errors."""
    pass

class AnsatzError(VQEBenchError):
    """Raised when there is an issue with the ansatz."""
    pass

class HamiltonianError(VQEBenchError):
    """Raised when there is an issue building the Hamiltonian."""
    pass