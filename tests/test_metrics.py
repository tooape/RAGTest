"""Tests for evaluation metrics."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from evaluation.metrics import (
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)
from strategies.base import RetrievalResult


def test_mrr_perfect_match():
    """Test MRR with perfect first-rank match."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2", "doc3"],
            scores=[1.0, 0.5, 0.3],
        ),
    }

    qrels = {
        "q1": {"doc1": 1},
    }

    mrr = mean_reciprocal_rank(results, qrels, k=10)
    assert mrr == 1.0, "Perfect first-rank match should give MRR=1.0"


def test_mrr_second_rank():
    """Test MRR with relevant doc in second position."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc2", "doc1", "doc3"],
            scores=[1.0, 0.5, 0.3],
        ),
    }

    qrels = {
        "q1": {"doc1": 1},
    }

    mrr = mean_reciprocal_rank(results, qrels, k=10)
    assert mrr == 0.5, "Second-rank match should give MRR=0.5"


def test_mrr_no_match():
    """Test MRR with no relevant docs retrieved."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc2", "doc3"],
            scores=[1.0, 0.5],
        ),
    }

    qrels = {
        "q1": {"doc1": 1},
    }

    mrr = mean_reciprocal_rank(results, qrels, k=10)
    assert mrr == 0.0, "No match should give MRR=0.0"


def test_precision_at_k():
    """Test Precision@k calculation."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2", "doc3", "doc4"],
            scores=[1.0, 0.8, 0.6, 0.4],
        ),
    }

    qrels = {
        "q1": {"doc1": 1, "doc3": 1},  # 2 relevant docs
    }

    # At k=2, only doc1 is relevant
    prec_2 = precision_at_k(results, qrels, k=2)
    assert prec_2 == 0.5, "1 relevant in top-2 should give P@2=0.5"

    # At k=3, doc1 and doc3 are relevant
    prec_3 = precision_at_k(results, qrels, k=3)
    assert prec_3 == pytest.approx(2.0 / 3.0), "2 relevant in top-3 should give P@3=0.667"

    # At k=4, still 2 relevant
    prec_4 = precision_at_k(results, qrels, k=4)
    assert prec_4 == 0.5, "2 relevant in top-4 should give P@4=0.5"


def test_recall_at_k():
    """Test Recall@k calculation."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2", "doc3"],
            scores=[1.0, 0.8, 0.6],
        ),
    }

    qrels = {
        "q1": {"doc1": 1, "doc3": 1, "doc4": 1},  # 3 relevant total
    }

    # At k=2, found doc1 (1 of 3)
    recall_2 = recall_at_k(results, qrels, k=2)
    assert recall_2 == pytest.approx(1.0 / 3.0), "1 of 3 should give R@2=0.333"

    # At k=3, found doc1 and doc3 (2 of 3)
    recall_3 = recall_at_k(results, qrels, k=3)
    assert recall_3 == pytest.approx(2.0 / 3.0), "2 of 3 should give R@3=0.667"


def test_ndcg_perfect():
    """Test NDCG with perfect ranking."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2", "doc3"],
            scores=[1.0, 0.8, 0.6],
        ),
    }

    qrels = {
        "q1": {"doc1": 1, "doc2": 1, "doc3": 1},
    }

    ndcg = ndcg_at_k(results, qrels, k=10)
    assert ndcg == 1.0, "Perfect ranking should give NDCG=1.0"


def test_ndcg_zero():
    """Test NDCG with no relevant docs."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc2", "doc3"],
            scores=[1.0, 0.8],
        ),
    }

    qrels = {
        "q1": {"doc1": 1},
    }

    ndcg = ndcg_at_k(results, qrels, k=10)
    assert ndcg == 0.0, "No relevant docs should give NDCG=0.0"


def test_ndcg_graded_relevance():
    """Test NDCG with graded relevance scores."""
    results = {
        "q1": RetrievalResult(
            query_id="q1",
            ranked_docs=["doc1", "doc2", "doc3"],
            scores=[1.0, 0.8, 0.6],
        ),
    }

    qrels = {
        "q1": {"doc1": 2, "doc2": 1, "doc3": 1},  # Graded relevance
    }

    ndcg = ndcg_at_k(results, qrels, k=10)
    assert 0 < ndcg <= 1.0, "NDCG should be in (0, 1] for graded relevance"


def test_metrics_multiple_queries():
    """Test metrics averaged over multiple queries."""
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

    # q1: doc1 at rank 1 -> RR = 1.0
    # q2: doc4 at rank 2 -> RR = 0.5
    # MRR = (1.0 + 0.5) / 2 = 0.75
    mrr = mean_reciprocal_rank(results, qrels, k=10)
    assert mrr == 0.75, "MRR should average over queries"
