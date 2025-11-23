# RAGTest Experiments

Comprehensive ablation studies and parameter sweeps for retrieval strategies.

## Experiments

### 1. Matryoshka Dimension Comparison ⭐ HIGHEST PRIORITY
**File**: `matryoshka_comparison.py`
**Runtime**: ~2-3 hours (all datasets)
**GPU**: Required

Test embedding dimensions: 1024d, 768d, 512d, 256d

**Research Question**: Does 256d maintain quality with 2.8x speedup?

**Expected Result**: 256d has zero quality loss (based on prior benchmarks)

**Command**:
```bash
python experiments/matryoshka_comparison.py
```

---

### 2. Reranker Ablation Study
**File**: `reranker_ablation.py`
**Runtime**: ~3-4 hours (all datasets × strategies × 2)
**GPU**: Required

Compare each strategy WITH vs WITHOUT reranking.

**Research Question**: Does reranking help or hurt?

**Key Finding from Vault**: Reranking DECREASED NDCG@10 by 53%!
- `multisignal`: 0.142 NDCG@10
- `multisignal_reranked`: 0.067 NDCG@10

**Hypothesis**: Reranker may over-correct good initial rankings.

**Command**:
```bash
python experiments/reranker_ablation.py
```

---

### 3. Fusion Weight Sweep
**File**: `fusion_weight_sweep.py`
**Runtime**: ~2-3 hours
**GPU**: Required

Test alpha values: 0.1, 0.3, 0.5, 0.7, 0.9

**What alpha means**:
- `alpha=0.1`: 10% semantic, 90% BM25
- `alpha=0.5`: 50/50 split (default)
- `alpha=0.9`: 90% semantic, 10% BM25

**Research Question**: What's the optimal BM25 vs semantic balance?

**Expected Result**: Vault may prefer high BM25 weight (alpha ~0.3)

**Command**:
```bash
python experiments/fusion_weight_sweep.py
```

---

### 4. Embedding Model Comparison
**File**: `embedding_model_comparison.py`
**Runtime**: ~4-5 hours (4 models × 3 datasets)
**GPU**: Required
**Storage**: ~8GB (will download 4 models)

Compare models:
1. `mxbai-embed-large-v1` (current, 1024d)
2. `bge-large-en-v1.5` (current SOTA, 1024d)
3. `gte-large-en-v1.5` (Google, 1024d)
4. `e5-large-v2` (Microsoft, 1024d)

**Research Question**: Does model choice matter more than retrieval strategy?

**Command**:
```bash
python experiments/embedding_model_comparison.py
```

---

### 5. Top-K Retrieval Depth Study
**File**: `topk_depth_study.py`
**Runtime**: ~2-3 hours
**GPU**: Required

Test candidate counts: k = [10, 20, 50, 100, 200]

**Research Question**: Does retrieving more candidates improve final top-10 quality?

**Trade-off**: More candidates = better recall but slower + more noise

**Expected Result**: k=50-100 optimal balance

**Command**:
```bash
python experiments/topk_depth_study.py
```

---

### 6. Vault Signal Tuning (Vault-Specific)
**File**: `vault_signal_tuning.py`
**Runtime**: ~30-45 minutes (vault only)
**GPU**: Required

Test graph and temporal boost multipliers: [0.0, 0.1, 0.2, 0.5, 1.0]

**Research Questions**:
1. How much do graph signals (PageRank) help?
2. How much do temporal signals (recency) help?
3. What's the optimal combination?

**Note**: BM25 is hard to beat on vault - graph/temporal may not help much!

**Command**:
```bash
python experiments/vault_signal_tuning.py
```

---

## Priority Execution Order

1. **Matryoshka** (free speedup if 256d works) - Run ASAP
2. **Reranker ablation** (understand cost/benefit) - Run in parallel
3. **Fusion weights** (optimize hybrid) - Quick wins
4. **Embedding models** (compare SOTA) - Longer but valuable
5. **Top-K depth** (recall vs noise) - Nice to have
6. **Vault tuning** (domain-specific) - Low priority given BM25 dominance

## Running All Experiments

**Sequential**:
```bash
for exp in matryoshka_comparison reranker_ablation fusion_weight_sweep \
           embedding_model_comparison topk_depth_study vault_signal_tuning; do
    python experiments/${exp}.py
done
```

**Parallel** (if you have multiple GPUs):
```bash
# GPU 0-1: Matryoshka
CUDA_VISIBLE_DEVICES=0,1 python experiments/matryoshka_comparison.py &

# GPU 2-3: Reranker
CUDA_VISIBLE_DEVICES=2,3 python experiments/reranker_ablation.py &

# GPU 4-5: Fusion
CUDA_VISIBLE_DEVICES=4,5 python experiments/fusion_weight_sweep.py &
```

## Results Location

All experiments save results to:
```
results/
├── matryoshka_summary.json
├── reranker_ablation_summary.json
├── fusion_weight_summary.json
├── embedding_model_summary.json
├── topk_depth_summary.json
└── vault_signal_tuning_summary.json
```

## Key Insights from Initial Vault Results

### BM25 Dominance
- **BM25 alternate**: 0.166 NDCG@10 (BEST)
- **BM25 primary**: 0.154 NDCG@10
- 37x faster than semantic (0.48ms vs 17.9ms)

**Why BM25 won:**
1. Exact term matching (entity names: "Hao Xu", "Photoshop Web")
2. Small corpus effect (158 docs - no need for semantic understanding)
3. Query type (alternate queries more keyword-focused)

### Reranking Hurts
- `multisignal`: 0.142 NDCG@10
- `multisignal_reranked`: 0.067 NDCG@10 (**53% WORSE**)
- Adds 470ms latency for worse results

**Why reranking failed:**
- Reranker trained on different data distribution
- Over-corrects good initial rankings
- Vault queries too simple to benefit from cross-attention

### Strategy Performance Order
1. BM25 (0.154-0.166) ⭐
2. Multisignal (0.142)
3. RRF (0.128)
4. Dynamic chunking (0.122-0.125)
5. Weighted (0.067-0.112)
6. Two-stage + reranked (0.054-0.080) ❌

## Recommendations

### For Small Corpora (<1000 docs)
- **Use BM25** - faster and more accurate
- Skip reranking - it hurts more than helps
- Semantic embeddings add complexity without benefit

### For Large Corpora (>100k docs)
- Hybrid approaches may help
- Test Matryoshka 256d for speed
- Reranker impact unclear - run ablation first

### For Domain-Specific (like vault)
- Exact matching (BM25) beats semantic
- Graph/temporal signals may not overcome BM25
- Focus on query expansion instead
