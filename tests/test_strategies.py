"""Tests for retrieval strategies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pytest

from strategies.base import normalize_scores
from strategies.hybrid import BM25Strategy


def test_bm25_basic(small_corpus, test_queries):
    """Test basic BM25 retrieval."""
    strategy = BM25Strategy()
    strategy.index(small_corpus)

    result = strategy.search(
        query=test_queries["q1"],
        query_id="q1",
        top_k=3,
    )

    # Should return results
    assert len(result.ranked_docs) <= 3
    assert len(result.ranked_docs) == len(result.scores)

    # Scores should be descending
    assert all(
        result.scores[i] >= result.scores[i + 1] for i in range(len(result.scores) - 1)
    )

    # All docs should be in corpus
    assert all(doc_id in small_corpus for doc_id in result.ranked_docs)


def test_bm25_batch_search(small_corpus, test_queries):
    """Test BM25 batch search."""
    strategy = BM25Strategy()
    strategy.index(small_corpus)

    results = strategy.batch_search(test_queries, top_k=3)

    assert len(results) == len(test_queries)

    for qid, result in results.items():
        assert qid in test_queries
        assert len(result.ranked_docs) <= 3


def test_bm25_empty_query(small_corpus):
    """Test BM25 with empty query."""
    strategy = BM25Strategy()
    strategy.index(small_corpus)

    result = strategy.search(query="", query_id="q_empty", top_k=3)

    # Should return empty or handle gracefully
    assert len(result.ranked_docs) <= 3


def test_bm25_no_matches(small_corpus):
    """Test BM25 with query that has no matches."""
    strategy = BM25Strategy()
    strategy.index(small_corpus)

    # Use terms not in corpus
    result = strategy.search(
        query="xyzabc nonexistent query terms",
        query_id="q_nomatch",
        top_k=3,
    )

    # Should still return something (all docs with zero scores)
    assert isinstance(result.ranked_docs, list)


def test_normalize_scores_minmax():
    """Test min-max normalization."""
    scores = np.array([1.0, 5.0, 10.0])
    normalized = normalize_scores(scores, method="min-max")

    assert normalized[0] == 0.0  # Min -> 0
    assert normalized[2] == 1.0  # Max -> 1
    assert 0 <= normalized[1] <= 1  # Middle value in range


def test_normalize_scores_zscore():
    """Test z-score normalization."""
    scores = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    normalized = normalize_scores(scores, method="z-score")

    # Z-score should have mean ~0, std ~1
    assert abs(normalized.mean()) < 0.1
    assert abs(normalized.std() - 1.0) < 0.1


def test_normalize_scores_rank():
    """Test rank-based normalization."""
    scores = np.array([10.0, 5.0, 1.0])
    normalized = normalize_scores(scores, method="rank")

    # Highest score gets highest rank score
    assert normalized[0] > normalized[1] > normalized[2]


def test_normalize_scores_constant():
    """Test normalization with constant values."""
    scores = np.array([5.0, 5.0, 5.0])

    # Min-max with constant should return all 0.5
    normalized = normalize_scores(scores, method="min-max")
    assert all(abs(v - 0.5) < 0.01 for v in normalized)


def test_normalize_scores_single():
    """Test normalization with single value."""
    scores = np.array([5.0])

    normalized = normalize_scores(scores, method="min-max")
    assert len(normalized) == 1


def test_bm25_parameters():
    """Test BM25 with different parameters."""
    corpus = {"doc1": "test document", "doc2": "another test"}

    # Test with different k1 values
    strategy1 = BM25Strategy(k1=1.2)
    strategy2 = BM25Strategy(k1=2.0)

    strategy1.index(corpus)
    strategy2.index(corpus)

    result1 = strategy1.search("test", "q1", top_k=2)
    result2 = strategy2.search("test", "q1", top_k=2)

    # Different k1 should give different scores
    assert result1.scores != result2.scores


@pytest.mark.parametrize("top_k", [1, 3, 5, 10])
def test_bm25_top_k(small_corpus, top_k):
    """Test BM25 respects top_k parameter."""
    strategy = BM25Strategy()
    strategy.index(small_corpus)

    result = strategy.search(
        query="machine learning",
        query_id="q1",
        top_k=top_k,
    )

    # Should return at most top_k results
    assert len(result.ranked_docs) <= top_k
    assert len(result.ranked_docs) <= len(small_corpus)
