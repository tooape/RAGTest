"""Document chunking strategies for dynamic text splitting."""

import re
from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np


class Chunker(ABC):
    """Base class for document chunking strategies."""

    @abstractmethod
    def chunk(self, text: str, doc_id: str) -> List[Tuple[str, str]]:
        """Chunk a document into smaller pieces.

        Args:
            text: Document text
            doc_id: Document identifier

        Returns:
            List of (chunk_id, chunk_text) tuples
        """
        pass


class SlidingWindowChunker(Chunker):
    """Sliding window chunking with token-based overlap.

    Splits text into fixed-size chunks with overlap, ignoring
    semantic boundaries.
    """

    def __init__(self, chunk_size: int = 250, overlap: int = 50):
        """Initialize sliding window chunker.

        Args:
            chunk_size: Target chunk size in tokens (approximate)
            overlap: Overlap between chunks in tokens
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, doc_id: str) -> List[Tuple[str, str]]:
        """Chunk text using sliding window."""
        # Simple tokenization (split on whitespace)
        tokens = text.split()

        if len(tokens) <= self.chunk_size:
            # Document fits in one chunk
            return [(f"{doc_id}_chunk_0", text)]

        chunks = []
        chunk_idx = 0
        start = 0

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = " ".join(chunk_tokens)

            chunk_id = f"{doc_id}_chunk_{chunk_idx}"
            chunks.append((chunk_id, chunk_text))

            chunk_idx += 1

            # Move window forward (minus overlap)
            if end >= len(tokens):
                break
            start += self.chunk_size - self.overlap

        return chunks


class SentenceAwareChunker(Chunker):
    """Sentence-aware chunking that respects sentence boundaries.

    Splits text at sentence boundaries to maintain semantic coherence.
    """

    def __init__(self, chunk_size: int = 250, overlap: int = 50):
        """Initialize sentence-aware chunker.

        Args:
            chunk_size: Target chunk size in tokens (approximate)
            overlap: Overlap in tokens (will snap to sentence boundaries)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

        # Sentence boundary regex (simple version)
        self.sentence_pattern = re.compile(r'(?<=[.!?])\s+')

    def chunk(self, text: str, doc_id: str) -> List[Tuple[str, str]]:
        """Chunk text respecting sentence boundaries."""
        # Split into sentences
        sentences = self.sentence_pattern.split(text)

        if not sentences:
            return [(f"{doc_id}_chunk_0", text)]

        chunks = []
        chunk_idx = 0
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence.split())

            # If single sentence exceeds chunk size, split it
            if sentence_size > self.chunk_size * 1.5:
                # Save current chunk if not empty
                if current_chunk:
                    chunk_text = " ".join(current_chunk)
                    chunks.append((f"{doc_id}_chunk_{chunk_idx}", chunk_text))
                    chunk_idx += 1
                    current_chunk = []
                    current_size = 0

                # Split long sentence with sliding window
                long_chunks = self._split_long_sentence(sentence, doc_id, chunk_idx)
                chunks.extend(long_chunks)
                chunk_idx += len(long_chunks)
                continue

            # Check if adding sentence would exceed chunk size
            if current_size + sentence_size > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append((f"{doc_id}_chunk_{chunk_idx}", chunk_text))
                chunk_idx += 1

                # Start new chunk with overlap
                # Keep last few sentences for overlap
                overlap_sentences = []
                overlap_size = 0
                for sent in reversed(current_chunk):
                    sent_size = len(sent.split())
                    if overlap_size + sent_size > self.overlap:
                        break
                    overlap_sentences.insert(0, sent)
                    overlap_size += sent_size

                current_chunk = overlap_sentences
                current_size = overlap_size

            current_chunk.append(sentence)
            current_size += sentence_size

        # Add remaining chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append((f"{doc_id}_chunk_{chunk_idx}", chunk_text))

        return chunks if chunks else [(f"{doc_id}_chunk_0", text)]

    def _split_long_sentence(
        self, sentence: str, doc_id: str, start_idx: int
    ) -> List[Tuple[str, str]]:
        """Split a very long sentence using sliding window."""
        tokens = sentence.split()
        chunks = []
        chunk_idx = start_idx
        start = 0

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = " ".join(chunk_tokens)

            chunk_id = f"{doc_id}_chunk_{chunk_idx}"
            chunks.append((chunk_id, chunk_text))

            chunk_idx += 1

            if end >= len(tokens):
                break
            start += self.chunk_size - self.overlap

        return chunks


class SemanticChunker(Chunker):
    """Semantic chunking using embedding similarity.

    Splits text at points where semantic similarity drops,
    indicating topic boundaries.
    """

    def __init__(
        self,
        embedder,
        chunk_size: int = 250,
        overlap: int = 50,
        similarity_threshold: float = 0.7,
    ):
        """Initialize semantic chunker.

        Args:
            embedder: Embedding model for computing sentence similarities
            chunk_size: Target chunk size in tokens
            overlap: Overlap in tokens
            similarity_threshold: Similarity threshold for splitting
        """
        self.embedder = embedder
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.similarity_threshold = similarity_threshold

        # Sentence boundary regex
        self.sentence_pattern = re.compile(r'(?<=[.!?])\s+')

    def chunk(self, text: str, doc_id: str) -> List[Tuple[str, str]]:
        """Chunk text at semantic boundaries."""
        # Split into sentences
        sentences = self.sentence_pattern.split(text)

        if len(sentences) <= 1:
            return [(f"{doc_id}_chunk_0", text)]

        # Compute embeddings for each sentence
        embeddings = self.embedder.encode(sentences)

        # Find semantic breaks (low similarity between consecutive sentences)
        break_points = [0]

        for i in range(len(sentences) - 1):
            # Compute cosine similarity
            sim = np.dot(embeddings[i], embeddings[i + 1])

            # Low similarity = potential break point
            if sim < self.similarity_threshold:
                break_points.append(i + 1)

        break_points.append(len(sentences))

        # Group sentences into chunks respecting break points
        chunks = []
        chunk_idx = 0

        for i in range(len(break_points) - 1):
            start_sent = break_points[i]
            end_sent = break_points[i + 1]

            segment_sentences = sentences[start_sent:end_sent]
            segment_text = " ".join(segment_sentences)
            segment_size = len(segment_text.split())

            # If segment is too large, split it further
            if segment_size > self.chunk_size * 1.5:
                sub_chunks = self._split_large_segment(
                    segment_sentences, doc_id, chunk_idx
                )
                chunks.extend(sub_chunks)
                chunk_idx += len(sub_chunks)
            else:
                chunks.append((f"{doc_id}_chunk_{chunk_idx}", segment_text))
                chunk_idx += 1

        return chunks if chunks else [(f"{doc_id}_chunk_0", text)]

    def _split_large_segment(
        self, sentences: List[str], doc_id: str, start_idx: int
    ) -> List[Tuple[str, str]]:
        """Split large segment respecting chunk size."""
        chunks = []
        chunk_idx = start_idx
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence.split())

            if current_size + sentence_size > self.chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append((f"{doc_id}_chunk_{chunk_idx}", chunk_text))
                chunk_idx += 1

                # Overlap: keep last sentence
                if self.overlap > 0 and current_chunk:
                    current_chunk = [current_chunk[-1]]
                    current_size = len(current_chunk[-1].split())
                else:
                    current_chunk = []
                    current_size = 0

            current_chunk.append(sentence)
            current_size += sentence_size

        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append((f"{doc_id}_chunk_{chunk_idx}", chunk_text))

        return chunks
