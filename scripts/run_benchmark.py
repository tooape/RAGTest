#!/usr/bin/env python3
"""Main benchmark runner for RAG evaluation.

Orchestrates full benchmarking pipeline:
- Loads datasets (BEIR or Vault)
- Initializes retrieval strategies
- Runs experiments with optional hyperparameter optimization
- Caches embeddings for reuse
- Tracks and saves results

Usage:
    # Run on specific dataset
    python run_benchmark.py --dataset nq --strategies semantic bm25 weighted

    # Run hyperparameter optimization
    python run_benchmark.py --dataset vault --optimize --n-trials 50

    # Run all strategies on all datasets
    python run_benchmark.py --all

    # Resume from cached embeddings
    python run_benchmark.py --dataset nq --cache-dir cache/nq
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import torch
from loguru import logger

from datasets.beir_loader import BEIRDataset
from datasets.vault_loader import VaultDataset
from evaluation.evaluator import Evaluator
from models.embedders import SentenceTransformerEmbedder
from models.rerankers import CrossEncoderReranker
from optimization.bayesian import BayesianOptimizer
from optimization.grid_search import GridSearchOptimizer, coarse_grid
from strategies import (
    BM25Strategy,
    DynamicChunkingMultiSignal,
    MultiSignalFusion,
    MultiSignalWithReranking,
    RRFHybrid,
    SemanticSearch,
    TwoStageReranking,
    WeightedHybrid,
)
from utils.chunker import SemanticChunker, SentenceAwareChunker, SlidingWindowChunker
from utils.results import ResultsTracker
from utils.gpu_manager import get_gpu_manager
from utils.parallel_executor import StrategyExecutor


# ============================================================================
# Configuration
# ============================================================================

DATASET_CONFIGS = {
    "nq": {
        "loader": BEIRDataset,
        "path": "beir_datasets/nq",
        "name": "nq",
        "graph_enabled": False,
        "temporal_enabled": False,
    },
    "hotpotqa": {
        "loader": BEIRDataset,
        "path": "beir_datasets/hotpotqa",
        "name": "hotpotqa",
        "graph_enabled": False,
        "temporal_enabled": False,
    },
    "vault": {
        "loader": VaultDataset,
        "path": "vault copy",
        "qrels_path": "vault copy/test_qrels.json",
        "graph_enabled": True,
        "temporal_enabled": True,
    },
}

EMBEDDING_MODELS = {
    "gemma-256": ("google/embedding-gemma-2b", 256),
    "gemma-512": ("google/embedding-gemma-2b", 512),
    "gemma-768": ("google/embedding-gemma-2b", 768),
    "mxbai-large-256": ("mixedbread-ai/mxbai-embed-large-v1", 256),
    "mxbai-large-512": ("mixedbread-ai/mxbai-embed-large-v1", 512),
}

RERANKER_MODELS = {
    "mxbai-xsmall": "mixedbread-ai/mxbai-rerank-xsmall-v1",
    "mxbai-base": "mixedbread-ai/mxbai-rerank-base-v2",
}

STRATEGY_CONFIGS = {
    "semantic": {
        "class": SemanticSearch,
        "requires": ["embedder"],
    },
    "bm25": {
        "class": BM25Strategy,
        "requires": [],
    },
    "weighted": {
        "class": WeightedHybrid,
        "requires": ["embedder"],
    },
    "rrf": {
        "class": RRFHybrid,
        "requires": ["embedder"],
    },
    "multisignal": {
        "class": MultiSignalFusion,
        "requires": ["embedder"],
    },
    "two_stage": {
        "class": TwoStageReranking,
        "requires": ["embedder", "reranker"],
    },
    "multisignal_reranked": {
        "class": MultiSignalWithReranking,
        "requires": ["embedder", "reranker"],
    },
    "dynamic_chunking_sliding": {
        "class": DynamicChunkingMultiSignal,
        "requires": ["embedder"],
        "chunker_class": SlidingWindowChunker,
    },
    "dynamic_chunking_sentence": {
        "class": DynamicChunkingMultiSignal,
        "requires": ["embedder"],
        "chunker_class": SentenceAwareChunker,
    },
    "dynamic_chunking_semantic": {
        "class": DynamicChunkingMultiSignal,
        "requires": ["embedder"],
        "chunker_class": SemanticChunker,
    },
}


# ============================================================================
# Dataset Loading
# ============================================================================


def load_dataset(dataset_name: str):
    """Load dataset by name."""
    if dataset_name not in DATASET_CONFIGS:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    config = DATASET_CONFIGS[dataset_name]
    logger.info(f"Loading {dataset_name} dataset from {config['path']}...")

    if config["loader"] == VaultDataset:
        dataset = VaultDataset(
            vault_path=config["path"],
            qrels_path=config.get("qrels_path"),
        )
    else:
        dataset = BEIRDataset(
            dataset_path=config["path"],
            name=config["name"],
        )

    dataset.load()

    logger.info(
        f"Loaded {dataset_name}: "
        f"{len(dataset.corpus):,} docs, "
        f"{len(dataset.queries):,} queries"
    )

    return dataset, config


# ============================================================================
# Model Initialization
# ============================================================================


def init_models(
    embedder_name: str = "mxbai-large-256",
    reranker_name: str = "mxbai-xsmall",
    gpu_id: int = None,
):
    """Initialize embedding and reranking models.

    Args:
        embedder_name: Name of the embedding model
        reranker_name: Name of the reranker model
        gpu_id: GPU ID to use (None for auto-detection)
    """
    logger.info(f"Initializing models: {embedder_name}, {reranker_name}...")

    # Determine device
    device = None
    if gpu_id is not None:
        device = f"cuda:{gpu_id}"
        logger.info(f"Using GPU {gpu_id}")

    # Embedder
    if embedder_name not in EMBEDDING_MODELS:
        raise ValueError(f"Unknown embedder: {embedder_name}")

    model_name, truncate_dim = EMBEDDING_MODELS[embedder_name]
    embedder = SentenceTransformerEmbedder(
        model_name=model_name,
        truncate_dim=truncate_dim,
        device=device,
    )

    logger.success(f"✓ Loaded embedder: {embedder_name}")

    # Reranker
    if reranker_name not in RERANKER_MODELS:
        raise ValueError(f"Unknown reranker: {reranker_name}")

    reranker = CrossEncoderReranker(
        model_name=RERANKER_MODELS[reranker_name],
        device=device,
    )

    logger.success(f"✓ Loaded reranker: {reranker_name}")

    return embedder, reranker


# ============================================================================
# Strategy Initialization
# ============================================================================


def init_strategy(
    strategy_name: str,
    embedder=None,
    reranker=None,
    graph_enabled: bool = True,
    temporal_enabled: bool = True,
    use_gpu: bool = False,
    gpu_id: int = 0,
    **params,
):
    """Initialize retrieval strategy.

    Args:
        strategy_name: Name of the strategy
        embedder: Embedding model
        reranker: Reranker model
        graph_enabled: Enable graph signals
        temporal_enabled: Enable temporal signals
        use_gpu: Enable GPU for FAISS (semantic search)
        gpu_id: GPU ID to use for FAISS
        **params: Additional strategy parameters
    """
    if strategy_name not in STRATEGY_CONFIGS:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    config = STRATEGY_CONFIGS[strategy_name]
    strategy_class = config["class"]

    # Check requirements
    if "embedder" in config["requires"] and embedder is None:
        raise ValueError(f"Strategy {strategy_name} requires embedder")
    if "reranker" in config["requires"] and reranker is None:
        raise ValueError(f"Strategy {strategy_name} requires reranker")

    # Build kwargs
    kwargs = {"name": strategy_name}

    if "embedder" in config["requires"]:
        kwargs["embedder"] = embedder
    if "reranker" in config["requires"]:
        kwargs["reranker"] = reranker

    # Add graph/temporal config for multi-signal strategies
    if strategy_name in ["multisignal", "multisignal_reranked"]:
        kwargs["graph_enabled"] = graph_enabled
        kwargs["temporal_enabled"] = temporal_enabled

    # Add chunker for dynamic chunking strategies
    if "chunker_class" in config:
        chunker_class = config["chunker_class"]
        # Pass embedder to SemanticChunker if needed
        if chunker_class == SemanticChunker:
            chunker = chunker_class(embedder=embedder)
        else:
            chunker = chunker_class()
        kwargs["chunker"] = chunker
        kwargs["graph_enabled"] = graph_enabled
        kwargs["temporal_enabled"] = temporal_enabled

    # Add GPU config for semantic search strategies
    if strategy_name == "semantic" or strategy_name.startswith("dynamic_chunking"):
        kwargs["use_gpu"] = use_gpu
        kwargs["gpu_id"] = gpu_id

    # Add custom params
    kwargs.update(params)

    strategy = strategy_class(**kwargs)
    return strategy


# ============================================================================
# Benchmark Execution
# ============================================================================


def run_single_experiment(
    strategy_name: str,
    dataset_name: str,
    dataset,
    embedder,
    reranker,
    graph_enabled: bool,
    temporal_enabled: bool,
    params: Dict = None,
    evaluator: Evaluator = None,
    use_gpu: bool = False,
    gpu_id: int = 0,
):
    """Run single experiment with given configuration.

    Args:
        strategy_name: Name of the strategy
        dataset_name: Name of the dataset
        dataset: Dataset object
        embedder: Embedding model
        reranker: Reranker model
        graph_enabled: Enable graph signals
        temporal_enabled: Enable temporal signals
        params: Strategy parameters
        evaluator: Evaluator instance
        use_gpu: Enable GPU for FAISS
        gpu_id: GPU ID to use
    """
    if params is None:
        params = {}

    if evaluator is None:
        evaluator = Evaluator()

    # Initialize strategy
    strategy = init_strategy(
        strategy_name,
        embedder=embedder,
        reranker=reranker,
        graph_enabled=graph_enabled,
        temporal_enabled=temporal_enabled,
        use_gpu=use_gpu,
        gpu_id=gpu_id,
        **params,
    )

    # Index corpus
    logger.info(f"Indexing corpus for {strategy_name}...")
    start = time.time()
    strategy.index(dataset.corpus)
    index_time = time.time() - start
    logger.info(f"Indexed in {index_time:.1f}s")

    # Run queries (batch)
    logger.info(f"Running {len(dataset.queries):,} queries...")
    start = time.time()
    results = strategy.batch_search(dataset.queries, top_k=10)
    query_time = time.time() - start

    avg_latency = (query_time * 1000) / len(dataset.queries)
    logger.info(f"Queried in {query_time:.1f}s ({avg_latency:.1f}ms/query)")

    # Evaluate
    eval_results = evaluator.evaluate(
        results=results,
        qrels=dataset.qrels,
        dataset_name=dataset_name,
        strategy_name=strategy_name,
    )

    # Add latency to metadata
    eval_results.metadata["latency_ms"] = avg_latency
    eval_results.metadata["index_time_s"] = index_time

    return eval_results


# ============================================================================
# Hyperparameter Optimization
# ============================================================================


def optimize_hyperparameters(
    strategy_name: str,
    dataset_name: str,
    dataset,
    embedder,
    reranker,
    graph_enabled: bool,
    temporal_enabled: bool,
    method: str = "grid",
    n_trials: int = 30,
):
    """Run hyperparameter optimization."""
    logger.info(f"\nOptimizing {strategy_name} on {dataset_name} using {method}...")

    # Define parameter space (example for weighted hybrid)
    if strategy_name == "weighted":
        param_space = {
            "semantic_weight": [0.3, 0.5, 0.7, 0.9],
            "bm25_weight": [0.1, 0.3, 0.5, 0.7],
            "normalization": ["min-max", "z-score"],
        }
    elif strategy_name == "multisignal":
        param_space = {
            "semantic_weight": [0.3, 0.5, 0.7],
            "bm25_weight": [0.2, 0.3, 0.4],
            "graph_weight": [0.05, 0.15, 0.25] if graph_enabled else [0.0],
            "temporal_weight": [0.05, 0.1] if temporal_enabled else [0.0],
            "normalization": ["min-max", "z-score"],
        }
    else:
        logger.warning(f"No param space defined for {strategy_name}, using defaults")
        return None

    # Create evaluator
    evaluator = Evaluator()

    # Objective function
    def objective(params):
        eval_results = run_single_experiment(
            strategy_name=strategy_name,
            dataset_name=dataset_name,
            dataset=dataset,
            embedder=embedder,
            reranker=reranker,
            graph_enabled=graph_enabled,
            temporal_enabled=temporal_enabled,
            params=params,
            evaluator=evaluator,
        )

        # Optimize for NDCG@10
        return eval_results.metrics["ndcg@10"]

    # Run optimization
    if method == "grid":
        optimizer = GridSearchOptimizer(param_space)

        for params in optimizer:
            score = objective(params)
            optimizer.report(params, score)

            if optimizer.should_stop():
                logger.info("Early stopping triggered")
                break

        best = optimizer.get_best()

    elif method == "bayesian":
        # Convert to Bayesian format
        bayesian_space = {}
        for name, values in param_space.items():
            if isinstance(values[0], str):
                bayesian_space[name] = ("categorical", values)
            else:
                bayesian_space[name] = ("continuous", min(values), max(values))

        optimizer = BayesianOptimizer(
            param_space=bayesian_space,
            n_trials=n_trials,
            direction="maximize",
        )

        best = optimizer.optimize(objective)

    else:
        raise ValueError(f"Unknown optimization method: {method}")

    logger.success(
        f"✓ Optimization complete: best {best['score']:.4f} "
        f"with params {best['params']}"
    )

    return best


# ============================================================================
# Main
# ============================================================================


def main():
    parser = argparse.ArgumentParser(description="Run RAG benchmarks")

    # Dataset selection
    parser.add_argument(
        "--dataset",
        choices=["nq", "hotpotqa", "vault", "all"],
        default="vault",
        help="Dataset to benchmark",
    )

    # Strategy selection
    parser.add_argument(
        "--strategies",
        nargs="+",
        choices=list(STRATEGY_CONFIGS.keys()) + ["all"],
        default=["all"],
        help="Strategies to test",
    )

    # Model selection
    parser.add_argument(
        "--embedder",
        choices=list(EMBEDDING_MODELS.keys()),
        default="mxbai-large-256",
        help="Embedding model",
    )

    parser.add_argument(
        "--reranker",
        choices=list(RERANKER_MODELS.keys()),
        default="mxbai-xsmall",
        help="Reranker model",
    )

    # Optimization
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Run hyperparameter optimization",
    )

    parser.add_argument(
        "--optimize-method",
        choices=["grid", "bayesian"],
        default="grid",
        help="Optimization method",
    )

    parser.add_argument(
        "--n-trials",
        type=int,
        default=30,
        help="Number of optimization trials",
    )

    # Output
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Output directory for results",
    )

    # Parallel execution
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run strategies in parallel",
    )

    parser.add_argument(
        "--max-parallel",
        type=int,
        default=None,
        help="Maximum number of strategies to run in parallel (default: number of GPUs or CPU count)",
    )

    parser.add_argument(
        "--use-gpu",
        action="store_true",
        help="Enable GPU acceleration for FAISS",
    )

    args = parser.parse_args()

    # Setup
    logger.info("=" * 80)
    logger.info("RAG BENCHMARK RUNNER")
    logger.info("=" * 80)

    # Initialize GPU manager
    gpu_manager = get_gpu_manager()
    gpu_stats = gpu_manager.get_gpu_stats()

    # GPU info
    if gpu_stats["num_gpus"] > 0:
        logger.info(f"Detected {gpu_stats['num_gpus']} GPU(s):")
        for gpu_info in gpu_stats.get("gpu_info", []):
            logger.info(f"  GPU {gpu_info['id']}: {gpu_info['name']} ({gpu_info['memory_total_gb']:.1f} GB)")
    else:
        logger.warning("No GPU available, using CPU")

    # Parallel execution info
    if args.parallel:
        max_workers = args.max_parallel or gpu_stats["num_gpus"] or 1
        logger.info(f"Parallel mode enabled: {max_workers} concurrent strategies")
    else:
        logger.info("Sequential mode enabled")

    # Initialize models (use GPU 0 by default for shared models)
    embedder, reranker = init_models(args.embedder, args.reranker, gpu_id=0 if args.use_gpu and gpu_stats["num_gpus"] > 0 else None)

    # Determine datasets
    datasets_to_run = (
        ["nq", "hotpotqa", "vault"] if args.dataset == "all" else [args.dataset]
    )

    # Determine strategies
    strategies_to_run = (
        list(STRATEGY_CONFIGS.keys()) if "all" in args.strategies else args.strategies
    )

    logger.info(f"Datasets: {datasets_to_run}")
    logger.info(f"Strategies: {strategies_to_run}")

    # Results tracker
    tracker = ResultsTracker(output_dir=args.output_dir)

    # Run benchmarks
    for dataset_name in datasets_to_run:
        logger.info("\n" + "=" * 80)
        logger.info(f"DATASET: {dataset_name.upper()}")
        logger.info("=" * 80)

        # Load dataset
        dataset, dataset_config = load_dataset(dataset_name)

        # Parallel execution
        if args.parallel and not args.optimize:
            logger.info(f"\nRunning {len(strategies_to_run)} strategies in parallel...")

            # Create strategy executor
            strategy_executor = StrategyExecutor(
                max_parallel=args.max_parallel,
                enable_gpu=args.use_gpu and gpu_stats["num_gpus"] > 0,
                sequential_mode=False,
            )

            # Prepare experiment runner function
            def experiment_runner(strategy_name, params=None, gpu_id=None):
                """Run experiment for a single strategy."""
                if gpu_id is None:
                    gpu_id = 0  # Default to GPU 0

                # Create models for this strategy (if multi-GPU, use different GPU)
                if gpu_stats["num_gpus"] > 1:
                    strategy_embedder, strategy_reranker = init_models(
                        args.embedder, args.reranker, gpu_id=gpu_id
                    )
                else:
                    # Share models if single GPU or CPU
                    strategy_embedder = embedder
                    strategy_reranker = reranker

                evaluator = Evaluator()
                return run_single_experiment(
                    strategy_name=strategy_name,
                    dataset_name=dataset_name,
                    dataset=dataset,
                    embedder=strategy_embedder,
                    reranker=strategy_reranker,
                    graph_enabled=dataset_config["graph_enabled"],
                    temporal_enabled=dataset_config["temporal_enabled"],
                    params=params or {},
                    evaluator=evaluator,
                    use_gpu=args.use_gpu,
                    gpu_id=gpu_id,
                )

            # Create strategy configs
            strategy_configs = [
                {"strategy_name": strategy_name, "params": {}}
                for strategy_name in strategies_to_run
            ]

            # Run strategies in parallel
            results = strategy_executor.run_strategies(
                strategy_configs=strategy_configs,
                experiment_runner=experiment_runner,
                show_progress=True,
            )

            # Record results
            for strategy_name, eval_results in results.items():
                if eval_results:
                    logger.info(f"\n--- Results for {strategy_name} ---")
                    eval_results.print_summary()

                    tracker.add_result(
                        strategy_name=strategy_name,
                        dataset_name=dataset_name,
                        params={},
                        metrics=eval_results.metrics,
                        metadata=eval_results.metadata,
                    )
                else:
                    logger.error(f"Strategy {strategy_name} failed")

        # Sequential execution
        else:
            for strategy_name in strategies_to_run:
                logger.info(f"\n--- Strategy: {strategy_name} ---")

                try:
                    if args.optimize:
                        # Run optimization
                        best = optimize_hyperparameters(
                            strategy_name=strategy_name,
                            dataset_name=dataset_name,
                            dataset=dataset,
                            embedder=embedder,
                            reranker=reranker,
                            graph_enabled=dataset_config["graph_enabled"],
                            temporal_enabled=dataset_config["temporal_enabled"],
                            method=args.optimize_method,
                            n_trials=args.n_trials,
                        )

                        if best:
                            # Record best result
                            tracker.add_result(
                                strategy_name=strategy_name,
                                dataset_name=dataset_name,
                                params=best["params"],
                                metrics={"ndcg@10": best["score"]},
                                metadata={"optimization": args.optimize_method},
                            )

                    else:
                        # Run with default params
                        evaluator = Evaluator()

                        # Assign GPU for FAISS
                        gpu_id = 0 if args.use_gpu and gpu_stats["num_gpus"] > 0 else 0

                        eval_results = run_single_experiment(
                            strategy_name=strategy_name,
                            dataset_name=dataset_name,
                            dataset=dataset,
                            embedder=embedder,
                            reranker=reranker,
                            graph_enabled=dataset_config["graph_enabled"],
                            temporal_enabled=dataset_config["temporal_enabled"],
                            evaluator=evaluator,
                            use_gpu=args.use_gpu,
                            gpu_id=gpu_id,
                        )

                        # Print results
                        eval_results.print_summary()

                        # Record result
                        tracker.add_result(
                            strategy_name=strategy_name,
                            dataset_name=dataset_name,
                            params={},
                            metrics=eval_results.metrics,
                            metadata=eval_results.metadata,
                        )

                except Exception as e:
                    logger.error(f"Strategy {strategy_name} failed: {e}")
                    import traceback

                    traceback.print_exc()

    # Save results
    logger.info("\n" + "=" * 80)
    logger.info("SAVING RESULTS")
    logger.info("=" * 80)

    json_path = tracker.save_json()
    csv_path = tracker.save_csv()

    logger.info(f"JSON: {json_path}")
    logger.info(f"CSV: {csv_path}")

    # Print summary
    tracker.print_summary()

    logger.success("\n✓ Benchmark complete!")


if __name__ == "__main__":
    main()
