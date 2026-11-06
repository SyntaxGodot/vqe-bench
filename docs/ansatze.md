
### 2. `docs/ansatze.md`
```markdown
# Ansätze

`vqe-bench` provides three distinct quantum circuit architectures (ansätze) to prepare the trial wavefunctions.

## Hardware-Efficient Ansatz
The hardware-efficient ansatz is designed to minimize circuit depth and respect the topology of near-term quantum devices. It alternates layers of parameterized single-qubit rotations (e.g., $R_y$) with layers of entangling two-qubit gates (e.g., `CX`).

**Configuration Options:**
- `depth`: The number of repeated layers.
- `entanglement`: The pattern of entangling gates (`linear`, `circular`, `full`, `sca`).

```python
from vqe_bench.ansatze.hardware_efficient import HardwareEfficientAnsatz

ansatz = HardwareEfficientAnsatz(num_qubits=4, depth=2, entanglement="linear")