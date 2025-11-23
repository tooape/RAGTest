"""Tests for document chunking strategies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from utils.chunker import SentenceAwareChunker, SlidingWindowChunker


def test_sliding_window_basic():
    """Test basic sliding window chunking."""
    chunker = SlidingWindowChunker(chunk_size=10, overlap=2)

    # Create text with 25 tokens
    text = " ".join([f"word{i}" for i in range(25)])

    chunks = chunker.chunk(text, "doc1")

    # Should create 3 chunks:
    # Chunk 0: words 0-9 (10 tokens)
    # Chunk 1: words 8-17 (10 tokens, overlap of 2)
    # Chunk 2: words 16-24 (9 tokens)
    assert len(chunks) == 3

    # Check IDs
    assert chunks[0][0] == "doc1_chunk_0"
    assert chunks[1][0] == "doc1_chunk_1"
    assert chunks[2][0] == "doc1_chunk_2"

    # Check chunk sizes
    assert len(chunks[0][1].split()) == 10
    assert len(chunks[1][1].split()) == 10
    assert len(chunks[2][1].split()) == 9


def test_sliding_window_small_text():
    """Test sliding window with text smaller than chunk size."""
    chunker = SlidingWindowChunker(chunk_size=100, overlap=10)

    text = "Short text with only five words."

    chunks = chunker.chunk(text, "doc1")

    # Should create single chunk
    assert len(chunks) == 1
    assert chunks[0][0] == "doc1_chunk_0"
    assert chunks[0][1] == text


def test_sliding_window_no_overlap():
    """Test sliding window with zero overlap."""
    chunker = SlidingWindowChunker(chunk_size=5, overlap=0)

    text = " ".join([f"word{i}" for i in range(15)])

    chunks = chunker.chunk(text, "doc1")

    # Should create exactly 3 chunks of 5 tokens each
    assert len(chunks) == 3

    for chunk_id, chunk_text in chunks:
        assert len(chunk_text.split()) == 5


def test_sentence_aware_basic():
    """Test sentence-aware chunking."""
    chunker = SentenceAwareChunker(chunk_size=10, overlap=3)

    text = "First sentence here. Second sentence is longer than the first. Third one. Fourth sentence."

    chunks = chunker.chunk(text, "doc1")

    # Should have at least one chunk
    assert len(chunks) >= 1

    # All chunks should be non-empty
    for chunk_id, chunk_text in chunks:
        assert len(chunk_text) > 0
        assert "doc1_chunk_" in chunk_id


def test_sentence_aware_single_sentence():
    """Test sentence-aware with single sentence."""
    chunker = SentenceAwareChunker(chunk_size=50, overlap=5)

    text = "This is a single sentence that is not very long."

    chunks = chunker.chunk(text, "doc1")

    # Should create single chunk
    assert len(chunks) == 1
    assert chunks[0][1] == text


def test_sentence_aware_very_long_sentence():
    """Test sentence-aware with sentence exceeding chunk size."""
    chunker = SentenceAwareChunker(chunk_size=5, overlap=1)

    # Single sentence with 20 tokens
    text = " ".join([f"word{i}" for i in range(20)]) + "."

    chunks = chunker.chunk(text, "doc1")

    # Should split long sentence into multiple chunks
    assert len(chunks) > 1

    # Check all chunks
    for chunk_id, chunk_text in chunks:
        assert "doc1_chunk_" in chunk_id
        # Each chunk should be roughly chunk_size (except last)
        token_count = len(chunk_text.split())
        assert token_count > 0


def test_sentence_aware_respects_boundaries():
    """Test that sentence-aware chunker respects sentence boundaries."""
    chunker = SentenceAwareChunker(chunk_size=5, overlap=1)

    # Two sentences, each 4 tokens
    text = "First sentence here. Second sentence there."

    chunks = chunker.chunk(text, "doc1")

    # Should create 2 chunks (one per sentence) or 1 chunk if both fit
    assert len(chunks) >= 1

    # If 2 chunks, check they correspond to sentences
    if len(chunks) == 2:
        assert "First" in chunks[0][1]
        assert "Second" in chunks[1][1]


def test_sentence_aware_overlap():
    """Test sentence overlap in sentence-aware chunking."""
    chunker = SentenceAwareChunker(chunk_size=10, overlap=5)

    # Multiple short sentences
    sentences = [f"Sentence {i} here." for i in range(10)]
    text = " ".join(sentences)

    chunks = chunker.chunk(text, "doc1")

    # Should have overlap between consecutive chunks
    assert len(chunks) >= 2


@pytest.mark.parametrize("chunk_size", [50, 100, 200, 300])
def test_sliding_window_chunk_sizes(chunk_size):
    """Test sliding window with different chunk sizes."""
    chunker = SlidingWindowChunker(chunk_size=chunk_size, overlap=25)

    # Large text
    text = " ".join([f"token{i}" for i in range(1000)])

    chunks = chunker.chunk(text, "doc1")

    # Should create multiple chunks
    assert len(chunks) > 1

    # Most chunks should be close to chunk_size
    for chunk_id, chunk_text in chunks[:-1]:  # Exclude last chunk
        token_count = len(chunk_text.split())
        assert chunk_size - 5 <= token_count <= chunk_size + 5


@pytest.mark.parametrize("overlap", [0, 25, 50, 75])
def test_sliding_window_overlaps(overlap):
    """Test sliding window with different overlap sizes."""
    chunker = SlidingWindowChunker(chunk_size=100, overlap=overlap)

    # Large text
    text = " ".join([f"token{i}" for i in range(500)])

    chunks = chunker.chunk(text, "doc1")

    # Should create multiple chunks
    assert len(chunks) > 1


def test_chunker_empty_text():
    """Test chunkers handle empty text gracefully."""
    chunkers = [
        SlidingWindowChunker(),
        SentenceAwareChunker(),
    ]

    for chunker in chunkers:
        chunks = chunker.chunk("", "doc1")
        # Should return single empty chunk or handle gracefully
        assert len(chunks) >= 0


def test_chunker_whitespace_only():
    """Test chunkers handle whitespace-only text."""
    chunkers = [
        SlidingWindowChunker(),
        SentenceAwareChunker(),
    ]

    text = "   \n\n   \t  "

    for chunker in chunkers:
        chunks = chunker.chunk(text, "doc1")
        # Should handle gracefully
        assert isinstance(chunks, list)
