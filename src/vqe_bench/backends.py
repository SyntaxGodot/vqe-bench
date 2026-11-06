"""Backend setup for Qiskit Aer."""

from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Estimator as AerEstimator

def get_backend(backend_type: str, noise_model=None):
    """Return an AerSimulator backend."""
    if backend_type == "aer_qasm":
        return AerSimulator(noise_model=noise_model)
    return AerSimulator(method="statevector", noise_model=noise_model)

def get_estimator(backend_type: str, shots: int | None = None, noise_model=None):
    """Return an Aer Estimator primitive."""
    options = {"method": "statevector"}
    if noise_model:
        options["noise_model"] = noise_model
        
    run_options = {}
    if shots is not None:
        run_options["shots"] = shots

    return AerEstimator(backend_options=options, run_options=run_options)