#!/usr/bin/env python3
"""Smoke test to validate benchmarking framework before full run.

Quick validation on synthetic data:
- Tests all strategies run without errors
- Validates output format correctness
- Verifies metrics calculation
- Tests optimization on tiny grid
- Should complete in < 2 minutes

Run this before committing to full dataset benchmark.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import time

from loguru import logger

from datasets.base import Document, QRels, Queries
from evaluation.evaluator import Evaluator
from evaluation.metrics import mean_reciprocal_rank, ndcg_at_k, precision_at_k
from models.embedders import SentenceTransformerEmbedder
from models.rerankers import CrossEncoderReranker
from optimization.grid_search import GridSearchOptimizer
from strategies import (
    BM25Strategy,
    MultiSignalFusion,
    RRFHybrid,
    SemanticSearch,
    TwoStageReranking,
    WeightedHybrid,
)

logger.info("Starting smoke test...")


# ============================================================================
# Synthetic test data
# ============================================================================

CORPUS = {
    "doc1": "Machine learning is a subset of artificial intelligence.",
    "doc2": "Deep learning uses neural networks with multiple layers.",
    "doc3": "Natural language processing enables computers to understand text.",
    "doc4": "Computer vision allows machines to interpret visual information.",
    "doc5": "Reinforcement learning teaches agents through rewards and penalties.",
    "doc6": "Python is a popular programming language for data science.",
    "doc7": "TensorFlow and PyTorch are deep learning frameworks.",
    "doc8": "Data preprocessing is crucial for machine learning success.",
    "doc9": "Feature engineering improves model performance.",
    "doc10": "Model evaluation requires proper metrics and validation.",
}

QUERIES = {
    "q1": "What is deep learning?",
    "q2": "How does reinforcement learning work?",
    "q3": "What tools are used for machine learning?",
}

QRELS = {
    "q1": {"doc2": 1, "doc7": 1},  # Deep learning
    "q2": {"doc5": 1},  # Reinforcement learning
    "q3": {"doc6": 1, "doc7": 1, "doc8": 1},  # ML tools
}


# ============================================================================
# Test 1: Model loading
# ============================================================================

logger.info("Test 1: Loading models...")

try:
    embedder = SentenceTransformerEmbedder(
        model_name="mixedbread-ai/mxbai-embed-xsmall-v1",
        truncate_dim=256,  # Small for smoke test
    )
    logger.success("✓ Embedder loaded")
except Exception as e:
    logger.error(f"✗ Embedder failed: {e}")
    sys.exit(1)

try:
    reranker = CrossEncoderReranker(
        model_name="mixedbread-ai/mxbai-rerank-xsmall-v1",
    )
    logger.success("✓ Reranker loaded")
except Exception as e:
    logger.error(f"✗ Reranker failed: {e}")
    sys.exit(1)


# ============================================================================
# Test 2: Retrieval strategies
# ============================================================================

logger.info("\nTest 2: Testing retrieval strategies...")

strategies_to_test = [
    ("SemanticSearch", SemanticSearch(embedder)),
    ("BM25", BM25Strategy()),
    ("WeightedHybrid", WeightedHybrid(embedder)),
    ("RRF", RRFHybrid(embedder)),
    ("MultiSignal", MultiSignalFusion(embedder, graph_enabled=False, temporal_enabled=False)),
    ("TwoStage", TwoStageReranking(embedder, reranker, stage1_k=5)),
]

results = {}

for strategy_name, strategy in strategies_to_test:
    try:
        logger.info(f"  Testing {strategy_name}...")

        # Index corpus
        start = time.time()
        strategy.index(CORPUS)
        index_time = time.time() - start

        # Run queries
        start = time.time()
        strategy_results = {}
        for qid, query in QUERIES.items():
            result = strategy.search(query, qid, top_k=3)
            strategy_results[qid] = result

            # Validate result format
            assert len(result.ranked_docs) <= 3, "top_k not respected"
            assert len(result.ranked_docs) == len(result.scores), "Mismatched docs/scores"
            assert all(
                doc_id in CORPUS for doc_id in result.ranked_docs
            ), "Invalid doc_id returned"

        query_time = time.time() - start

        results[strategy_name] = strategy_results

        logger.success(
            f"  ✓ {strategy_name}: indexed in {index_time:.2f}s, "
            f"queried in {query_time:.2f}s"
        )

    except Exception as e:
        logger.error(f"  ✗ {strategy_name} failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


# ============================================================================
# Test 3: Evaluation metrics
# ============================================================================

logger.info("\nTest 3: Testing evaluation metrics...")

try:
    # Test MRR
    mrr = mean_reciprocal_rank(results["SemanticSearch"], QRELS, k=10)
    assert 0 <= mrr <= 1, f"MRR out of range: {mrr}"
    logger.success(f"  ✓ MRR@10: {mrr:.3f}")

    # Test NDCG
    ndcg = ndcg_at_k(results["SemanticSearch"], QRELS, k=10)
    assert 0 <= ndcg <= 1, f"NDCG out of range: {ndcg}"
    logger.success(f"  ✓ NDCG@10: {ndcg:.3f}")

    # Test Precision
    prec = precision_at_k(results["SemanticSearch"], QRELS, k=10)
    assert 0 <= prec <= 1, f"Precision out of range: {prec}"
    logger.success(f"  ✓ Precision@10: {prec:.3f}")

except Exception as e:
    logger.error(f"  ✗ Metrics failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# Test 4: Evaluator
# ============================================================================

logger.info("\nTest 4: Testing evaluator...")

try:
    evaluator = Evaluator(metrics=["mrr@10", "ndcg@10", "precision@10"])

    for strategy_name, strategy_results in results.items():
        eval_results = evaluator.evaluate(
            results=strategy_results,
            qrels=QRELS,
            dataset_name="smoke_test",
            strategy_name=strategy_name,
        )

        logger.success(
            f"  ✓ {strategy_name}: "
            f"MRR={eval_results.metrics['mrr@10']:.3f}, "
            f"NDCG={eval_results.metrics['ndcg@10']:.3f}"
        )

except Exception as e:
    logger.error(f"  ✗ Evaluator failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# Test 5: Grid search optimization
# ============================================================================

logger.info("\nTest 5: Testing grid search optimization...")

try:
    # Tiny grid for smoke test
    param_space = {
        "semantic_weight": [0.5, 0.7],
        "bm25_weight": [0.3, 0.5],
    }

    optimizer = GridSearchOptimizer(param_space)

    # Test iteration
    tested_configs = []
    for params in optimizer:
        tested_configs.append(params)

        # Create strategy with these params
        strategy = WeightedHybrid(
            embedder,
            semantic_weight=params["semantic_weight"],
            bm25_weight=params["bm25_weight"],
        )

        # Quick evaluation
        strategy.index(CORPUS)
        strategy_results = {}
        for qid, query in QUERIES.items():
            strategy_results[qid] = strategy.search(query, qid, top_k=3)

        # Calculate score
        ndcg = ndcg_at_k(strategy_results, QRELS, k=10)

        # Report to optimizer
        optimizer.report(params, ndcg)

    assert len(tested_configs) == 4, "Grid size mismatch"

    best = optimizer.get_best()
    logger.success(
        f"  ✓ Grid search: tested {len(tested_configs)} configs, "
        f"best NDCG={best['score']:.3f}"
    )

except Exception as e:
    logger.error(f"  ✗ Grid search failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# Test 6: Batch search
# ============================================================================

logger.info("\nTest 6: Testing batch search...")

try:
    strategy = SemanticSearch(embedder)
    strategy.index(CORPUS)

    batch_results = strategy.batch_search(QUERIES, top_k=3)

    assert len(batch_results) == len(QUERIES), "Batch size mismatch"
    for qid, result in batch_results.items():
        assert qid in QUERIES, f"Unknown query ID: {qid}"
        assert len(result.ranked_docs) <= 3, "top_k not respected"

    logger.success(f"  ✓ Batch search: processed {len(QUERIES)} queries")

except Exception as e:
    logger.error(f"  ✗ Batch search failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# Summary
# ============================================================================

logger.info("\n" + "=" * 80)
logger.success("✓ ALL SMOKE TESTS PASSED")
logger.info("=" * 80)
logger.info("Framework is ready for full benchmark runs!")
logger.info("\nNext steps:")
logger.info("  1. Run full BEIR benchmarks: python scripts/run_benchmark.py --dataset nq")
logger.info("  2. Run vault benchmark: python scripts/run_benchmark.py --dataset vault")
logger.info("  3. Run hyperparameter optimization")
