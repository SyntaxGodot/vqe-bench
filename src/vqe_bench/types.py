"""Shared type definitions."""

from typing import Any, Callable, Dict, List, Tuple
import numpy as np
from qiskit.quantum_info import SparsePauliOp

# A cost function takes a numpy array of parameters and returns a float
CostFunction = Callable[[np.ndarray], float]

# Dictionary structure returned by Hamiltonian builders
HamiltonianData = Dict[str, Any]

# Result of an optimization run
OptimizationResult = Dict[str, Any]