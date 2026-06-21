import time
from typing import Dict, Any

class LatencyTracker:
    """Timer wrapper to track component-wise execution latency."""
    def __init__(self) -> None:
        self.starts = {}
        self.latencies = {}

    def start(self, component: str) -> None:
        """Start recording time for a component."""
        self.starts[component] = time.perf_counter()

    def stop(self, component: str) -> float:
        """Stop recording and save the elapsed duration in seconds."""
        if component not in self.starts:
            raise ValueError(f"Timer for '{component}' was never started.")
        elapsed = time.perf_counter() - self.starts[component]
        self.latencies[component] = self.latencies.get(component, 0.0) + elapsed
        del self.starts[component]
        return elapsed

    def get_latencies(self) -> Dict[str, float]:
        """Return component-wise accumulated times."""
        return self.latencies
