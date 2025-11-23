"""Hybrid retrieval strategies combining multiple signals."""

from typing import Dict, List, Tuple

import numpy as np
from loguru import logger

from ..models import BM25Searcher, Embedder
from .base import RetrievalResult, RetrievalStrategy, normalize_scores
from .semantic import SemanticSearch


class BM25Strategy(RetrievalStrategy):
    """BM25 lexical search strategy."""

    def __init__(
        self,
        name: str = "bm25",
        k1: float = 1.2,
        b: float = 0.75,
        **config,
    ):
        """Initialize BM25 strategy.

        Args:
            name: Strategy name
            k1: Term frequency saturation
            b: Length normalization
            **config: Additional configuration
        """
        super().__init__(name, k1=k1, b=b, **config)
        self.searcher = None

    def index(self, corpus: Dict[str, str]) -> None:
        """Build BM25 index."""
        logger.info(f"Building BM25 index for {len(corpus):,} documents")
        self.searcher = BM25Searcher(
            corpus=corpus,
            k1=self.config["k1"],
            b=self.config["b"],
        )

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search using BM25."""
        if self.searcher is None:
            raise ValueError("Index not built. Call index() first.")

        results = self.searcher.search(query, top_k=top_k)
        ranked_docs = [doc_id for doc_id, _ in results]
        scores = [score for _, score in results]

        return RetrievalResult(
            query_id=query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={"strategy": self.name},
        )


class WeightedHybrid(RetrievalStrategy):
    """Weighted combination of semantic and BM25."""

    def __init__(
        self,
        embedder: Embedder,
        name: str = "weighted_hybrid",
        semantic_weight: float = 0.7,
        bm25_weight: float = 0.3,
        normalization: str = "min-max",
        k1: float = 1.2,
        b: float = 0.75,
        **config,
    ):
        """Initialize weighted hybrid.

        Args:
            embedder: Embedding model for semantic search
            name: Strategy name
            semantic_weight: Weight for semantic scores
            bm25_weight: Weight for BM25 scores
            normalization: Score normalization method
            k1: BM25 k1 parameter
            b: BM25 b parameter
            **config: Additional configuration
        """
        super().__init__(
            name,
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            normalization=normalization,
            k1=k1,
            b=b,
            **config,
        )

        # Create component strategies
        self.semantic = SemanticSearch(embedder, name=f"{name}_semantic")
        self.bm25 = BM25Strategy(name=f"{name}_bm25", k1=k1, b=b)

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus with both strategies."""
        logger.info(f"Indexing with {self.name}")
        self.semantic.index(corpus)
        self.bm25.index(corpus)

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search using weighted combination."""
        # Retrieve more candidates from each strategy
        retrieve_k = min(top_k * 5, 100)  # Get more for fusion

        # Get results from both strategies
        sem_result = self.semantic.search(query, query_id, retrieve_k)
        bm25_result = self.bm25.search(query, query_id, retrieve_k)

        # Combine scores
        combined_scores = self._combine_scores(
            sem_result.ranked_docs,
            sem_result.scores,
            bm25_result.ranked_docs,
            bm25_result.scores,
        )

        # Sort by combined score
        ranked_items = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        ranked_docs = [doc_id for doc_id, _ in ranked_items[:top_k]]
        scores = [score for _, score in ranked_items[:top_k]]

        return RetrievalResult(
            query_id=query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={
                "strategy": self.name,
                "semantic_weight": self.config["semantic_weight"],
                "bm25_weight": self.config["bm25_weight"],
            },
        )

    def _combine_scores(
        self,
        sem_docs: List[str],
        sem_scores: List[float],
        bm25_docs: List[str],
        bm25_scores: List[float],
    ) -> Dict[str, float]:
        """Combine scores from both strategies."""
        # Normalize scores
        sem_norm = normalize_scores(
            np.array(sem_scores),
            method=self.config["normalization"],
        )
        bm25_norm = normalize_scores(
            np.array(bm25_scores),
            method=self.config["normalization"],
        )

        # Create score dictionaries
        sem_dict = dict(zip(sem_docs, sem_norm))
        bm25_dict = dict(zip(bm25_docs, bm25_norm))

        # Combine scores
        all_docs = set(sem_docs) | set(bm25_docs)
        combined = {}

        for doc_id in all_docs:
            sem_score = sem_dict.get(doc_id, 0.0)
            bm25_score = bm25_dict.get(doc_id, 0.0)

            combined[doc_id] = (
                self.config["semantic_weight"] * sem_score +
                self.config["bm25_weight"] * bm25_score
            )

        return combined


class RRFHybrid(RetrievalStrategy):
    """Reciprocal Rank Fusion of semantic and BM25."""

    def __init__(
        self,
        embedder: Embedder,
        name: str = "rrf_hybrid",
        rrf_k: int = 60,
        k1: float = 1.2,
        b: float = 0.75,
        **config,
    ):
        """Initialize RRF hybrid.

        Args:
            embedder: Embedding model
            name: Strategy name
            rrf_k: RRF constant (higher = more weight to lower ranks)
            k1: BM25 k1 parameter
            b: BM25 b parameter
            **config: Additional configuration
        """
        super().__init__(name, rrf_k=rrf_k, k1=k1, b=b, **config)

        self.semantic = SemanticSearch(embedder, name=f"{name}_semantic")
        self.bm25 = BM25Strategy(name=f"{name}_bm25", k1=k1, b=b)

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus."""
        logger.info(f"Indexing with {self.name}")
        self.semantic.index(corpus)
        self.bm25.index(corpus)

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search using RRF."""
        retrieve_k = min(top_k * 5, 100)

        # Get results
        sem_result = self.semantic.search(query, query_id, retrieve_k)
        bm25_result = self.bm25.search(query, query_id, retrieve_k)

        # Calculate RRF scores
        rrf_scores = {}
        k = self.config["rrf_k"]

        # Add semantic ranks
        for rank, doc_id in enumerate(sem_result.ranked_docs, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

        # Add BM25 ranks
        for rank, doc_id in enumerate(bm25_result.ranked_docs, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

        # Sort by RRF score
        ranked_items = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        ranked_docs = [doc_id for doc_id, _ in ranked_items[:top_k]]
        scores = [score for _, score in ranked_items[:top_k]]

        return RetrievalResult(
            query_id=query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={
                "strategy": self.name,
                "rrf_k": self.config["rrf_k"],
            },
        )
