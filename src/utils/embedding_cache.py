"""Embedding cache for reusing computed embeddings across runs."""

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from loguru import logger


class EmbeddingCache:
    """Cache for storing and retrieving document embeddings."""

    def __init__(self, cache_dir: str = "embedding_cache"):
        """Initialize embedding cache.

        Args:
            cache_dir: Directory to store cached embeddings
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Embedding cache: {self.cache_dir.absolute()}")

    def _get_cache_key(
        self,
        dataset_name: str,
        model_name: str,
        truncate_dim: Optional[int] = None,
    ) -> str:
        """Generate cache key from dataset and model config.

        Args:
            dataset_name: Name of the dataset
            model_name: Name of the embedding model
            truncate_dim: Matryoshka truncation dimension (if any)

        Returns:
            Cache key string
        """
        key_parts = [dataset_name, model_name]
        if truncate_dim:
            key_parts.append(f"dim{truncate_dim}")

        # Create hash of the key parts for filename safety
        key_str = "|".join(key_parts)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()[:12]

        # Use readable prefix + hash
        safe_model = model_name.replace("/", "_").replace("-", "_")
        prefix = f"{dataset_name}_{safe_model}"
        if truncate_dim:
            prefix += f"_dim{truncate_dim}"

        return f"{prefix}_{key_hash}"

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path to cache file.

        Args:
            cache_key: Cache key

        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{cache_key}.npz"

    def _get_metadata_path(self, cache_key: str) -> Path:
        """Get path to metadata file.

        Args:
            cache_key: Cache key

        Returns:
            Path to metadata file
        """
        return self.cache_dir / f"{cache_key}_meta.json"

    def exists(
        self,
        dataset_name: str,
        model_name: str,
        truncate_dim: Optional[int] = None,
    ) -> bool:
        """Check if embeddings exist in cache.

        Args:
            dataset_name: Name of the dataset
            model_name: Name of the embedding model
            truncate_dim: Matryoshka truncation dimension (if any)

        Returns:
            True if cache exists, False otherwise
        """
        cache_key = self._get_cache_key(dataset_name, model_name, truncate_dim)
        cache_path = self._get_cache_path(cache_key)
        return cache_path.exists()

    def save(
        self,
        embeddings: Dict[str, np.ndarray],
        dataset_name: str,
        model_name: str,
        truncate_dim: Optional[int] = None,
        metadata: Optional[Dict] = None,
    ) -> None:
        """Save embeddings to cache.

        Args:
            embeddings: Dict mapping doc_id -> embedding array
            dataset_name: Name of the dataset
            model_name: Name of the embedding model
            truncate_dim: Matryoshka truncation dimension (if any)
            metadata: Optional metadata to save alongside embeddings
        """
        cache_key = self._get_cache_key(dataset_name, model_name, truncate_dim)
        cache_path = self._get_cache_path(cache_key)

        # Save embeddings as compressed numpy archive
        logger.info(
            f"Saving {len(embeddings):,} embeddings to cache: {cache_path.name}"
        )

        # Convert dict to arrays for efficient storage
        doc_ids = list(embeddings.keys())
        embedding_matrix = np.stack([embeddings[doc_id] for doc_id in doc_ids])

        np.savez_compressed(
            cache_path,
            doc_ids=doc_ids,
            embeddings=embedding_matrix,
        )

        # Save metadata
        meta = {
            "dataset_name": dataset_name,
            "model_name": model_name,
            "truncate_dim": truncate_dim,
            "num_embeddings": len(embeddings),
            "embedding_dim": embedding_matrix.shape[1],
        }
        if metadata:
            meta.update(metadata)

        meta_path = self._get_metadata_path(cache_key)
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        logger.success(
            f"✓ Cached {len(embeddings):,} embeddings "
            f"({embedding_matrix.nbytes / 1024 / 1024:.1f} MB)"
        )

    def load(
        self,
        dataset_name: str,
        model_name: str,
        truncate_dim: Optional[int] = None,
    ) -> Dict[str, np.ndarray]:
        """Load embeddings from cache.

        Args:
            dataset_name: Name of the dataset
            model_name: Name of the embedding model
            truncate_dim: Matryoshka truncation dimension (if any)

        Returns:
            Dict mapping doc_id -> embedding array

        Raises:
            FileNotFoundError: If cache doesn't exist
        """
        cache_key = self._get_cache_key(dataset_name, model_name, truncate_dim)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            raise FileNotFoundError(f"Cache not found: {cache_path}")

        logger.info(f"Loading embeddings from cache: {cache_path.name}")

        # Load from compressed archive
        data = np.load(cache_path, allow_pickle=True)
        doc_ids = data["doc_ids"]
        embedding_matrix = data["embeddings"]

        # Convert back to dict
        embeddings = {
            doc_id: embedding_matrix[i] for i, doc_id in enumerate(doc_ids)
        }

        logger.success(
            f"✓ Loaded {len(embeddings):,} embeddings "
            f"({embedding_matrix.nbytes / 1024 / 1024:.1f} MB)"
        )

        return embeddings

    def get_metadata(
        self,
        dataset_name: str,
        model_name: str,
        truncate_dim: Optional[int] = None,
    ) -> Dict:
        """Get metadata for cached embeddings.

        Args:
            dataset_name: Name of the dataset
            model_name: Name of the embedding model
            truncate_dim: Matryoshka truncation dimension (if any)

        Returns:
            Metadata dict

        Raises:
            FileNotFoundError: If metadata doesn't exist
        """
        cache_key = self._get_cache_key(dataset_name, model_name, truncate_dim)
        meta_path = self._get_metadata_path(cache_key)

        if not meta_path.exists():
            raise FileNotFoundError(f"Metadata not found: {meta_path}")

        with open(meta_path) as f:
            return json.load(f)

    def clear(self) -> None:
        """Clear all cached embeddings."""
        import shutil

        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Cleared embedding cache")

    def list_caches(self) -> List[Dict]:
        """List all cached embeddings with metadata.

        Returns:
            List of metadata dicts for all caches
        """
        caches = []
        for meta_file in self.cache_dir.glob("*_meta.json"):
            with open(meta_file) as f:
                metadata = json.load(f)
                cache_file = meta_file.parent / meta_file.name.replace(
                    "_meta.json", ".npz"
                )
                if cache_file.exists():
                    metadata["cache_file"] = cache_file.name
                    metadata["size_mb"] = cache_file.stat().st_size / 1024 / 1024
                    caches.append(metadata)

        return caches
