#!/usr/bin/env python3
"""Fusion Weight Sweep for Hybrid Strategies

Test alpha values: [0.1, 0.3, 0.5, 0.7, 0.9]
Alpha = weight for semantic vs BM25 in hybrid fusion

alpha=0.1: 10% semantic, 90% BM25
alpha=0.5: 50/50 split (default)
alpha=0.9: 90% semantic, 10% BM25
"""

import json
import subprocess
from pathlib import Path
from typing import List

DATASETS = ["nq", "vault"]
ALPHA_VALUES = [0.1, 0.3, 0.5, 0.7, 0.9]
STRATEGIES = ["weighted", "rrf"]  # Fusion strategies


def run_fusion_experiment(dataset: str, strategy: str, alpha: float):
    """Run hybrid strategy with specific alpha."""
    print(f"\n{'='*80}")
    print(f"{dataset} - {strategy} - alpha={alpha}")
    print(f"{'='*80}\n")

    cmd = [
        "python", "scripts/run_benchmark.py",
        "--dataset", dataset,
        "--strategies", strategy,
        "--use-gpu",
        "--batch-size", "4096",
        "--fusion-alpha", str(alpha),
        "--output-suffix", f"_alpha{alpha:.1f}"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    return {
        "alpha": alpha,
        "success": result.returncode == 0,
        "output": result.stdout if result.returncode == 0 else result.stderr
    }


def main():
    """Run full fusion weight sweep."""
    all_results = []

    for dataset in DATASETS:
        for strategy in STRATEGIES:
            strategy_results = []

            for alpha in ALPHA_VALUES:
                result = run_fusion_experiment(dataset, strategy, alpha)
                strategy_results.append(result)

            all_results.append({
                "dataset": dataset,
                "strategy": strategy,
                "results": strategy_results
            })

    # Save summary
    output_path = Path("results/fusion_weight_summary.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n✅ Fusion weight sweep complete!")
    print(f"Results: {output_path}")
    print(f"\nExpected finding: Vault may prefer high BM25 weight (alpha ~0.3)")


if __name__ == "__main__":
    main()
