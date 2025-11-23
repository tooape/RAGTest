"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def small_corpus():
    """Small test corpus."""
    return {
        "doc1": "Machine learning is a subset of artificial intelligence.",
        "doc2": "Deep learning uses neural networks.",
        "doc3": "Natural language processing enables text understanding.",
        "doc4": "Computer vision interprets visual information.",
        "doc5": "Reinforcement learning uses rewards and penalties.",
    }


@pytest.fixture
def test_queries():
    """Test queries."""
    return {
        "q1": "What is deep learning?",
        "q2": "How does reinforcement learning work?",
    }


@pytest.fixture
def test_qrels():
    """Test query relevance judgments."""
    return {
        "q1": {"doc2": 1},
        "q2": {"doc5": 1},
    }


@pytest.fixture
def tiny_corpus():
    """Tiny corpus for quick tests."""
    return {
        "doc1": "cat",
        "doc2": "dog",
        "doc3": "bird",
    }


@pytest.fixture
def tiny_queries():
    """Tiny queries."""
    return {
        "q1": "cat",
        "q2": "dog",
    }
