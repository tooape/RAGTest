---
created: 2025-10-31
pageType: misc
tags:
  - claude
Related Pages:
  - "[[Smart Connections Enhancement - Custom RAG]]"
aliases:
  - RAG Phase 1
---
# Obsidian RAG - Phase 1 Implementation
---

**Status**: ✅ Complete (October 31, 2025)

Detailed implementation notes, architecture decisions, and component overview for Phase 1 (Hybrid Search + Graph Boosting).

## System Architecture
---

**Recall Set = Semantic ∪ Graph-Expanded ∪ BM25**

```
Query: "Lr Agent status"
    ↓
Semantic Search (EmbeddingGemma @ 256d) 
    → finds [[Lr Home]]
    ↓
Graph Expansion 
    → backlinks TO [[Lr Home]]:
      - October 30, 2025.md
      - October 27, 2025.md
      - September 30, 2025.md
    ↓
BM25 Search (with query expansion via aliases)
    → finds keyword matches
    ↓
RRF Fusion (4 signals: semantic, BM25, graph, temporal)
    ↓
Result: Recent daily notes with status updates in top-10 ✓
```

## Completed Components
---

### 1. Python Backend with EmbeddingGemma @ 256d

**FastAPI server on localhost:8000**

Features:
- Embedding Generation: `POST /api/embed` 
- Matryoshka Truncation: 768d → 256d (zero quality loss, 66% storage reduction)
- Persistent Caching: Disk-based NPZ cache
- Semantic Search: `POST /api/search` with similarity ranking
- Health Monitoring: `GET /health` with auto-restart

Performance:
- Query latency: ~18-20ms
- Storage: ~600 KB for 670-note vault
- Fully local and offline after initial download

### 2. Graph Traversal with PageRank

**GraphAnalyzer.ts**: Wikilink-based traversal

Features:
- Backlinks (inbound): Finds daily notes linking TO canonical pages
- Forward links (outbound): Finds pages linked FROM canonical pages
- Weighted filtering: PageRank × log(1 + edge count) × recency
- Temporal-aware: Recent notes (last 30 days) get 2.0x boost

Configuration:
```typescript
graphExpansionConfig: {
    enabled: true,
    maxNeighborsPerSeed: 15,
    traversalDepth: 1,
    weightByPageRank: true,
}
```

Impact: Expands candidate set by 3-5x, finding daily notes semantic/BM25 miss

### 3. Multi-Signal Ranking with RRF

**SearchOrchestrator.ts**: Reciprocal Rank Fusion

Signal Weights (equal by default):
```typescript
const signalWeights = new Map<string, number>([
    ['semantic', 1.0],  // Conceptual match
    ['bm25', 1.0],      // Keyword match
    ['graph', 1.0],     // Importance (PageRank)
    ['temporal', 1.0],  // Recency
]);
```

Key Design: Graph and temporal signals only boost query-relevant items (found by semantic/BM25/graph), preventing irrelevant recent notes from polluting results.

### 4. BM25 with MiniSearch

**MiniSearchIndexer.ts**: Keyword matching

Library: `minisearch` (battle-tested, powers Omnisearch)

Field Weighting:
```typescript
boost: {
    title: 2.0,      // Filename: 2x
    aliases: 2.0,    // Aliases: 2x
    tags: 2.0,       // Tags: 2x
    pageType: 1.5,   // PageType: 1.5x
    h1: 1.5,         // H1 headings: 1.5x
    h2: 1.3,         // H2 headings: 1.3x
    h3: 1.1,         // H3 headings: 1.1x
    content: 1.0,    // Content: 1x (baseline)
}
```

Features: Fuzzy matching (0.2 threshold), prefix matching, grouped headings

### 5. Query Expansion via Alias Extraction

**QueryExpander.ts**: Leverage vault's own terminology

Strategy:
1. Semantic search finds top 5 conceptually relevant pages
2. Extract aliases from those pages
3. Build OR query: `"photoshop OR ps OR 'ps web'"`
4. MiniSearch finds mentions using abbreviations

Result: "photoshop" query finds "PS Web recs" meeting via fuzzy alias matching

### 6. Temporal Analysis with Recency Decay

**TemporalAnalyzer.ts**: Time-based scoring

Formula: Exponential decay with configurable half-life (default: 30 days)
```typescript
score = exp(-ln(2) * age_days / halfLife)
```

Settings: Half-life adjustable via UI (30 days default)

Hybrid Strategy:
- Always include: Notes from last 120 days
- Filter older notes: Only boost if query-relevant (semantic/BM25 match)

## Key Implementation Decisions
---

| Decision | Why |
|----------|-----|
| MiniSearch over custom BM25 | Battle-tested, built-in fuzzy matching, field boosting |
| Query expansion via semantic | Leverages vault's own aliases, no external data |
| Signal filtering (query-relevant only) | Prevents irrelevant boosting, maintains precision |
| Text inputs for weights | Exact values (0.30 vs slider approximation), copy-paste friendly |
| Empty file filtering | EmbeddingGemma generates real vectors for empty strings, causing false matches |

## Repository Structure
---

```
obsidianrag/
├── obsidian-plugin/               # TypeScript plugin
│   ├── src/
│   │   ├── main.ts                # Plugin entry point
│   │   ├── SearchOrchestrator.ts  # Multi-signal ranking + graph expansion
│   │   ├── GraphAnalyzer.ts       # Graph traversal + PageRank
│   │   ├── MiniSearchIndexer.ts   # BM25 wrapper
│   │   ├── QueryExpander.ts       # Query expansion
│   │   ├── TemporalAnalyzer.ts    # Recency scoring
│   │   ├── FileChangeHandler.ts   # Incremental updates
│   │   ├── SearchModal.ts         # UI
│   │   └── SettingsTab.ts         # Configuration
│   └── package.json               # Dependencies
└── python-backend/                # FastAPI server
    ├── app/
    │   ├── main.py                # FastAPI app
    │   └── models/embedder.py     # EmbeddingGemma @ 256d
    ├── requirements.txt
    └── cache/embeddings.npz       # Persistent cache (600 KB)
```

## Success Criteria: ACHIEVED ✓
---

- ✅ Graph traversal expands candidate set (solves "missing daily notes")
- ✅ Multi-signal ranking combines semantic + lexical + graph + temporal
- ✅ MCP compatible (`search_vault_smart` interface)
- ✅ Query latency <100ms target (actual: ~40-50ms)
- ✅ Token-efficient (200-char excerpts, ~1,000 tokens vs 40,000 with full content)

