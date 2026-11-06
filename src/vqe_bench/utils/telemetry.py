"""Hardware and resource telemetry for VQE experiments."""

import time
import psutil
import os
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Any

@dataclass
class TelemetryRecord:
    wall_time_sec: float
    cpu_time_sec: float
    peak_memory_mb: float
    cpu_percent: float

def track_resources(func: Callable) -> Callable:
    """Decorator to track resource usage of any function."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / (1024 * 1024)
        cpu_before = process.cpu_times()
        t0 = time.perf_counter()

        result = func(*args, **kwargs)

        t1 = time.perf_counter()
        cpu_after = process.cpu_times()
        mem_after = process.memory_info().rss / (1024 * 1024)

        # Attach telemetry to the result if it's a dataclass
        if hasattr(result, "metadata"):
            if "telemetry" not in result.metadata:
                result.metadata["telemetry"] = {}
            result.metadata["telemetry"].update({
                "wall_time_sec": round(t1 - t0, 3),
                "cpu_time_sec": round(
                    (cpu_after.user - cpu_before.user) + (cpu_after.system - cpu_before.system), 3
                ),
                "peak_memory_mb": round(max(mem_before, mem_after), 2),
            })
        return result
    return wrapper