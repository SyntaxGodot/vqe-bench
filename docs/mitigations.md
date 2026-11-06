
### 4. `docs/mitigations.md`
```markdown
# Error Mitigation

Near-term quantum computers are subject to significant noise. `vqe-bench` provides built-in support for **Zero-Noise Extrapolation (ZNE)**.

## Zero-Noise Extrapolation (ZNE)
ZNE works by running the same quantum circuit at different "noise levels" and extrapolating the expected value back to the zero-noise limit.

### 1. Unitary Folding
We artificially increase the noise by replacing gates with sequences that do the same thing but take longer. 
- **Global Folding:** Folds the entire circuit ($U \to U U^\dagger U$).
- **Local Folding:** Folds individual gates.

### 2. Extrapolation Methods
`vqe-bench` supports three extrapolation techniques to fit the data points:
1. **Linear:** Fits a straight line.
2. **Richardson:** Fits a polynomial of degree $n-1$.
3. **Exponential:** Fits $y = a + b \cdot e^{cx}$.

## Configuration

To enable ZNE, update your YAML config:

```yaml
mitigation:
  type: zne
  scaling_factors: [1.0, 3.0, 5.0]  # Must start at 1.0
  folding: global
  extrapolation: richardson