"""Results tracking and persistence."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from loguru import logger


class ResultsTracker:
    """Track and save benchmark results."""

    def __init__(self, output_dir: str = "results"):
        """Initialize results tracker.

        Args:
            output_dir: Directory to save results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.results = []
        self.run_metadata = {
            "start_time": datetime.now().isoformat(),
            "runs": [],
        }

    def add_result(
        self,
        strategy_name: str,
        dataset_name: str,
        params: Dict[str, Any],
        metrics: Dict[str, float],
        metadata: Dict = None,
    ):
        """Add a single benchmark result.

        Args:
            strategy_name: Name of retrieval strategy
            dataset_name: Name of dataset
            params: Hyperparameters used
            metrics: Performance metrics
            metadata: Additional metadata (latency, etc.)
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy_name,
            "dataset": dataset_name,
            "params": params,
            "metrics": metrics,
            "metadata": metadata or {},
        }

        self.results.append(result)
        logger.debug(f"Added result: {strategy_name} on {dataset_name}")

    def save_json(self, filename: str = None):
        """Save results to JSON.

        Args:
            filename: Output filename (auto-generated if None)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"

        filepath = self.output_dir / filename

        output = {
            "metadata": self.run_metadata,
            "results": self.results,
        }

        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)

        logger.info(f"Saved results to {filepath}")
        return filepath

    def save_csv(self, filename: str = None):
        """Save results to CSV (flattened format).

        Args:
            filename: Output filename (auto-generated if None)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.csv"

        filepath = self.output_dir / filename

        # Flatten results for CSV
        flattened = []
        for result in self.results:
            row = {
                "timestamp": result["timestamp"],
                "strategy": result["strategy"],
                "dataset": result["dataset"],
            }

            # Add params with 'param_' prefix
            for k, v in result["params"].items():
                row[f"param_{k}"] = v

            # Add metrics with 'metric_' prefix
            for k, v in result["metrics"].items():
                row[f"metric_{k}"] = v

            # Add metadata
            for k, v in result["metadata"].items():
                row[f"meta_{k}"] = v

            flattened.append(row)

        df = pd.DataFrame(flattened)
        df.to_csv(filepath, index=False)

        logger.info(f"Saved CSV to {filepath}")
        return filepath

    def get_best_by_metric(
        self,
        metric: str,
        dataset: str = None,
        strategy: str = None,
    ) -> Dict:
        """Get best result by metric.

        Args:
            metric: Metric name (e.g., 'ndcg@10')
            dataset: Optional dataset filter
            strategy: Optional strategy filter

        Returns:
            Best result dict
        """
        filtered = self.results

        if dataset:
            filtered = [r for r in filtered if r["dataset"] == dataset]
        if strategy:
            filtered = [r for r in filtered if r["strategy"] == strategy]

        if not filtered:
            return None

        best = max(filtered, key=lambda x: x["metrics"].get(metric, float("-inf")))
        return best

    def get_summary_table(self) -> pd.DataFrame:
        """Get summary table of all results.

        Returns:
            DataFrame with one row per strategy-dataset combination
        """
        summary = []

        # Group by strategy and dataset
        groups = {}
        for result in self.results:
            key = (result["strategy"], result["dataset"])
            if key not in groups:
                groups[key] = []
            groups[key].append(result)

        # Aggregate each group
        for (strategy, dataset), results in groups.items():
            # Take best by NDCG@10
            best = max(results, key=lambda x: x["metrics"].get("ndcg@10", 0))

            row = {
                "strategy": strategy,
                "dataset": dataset,
                "n_runs": len(results),
                **{f"best_{k}": v for k, v in best["metrics"].items()},
            }

            # Add latency if available
            if "latency_ms" in best["metadata"]:
                row["latency_ms"] = best["metadata"]["latency_ms"]

            summary.append(row)

        return pd.DataFrame(summary)

    def print_summary(self):
        """Print summary to console."""
        df = self.get_summary_table()

        print("\n" + "=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)
        print(df.to_string(index=False))
        print("=" * 80 + "\n")


def load_results(filepath: str) -> ResultsTracker:
    """Load results from JSON file.

    Args:
        filepath: Path to results JSON

    Returns:
        ResultsTracker with loaded results
    """
    with open(filepath) as f:
        data = json.load(f)

    tracker = ResultsTracker()
    tracker.run_metadata = data.get("metadata", {})
    tracker.results = data.get("results", [])

    logger.info(f"Loaded {len(tracker.results)} results from {filepath}")
    return tracker
