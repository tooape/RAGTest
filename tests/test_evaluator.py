"""Tests for evaluator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from evaluation.evaluator import EvaluationResults, Evaluator
from strategies.base import RetrievalResult


def test_evaluator_basic(test_qrels):
    """Test basic evaluator functionality."""
    evaluator = Evaluator(metrics=["mrr@10", "ndcg@10", "precision@10"])

    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2", "doc3"],
            scores=[1.0, 0.5, 0.3],
        ),
        "q2": RetrievalResult(
            query_id="q2",
            ranked_docs=["doc4", "doc5"],
            scores=[1.0, 0.5],
        ),
    }

    qrels = {
        "q1": {"doc1": 1},
        "q2": {"doc5": 1},
    }

    eval_results = evaluator.evaluate(
        results=results,
        qrels=qrels,
        dataset_name="test",
        strategy_name="test_strategy",
    )

    # Check structure
    assert isinstance(eval_results, EvaluationResults)
    assert eval_results.dataset_name == "test"
    assert eval_results.strategy_name == "test_strategy"

    # Check metrics exist
    assert "mrr@10" in eval_results.metrics
    assert "ndcg@10" in eval_results.metrics
    assert "precision@10" in eval_results.metrics

    # Check values are reasonable
    for metric, value in eval_results.metrics.items():
        assert 0 <= value <= 1, f"Metric {metric} out of range: {value}"


def test_evaluator_custom_k():
    """Test evaluator with custom k values."""
    evaluator = Evaluator(metrics=["precision@5", "recall@5", "ndcg@5"])

    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2", "doc3", "doc4", "doc5"],
            scores=[1.0, 0.9, 0.8, 0.7, 0.6],
        ),
    }

    qrels = {
        "q1": {"doc1": 1, "doc3": 1},
    }

    eval_results = evaluator.evaluate(
        results=results,
        qrels=qrels,
        dataset_name="test",
        strategy_name="test",
    )

    # Should calculate at k=5
    assert "precision@5" in eval_results.metrics
    assert eval_results.metrics["precision@5"] == 2.0 / 5.0  # 2 relevant in top 5


def test_evaluator_per_query_metrics():
    """Test per-query metrics."""
    evaluator = Evaluator(metrics=["mrr@10"])

    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2"],
            scores=[1.0, 0.5],
        ),
        "q2": RetrievalResult(
            query_id="q2",
            ranked_docs=["doc3", "doc4"],
            scores=[1.0, 0.5],
        ),
    }

    qrels = {
        "q1": {"doc1": 1},
        "q2": {"doc4": 1},
    }

    eval_results = evaluator.evaluate(
        results=results,
        qrels=qrels,
        dataset_name="test",
        strategy_name="test",
    )

    # Check per-query metrics
    per_query = eval_results.per_query_metrics
    assert "q1" in per_query
    assert "q2" in per_query

    # q1: doc1 at rank 1 -> RR = 1.0
    assert per_query["q1"]["mrr@10"] == 1.0

    # q2: doc4 at rank 2 -> RR = 0.5
    assert per_query["q2"]["mrr@10"] == 0.5


def test_evaluator_missing_query():
    """Test evaluator handles missing queries gracefully."""
    evaluator = Evaluator(metrics=["mrr@10"])

    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1"],
            scores=[1.0],
        ),
    }

    qrels = {
        "q1": {"doc1": 1},
        "q2": {"doc2": 1},  # q2 not in results
    }

    # Should handle gracefully
    eval_results = evaluator.evaluate(
        results=results,
        qrels=qrels,
        dataset_name="test",
        strategy_name="test",
    )

    assert "mrr@10" in eval_results.metrics


def test_evaluation_results_print(capsys):
    """Test EvaluationResults print_summary."""
    eval_results = EvaluationResults(
        dataset_name="test",
        strategy_name="test_strategy",
        metrics={"mrr@10": 0.75, "ndcg@10": 0.85},
        per_query_metrics={},
        metadata={"param1": "value1"},
    )

    eval_results.print_summary()

    captured = capsys.readouterr()
    assert "test_strategy" in captured.out
    assert "test" in captured.out
    assert "mrr@10" in captured.out
    assert "0.75" in captured.out
