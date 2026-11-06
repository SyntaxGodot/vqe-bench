
### 3. `docs/config_reference.md`
```markdown
# Configuration Reference

All experiments in `vqe-bench` are fully declarative. They are defined using YAML files and validated using `pydantic` to ensure type safety and logical consistency.

## Example Configuration

```yaml
experiment:
  name: "h2_uccsd_sto3g"
  seed: 42
  output_dir: "results/h2_uccsd"

system:
  type: molecule
  molecule:
    name: "H2"
    basis: "sto-3g"
    geometry: [["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]]
    mapping: parity
    tapering: true

ansatz:
  type: uccsd

optimizer:
  method: cobyla
  maxiter: 500
  num_restarts: 5

backend:
  type: aer_statevector