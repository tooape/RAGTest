#!/usr/bin/env python3
"""Embedding Model Comparison

Compare multiple embedding models across all datasets:
1. mxbai-embed-large-v1 (current, 1024d)
2. bge-large-en-v1.5 (current SOTA, 1024d)
3. gte-large-en-v1.5 (Google, 1024d)
4. e5-large-v2 (Microsoft, 1024d)

Research question: Does model choice matter more than retrieval strategy?
"""

import json
import subprocess
from pathlib import Path
from typing import List, Dict

DATASETS = ["nq", "hotpotqa", "vault"]

MODELS = [
    {
        "name": "mxbai-embed-large-v1",
        "hf_name": "mixedbread-ai/mxbai-embed-large-v1",
        "dim": 1024,
        "description": "Current model (good Matryoshka support)"
    },
    {
        "name": "bge-large-en-v1.5",
        "hf_name": "BAAI/bge-large-en-v1.5",
        "dim": 1024,
        "description": "Current SOTA on MTEB"
    },
    {
        "name": "gte-large-en-v1.5",
        "hf_name": "Alibaba-NLP/gte-large-en-v1.5",
        "dim": 1024,
        "description": "Strong performance, good generalization"
    },
    {
        "name": "e5-large-v2",
        "hf_name": "intfloat/e5-large-v2",
        "dim": 1024,
        "description": "Microsoft's strong baseline"
    }
]

STRATEGIES = ["semantic", "hybrid", "multisignal"]


def run_model_experiment(dataset: str, model: Dict, strategies: List[str]):
    """Run benchmark with specific embedding model."""
    print(f"\n{'='*80}")
    print(f"Testing {dataset} with {model['name']}")
    print(f"Description: {model['description']}")
    print(f"{'='*80}\n")

    cmd = [
        "python", "scripts/run_benchmark.py",
        "--dataset", dataset,
        "--strategies", ",".join(strategies),
        "--use-gpu",
        "--batch-size", "4096",
        "--embedding-model", model["hf_name"],
        "--output-suffix", f"_{model['name']}"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    return {
        "model": model["name"],
        "success": result.returncode == 0,
        "output": result.stdout if result.returncode == 0 else result.stderr
    }


def main():
    """Run full embedding model comparison."""
    all_results = []

    for dataset in DATASETS:
        dataset_results = []

        for model in MODELS:
            result = run_model_experiment(dataset, model, STRATEGIES)
            dataset_results.append(result)

        all_results.append({
            "dataset": dataset,
            "results": dataset_results
        })

    # Save summary
    output_path = Path("results/embedding_model_summary.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n✅ Embedding model comparison complete!")
    print(f"Results: {output_path}")
    print(f"\nResearch question: Does model matter more than strategy?")


if __name__ == "__main__":
    main()
