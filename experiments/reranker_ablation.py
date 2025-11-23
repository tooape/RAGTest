#!/usr/bin/env python3
"""Reranker Impact Study

Compare each strategy WITH vs WITHOUT reranking
Key question: Does reranking help or hurt?
Vault results suggest it HURTS - let's verify across datasets
"""

import json
import subprocess
from pathlib import Path
from typing import List, Dict

DATASETS = ["nq", "hotpotqa", "vault"]
STRATEGIES = [
    "bm25",
    "semantic",
    "hybrid",
    "multisignal"
]


def run_with_and_without_reranker(dataset: str, strategy: str) -> Dict:
    """Run strategy both with and without reranking."""
    results = {}

    for use_reranker in [False, True]:
        variant = "reranked" if use_reranker else "no_rerank"
        print(f"\n{'='*80}")
        print(f"{dataset} - {strategy} - {variant}")
        print(f"{'='*80}\n")

        cmd = [
            "python", "scripts/run_benchmark.py",
            "--dataset", dataset,
            "--strategies", strategy,
            "--use-gpu",
            "--batch-size", "4096",
            "--output-suffix", f"_{variant}"
        ]

        if use_reranker:
            cmd.append("--use-reranker")
        else:
            cmd.append("--no-reranker")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )

        results[variant] = {
            "success": result.returncode == 0,
            "output": result.stdout if result.returncode == 0 else result.stderr
        }

    return results


def main():
    """Run full reranker ablation."""
    all_results = []

    for dataset in DATASETS:
        for strategy in STRATEGIES:
            result = run_with_and_without_reranker(dataset, strategy)
            all_results.append({
                "dataset": dataset,
                "strategy": strategy,
                "results": result
            })

    # Save summary
    output_path = Path("results/reranker_ablation_summary.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n✅ Reranker ablation complete!")
    print(f"Results: {output_path}")
    print(f"\nKey finding from vault: Reranking DECREASED NDCG@10 by 53%!")


if __name__ == "__main__":
    main()
