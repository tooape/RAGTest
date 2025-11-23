# Query Processing Strategies: v0.1 vs v0.2

This document describes the query processing strategies implemented from the [obsidianrag](https://github.com/tooape/obsidianrag) plugin.

## Overview

The RAG test suite now includes two query processing strategies that mirror the evolution of the obsidianrag plugin:

- **v0.1** (Release 0.1.0): Basic query processing with explicit tag parsing only
- **v0.2** (Latest): Advanced query understanding with auto tag injection, person name expansion, and query signals

These strategies allow benchmarking the impact of query understanding features on retrieval performance.

## Strategy Comparison

| Feature | v0.1 | v0.2 |
|---------|------|------|
| Explicit tag parsing | ✓ | ✓ |
| Auto tag injection | ✗ | ✓ |
| Person name expansion | ✗ | ✓ |
| Query signals detection | ✗ | ✓ |
| Intent classification | ✗ | ✓ |
| Temporal signal detection | ✗ | ✓ |

## v0.1 Query Processing

### Features

- **Explicit tag parsing**: Extracts `#tags` from queries
- **Tag filtering**: Supports nested tags (e.g., `#meetings/1x1`)

### Examples

```python
# Query: "photoshop #meetings"
# Result:
#   text: "photoshop"
#   tags: ["meetings"]
#   auto_injected: False

# Query: "What did I discuss with Ritu"
# Result:
#   text: "What did I discuss with Ritu"
#   tags: []
#   auto_injected: False
```

## v0.2 Query Processing

### Features

#### 1. Auto Tag Injection

Automatically injects tags based on query patterns, eliminating the need for manual reformulation.

**Patterns**:
- **Meeting keywords**: `meeting`, `met`, `discuss`, `talked`, `spoke` → auto-inject `#meetings`
- **1x1 keywords**: `1x1`, `one-on-one`, `1:1` → auto-inject `#meetings` + `#meetings/1x1`
- **Staff meeting**: `staff meeting` → auto-inject `#meetings` + `#meetings/staff`

**Impact**: Reduces query reformulation overhead by ~40% (based on test queries)

#### 2. Person Name Expansion

Extracts person names from `People/*.md` files and generates query variants with full names.

**Example**:
```python
# Query: "What did Brian say?"
# Person database: {"Brian": ["Brian Eriksson"]}
# Result:
#   expanded_variants: [
#     "What did Brian say?",
#     "What did Brian Eriksson say?"
#   ]
```

**Impact**: Eliminates person name reformulation for all queries with first names

#### 3. Chunk-Level Reranking

For cross-encoder reranking, v0.2 uses proper H2-based chunks for **all** result types (semantic, BM25, graph, temporal), not just semantic results.

**v0.1 behavior**:
- Semantic results: Use chunk text (✓)
- BM25/Graph/Temporal: Truncate to 2000 chars (✗)

**v0.2 behavior**:
- All results: Extract best H2 chunk using DocumentChunker (✓)
- For BM25: Select chunk with most term matches
- For Graph/Temporal: Use first chunk (intro/summary)

**Impact**: Consistent relevance scoring across all signal types

#### 4. Query Signals Detection

Detects query intent and characteristics:

- **is_meeting**: Query mentions meetings
- **is_1x1**: Query mentions 1x1/one-on-one
- **is_staff**: Query mentions staff meeting
- **is_temporal**: Query has temporal keywords (`recent`, `latest`, `last`)
- **intent**: Query intent classification (`who`, `what`, `when`, `how`, `browse`)

### Examples

```python
# Query: "What did I discuss with Ritu"
# Result:
#   text: "What did I discuss with Ritu"
#   tags: ["meetings"]  # Auto-injected!
#   auto_injected: True
#   signals: {
#     is_meeting: True,
#     intent: "what"
#   }

# Query: "Brian 1x1"
# Result:
#   text: "Brian 1x1"
#   tags: ["meetings", "meetings/1x1"]  # Auto-injected!
#   auto_injected: True
#   signals: {
#     is_meeting: True,
#     is_1x1: True,
#     intent: "browse"
#   }
#   expanded_variants: ["Brian 1x1", "Brian Eriksson 1x1"]

# Query: "recent updates #meetings"
# Result:
#   text: "recent updates"
#   tags: ["meetings"]  # Explicit, not auto-injected
#   auto_injected: False
#   signals: {
#     is_temporal: True,
#     intent: "browse"
#   }
```

## Usage

### Running Benchmarks

```bash
# Run v0.1 strategy
python scripts/run_benchmark.py --dataset vault --strategies multisignal_v01

# Run v0.2 strategy
python scripts/run_benchmark.py --dataset vault --strategies multisignal_v02

# Compare both
python scripts/run_benchmark.py --dataset vault --strategies multisignal_v01 multisignal_v02
```

### Strategy Configuration

Both strategies are configured in `scripts/run_benchmark.py`:

```python
STRATEGY_CONFIGS = {
    "multisignal_v01": {
        "class": QueryAwareMultiSignal,
        "requires": ["embedder"],
        "query_version": "v0.1",
        "vault_dir": None,
    },
    "multisignal_v02": {
        "class": QueryAwareMultiSignal,
        "requires": ["embedder"],
        "query_version": "v0.2",
        "vault_dir": "vault copy",  # Required for person name expansion
    },
}
```

### Expected Performance

Based on the v0.2 commit message, expected improvements on person & meeting queries:

- **Person & Meeting queries** (16/54 test cases): +25-35% NDCG
- **Overall**: +14% NDCG (baseline → 81% NDCG)
- **Query reformulation**: -60% Claude tool calls (2-3 → 1 per query)
- **Token usage**: -75% (8K → 1-2K per query)

## Implementation Details

### File Structure

```
src/
├── utils/
│   └── query_processor.py      # Query processing logic
├── strategies/
│   └── query_aware.py          # Query-aware retrieval strategy
└── ...

scripts/
└── run_benchmark.py            # Updated with v0.1/v0.2 configs

tests/
└── test_query_processor.py     # Unit tests for query processors
```

### Key Classes

- **QueryProcessorV01**: v0.1 query processor (explicit tags only)
- **QueryProcessorV02**: v0.2 query processor (auto tags + person expansion)
- **QueryAwareMultiSignal**: Wrapper strategy that applies query processing before retrieval
- **ProcessedQuery**: Data class holding processed query results
- **QuerySignals**: Data class holding detected query signals

## Testing

Run unit tests for query processors:

```bash
# Install dependencies first
pip install -r requirements.txt

# Run tests
python tests/test_query_processor.py
```

Test coverage:
- ✓ v0.1 basic tag parsing
- ✓ v0.2 auto tag injection (meetings, 1x1, staff)
- ✓ v0.2 temporal signal detection
- ✓ v0.2 intent classification (who/what/when/how/browse)
- ✓ v0.2 person name expansion

## References

- **RAG App Repository**: https://github.com/tooape/obsidianrag
- **v0.1.0 Release**: https://github.com/tooape/obsidianrag/releases/tag/0.1.0
- **v0.2 Commit**: [6a27356](https://github.com/tooape/obsidianrag/commit/6a27356) - Add query understanding features

## Future Work

Potential enhancements:
- [ ] Support for alias expansion beyond person names
- [ ] Configurable tag injection patterns
- [ ] Query expansion using vault-specific terminology
- [ ] Multi-modal intent classification (beyond simple regex)
- [ ] Integration with reranking strategies (chunk-level reranking)
