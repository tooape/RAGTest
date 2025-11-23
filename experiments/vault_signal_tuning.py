#!/usr/bin/env python3
"""Vault-Specific Graph & Temporal Signal Tuning

Test boost multipliers for PageRank and temporal signals:
boost = [0.0, 0.1, 0.2, 0.5, 1.0]

Only applicable to vault dataset (has graph + temporal metadata)

Research questions:
1. How much do graph signals help?
2. How much do temporal signals help?
3. What's the optimal combination?
"""

import json
import subprocess
from pathlib import Path
from typing import List, Tuple

BOOST_VALUES = [0.0, 0.1, 0.2, 0.5, 1.0]
STRATEGIES = ["multisignal"]  # Only multisignal uses boost parameters


def run_boost_experiment(
    graph_boost: float,
    temporal_boost: float
):
    """Run multisignal with specific boost values."""
    print(f"\n{'='*80}")
    print(f"vault - graph_boost={graph_boost}, temporal_boost={temporal_boost}")
    print(f"{'='*80}\n")

    cmd = [
        "python", "scripts/run_benchmark.py",
        "--dataset", "vault",
        "--strategies", "multisignal",
        "--use-gpu",
        "--batch-size", "4096",
        "--graph-boost", str(graph_boost),
        "--temporal-boost", str(temporal_boost),
        "--output-suffix", f"_g{graph_boost:.1f}_t{temporal_boost:.1f}"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    return {
        "graph_boost": graph_boost,
        "temporal_boost": temporal_boost,
        "success": result.returncode == 0,
        "output": result.stdout if result.returncode == 0 else result.stderr
    }


def main():
    """Run full vault signal tuning study."""
    all_results = []

    # Test each signal independently first
    print("\n" + "="*80)
    print("PHASE 1: Independent Signal Testing")
    print("="*80)

    # Baseline: No boosts
    all_results.append(run_boost_experiment(0.0, 0.0))

    # Graph boost only
    for graph_boost in BOOST_VALUES[1:]:
        all_results.append(run_boost_experiment(graph_boost, 0.0))

    # Temporal boost only
    for temporal_boost in BOOST_VALUES[1:]:
        all_results.append(run_boost_experiment(0.0, temporal_boost))

    # Phase 2: Combined (grid search on top performers)
    print("\n" + "="*80)
    print("PHASE 2: Combined Signal Testing (grid search)")
    print("="*80)

    for graph_boost in [0.1, 0.2, 0.5]:
        for temporal_boost in [0.1, 0.2, 0.5]:
            all_results.append(run_boost_experiment(graph_boost, temporal_boost))

    # Save summary
    output_path = Path("results/vault_signal_tuning_summary.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n✅ Vault signal tuning complete!")
    print(f"Results: {output_path}")
    print(f"\nNote: Vault results show BM25 is hard to beat!")
    print(f"Graph/temporal boosts may not help much given BM25's dominance")


if __name__ == "__main__":
    main()
