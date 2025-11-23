"""Base retrieval strategy interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class RetrievalResult:
    """Result from a retrieval strategy."""

    query_id: str
    ranked_docs: List[str]  # Ordered list of doc_ids
    scores: List[float]  # Corresponding scores
    metadata: Optional[Dict] = None  # Strategy-specific metadata

    def to_ranked_list(self, k: Optional[int] = None) -> List[str]:
        """Get top-k ranked document IDs.

        Args:
            k: Number of results to return (None = all)

        Returns:
            List of doc_ids
        """
        if k is None:
            return self.ranked_docs
        return self.ranked_docs[:k]


class RetrievalStrategy(ABC):
    """Abstract base class for retrieval strategies."""

    def __init__(self, name: str, **config):
        """Initialize strategy.

        Args:
            name: Strategy name
            **config: Configuration parameters
        """
        self.name = name
        self.config = config

    @abstractmethod
    def index(self, corpus: Dict[str, str]) -> None:
        """Index the corpus.

        Args:
            corpus: Dict mapping doc_id -> text
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search for a single query.

        Args:
            query: Query text
            query_id: Query identifier
            top_k: Number of results to return

        Returns:
            RetrievalResult
        """
        pass

    def batch_search(
        self,
        queries: Dict,
        top_k: int = 10,
        query_variant: str = "primary",
    ) -> Dict[str, RetrievalResult]:
        """Search for multiple queries.

        Args:
            queries: Dict mapping query_id -> text (str) or query_id -> Query object
            top_k: Number of results per query
            query_variant: Which query variant to use ('primary', 'alternate', or 'original')
                          Only applies when queries are Query objects with reformulations

        Returns:
            Dict mapping query_id -> RetrievalResult
        """
        from datasets.base import Query  # Import here to avoid circular dependency

        results = {}
        for query_id, query in queries.items():
            # Handle both str and Query objects
            if isinstance(query, str):
                query_text = query
            elif isinstance(query, Query):
                # Use specified variant
                if query_variant == "primary" and query.search_query_primary:
                    query_text = query.search_query_primary
                elif query_variant == "alternate" and query.search_query_alternate:
                    query_text = query.search_query_alternate
                else:
                    query_text = query.text  # Fallback to original
            else:
                raise TypeError(f"Expected str or Query, got {type(query)}")

            results[query_id] = self.search(query_text, query_id, top_k)
        return results

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"


def normalize_scores(scores: np.ndarray, method: str = "min-max") -> np.ndarray:
    """Normalize scores to [0, 1] range.

    Args:
        scores: Array of scores
        method: Normalization method ('min-max', 'z-score', 'rank')

    Returns:
        Normalized scores
    """
    if len(scores) == 0:
        return scores

    if method == "min-max":
        min_score = scores.min()
        max_score = scores.max()
        if max_score - min_score > 0:
            return (scores - min_score) / (max_score - min_score)
        return np.ones_like(scores)

    elif method == "z-score":
        mean = scores.mean()
        std = scores.std()
        if std > 0:
            z_scores = (scores - mean) / std
            # Convert to [0, 1] using sigmoid
            return 1 / (1 + np.exp(-z_scores))
        return np.ones_like(scores)

    elif method == "rank":
        # Rank normalization: best rank = 1.0, worst = 0.0
        ranks = np.argsort(np.argsort(-scores))  # Lower rank = better
        return 1 - (ranks / len(ranks))

    else:
        raise ValueError(f"Unknown normalization method: {method}")
