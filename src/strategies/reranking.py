"""Two-stage retrieval with reranking."""

from typing import Dict, List

from loguru import logger

from ..models import Embedder, Reranker
from .base import RetrievalResult, RetrievalStrategy
from .multisignal import MultiSignalFusion
from .semantic import SemanticSearch


class TwoStageReranking(RetrievalStrategy):
    """Two-stage retrieval: fast retrieval + precise reranking."""

    def __init__(
        self,
        embedder: Embedder,
        reranker: Reranker,
        name: str = "two_stage_reranking",
        stage1_k: int = 100,
        **config,
    ):
        """Initialize two-stage reranking.

        Args:
            embedder: Embedding model for stage 1
            reranker: Reranker model for stage 2
            name: Strategy name
            stage1_k: Number of candidates to retrieve in stage 1
            **config: Additional configuration
        """
        super().__init__(name, stage1_k=stage1_k, **config)

        # Stage 1: Fast semantic retrieval
        self.stage1 = SemanticSearch(embedder, name=f"{name}_stage1")

        # Stage 2: Reranker
        self.reranker = reranker

        # Store corpus for reranking
        self.corpus = None

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus for stage 1."""
        logger.info(f"Indexing with {self.name}")
        self.corpus = corpus
        self.stage1.index(corpus)

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Two-stage search with reranking."""
        if self.corpus is None:
            raise ValueError("Corpus not indexed. Call index() first.")

        # Stage 1: Retrieve candidates
        stage1_result = self.stage1.search(
            query,
            query_id,
            top_k=self.config["stage1_k"],
        )

        # Prepare documents for reranking
        candidates = [
            (doc_id, self.corpus[doc_id])
            for doc_id in stage1_result.ranked_docs
        ]

        # Stage 2: Rerank
        reranked = self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=top_k,
        )

        ranked_docs = [doc_id for doc_id, _ in reranked]
        scores = [score for _, score in reranked]

        return RetrievalResult(
            query_id=query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={
                "strategy": self.name,
                "stage1_k": self.config["stage1_k"],
                "reranker": self.reranker.model_name,
            },
        )


class MultiSignalWithReranking(RetrievalStrategy):
    """Multi-signal fusion with reranking before fusion."""

    def __init__(
        self,
        embedder: Embedder,
        reranker: Reranker,
        name: str = "multisignal_reranked",
        semantic_weight: float = 0.5,
        bm25_weight: float = 0.3,
        graph_weight: float = 0.15,
        temporal_weight: float = 0.05,
        stage1_k: int = 100,
        reranked_k: int = 50,
        **config,
    ):
        """Initialize multi-signal with reranking.

        Pipeline:
        1. Retrieve candidates with semantic + BM25
        2. Rerank each signal independently
        3. Fuse reranked results with graph + temporal

        Args:
            embedder: Embedding model
            reranker: Reranker model
            name: Strategy name
            semantic_weight: Weight for semantic signal
            bm25_weight: Weight for BM25 signal
            graph_weight: Weight for graph signal
            temporal_weight: Weight for temporal signal
            stage1_k: Candidates to retrieve in stage 1
            reranked_k: Candidates to keep after reranking
            **config: Additional configuration
        """
        super().__init__(
            name,
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            graph_weight=graph_weight,
            temporal_weight=temporal_weight,
            stage1_k=stage1_k,
            reranked_k=reranked_k,
            **config,
        )

        # Use multi-signal as base (without reranking)
        self.multisignal = MultiSignalFusion(
            embedder=embedder,
            name=f"{name}_multisignal",
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            graph_weight=graph_weight,
            temporal_weight=temporal_weight,
            **config,
        )

        self.reranker = reranker
        self.corpus = None

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus."""
        logger.info(f"Indexing with {self.name}")
        self.corpus = corpus
        self.multisignal.index(corpus)

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search with reranking before fusion."""
        if self.corpus is None:
            raise ValueError("Corpus not indexed. Call index() first.")

        # Get multi-signal results (more candidates for reranking)
        multisignal_result = self.multisignal.search(
            query,
            query_id,
            top_k=self.config["stage1_k"],
        )

        # Prepare for reranking
        candidates = [
            (doc_id, self.corpus[doc_id])
            for doc_id in multisignal_result.ranked_docs
        ]

        # Rerank
        reranked = self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=top_k,
        )

        ranked_docs = [doc_id for doc_id, _ in reranked]
        scores = [score for _, score in reranked]

        return RetrievalResult(
            query_id=query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={
                "strategy": self.name,
                "stage1_k": self.config["stage1_k"],
                "reranker": self.reranker.model_name,
            },
        )

    def set_graph_scores(self, graph_scores: Dict[str, float]) -> None:
        """Pass through to multi-signal."""
        self.multisignal.set_graph_scores(graph_scores)

    def set_temporal_scores(self, temporal_scores: Dict[str, float]) -> None:
        """Pass through to multi-signal."""
        self.multisignal.set_temporal_scores(temporal_scores)
