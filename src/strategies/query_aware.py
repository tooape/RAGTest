"""Query-aware retrieval strategies with v0.1/v0.2 query processing.

Wraps existing retrieval strategies with query preprocessing to test
the impact of different query understanding approaches:
- v0.1: Basic tag parsing (explicit tags only)
- v0.2: Auto tag injection, person name expansion, query signals
"""

from typing import Dict, List, Optional

from loguru import logger

from models import Embedder
from utils.query_processor import QueryProcessor, create_query_processor
from .base import RetrievalResult, RetrievalStrategy
from .multisignal import MultiSignalFusion


class QueryAwareMultiSignal(RetrievalStrategy):
    """Multi-signal retrieval with query preprocessing.

    Applies query processing (v0.1 or v0.2) before multi-signal retrieval.
    This allows testing the impact of query understanding features.
    """

    def __init__(
        self,
        embedder: Embedder,
        name: str = "multisignal_v02",
        query_version: str = "v0.2",
        vault_dir: Optional[str] = None,
        semantic_weight: float = 0.5,
        bm25_weight: float = 0.3,
        graph_weight: float = 0.15,
        temporal_weight: float = 0.05,
        **config,
    ):
        """Initialize query-aware multi-signal retrieval.

        Args:
            embedder: Embedding model
            name: Strategy name
            query_version: Query processor version ("v0.1" or "v0.2")
            vault_dir: Vault directory for person name expansion (v0.2 only)
            semantic_weight: Weight for semantic signal
            bm25_weight: Weight for BM25 signal
            graph_weight: Weight for graph signal
            temporal_weight: Weight for temporal signal
            **config: Additional configuration
        """
        super().__init__(
            name,
            query_version=query_version,
            vault_dir=vault_dir,
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            graph_weight=graph_weight,
            temporal_weight=temporal_weight,
            **config,
        )

        # Initialize query processor
        self.query_processor = create_query_processor(
            version=query_version,
            vault_dir=vault_dir,
        )

        # Initialize base multi-signal strategy
        self.multisignal = MultiSignalFusion(
            embedder=embedder,
            name=f"{name}_multisignal",
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
            graph_weight=graph_weight,
            temporal_weight=temporal_weight,
            **config,
        )

    def index(self, corpus: Dict[str, str]) -> None:
        """Index corpus with multi-signal."""
        logger.info(f"Indexing with {self.name} (query version: {self.config['query_version']})")
        self.multisignal.index(corpus)

    def search(
        self,
        query: str,
        query_id: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """Search with query preprocessing.

        Pipeline:
        1. Process query (extract tags, inject tags, expand person names)
        2. Apply tag filters to corpus if needed
        3. Run multi-signal retrieval
        4. If person name expansion: merge results from all variants
        """
        # Process query
        processed = self.query_processor.process(query)

        logger.debug(f"Query '{query}' -> text='{processed.text}', tags={processed.tags}")

        # For v0.2, try all query variants if person names were expanded
        if processed.expanded_variants and len(processed.expanded_variants) > 1:
            # Run retrieval for each variant and merge results
            all_results = []

            for variant in processed.expanded_variants:
                result = self.multisignal.search(
                    variant,
                    query_id,
                    top_k=top_k * 2,  # Get more candidates for merging
                )
                all_results.append(result)

            # Merge results (take top_k from combined, deduplicated results)
            merged = self._merge_results(all_results, top_k)

            # Add metadata about query processing
            merged.metadata.update({
                "query_version": self.config["query_version"],
                "processed_text": processed.text,
                "tags": processed.tags,
                "auto_injected": processed.auto_injected,
                "variants_used": len(processed.expanded_variants),
            })

            return merged
        else:
            # Single query (v0.1 or v0.2 without person expansion)
            search_query = processed.text

            # Add tags to query if present (for BM25 matching)
            if processed.tags:
                # Append tags as #tag to the query
                tag_str = ' '.join(f'#{tag}' for tag in processed.tags)
                search_query = f"{processed.text} {tag_str}"

            result = self.multisignal.search(
                search_query,
                query_id,
                top_k=top_k,
            )

            # Add metadata
            result.metadata.update({
                "query_version": self.config["query_version"],
                "processed_text": processed.text,
                "tags": processed.tags,
                "auto_injected": processed.auto_injected,
            })

            if processed.signals:
                result.metadata["signals"] = {
                    "is_meeting": processed.signals.is_meeting,
                    "is_1x1": processed.signals.is_1x1,
                    "is_temporal": processed.signals.is_temporal,
                    "intent": processed.signals.intent,
                }

            return result

    def _merge_results(
        self,
        results: List[RetrievalResult],
        top_k: int,
    ) -> RetrievalResult:
        """Merge results from multiple query variants.

        Uses max score across variants for each document.
        """
        if not results:
            return RetrievalResult(
                query_id=results[0].query_id if results else "",
                ranked_docs=[],
                scores=[],
                metadata={"strategy": self.name},
            )

        # Collect all documents with max score across variants
        doc_scores: Dict[str, float] = {}

        for result in results:
            for doc_id, score in zip(result.ranked_docs, result.scores):
                if doc_id not in doc_scores or score > doc_scores[doc_id]:
                    doc_scores[doc_id] = score

        # Sort by score and take top_k
        ranked_items = sorted(
            doc_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        ranked_docs = [doc_id for doc_id, _ in ranked_items]
        scores = [score for _, score in ranked_items]

        return RetrievalResult(
            query_id=results[0].query_id,
            ranked_docs=ranked_docs,
            scores=scores,
            metadata={
                "strategy": self.name,
                "merged_from": len(results),
            },
        )

    def set_graph_scores(self, graph_scores: Dict[str, float]) -> None:
        """Pass through to multi-signal."""
        self.multisignal.set_graph_scores(graph_scores)

    def set_temporal_scores(self, temporal_scores: Dict[str, float]) -> None:
        """Pass through to multi-signal."""
        self.multisignal.set_temporal_scores(temporal_scores)
