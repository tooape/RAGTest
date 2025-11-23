"""Reranking models for two-stage retrieval."""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import torch
from loguru import logger
from sentence_transformers import CrossEncoder


class Reranker(ABC):
    """Abstract base class for rerankers."""

    def __init__(self, model_name: str, device: Optional[str] = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    @abstractmethod
    def rerank(
        self,
        query: str,
        documents: List[Tuple[str, str]],  # [(doc_id, text), ...]
        top_k: Optional[int] = None,
    ) -> List[Tuple[str, float]]:
        """Rerank documents for a query.

        Args:
            query: Query text
            documents: List of (doc_id, text) tuples
            top_k: Number of results to return (None = all)

        Returns:
            List of (doc_id, score) tuples, sorted by score descending
        """
        pass


class CrossEncoderReranker(Reranker):
    """Reranker using cross-encoder models."""

    def __init__(
        self,
        model_name: str,
        device: Optional[str] = None,
        batch_size: int = 1028,
    ):
        """Initialize cross-encoder reranker.

        Args:
            model_name: Name of cross-encoder model
            device: Device to run on
            batch_size: Batch size for inference
        """
        super().__init__(model_name, device)
        self.batch_size = batch_size

        logger.info(f"Loading reranker: {model_name} on {self.device}")
        self.model = CrossEncoder(model_name, device=self.device)

        # Enable mixed precision (FP16) for CUDA devices
        if self.device == "cuda":
            logger.info("Enabling mixed precision (FP16) for reranker")
            self.model.model = self.model.model.half()

    def rerank(
        self,
        query: str,
        documents: List[Tuple[str, str]],
        top_k: Optional[int] = None,
    ) -> List[Tuple[str, float]]:
        """Rerank documents using cross-encoder."""
        if not documents:
            return []

        # Extract doc_ids and texts
        doc_ids = [doc_id for doc_id, _ in documents]
        texts = [text for _, text in documents]

        # Create query-document pairs
        pairs = [[query, text] for text in texts]

        # Get scores from cross-encoder
        scores = self.model.predict(
            pairs,
            batch_size=self.batch_size,
            show_progress_bar=False,
        )

        # Combine doc_ids with scores and sort
        results = list(zip(doc_ids, scores))
        results.sort(key=lambda x: x[1], reverse=True)

        # Return top-k if specified
        if top_k is not None:
            results = results[:top_k]

        return results


class MixedbreadReranker(CrossEncoderReranker):
    """Mixedbread reranker wrapper."""

    def __init__(
        self,
        model_variant: str = "xsmall-v1",
        device: Optional[str] = None,
        batch_size: int = 1028,
    ):
        """Initialize Mixedbread reranker.

        Args:
            model_variant: Model variant ('xsmall-v1', 'base-v2')
            device: Device to run on
            batch_size: Batch size for inference
        """
        if model_variant == "xsmall-v1":
            model_name = "mixedbread-ai/mxbai-rerank-xsmall-v1"
        elif model_variant == "base-v2":
            model_name = "mixedbread-ai/mxbai-rerank-base-v2"
        else:
            raise ValueError(f"Unknown variant: {model_variant}")

        super().__init__(
            model_name=model_name,
            device=device,
            batch_size=batch_size,
        )


def create_reranker(
    model_type: str,
    device: Optional[str] = None,
    **kwargs,
) -> Reranker:
    """Factory function to create rerankers.

    Args:
        model_type: Type of reranker ('mixedbread-xsmall', 'mixedbread-base', or model name)
        device: Device to run on
        **kwargs: Additional arguments

    Returns:
        Reranker instance
    """
    if model_type == "mixedbread-xsmall":
        return MixedbreadReranker(model_variant="xsmall-v1", device=device, **kwargs)
    elif model_type == "mixedbread-base":
        return MixedbreadReranker(model_variant="base-v2", device=device, **kwargs)
    else:
        # Assume it's a cross-encoder model name
        return CrossEncoderReranker(model_name=model_type, device=device, **kwargs)
