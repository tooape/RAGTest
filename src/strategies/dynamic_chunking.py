"""Multi-signal retrieval with dynamic chunking."""

from collections import defaultdict
from typing import Dict, List

from loguru import logger

from ..models import Embedder
from ..utils.chunker import Chunker, SentenceAwareChunker
from .base import RetrievalResult, RetrievalStrategy
from .multisignal import MultiSignalFusion


class DynamicChunkingMultiSignal(RetrievalStrategy):
    """Multi-signal fusion with dynamic chunking.

    Instead of using H2-based document splitting, this strategy:
    1. Chunks documents dynamically (sliding window, sentence-aware, semantic)
    2. Indexes chunks with multi-signal retrieval
    3. Aggregates chunk scores to document level
    """

    def __init__(
        self,
        embedder: Embedder,
        chunker: Chunker = None,
        name: str = "dynamic_chunking_multisignal",
        chunk_size: int = 250,
        overlap: int = 50,
        aggregation: str = "max",
        semantic_weight: float = 0.5,
        bm25_weight: float = 0.3,
        graph_weight: float = 0.15,
        temporal_weight: float = 0.05,
        graph_enabled: bool = True,
        temporal_enabled: bool = True,
        **config,
    ):
        """Initialize dynamic chunking multi-signal strategy.

        Args:
            embedder: Embedding model
            chunker: Chunking strategy (defaults to SentenceAwareChunker)
            name: Strategy name
            chunk_size: Target chunk size in tokens
            overlap: Overlap between chunks in tokens
            aggregation: How to aggregate chunk scores ('max', 'mean', 'sum')
            semantic_weight: Weight for semantic signal
            bm25_weight: Weight for BM25 signal
            graph_weight: Weight for graph signal
            temporal_weight: Weight for temporal signal
            graph_enabled: Enable graph signal
            temporal_enabled: Enable temporal signal
            **config: Additional configuration
        """
        super().__init__(
            name,
            chunk_size=chunk_size,
            overlap=overlap,
            aggregation=aggregation,
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            graph_weight=graph_weight,
            temporal_weight=temporal_weight,
            graph_enabled=graph_enabled,
            temporal_enabled=temporal_enabled,
            **config,
        )

        # Chunker
        if chunker is None:
            chunker = SentenceAwareChunker(chunk_size=chunk_size, overlap=overlap)
        self.chunker = chunker

        # Multi-signal strategy (operates on chunks)
        self.multisignal = MultiSignalFusion(
            embedder=embedder,
            name=f"{name}_multisignal",
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            graph_weight=graph_weight,
            temporal_weight=temporal_weight,
            graph_enabled=graph_enabled,
            temporal_enabled=temporal_enabled,
            **config,
        )

        # Mappings
        self.chunk_to_doc = {}  # chunk_id -> doc_id
        self.doc_to_chunks = defaultdict(list)  # doc_id -> [chunk_ids]
        self.original_corpus = {}  # doc_id -> full document text

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus with dynamic chunking."""
        logger.info(f"Indexing with {self.name} (chunking documents)...")

        self.original_corpus = corpus

        # Chunk all documents
        chunk_corpus = {}
        total_chunks = 0

        for doc_id, text in corpus.items():
            chunks = self.chunker.chunk(text, doc_id)

            for chunk_id, chunk_text in chunks:
                chunk_corpus[chunk_id] = chunk_text
                self.chunk_to_doc[chunk_id] = doc_id
                self.doc_to_chunks[doc_id].append(chunk_id)

            total_chunks += len(chunks)

        logger.info(
            f"Created {total_chunks:,} chunks from {len(corpus):,} documents "
            f"({total_chunks / len(corpus):.1f} chunks/doc)"
        )

        # Index chunks with multi-signal
        self.multisignal.index(chunk_corpus)

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search with chunk-level retrieval and document-level aggregation."""
        # Retrieve more chunks to ensure we get enough documents
        retrieve_k = min(top_k * 10, 200)

        # Search at chunk level
        chunk_result = self.multisignal.search(query, query_id, top_k=retrieve_k)

        # Aggregate chunk scores to document level
        doc_scores = defaultdict(list)

        for chunk_id, score in zip(chunk_result.ranked_docs, chunk_result.scores):
            doc_id = self.chunk_to_doc[chunk_id]
            doc_scores[doc_id].append(score)

        # Apply aggregation
        aggregated = {}
        for doc_id, scores in doc_scores.items():
            if self.config["aggregation"] == "max":
                aggregated[doc_id] = max(scores)
            elif self.config["aggregation"] == "mean":
                aggregated[doc_id] = sum(scores) / len(scores)
            elif self.config["aggregation"] == "sum":
                aggregated[doc_id] = sum(scores)
            else:
                raise ValueError(f"Unknown aggregation: {self.config['aggregation']}")

        # Sort by aggregated score
        ranked_items = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)

        ranked_docs = [doc_id for doc_id, _ in ranked_items[:top_k]]
        scores = [score for _, score in ranked_items[:top_k]]

        return RetrievalResult(
            query_id=query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={
                "strategy": self.name,
                "chunker": self.chunker.__class__.__name__,
                "chunk_size": self.config["chunk_size"],
                "overlap": self.config["overlap"],
                "aggregation": self.config["aggregation"],
                "chunks_retrieved": len(chunk_result.ranked_docs),
                "docs_retrieved": len(doc_scores),
            },
        )

    def set_graph_scores(self, graph_scores: Dict[str, float]) -> None:
        """Set graph scores (document-level).

        Note: Graph scores are applied at document level, then
        inherited by all chunks from that document.
        """
        # Expand to chunk level
        chunk_graph_scores = {}
        for doc_id, score in graph_scores.items():
            for chunk_id in self.doc_to_chunks[doc_id]:
                chunk_graph_scores[chunk_id] = score

        self.multisignal.set_graph_scores(chunk_graph_scores)
        logger.info(
            f"Updated graph scores: {len(graph_scores):,} docs -> "
            f"{len(chunk_graph_scores):,} chunks"
        )

    def set_temporal_scores(self, temporal_scores: Dict[str, float]) -> None:
        """Set temporal scores (document-level).

        Note: Temporal scores are applied at document level, then
        inherited by all chunks from that document.
        """
        # Expand to chunk level
        chunk_temporal_scores = {}
        for doc_id, score in temporal_scores.items():
            for chunk_id in self.doc_to_chunks[doc_id]:
                chunk_temporal_scores[chunk_id] = score

        self.multisignal.set_temporal_scores(chunk_temporal_scores)
        logger.info(
            f"Updated temporal scores: {len(temporal_scores):,} docs -> "
            f"{len(chunk_temporal_scores):,} chunks"
        )
