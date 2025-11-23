"""Evaluation metrics for information retrieval."""

from typing import Dict, List, Set, Union

import numpy as np


def _get_ranked_docs(result: Union[List[str], "RetrievalResult"]) -> List[str]:
    """Extract ranked doc IDs from result (handles both list and RetrievalResult)."""
    if isinstance(result, list):
        return result
    # Handle RetrievalResult object
    return result.ranked_docs


def mean_reciprocal_rank(
    results: Dict[str, Union[List[str], "RetrievalResult"]],
    qrels: Dict[str, Dict[str, int]],
    k: int = 10,
) -> float:
    """Calculate Mean Reciprocal Rank (MRR@k).

    Args:
        results: Dict mapping query_id -> [ranked_doc_ids] or RetrievalResult
        qrels: Dict mapping query_id -> {doc_id: relevance}
        k: Cutoff rank

    Returns:
        MRR@k score
    """
    reciprocal_ranks = []

    for query_id, result in results.items():
        ranked_docs = _get_ranked_docs(result)
        if query_id not in qrels:
            continue

        relevant_docs = {
            doc_id for doc_id, rel in qrels[query_id].items() if rel > 0
        }

        # Find rank of first relevant document
        for rank, doc_id in enumerate(ranked_docs[:k], start=1):
            if doc_id in relevant_docs:
                reciprocal_ranks.append(1.0 / rank)
                break
        else:
            # No relevant document found in top-k
            reciprocal_ranks.append(0.0)

    return float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0


def ndcg_at_k(
    results: Dict[str, Union[List[str], "RetrievalResult"]],
    qrels: Dict[str, Dict[str, int]],
    k: int = 10,
) -> float:
    """Calculate Normalized Discounted Cumulative Gain (NDCG@k).

    Args:
        results: Dict mapping query_id -> [ranked_doc_ids] or RetrievalResult
        qrels: Dict mapping query_id -> {doc_id: relevance}
        k: Cutoff rank

    Returns:
        NDCG@k score
    """
    ndcg_scores = []

    for query_id, result in results.items():
        ranked_docs = _get_ranked_docs(result)
        if query_id not in qrels:
            continue

        # Get relevance scores for ranked documents
        relevances = [
            qrels[query_id].get(doc_id, 0)
            for doc_id in ranked_docs[:k]
        ]

        # Calculate DCG
        dcg = relevances[0] if relevances else 0.0
        for i, rel in enumerate(relevances[1:], start=2):
            dcg += rel / np.log2(i + 1)

        # Calculate ideal DCG (sort by relevance)
        ideal_relevances = sorted(qrels[query_id].values(), reverse=True)[:k]
        idcg = ideal_relevances[0] if ideal_relevances else 0.0
        for i, rel in enumerate(ideal_relevances[1:], start=2):
            idcg += rel / np.log2(i + 1)

        # Calculate NDCG
        if idcg > 0:
            ndcg_scores.append(dcg / idcg)
        else:
            ndcg_scores.append(0.0)

    return float(np.mean(ndcg_scores)) if ndcg_scores else 0.0


def recall_at_k(
    results: Dict[str, Union[List[str], "RetrievalResult"]],
    qrels: Dict[str, Dict[str, int]],
    k: int = 10,
) -> float:
    """Calculate Recall@k.

    Args:
        results: Dict mapping query_id -> [ranked_doc_ids] or RetrievalResult
        qrels: Dict mapping query_id -> {doc_id: relevance}
        k: Cutoff rank

    Returns:
        Recall@k score
    """
    recall_scores = []

    for query_id, result in results.items():
        ranked_docs = _get_ranked_docs(result)
        if query_id not in qrels:
            continue

        relevant_docs = {
            doc_id for doc_id, rel in qrels[query_id].items() if rel > 0
        }

        if not relevant_docs:
            continue

        # Count how many relevant docs are in top-k
        retrieved_relevant = set(ranked_docs[:k]) & relevant_docs
        recall = len(retrieved_relevant) / len(relevant_docs)
        recall_scores.append(recall)

    return float(np.mean(recall_scores)) if recall_scores else 0.0


def precision_at_k(
    results: Dict[str, Union[List[str], "RetrievalResult"]],
    qrels: Dict[str, Dict[str, int]],
    k: int = 10,
) -> float:
    """Calculate Precision@k.

    Args:
        results: Dict mapping query_id -> [ranked_doc_ids] or RetrievalResult
        qrels: Dict mapping query_id -> {doc_id: relevance}
        k: Cutoff rank

    Returns:
        Precision@k score
    """
    precision_scores = []

    for query_id, result in results.items():
        ranked_docs = _get_ranked_docs(result)
        if query_id not in qrels:
            continue

        relevant_docs = {
            doc_id for doc_id, rel in qrels[query_id].items() if rel > 0
        }

        # Count how many of top-k are relevant
        retrieved_relevant = set(ranked_docs[:k]) & relevant_docs
        precision = len(retrieved_relevant) / min(k, len(ranked_docs))
        precision_scores.append(precision)

    return float(np.mean(precision_scores)) if precision_scores else 0.0


def evaluate_all(
    results: Dict[str, Union[List[str], "RetrievalResult"]],
    qrels: Dict[str, Dict[str, int]],
    k_values: List[int] = [10],
) -> Dict[str, float]:
    """Calculate all metrics at multiple k values.

    Args:
        results: Dict mapping query_id -> [ranked_doc_ids] or RetrievalResult
        qrels: Dict mapping query_id -> {doc_id: relevance}
        k_values: List of k values to evaluate at

    Returns:
        Dict mapping metric@k -> score
    """
    metrics = {}

    for k in k_values:
        metrics[f"MRR@{k}"] = mean_reciprocal_rank(results, qrels, k)
        metrics[f"NDCG@{k}"] = ndcg_at_k(results, qrels, k)
        metrics[f"Recall@{k}"] = recall_at_k(results, qrels, k)
        metrics[f"P@{k}"] = precision_at_k(results, qrels, k)

    return metrics
