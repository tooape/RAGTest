#!/usr/bin/env python3
"""Matryoshka Dimension Ablation Study

Compare embedding dimensions: 1024d (full) vs 768d vs 512d vs 256d
Hypothesis: 256d maintains quality with 2.8x speedup
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict

DIMENSIONS = [1024, 768, 512, 256]
DATASETS = ["nq", "vault"]
STRATEGIES = ["semantic", "hybrid", "multisignal"]  # Focus on embedding-based strategies


def run_experiment(dataset: str, dimension: int, strategies: List[str]) -> Dict:
    """Run benchmark for specific dimension."""
    print(f"\n{'='*80}")
    print(f"Testing {dataset} with {dimension}d embeddings")
    print(f"{'='*80}\n")

    # Build command
    cmd = [
        "python", "scripts/run_benchmark.py",
        "--dataset", dataset,
        "--strategies", ",".join(strategies),
        "--use-gpu",
        "--batch-size", "4096",
        "--embedding-dim", str(dimension),
        "--output-suffix", f"_dim{dimension}"
    ]

    # Run benchmark
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    if result.returncode != 0:
        print(f"ERROR running {dataset} @ {dimension}d:")
        print(result.stderr)
        return {"error": result.stderr}

    print(result.stdout)
    return {"success": True}


def main():
    """Run full Matryoshka comparison."""
    results = []

    for dataset in DATASETS:
        for dim in DIMENSIONS:
            result = run_experiment(dataset, dim, STRATEGIES)
            results.append({
                "dataset": dataset,
                "dimension": dim,
                "result": result
            })

    # Save summary
    output_path = Path("results/matryoshka_summary.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Matryoshka comparison complete!")
    print(f"Results: {output_path}")


if __name__ == "__main__":
    main()
