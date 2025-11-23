"""BM25 lexical search implementation."""

from typing import Dict, List, Tuple

import numpy as np
from loguru import logger
from rank_bm25 import BM25Okapi


class BM25Searcher:
    """BM25 lexical searcher."""

    def __init__(
        self,
        corpus: Dict[str, str],
        k1: float = 1.2,
        b: float = 0.75,
    ):
        """Initialize BM25 searcher.

        Args:
            corpus: Dict mapping doc_id -> text
            k1: Term frequency saturation parameter
            b: Length normalization parameter
        """
        self.k1 = k1
        self.b = b
        self.doc_ids = list(corpus.keys())

        logger.info(f"Building BM25 index (k1={k1}, b={b})...")

        # Tokenize corpus
        tokenized_corpus = [self._tokenize(corpus[doc_id]) for doc_id in self.doc_ids]

        # Build BM25 index
        self.bm25 = BM25Okapi(tokenized_corpus, k1=k1, b=b)

        logger.info(f"BM25 index built for {len(self.doc_ids):,} documents")

    def _tokenize(self, text: str) -> List[str]:
        """Simple whitespace tokenization.

        For better results, could use:
        - Lowercase normalization
        - Stemming/lemmatization
        - Stopword removal
        - Subword tokenization
        """
        return text.lower().split()

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> List[Tuple[str, float]]:
        """Search for query using BM25.

        Args:
            query: Query text
            top_k: Number of results to return

        Returns:
            List of (doc_id, score) tuples, sorted by score descending
        """
        # Tokenize query
        tokenized_query = self._tokenize(query)

        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)

        # Get top-k indices
        top_indices = np.argsort(scores)[::-1][:top_k]

        # Return doc_ids and scores
        results = [
            (self.doc_ids[idx], float(scores[idx]))
            for idx in top_indices
        ]

        return results

    def batch_search(
        self,
        queries: List[str],
        top_k: int = 10,
    ) -> List[List[Tuple[str, float]]]:
        """Batch search for multiple queries.

        Args:
            queries: List of query texts
            top_k: Number of results per query

        Returns:
            List of result lists, one per query
        """
        return [self.search(query, top_k) for query in queries]
