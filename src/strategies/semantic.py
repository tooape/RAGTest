"""Semantic search using dense embeddings."""

from typing import Dict

import faiss
import numpy as np
from loguru import logger

from models import Embedder
from .base import RetrievalResult, RetrievalStrategy


class SemanticSearch(RetrievalStrategy):
    """Pure semantic search using dense embeddings."""

    def __init__(
        self,
        embedder: Embedder,
        name: str = "semantic",
        use_gpu: bool = True,
        gpu_id: int = 0,
        **config,
    ):
        """Initialize semantic search.

        Args:
            embedder: Embedding model
            name: Strategy name
            use_gpu: Whether to use GPU for FAISS
            gpu_id: GPU ID to use (if use_gpu=True)
            **config: Additional configuration
        """
        super().__init__(name, **config)
        self.embedder = embedder
        self.use_gpu = use_gpu
        self.gpu_id = gpu_id
        self.index = None
        self.doc_ids = None

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus using embeddings."""
        logger.info(f"Indexing {len(corpus):,} documents with {self.name}")

        # Store document IDs in order
        self.doc_ids = list(corpus.keys())
        texts = [corpus[doc_id] for doc_id in self.doc_ids]

        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.embedder.encode(
            texts,
            batch_size=self.config.get("batch_size", 1028),
            show_progress=True,
        )

        # Build FAISS index
        logger.info("Building FAISS index...")
        embedding_dim = embeddings.shape[1]

        # Use flat L2 index (exact search)
        # For cosine similarity, embeddings should be L2-normalized
        self.index = faiss.IndexFlatIP(embedding_dim)  # Inner product (cosine)

        # Add GPU support if requested
        if self.use_gpu and faiss.get_num_gpus() > 0:
            logger.info(f"Using GPU {self.gpu_id} for FAISS")
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, self.gpu_id, self.index)

        # Add embeddings to index
        self.index.add(embeddings.astype(np.float32))

        logger.info(f"Indexed {self.index.ntotal:,} documents")

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search for query using semantic similarity."""
        if self.index is None:
            raise ValueError("Index not built. Call index() first.")

        # Encode query
        query_embedding = self.embedder.encode(
            [query],
            batch_size=1,
            show_progress=False,
        )

        # Search in FAISS index
        scores, indices = self.index.search(
            query_embedding.astype(np.float32),
            top_k,
        )

        # Convert to doc_ids and scores
        scores = scores[0].tolist()
        ranked_docs = [self.doc_ids[idx] for idx in indices[0]]

        return RetrievalResult(
            query_id=query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={"strategy": self.name},
        )

    def batch_search(
        self,
        queries: Dict[str, str],
        top_k: int = 10,
    ) -> Dict[str, RetrievalResult]:
        """Optimized batch search."""
        if self.index is None:
            raise ValueError("Index not built. Call index() first.")

        # Encode all queries at once
        query_ids = list(queries.keys())
        query_texts = [queries[qid] for qid in query_ids]

        query_embeddings = self.embedder.encode(
            query_texts,
            batch_size=self.config.get("batch_size", 1028),
            show_progress=True,
        )

        # Batch search in FAISS
        scores, indices = self.index.search(
            query_embeddings.astype(np.float32),
            top_k,
        )

        # Convert to results
        results = {}
        for i, query_id in enumerate(query_ids):
            query_scores = scores[i].tolist()
            ranked_docs = [self.doc_ids[idx] for idx in indices[i]]

            results[query_id] = RetrievalResult(
                query_id=query_id,
                ranked_docs=ranked_docs,
                scores=query_scores,
                metadata={"strategy": self.name},
            )

        return results
