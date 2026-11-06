import json
from pathlib import Path
from typing import Any

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>VQE Benchmark Report</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 900px; margin: 2em auto; background: #f9f9f9; }
        .card { background: white; padding: 1.5em; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 2em; }
        h1 { color: #2c3e50; }
        .metric { display: inline-block; margin-right: 2em; }
        .metric-label { color: #7f8c8d; font-size: 0.9em; }
        .metric-value { font-size: 1.4em; font-weight: bold; color: #2980b9; }
        .success { color: #27ae60; }
        .warning { color: #e67e22; }
        img { max-width: 100%; border-radius: 4px; margin-top: 1em; }
    </style>
</head>
<body>
    <h1>VQE Benchmark Report: {experiment_name}</h1>
    
    <div class="card">
        <h2>Results Summary</h2>
        <div class="metric">
            <div class="metric-label">VQE Energy (Ha)</div>
            <div class="metric-value">{vqe_energy:.6f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">FCI Reference (Ha)</div>
            <div class="metric-value">{fci_energy:.6f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Error</div>
            <div class="metric-value {status_class}">{error:.2e}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Chemical Accuracy</div>
            <div class="metric-value {status_class}">{chem_acc}</div>
        </div>
    </div>

    <div class="card">
        <h2>Resource Telemetry</h2>
        <p>Wall Time: <strong>{wall_time}s</strong> | CPU Time: <strong>{cpu_time}s</strong> | Peak RAM: <strong>{peak_mem} MB</strong></p>
    </div>

    <div class="card">
        <h2>Optimization Telemetry</h2>
        <p>Function Evaluations: <strong>{nfev}</strong> | Ansatz Depth: <strong>{depth}</strong> | 2Q Gates: <strong>{two_q}</strong></p>
        <p>Landscape Ruggedness: <strong>{ruggedness:.4f}</strong></p>
    </div>

    {plot_section}
</body>
</html>
"""

def generate_html_report(results_json_path: str | Path, output_html_path: str | Path) -> None:
    with open(results_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    res = data["result"]
    meta = res["metadata"]
    telemetry = meta.get("telemetry", {})
    
    error = res["error_vs_fci"]
    is_acc = error <= 1.6e-3
    
    plot_section = ""
    png_path = Path(results_json_path).parent / "fig_convergence.png"
    if png_path.exists():
        plot_section = f'<div class="card"><h2>Convergence Plot</h2><img src="fig_convergence.png" alt="Convergence"></div>'

    html = HTML_TEMPLATE.format(
        experiment_name=data["experiment"],
        vqe_energy=res["optimal_energy"],
        fci_energy=data["reference_energy"],
        error=error,
        status_class="success" if is_acc else "warning",
        chem_acc="✓ Yes" if is_acc else "✗ No",
        wall_time=telemetry.get("wall_time_sec", 0),
        cpu_time=telemetry.get("cpu_time_sec", 0),
        peak_mem=telemetry.get("peak_memory_mb", 0),
        nfev=res["num_function_evaluations"],
        depth=res["ansatz_depth"],
        two_q=res["two_qubit_gates"],
        ruggedness=meta.get("ruggedness", 0.0),
        plot_section=plot_section,
    )

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)