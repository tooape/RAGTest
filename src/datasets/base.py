"""Base dataset interface for benchmarking."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class Document:
    """Represents a document in the corpus."""

    id: str
    text: str
    metadata: Optional[Dict] = None

    def __repr__(self) -> str:
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Document(id={self.id}, text='{preview}')"


@dataclass
class Query:
    """Represents a search query."""

    id: str
    text: str  # Original user query (conversational)
    metadata: Optional[Dict] = None
    search_query_primary: Optional[str] = None  # Primary reformulated search query
    search_query_alternate: Optional[str] = None  # Alternate reformulated search query

    def __repr__(self) -> str:
        return f"Query(id={self.id}, text='{self.text}')"

    def get_search_queries(self) -> List[str]:
        """Get all available search query variations.

        Returns:
            List of search queries, prioritizing reformulated versions if available.
        """
        queries = []
        if self.search_query_primary:
            queries.append(self.search_query_primary)
        if self.search_query_alternate:
            queries.append(self.search_query_alternate)
        if not queries:  # Fallback to original text if no reformulations
            queries.append(self.text)
        return queries


@dataclass
class QRel:
    """Query relevance judgments (ground truth)."""

    query_id: str
    doc_id: str
    relevance: int  # 0 = not relevant, 1 = relevant, 2 = highly relevant

    def __repr__(self) -> str:
        return f"QRel(query={self.query_id}, doc={self.doc_id}, rel={self.relevance})"


class Dataset(ABC):
    """Abstract base class for datasets."""

    def __init__(self, name: str):
        self.name = name
        self._corpus: Optional[Dict[str, Document]] = None
        self._queries: Optional[Dict[str, Query]] = None
        self._qrels: Optional[Dict[str, Dict[str, int]]] = None

    @abstractmethod
    def load(self) -> None:
        """Load the dataset."""
        pass

    @property
    def corpus(self) -> Dict[str, Document]:
        """Get corpus documents."""
        if self._corpus is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        return self._corpus

    @property
    def queries(self) -> Dict[str, Query]:
        """Get queries."""
        if self._queries is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        return self._queries

    @property
    def qrels(self) -> Dict[str, Dict[str, int]]:
        """Get relevance judgments.

        Returns:
            Dict mapping query_id -> {doc_id: relevance_score}
        """
        if self._qrels is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        return self._qrels

    def get_relevant_docs(self, query_id: str, min_relevance: int = 1) -> Set[str]:
        """Get relevant document IDs for a query.

        Args:
            query_id: Query identifier
            min_relevance: Minimum relevance score to consider (default: 1)

        Returns:
            Set of relevant document IDs
        """
        if query_id not in self.qrels:
            return set()
        return {
            doc_id
            for doc_id, rel in self.qrels[query_id].items()
            if rel >= min_relevance
        }

    def __repr__(self) -> str:
        if self._corpus is None:
            return f"Dataset(name={self.name}, loaded=False)"
        return (
            f"Dataset(name={self.name}, "
            f"docs={len(self.corpus)}, "
            f"queries={len(self.queries)}, "
            f"qrels={len(self.qrels)})"
        )
