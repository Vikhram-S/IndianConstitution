"""CPU performance benchmark suite for IndianConstitution engine.

Measures p50, p95, p99 latencies and throughput (QPS) for core operations:
- Article Lookup
- Keyword Inverted-Index Search
- Fuzzy String Similarity Search
- Graph Construction & Traversal
- Amendment Diff Computation

Runs deterministically on local CPU with 0 cloud dependencies or API calls.
"""

import sys
import time
from typing import Callable, List

import numpy as np

from indianconstitution import Constitution, get_constitution

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass


def benchmark_op(name: str, fn: Callable[[], None], iterations: int = 1000) -> None:
    """Benchmark a function over N iterations and report latency distribution."""
    # Warmup
    for _ in range(min(50, iterations)):
        fn()

    latencies_ms: List[float] = []
    start_all = time.perf_counter()

    for _ in range(iterations):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)

    total_time_sec = time.perf_counter() - start_all
    qps = iterations / total_time_sec if total_time_sec > 0 else 0.0

    p50 = float(np.percentile(latencies_ms, 50))
    p95 = float(np.percentile(latencies_ms, 95))
    p99 = float(np.percentile(latencies_ms, 99))
    mean = float(np.mean(latencies_ms))

    print(f"| {name:<32} | {iterations:5d} | {p50:8.4f} ms | {p95:8.4f} ms | {p99:8.4f} ms | {mean:8.4f} ms | {qps:8.1f} |")


def run_benchmarks() -> None:
    """Run CPU benchmark suite."""
    print("=" * 105)
    print("INDIAN CONSTITUTION ENGINE CPU PERFORMANCE BENCHMARK (EMPIRICAL)")
    print("=" * 105)
    print(f"| {'Operation Name':<32} | {'Iters':<5} | {'p50 (ms)':<10} | {'p95 (ms)':<10} | {'p99 (ms)':<10} | {'Mean (ms)':<10} | {'QPS':<8} |")
    print("|" + "-" * 34 + "|" + "-" * 7 + "|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 10 + "|")

    ic = get_constitution()

    # 1. Article Lookup
    benchmark_op("Article Lookup (by num)", lambda: ic.get_article("14"), iterations=2000)

    # 2. Keyword Inverted Index Search
    benchmark_op("Keyword Search ('equality')", lambda: ic.search("equality", limit=10), iterations=1000)

    # 3. Fuzzy Search
    benchmark_op("Fuzzy Search ('liberty')", lambda: ic.fuzzy_search("liberty", limit=5), iterations=500)

    # 4. Graph Lookup
    benchmark_op("Graph Related Lookup", lambda: ic.get_related_articles("32"), iterations=1000)

    # 5. Diff Computation
    benchmark_op("Amendment Diff (Art 21A)", lambda: ic.diff_amendment("21A", 1950, 2026), iterations=1000)

    # 6. Graph Reconstruction
    benchmark_op("Graph Reconstruction", lambda: Constitution(ic._data_path).get_graph(), iterations=100)

    print("=" * 105)


if __name__ == "__main__":
    run_benchmarks()
