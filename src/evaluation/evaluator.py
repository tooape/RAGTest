"""Evaluator for retrieval strategies."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from loguru import logger

from .metrics import (
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


@dataclass
class EvaluationResults:
    """Results from evaluating a retrieval strategy."""

    dataset_name: str
    strategy_name: str
    metrics: Dict[str, float]
    per_query_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)

    def print_summary(self) -> None:
        """Print a summary of evaluation results."""
        print(f"\n{'='*80}")
        print(f"EVALUATION RESULTS: {self.strategy_name} on {self.dataset_name}")
        print(f"{'='*80}")

        # Print overall metrics
        print("\nOverall Metrics:")
        for metric_name, value in sorted(self.metrics.items()):
            print(f"  {metric_name:20s}: {value:.4f}")

        # Print metadata if present
        if self.metadata:
            print("\nMetadata:")
            for key, value in self.metadata.items():
                print(f"  {key:20s}: {value}")

        print(f"{'='*80}\n")


class Evaluator:
    """Evaluator for retrieval strategies.

    Supports metrics like:
    - mrr@k: Mean Reciprocal Rank at k
    - ndcg@k: Normalized Discounted Cumulative Gain at k
    - precision@k: Precision at k
    - recall@k: Recall at k
    """

    METRIC_FUNCTIONS = {
        "mrr": mean_reciprocal_rank,
        "ndcg": ndcg_at_k,
        "precision": precision_at_k,
        "recall": recall_at_k,
        "p": precision_at_k,  # Alias for precision
        "r": recall_at_k,     # Alias for recall
    }

    def __init__(self, metrics: List[str]):
        """Initialize evaluator.

        Args:
            metrics: List of metric names (e.g., ["mrr@10", "ndcg@10", "precision@5"])
        """
        self.metrics = metrics
        self._parsed_metrics = self._parse_metrics(metrics)

    def _parse_metrics(self, metrics: List[str]) -> List[tuple]:
        """Parse metric strings into (name, k) tuples.

        Args:
            metrics: List of metric strings like "mrr@10"

        Returns:
            List of (metric_name, k_value) tuples
        """
        parsed = []
        for metric in metrics:
            if "@" in metric:
                name, k_str = metric.split("@")
                k = int(k_str)
            else:
                # Default k=10 if not specified
                name = metric
                k = 10

            name = name.lower()
            if name not in self.METRIC_FUNCTIONS:
                raise ValueError(
                    f"Unknown metric: {name}. "
                    f"Supported: {list(self.METRIC_FUNCTIONS.keys())}"
                )

            parsed.append((name, k, metric))

        return parsed

    def evaluate(
        self,
        results: Dict[str, "RetrievalResult"],
        qrels: Dict[str, Dict[str, int]],
        dataset_name: str,
        strategy_name: str,
        metadata: Optional[Dict] = None,
    ) -> EvaluationResults:
        """Evaluate retrieval results.

        Args:
            results: Dict mapping query_id -> RetrievalResult
            qrels: Dict mapping query_id -> {doc_id: relevance}
            dataset_name: Name of the dataset
            strategy_name: Name of the strategy
            metadata: Optional metadata to include in results

        Returns:
            EvaluationResults object
        """
        overall_metrics = {}
        per_query_metrics = {}

        # Calculate per-query metrics first
        for metric_name, k, full_metric_name in self._parsed_metrics:
            metric_func = self.METRIC_FUNCTIONS[metric_name]

            # Calculate per-query scores
            for query_id in results.keys():
                if query_id not in qrels:
                    continue

                # Create single-query dict for metric calculation
                single_result = {query_id: results[query_id]}
                single_qrel = {query_id: qrels[query_id]}

                # Calculate metric for this query
                score = metric_func(single_result, single_qrel, k=k)

                # Store per-query metric
                if query_id not in per_query_metrics:
                    per_query_metrics[query_id] = {}
                per_query_metrics[query_id][full_metric_name] = score

        # Calculate overall metrics (averaged across all queries)
        for metric_name, k, full_metric_name in self._parsed_metrics:
            metric_func = self.METRIC_FUNCTIONS[metric_name]
            score = metric_func(results, qrels, k=k)
            overall_metrics[full_metric_name] = score

        return EvaluationResults(
            dataset_name=dataset_name,
            strategy_name=strategy_name,
            metrics=overall_metrics,
            per_query_metrics=per_query_metrics,
            metadata=metadata or {},
        )
