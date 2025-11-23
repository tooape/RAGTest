#!/usr/bin/env python3
"""Top-K Retrieval Depth Study

Test how many candidates to retrieve before reranking/evaluation:
k = [10, 20, 50, 100, 200]

Key question: Does retrieving more candidates improve final top-10 quality?
Trade-off: More candidates = better recall but slower + more noise
"""

import json
import subprocess
from pathlib import Path
from typing import List

DATASETS = ["nq", "vault"]
TOPK_VALUES = [10, 20, 50, 100, 200]
STRATEGIES = ["semantic", "hybrid", "multisignal"]


def run_topk_experiment(dataset: str, strategy: str, k: int):
    """Run strategy with specific top-k retrieval depth."""
    print(f"\n{'='*80}")
    print(f"{dataset} - {strategy} - top-k={k}")
    print(f"{'='*80}\n")

    cmd = [
        "python", "scripts/run_benchmark.py",
        "--dataset", dataset,
        "--strategies", strategy,
        "--use-gpu",
        "--batch-size", "4096",
        "--top-k", str(k),
        "--output-suffix", f"_topk{k}"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    return {
        "k": k,
        "success": result.returncode == 0,
        "output": result.stdout if result.returncode == 0 else result.stderr
    }


def main():
    """Run full top-k depth study."""
    all_results = []

    for dataset in DATASETS:
        for strategy in STRATEGIES:
            strategy_results = []

            for k in TOPK_VALUES:
                result = run_topk_experiment(dataset, strategy, k)
                strategy_results.append(result)

            all_results.append({
                "dataset": dataset,
                "strategy": strategy,
                "results": strategy_results
            })

    # Save summary
    output_path = Path("results/topk_depth_summary.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n✅ Top-K depth study complete!")
    print(f"Results: {output_path}")
    print(f"\nExpected: k=50-100 optimal balance (recall vs noise)")


if __name__ == "__main__":
    main()
