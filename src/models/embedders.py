"""Embedding models for semantic search."""

from abc import ABC, abstractmethod
from typing import List, Optional

import numpy as np
import torch
from loguru import logger
from sentence_transformers import SentenceTransformer


class Embedder(ABC):
    """Abstract base class for embedding models."""

    def __init__(self, model_name: str, device: Optional[str] = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    @abstractmethod
    def encode(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = True,
    ) -> np.ndarray:
        """Encode texts to embeddings.

        Args:
            texts: List of texts to encode
            batch_size: Batch size for encoding
            show_progress: Whether to show progress bar

        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        pass

    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        """Get embedding dimension."""
        pass


class SentenceTransformerEmbedder(Embedder):
    """Embedder using Sentence Transformers library."""

    def __init__(
        self,
        model_name: str,
        device: Optional[str] = None,
        truncate_dim: Optional[int] = None,
    ):
        """Initialize SentenceTransformer embedder.

        Args:
            model_name: Name of the sentence-transformers model
            device: Device to run on ('cuda' or 'cpu')
            truncate_dim: Matryoshka dimension to truncate to (optional)
        """
        super().__init__(model_name, device)
        self.truncate_dim = truncate_dim

        logger.info(f"Loading model: {model_name} on {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)

        # Get native embedding dimension
        self._native_dim = self.model.get_sentence_embedding_dimension()

        if truncate_dim:
            if truncate_dim > self._native_dim:
                raise ValueError(
                    f"truncate_dim ({truncate_dim}) cannot be larger than "
                    f"native dimension ({self._native_dim})"
                )
            logger.info(
                f"Using Matryoshka truncation: {self._native_dim} -> {truncate_dim}"
            )

    def encode(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = True,
    ) -> np.ndarray:
        """Encode texts using SentenceTransformer."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True,  # L2 normalization for cosine similarity
        )

        # Apply Matryoshka truncation if specified
        if self.truncate_dim:
            embeddings = embeddings[:, : self.truncate_dim]
            # Renormalize after truncation
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / (norms + 1e-8)

        return embeddings

    @property
    def embedding_dim(self) -> int:
        """Get effective embedding dimension."""
        return self.truncate_dim if self.truncate_dim else self._native_dim


class GemmaEmbedder(SentenceTransformerEmbedder):
    """EmbeddingGemma wrapper for convenience."""

    def __init__(
        self,
        device: Optional[str] = None,
        truncate_dim: Optional[int] = 256,
    ):
        """Initialize EmbeddingGemma.

        Args:
            device: Device to run on
            truncate_dim: Matryoshka dimension (default: 256)
        """
        super().__init__(
            model_name="google/embedding-gemma-001",
            device=device,
            truncate_dim=truncate_dim,
        )


class MixedbreadEmbedder(SentenceTransformerEmbedder):
    """Mixedbread embeddings wrapper."""

    def __init__(
        self,
        model_variant: str = "large",
        device: Optional[str] = None,
        truncate_dim: Optional[int] = None,
    ):
        """Initialize Mixedbread embedder.

        Args:
            model_variant: Model variant ('large' or 'base')
            device: Device to run on
            truncate_dim: Matryoshka dimension (optional)
        """
        if model_variant == "large":
            model_name = "mixedbread-ai/mxbai-embed-large-v1"
        elif model_variant == "base":
            model_name = "mixedbread-ai/mxbai-embed-base-v1"
        else:
            raise ValueError(f"Unknown variant: {model_variant}")

        super().__init__(
            model_name=model_name,
            device=device,
            truncate_dim=truncate_dim,
        )


def create_embedder(
    model_type: str,
    device: Optional[str] = None,
    **kwargs,
) -> Embedder:
    """Factory function to create embedders.

    Args:
        model_type: Type of embedder ('gemma', 'mixedbread', or model name)
        device: Device to run on
        **kwargs: Additional arguments for the embedder

    Returns:
        Embedder instance
    """
    if model_type == "gemma":
        return GemmaEmbedder(device=device, **kwargs)
    elif model_type == "mixedbread":
        return MixedbreadEmbedder(device=device, **kwargs)
    else:
        # Assume it's a sentence-transformers model name
        return SentenceTransformerEmbedder(
            model_name=model_type,
            device=device,
            **kwargs,
        )
