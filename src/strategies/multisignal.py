"""Multi-signal retrieval with graph and temporal boosting."""

from typing import Dict, List, Optional

import numpy as np
from loguru import logger

from ..models import Embedder
from .base import RetrievalResult, RetrievalStrategy, normalize_scores
from .hybrid import BM25Strategy
from .semantic import SemanticSearch


class MultiSignalFusion(RetrievalStrategy):
    """Multi-signal retrieval combining semantic, BM25, graph, and temporal signals."""

    def __init__(
        self,
        embedder: Embedder,
        name: str = "multisignal",
        semantic_weight: float = 0.5,
        bm25_weight: float = 0.3,
        graph_weight: float = 0.15,
        temporal_weight: float = 0.05,
        normalization: str = "min-max",
        k1: float = 1.2,
        b: float = 0.75,
        temporal_half_life_days: int = 30,
        temporal_bypass_days: int = 120,
        graph_enabled: bool = True,
        temporal_enabled: bool = True,
        **config,
    ):
        """Initialize multi-signal fusion.

        Args:
            embedder: Embedding model
            name: Strategy name
            semantic_weight: Weight for semantic similarity
            bm25_weight: Weight for BM25 lexical matching
            graph_weight: Weight for graph centrality (PageRank)
            temporal_weight: Weight for temporal recency
            normalization: Score normalization method
            k1: BM25 k1 parameter
            b: BM25 b parameter
            temporal_half_life_days: Half-life for exponential decay
            temporal_bypass_days: Days threshold for recency boost
            graph_enabled: Enable graph signal (set False for BEIR)
            temporal_enabled: Enable temporal signal (set False for BEIR)
            **config: Additional configuration
        """
        super().__init__(
            name,
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            graph_weight=graph_weight,
            temporal_weight=temporal_weight,
            normalization=normalization,
            k1=k1,
            b=b,
            temporal_half_life_days=temporal_half_life_days,
            temporal_bypass_days=temporal_bypass_days,
            graph_enabled=graph_enabled,
            temporal_enabled=temporal_enabled,
            **config,
        )

        # Component strategies
        self.semantic = SemanticSearch(embedder, name=f"{name}_semantic")
        self.bm25 = BM25Strategy(name=f"{name}_bm25", k1=k1, b=b)

        # Signal data
        self.graph_scores = {}
        self.temporal_scores = {}
        self.doc_metadata = {}

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus with all signals."""
        logger.info(f"Indexing with {self.name}")

        # Index semantic and BM25
        self.semantic.index(corpus)
        self.bm25.index(corpus)

        # Placeholder for graph scores (would need actual graph structure)
        # For BEIR datasets, this will be all zeros
        if self.config["graph_enabled"]:
            logger.info("Computing graph scores (placeholder - uniform)")
            # In a real implementation, would compute PageRank from wikilinks
            self.graph_scores = {doc_id: 1.0 for doc_id in corpus.keys()}
        else:
            self.graph_scores = {doc_id: 0.0 for doc_id in corpus.keys()}

        # Placeholder for temporal scores
        if self.config["temporal_enabled"]:
            logger.info("Computing temporal scores (placeholder - uniform)")
            # In a real implementation, would extract dates from metadata
            self.temporal_scores = {doc_id: 1.0 for doc_id in corpus.keys()}
        else:
            self.temporal_scores = {doc_id: 0.0 for doc_id in corpus.keys()}

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search using multi-signal fusion."""
        retrieve_k = min(top_k * 5, 100)

        # Get results from base strategies
        sem_result = self.semantic.search(query, query_id, retrieve_k)
        bm25_result = self.bm25.search(query, query_id, retrieve_k)

        # Combine all signals
        combined_scores = self._fuse_signals(
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
                "weights": {
                    "semantic": self.config["semantic_weight"],
                    "bm25": self.config["bm25_weight"],
                    "graph": self.config["graph_weight"],
                    "temporal": self.config["temporal_weight"],
                },
            },
        )

    def _fuse_signals(
        self,
        sem_docs: List[str],
        sem_scores: List[float],
        bm25_docs: List[str],
        bm25_scores: List[float],
    ) -> Dict[str, float]:
        """Fuse all signals with weights."""
        # Normalize semantic and BM25 scores
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

        # Get all candidate documents
        all_docs = set(sem_docs) | set(bm25_docs)

        # Normalize graph and temporal scores (global normalization)
        if self.config["graph_enabled"]:
            graph_values = np.array([self.graph_scores.get(d, 0.0) for d in all_docs])
            graph_norm_values = normalize_scores(graph_values, method=self.config["normalization"])
            graph_dict = dict(zip(all_docs, graph_norm_values))
        else:
            graph_dict = {d: 0.0 for d in all_docs}

        if self.config["temporal_enabled"]:
            temporal_values = np.array([self.temporal_scores.get(d, 0.0) for d in all_docs])
            temporal_norm_values = normalize_scores(temporal_values, method=self.config["normalization"])
            temporal_dict = dict(zip(all_docs, temporal_norm_values))
        else:
            temporal_dict = {d: 0.0 for d in all_docs}

        # Combine with weights
        combined = {}
        for doc_id in all_docs:
            sem_score = sem_dict.get(doc_id, 0.0)
            bm25_score = bm25_dict.get(doc_id, 0.0)
            graph_score = graph_dict.get(doc_id, 0.0)
            temporal_score = temporal_dict.get(doc_id, 0.0)

            combined[doc_id] = (
                self.config["semantic_weight"] * sem_score +
                self.config["bm25_weight"] * bm25_score +
                self.config["graph_weight"] * graph_score +
                self.config["temporal_weight"] * temporal_score
            )

        return combined

    def set_graph_scores(self, graph_scores: Dict[str, float]) -> None:
        """Set graph scores from external computation (e.g., PageRank).

        Args:
            graph_scores: Dict mapping doc_id -> graph centrality score
        """
        self.graph_scores = graph_scores
        logger.info(f"Updated graph scores for {len(graph_scores):,} documents")

    def set_temporal_scores(self, temporal_scores: Dict[str, float]) -> None:
        """Set temporal scores from external computation.

        Args:
            temporal_scores: Dict mapping doc_id -> temporal score
        """
        self.temporal_scores = temporal_scores
        logger.info(f"Updated temporal scores for {len(temporal_scores):,} documents")
