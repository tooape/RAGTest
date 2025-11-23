# RAG Test Repository

This repository contains test datasets for RAG (Retrieval-Augmented Generation) evaluation.

## Test Cases

For test case documentation, see: [Test Cases](obsidian://open?vault=My%20Vault&file=Notes%2FMisc%2FCode%20Projects%2FcustomRAG%2FTest%20cases)

## Datasets

### Vault Copy
- **vault copy/**: Snapshot of Obsidian vault content for testing

### BEIR Datasets

**Note**: Datasets are not included in this repository due to size (~3.6GB total). Download them locally using the provided script.

#### Download Instructions
```bash
# Install beir library
pip install beir

# Download datasets
python3 download_beir.py
```

This will download:
- **beir_datasets/nq/**: Natural Questions dataset (3.4k queries, 2.7M passages, ~1.5GB)
- **beir_datasets/hotpotqa/**: HotpotQA dataset (7.4k queries, 5.2M passages, ~2.1GB)

## Test Datasets

### Dataset 1: BEIR - Natural Questions (NQ)
- **Size**: 3.4k queries, 2.7M passages
- **Characteristics**: Keyword-heavy factoid questions
- **Use case**: Tests keyword matching and factual retrieval
- **Signals available**: Semantic, BM25 only (no graph/temporal)

### Dataset 2: BEIR - HotpotQA
- **Size**: 7.4k queries, 5.2M passages
- **Characteristics**: Multi-hop reasoning requiring multiple passages
- **Use case**: Tests complex reasoning and passage composition
- **Signals available**: Semantic, BM25, weak graph structure

### Dataset 3: Vault - Obsidian Personal Knowledge Base
- **Size**: 54 test queries, ~600-700 notes
- **Characteristics**: Work-specific terminology, heavy wikilink structure, temporal data
- **Use case**: Tests domain-specific retrieval with graph and temporal signals
- **Signals available**: Semantic, BM25, graph (PageRank), temporal (recency)

#### Vault Test Query Categories

**Hand-Written Queries (4 queries)**
- Direct validation of common use cases
- Example: "who's the PsW PM?" → Hao Xu

**Person & Meeting Queries (10 queries)**
- Who works on what, when did meetings happen, what was discussed
- Tests: Person pages, meeting notes, temporal retrieval
- Example: "What did Brian and I discuss in our most recent 1x1?"

**Project Status & Planning Queries (10 queries)**
- Current status, timelines, priorities, links to resources
- Tests: Hub pages, daily notes, temporal boosting
- Example: "What are my Q1 2026 priorities?"

**Technical & Architecture Queries (4 queries)**
- How systems work, design decisions, model choices
- Tests: Research artifacts, technical documentation
- Example: "How does temporal retrieval work in the RAG plugin?"

**Product & Platform Queries (5 queries)**
- Product differences, integration status, deployment info
- Tests: Cross-page synthesis, hub navigation
- Example: "What Adobe products currently have contextual recommendations integrated?"

**Browse & Relationship Queries (7 queries)**
- Graph traversal, concept exploration, related content
- Tests: Graph signals, wikilink following, semantic expansion
- Example: "Show me everything related to Query Understanding"

**Multi-Hop Reasoning Queries (4 queries)**
- Requires combining information across multiple notes
- Tests: Complex retrieval, synthesis, relationship inference
- Example: "Who should I talk to about improving the AdobeOne ranking for Lr?"

## Candidate Retrieval Strategies

**Implementation Status**: ✅ All 9 strategies implemented

### 1. Pure Semantic (Baseline) ✅
- **Implementation**: `SemanticSearch`
- **Models**: EmbeddingGemma, Mixedbread mxbai-embed-large-v1
- **Hyperparameters**: embedding_dim (256/512/768/1024), top_k (10/20/50)

### 2. BM25 (Baseline) ✅
- **Implementation**: `BM25Strategy`
- **Hyperparameters**: k1 (0.9/1.2/1.5/2.0), b (0.3/0.5/0.75), top_k (10/20/50)

### 3. Weighted Hybrid (Semantic + BM25) ✅
- **Implementation**: `WeightedHybrid`
- **Hyperparameters**: semantic_weight (0.3-0.9), normalization (min-max/z-score/rank)

### 4. RRF Hybrid (Semantic + BM25) ✅
- **Implementation**: `RRFHybrid`
- **Hyperparameters**: rrf_k (20/40/60/80), top_k (10/20/50)

### 5. Multi-Signal Fusion (Current System) ✅
- **Implementation**: `MultiSignalFusion`
- **Components**: Semantic + BM25 + Graph (PageRank) + Temporal (exponential decay)
- **Hyperparameters**:
  - Signal weights: semantic (0.4-0.7), bm25 (0.2-0.4), graph (0.0-0.2), temporal (0.0-0.15)
  - Graph: damping (0.85/0.9), normalization
  - Temporal: half_life (30/45/60 days), recency_bypass (90/120/150 days)

### 6. Two-Stage Reranking (xSmall v1) ✅
- **Implementation**: `TwoStageReranking` with `reranker="mxbai-xsmall"`
- **Stage 1**: Semantic retrieval (top_k: 50/100/200)
- **Stage 2**: Mixedbread reranker (xsmall-v1)
- **Hyperparameters**: stage1_k, final_k (10/20)

### 7. Two-Stage Reranking (base-v2) ✅
- **Implementation**: `TwoStageReranking` with `reranker="mxbai-base"`
- **Stage 1**: Semantic retrieval (top_k: 50/100/200)
- **Stage 2**: Mixedbread reranker (base-v2)
- **Hyperparameters**: stage1_k, final_k (10/20)
- **Note**: Same class as #6, different reranker model

### 8. Multi-Signal + Reranking Fusion ✅
- **Implementation**: `MultiSignalWithReranking`
- **Pipeline**:
  1. Parallel retrieval (Semantic + BM25)
  2. Rerank each signal independently (Mixedbread xsmall-v1)
  3. Multi-signal fusion with graph/temporal
- **Hyperparameters**: stage1_k, reranked_k (20/50), fusion weights

### 9. Multi-Signal + Dynamic Chunking ✅
- **Implementation**: `DynamicChunkingMultiSignal`
- **Chunking strategies**:
  - `dynamic_chunking_sliding`: Sliding window with fixed overlap
  - `dynamic_chunking_sentence`: Sentence-aware chunking (respects boundaries)
  - `dynamic_chunking_semantic`: Semantic chunking using embedding similarity
- **Features**:
  - Chunks at indexing time, aggregates at query time
  - Document-level graph/temporal scores inherited by chunks
  - Configurable aggregation: max, mean, or sum of chunk scores
- **Hyperparameters**: chunk_size (200/250/300), overlap (25/50/75), aggregation (max/mean/sum)

## Testing Strategy

### Unified Multi-Dataset Evaluation
All candidates tested simultaneously on all 3 datasets (NQ, HotpotQA, Vault) to identify:
- **Generalizable strategies**: Perform well across all datasets
- **BEIR specialists**: Excel on NQ/HotpotQA, struggle on vault
- **Vault specialists**: Optimized for domain-specific retrieval

### Evaluation Metrics
- **MRR@10** (Mean Reciprocal Rank): Position of first relevant result
- **NDCG@10** (Normalized Discounted Cumulative Gain): Ranked quality
- **Recall@10**: Coverage of relevant results
- **P@10** (Precision): Relevance of top 10
- **Latency**: Query execution time (ms)
- **Context tokens**: Token count for retrieved context

### Hyperparameter Optimization Strategy

#### Stage 1: Coarse Grid Search (Quick Filter)
**Objective**: Eliminate poor candidates, identify promising regions

**Approach**:
```python
# Test extremes and middle values for each hyperparameter
grid = {
    'semantic_weight': [0.3, 0.5, 0.7, 0.9],
    'bm25_weight': [0.1, 0.3, 0.5],
    'embedding_dim': [256, 768],
    'top_k': [10, 20]
}
# ~32 combinations per candidate
# Aggregate performance across all 3 datasets
# Keep top 50% of candidates
```

**Why**: Fast exploration of search space, rules out dead ends early

**Estimated time**: 8-12 hours, $5-7 (A10 GPU)

---

#### Stage 2: Bayesian Optimization (Deep Tuning)
**Objective**: Find optimal hyperparameters for top candidates

**Approach**:
```python
# Use Optuna or similar for intelligent search
# Optimize composite objective across datasets

objective =
    0.33 * MRR_NQ +
    0.33 * MRR_HotpotQA +
    0.34 * MRR_Vault

# Or weighted by priority:
objective =
    0.2 * MRR_NQ +
    0.2 * MRR_HotpotQA +
    0.6 * MRR_Vault  # Vault is primary use case

# Bayesian optimization converges in ~20-30 trials vs 100+ for grid
# Uses Gaussian Process to model objective function
# Intelligently samples high-uncertainty regions
```

**Search space per candidate**:
```python
{
    'semantic_weight': (0.3, 0.9),      # continuous
    'bm25_weight': (0.1, 0.5),          # continuous
    'graph_weight': (0.0, 0.25),        # continuous
    'embedding_dim': [256, 512, 768],   # categorical
    'rrf_k': (20, 100),                 # discrete
    'normalization': ['min-max', 'z-score', 'rank']  # categorical
}
```

**Constraints**:
- Weights must sum to 1.0 (or close)
- Graph/temporal weights = 0 for BEIR datasets
- Early stopping if performance plateaus (5 trials without improvement)

**Why**:
- More efficient than grid search (fewer trials)
- Finds global optimum better than random search
- Handles continuous + categorical + discrete parameters
- Can incorporate prior knowledge from Stage 1

**Estimated time**: 12-18 hours, $7-11 (A10 GPU)

---

#### Stage 3: Dataset-Specific Fine-Tuning (Optional)
**Objective**: Optimize separately for vault vs BEIR if unified tuning underperforms

**Approach**:
```python
# For top 3 candidates from Stage 2:
# 1. Keep unified config as baseline
# 2. Fine-tune for vault specifically
# 3. Compare vault-tuned vs unified

# Example: Multi-signal might need different weights for vault
vault_config = {
    'semantic_weight': 0.4,
    'bm25_weight': 0.2,
    'graph_weight': 0.25,      # Higher for vault (wikilinks!)
    'temporal_weight': 0.15    # Higher for vault (daily notes!)
}

beir_config = {
    'semantic_weight': 0.6,
    'bm25_weight': 0.4,
    'graph_weight': 0.0,       # No graph in BEIR
    'temporal_weight': 0.0     # No temporal in BEIR
}
```

**Decision criteria**:
- If vault-tuned improves MRR by >5%: Use separate configs
- If vault-tuned improves MRR by <5%: Keep unified (simpler)

**Why**:
- Vault has unique signals (graph, temporal) not in BEIR
- Dataset-specific tuning might unlock better performance
- Trade-off: Complexity vs performance gain

**Estimated time**: 4-6 hours, $2-4 (A10 GPU)

---

#### Stage 4: Ablation Studies
**Objective**: Understand which components matter most

**Approach**:
```python
# For winning multi-signal candidate, test component contributions:
configs = {
    'semantic_only':     {'sem': 1.0, 'bm25': 0.0, 'graph': 0.0, 'temp': 0.0},
    'sem_bm25':          {'sem': 0.7, 'bm25': 0.3, 'graph': 0.0, 'temp': 0.0},
    'sem_bm25_graph':    {'sem': 0.5, 'bm25': 0.3, 'graph': 0.2, 'temp': 0.0},
    'full_multisignal':  {'sem': 0.5, 'bm25': 0.2, 'graph': 0.2, 'temp': 0.1}
}

# Measure marginal contribution of each signal
delta_graph = MRR(sem_bm25_graph) - MRR(sem_bm25)
delta_temporal = MRR(full) - MRR(sem_bm25_graph)
```

**Key questions**:
1. Does graph signal help on BEIR? (Expected: No)
2. Does graph signal help on vault? (Expected: Yes, significantly)
3. Is BM25 still needed with good embeddings? (Unknown)
4. Does temporal help beyond top_k selection? (Unknown)
5. Is reranking worth 2-3x latency increase? (Unknown)

**Why**:
- Identifies which complexity is justified
- Informs production deployment decisions
- Validates architectural assumptions

**Estimated time**: 2-3 hours, $1-2 (A10 GPU)

---

### Multi-Objective Optimization

**Trade-offs to balance**:
1. **Accuracy vs Latency**: Reranking boosts MRR but adds 50-150ms
2. **Accuracy vs Cost**: Larger embeddings (768d) vs smaller (256d)
3. **Accuracy vs Complexity**: Multi-signal fusion vs simple hybrid

**Pareto Optimization**:
```python
# Define acceptable trade-offs
objectives = {
    'maximize': ['MRR@10', 'NDCG@10'],
    'minimize': ['latency_ms', 'context_tokens']
}

# Find Pareto frontier: configs where improving one metric
# requires degrading another
pareto_configs = find_pareto_frontier(all_results)

# User selects from Pareto set based on priorities:
# - Production: Low latency (< 100ms)
# - Research: High accuracy (MRR > 0.8)
# - Balanced: MRR > 0.7, latency < 150ms
```

**Example Pareto set**:
| Config | MRR | Latency | Context Tokens | Note |
|--------|-----|---------|----------------|------|
| Gemma-256d | 0.72 | 45ms | 3500 | Fast, good accuracy |
| Multi-signal-512d | 0.78 | 85ms | 4200 | Balanced |
| Rerank-base-v2 | 0.84 | 165ms | 4500 | Best accuracy, slow |

---

### Cross-Validation Strategy

**K-Fold on Vault** (BEIR has standard train/test splits):
```python
# Split 54 vault queries into 5 folds
# Train hyperparameters on 4 folds, validate on 1
# Repeat 5 times, average performance

# Ensures hyperparameters aren't overfit to specific queries
# Important because vault test set is small (54 queries)
```

**Why**: Prevents overfitting on small vault test set

---

### Meta-Learning: BEIR → Vault Transfer

**Hypothesis**: Good hyperparameters on BEIR generalize to vault

**Test**:
```python
# 1. Find best config on BEIR only
beir_best = optimize(datasets=['nq', 'hotpotqa'])

# 2. Test beir_best on vault (zero-shot transfer)
vault_zeroshot_mrr = evaluate(beir_best, dataset='vault')

# 3. Compare to vault-optimized config
vault_tuned_mrr = evaluate(vault_best, dataset='vault')

# 4. Measure transfer gap
transfer_gap = vault_tuned_mrr - vault_zeroshot_mrr
```

**If transfer gap < 5%**: BEIR tuning is sufficient (saves compute)
**If transfer gap > 10%**: Must tune on vault separately

---

### Early Stopping Criteria

**When to stop hyperparameter search**:

1. **Convergence**: No improvement in 5 consecutive trials
2. **Diminishing returns**: Last 10 trials improved MRR by < 0.01
3. **Budget exhausted**: Hit time/cost limit ($15 budget)
4. **Pareto optimal**: Found config dominating all objectives
5. **Good enough**: MRR > 0.75 on vault (user-defined threshold)

**Dynamic trial budgets**:
```python
# Allocate more trials to promising candidates
if candidate_avg_mrr > 0.7:
    n_trials = 30  # Deep search
elif candidate_avg_mrr > 0.6:
    n_trials = 20  # Medium search
else:
    n_trials = 10  # Quick search before dropping
```

---

### Hyperparameter Search Summary

**Total estimated compute**:
- Stage 1 (Coarse grid): 8-12 hours
- Stage 2 (Bayesian opt): 12-18 hours
- Stage 3 (Fine-tuning): 4-6 hours (optional)
- Stage 4 (Ablation): 2-3 hours
- **Total: 26-39 hours on A10 GPU = $16-24**

**Expected outputs**:
1. **Winning configuration** with optimized hyperparameters
2. **Performance table** across all datasets and metrics
3. **Ablation results** showing component contributions
4. **Pareto frontier** for accuracy/latency trade-offs
5. **Transfer learning insights** (BEIR → Vault generalization)

---

## Setup and Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download BEIR Datasets

```bash
python download_beir.py
```

This will download NQ and HotpotQA datasets (~3.6GB total).

---

## Testing

### Smoke Test (Pre-Flight Validation)

**Purpose**: Quick validation that the framework runs correctly before committing to full dataset benchmarks

**What it tests**:
- Model loading (embedders, rerankers)
- All retrieval strategies run without errors
- Evaluation metrics calculate correctly
- Hyperparameter optimization works
- Batch search functionality
- Output format validation

**Runtime**: < 2 minutes

**Run**:
```bash
python scripts/smoke_test.py
```

**Expected output**:
```
✓ Embedder loaded
✓ Reranker loaded
✓ SemanticSearch: indexed in 0.12s, queried in 0.05s
✓ BM25: indexed in 0.01s, queried in 0.02s
✓ WeightedHybrid: indexed in 0.13s, queried in 0.06s
✓ RRF: indexed in 0.14s, queried in 0.07s
✓ MultiSignal: indexed in 0.15s, queried in 0.08s
✓ TwoStage: indexed in 0.16s, queried in 0.25s
✓ MRR@10: 0.667
✓ NDCG@10: 0.734
✓ Precision@10: 0.500
✓ Grid search: tested 4 configs, best NDCG=0.745
✓ Batch search: processed 3 queries
✓ ALL SMOKE TESTS PASSED
```

**When to run**:
- Before full benchmark runs
- After code changes to core components
- Before deploying to Lambda GPU

---

### Unit Tests

**Purpose**: Comprehensive testing of individual components

**Coverage**:
- Evaluation metrics (MRR, NDCG, Precision, Recall)
- Retrieval strategies (BM25, normalization, batch search)
- Hyperparameter optimization (grid search, Bayesian)
- Results tracking (save/load, filtering, summary tables)
- Evaluator (aggregation, per-query metrics)

**Runtime**: < 10 seconds

**Run**:
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_metrics.py

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src
```

**Test files**:
- `tests/test_metrics.py`: Evaluation metrics
- `tests/test_strategies.py`: Retrieval strategies
- `tests/test_optimization.py`: Hyperparameter optimization
- `tests/test_evaluator.py`: Evaluator functionality
- `tests/test_results.py`: Results tracking

---

## Running Benchmarks

### Quick Start (Single Dataset)

```bash
# Run on vault with default settings
python scripts/run_benchmark.py --dataset vault

# Run on BEIR NQ dataset
python scripts/run_benchmark.py --dataset nq

# Run specific strategies only
python scripts/run_benchmark.py --dataset vault --strategies semantic bm25 weighted
```

### Full Benchmark (All Datasets)

```bash
python scripts/run_benchmark.py --dataset all --strategies all
```

### With Hyperparameter Optimization

```bash
# Grid search
python scripts/run_benchmark.py --dataset vault --optimize --optimize-method grid

# Bayesian optimization (faster)
python scripts/run_benchmark.py --dataset vault --optimize --optimize-method bayesian --n-trials 50
```

### Custom Model Selection

```bash
# Use specific embedder and reranker
python scripts/run_benchmark.py \
    --dataset vault \
    --embedder gemma-256 \
    --reranker mxbai-base
```

**Available embedders**:
- `gemma-256`: EmbeddingGemma @ 256d (fastest)
- `gemma-512`: EmbeddingGemma @ 512d
- `gemma-768`: EmbeddingGemma @ 768d (best quality)
- `mxbai-large-256`: Mixedbread @ 256d
- `mxbai-large-512`: Mixedbread @ 512d

**Available rerankers**:
- `mxbai-xsmall`: Mixedbread xsmall-v1 (fast)
- `mxbai-base`: Mixedbread base-v2 (accurate)

---

### Parallel Execution and Multi-GPU Support

**NEW**: Run multiple strategies concurrently to dramatically reduce benchmark runtime!

#### Parallel Mode

```bash
# Run strategies in parallel (automatically uses all available GPUs)
python scripts/run_benchmark.py --dataset vault --parallel

# Specify maximum number of parallel workers
python scripts/run_benchmark.py --dataset vault --parallel --max-parallel 4

# Enable GPU acceleration for FAISS indices
python scripts/run_benchmark.py --dataset vault --parallel --use-gpu
```

#### How It Works

1. **Multi-GPU Distribution**: When multiple GPUs are detected:
   - Each strategy runs on a separate GPU
   - Models (embedders, rerankers) are loaded per-GPU
   - FAISS indices are distributed across GPUs
   - Automatic load balancing via round-robin GPU assignment

2. **Single GPU Optimization**: With one GPU:
   - Shared models across strategies (reduced memory)
   - Parallel execution via threading
   - FAISS indices still benefit from GPU acceleration

3. **CPU Fallback**: No GPU available:
   - Parallel execution via threading
   - Automatic worker count based on CPU cores

#### Performance Benefits

**Multi-GPU (e.g., 4x A10 GPUs)**:
- **9 strategies sequentially**: ~4-6 hours
- **9 strategies in parallel**: ~1-1.5 hours (3-4x speedup)
- Each strategy gets dedicated GPU resources

**Single GPU**:
- **9 strategies sequentially**: ~4-6 hours
- **9 strategies in parallel**: ~2-3 hours (2x speedup)
- Parallel I/O and CPU operations while GPU processes

#### GPU Manager Features

The framework includes an intelligent GPU manager that:
- Auto-detects available GPUs and their capabilities
- Tracks GPU assignments for each task
- Balances load across GPUs (round-robin)
- Reports GPU memory usage and statistics
- Clears GPU cache automatically

**View GPU statistics**:
```bash
# GPU info is logged at startup
python scripts/run_benchmark.py --dataset vault --parallel

# Example output:
# Detected 4 GPU(s):
#   GPU 0: NVIDIA A10 (24.0 GB)
#   GPU 1: NVIDIA A10 (24.0 GB)
#   GPU 2: NVIDIA A10 (24.0 GB)
#   GPU 3: NVIDIA A10 (24.0 GB)
# Parallel mode enabled: 4 concurrent strategies
```

#### When to Use Parallel Mode

**Use parallel mode when**:
- Running multiple strategies for comparison
- You have multiple GPUs available
- You want to reduce total benchmark time
- Not using hyperparameter optimization (not yet parallelized)

**Use sequential mode when**:
- Running hyperparameter optimization (`--optimize`)
- Running a single strategy
- Debugging strategy behavior
- Limited GPU memory (large models or datasets)

#### Advanced Configuration

**Explicit GPU assignment** (advanced):
```python
# In custom scripts, you can explicitly assign GPUs
from utils.gpu_manager import get_gpu_manager
from utils.parallel_executor import StrategyExecutor

gpu_manager = get_gpu_manager()
executor = StrategyExecutor(
    max_parallel=2,           # Run 2 strategies at a time
    enable_gpu=True,          # Enable GPU support
    sequential_mode=False     # Parallel mode
)

# GPU manager automatically assigns GPUs 0 and 1 in round-robin
```

**Memory considerations**:
- Each parallel strategy loads its own models (~2-4 GB per strategy)
- FAISS indices scale with corpus size (~1-8 GB depending on dataset)
- With 24 GB GPU: Can run ~4-6 strategies in parallel
- With 16 GB GPU: Can run ~2-3 strategies in parallel

#### Limitations

- Hyperparameter optimization (`--optimize`) runs sequentially
- Parallel execution requires Python 3.7+ (for ThreadPoolExecutor)
- GPU memory must accommodate multiple model instances
- Some strategies (BM25) don't benefit from GPU acceleration

---

## Results

Results are saved in the `results/` directory:

- **JSON format**: Full results with metadata
- **CSV format**: Flattened table for analysis

**Example output**:
```
results/
├── benchmark_results_20250122_143052.json
├── benchmark_results_20250122_143052.csv
```

**Summary table** (printed after run):
```
================================================================================
BENCHMARK SUMMARY
================================================================================
   strategy      dataset  n_runs  best_mrr@10  best_ndcg@10  latency_ms
0  semantic      vault         1       0.7234        0.7891        45.2
1  bm25          vault         1       0.6123        0.6834        12.3
2  weighted      vault         1       0.7456        0.8012        52.1
3  multisignal   vault         1       0.7834        0.8234        89.4
================================================================================
```

---

## Project Structure

```
RAGTest/
├── README.md
├── requirements.txt
├── download_beir.py
│
├── vault copy/              # Obsidian vault snapshot
│
├── beir_datasets/           # Downloaded BEIR data (not in git)
│   ├── nq/
│   └── hotpotqa/
│
├── src/                     # Core framework
│   ├── datasets/            # Dataset loaders
│   │   ├── beir_loader.py
│   │   └── vault_loader.py
│   │
│   ├── models/              # Embedding and reranking models
│   │   ├── embedders.py
│   │   └── rerankers.py
│   │
│   ├── strategies/          # Retrieval strategies
│   │   ├── semantic.py
│   │   ├── hybrid.py
│   │   ├── multisignal.py
│   │   └── reranking.py
│   │
│   ├── evaluation/          # Metrics and evaluation
│   │   ├── metrics.py
│   │   └── evaluator.py
│   │
│   ├── optimization/        # Hyperparameter optimization
│   │   ├── grid_search.py
│   │   └── bayesian.py
│   │
│   └── utils/               # Utilities
│       ├── results.py
│       ├── gpu_manager.py          # Multi-GPU management
│       ├── parallel_executor.py    # Parallel strategy execution
│       └── chunker.py
│
├── scripts/                 # Executable scripts
│   ├── smoke_test.py        # Pre-flight validation
│   └── run_benchmark.py     # Main benchmark runner
│
├── tests/                   # Unit tests
│   ├── test_metrics.py
│   ├── test_strategies.py
│   ├── test_optimization.py
│   ├── test_evaluator.py
│   └── test_results.py
│
├── results/                 # Benchmark outputs
│   ├── *.json
│   └── *.csv
│
└── cache/                   # Cached embeddings (optional)
```
