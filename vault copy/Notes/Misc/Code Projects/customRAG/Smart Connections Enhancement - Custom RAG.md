---
created: 2025-10-23
pageType: misc
tags:
  - claude
  - vibe-code-project
Related Pages:
  - "[[Evaluation]]"
  - "[[RAG Enhancement Techniques - Reranking and Contextual Retrieval]]"
aliases:
  - obsidian rag
Status: Done
---
# Smart Connections Enhancement 
---

A vibe code project to build a new Obsidian RAG plugin that replaces Smart Connections, using hybrid search, graph-aware retrieval, and multi-signal ranking for improved vault discovery.

**GitHub Repository**: https://github.com/tooape/obsidianrag

## Current Status (November 2025)
---

✅ **Phase 1 Complete**: Hybrid search + graph-aware retrieval working

**What Works**:
- EmbeddingGemma @ 256d semantic search (78% better MRR than BGE)
- BM25 keyword matching with query expansion via aliases
- Graph traversal with PageRank weighting (finds daily notes linking to hubs)
- Temporal boosting with exponential decay (recent notes ranked higher)
- Multi-signal ranking via Reciprocal Rank Fusion
- MCP-compatible interface (`search_vault_smart`)
- Query latency: <50ms, storage: 600KB for 670 notes

🚧 **Phase 2 In Progress**: Tool redesign + chunk-based results

**Next Steps**:
1. Return chunk-level results instead of file-level (3-4x token efficiency for Claude Code)
2. Split into `smartSearch` (query-driven) + `graphBrowse` (structure-driven) tools
3. Fix cross-encoder reranking to work at chunk level (not file level)
4. Add "Recent Notes" signal (30-day edited window) to smart search

## November 2025 Architecture Review
---

### Key Insights from Claude Code Integration

**1. Chunk-Based Results for Agent Workflows**

Moving from file-level to chunk-level results for Claude Code:
- **Current limitation**: Search deduplicates to file level before returning results, losing chunk granularity
- **Better approach**: Return chunks directly to Claude, let it decide whether to Read full files
- **Token efficiency**: 3-4x improvement (answer from 5 chunks = ~2K tokens vs Read 2 files = ~10K tokens)
- **Chunk sizes**: H2 sections average 200-700 chars (vs 200-char excerpts), provide complete semantic units
- **Chunk format**: `${noteName} - ${heading}\n${content}` - includes context without file read

**Why this works**:
- Chunks already indexed and cached (no extra work)
- Natural semantic boundaries (H2 sections = complete thoughts)
- Include heading + document name for context
- Claude can selectively Read files only when chunk excerpts insufficient

**2. Tool Architecture Redesign: Split Search & Browse**

Current unified search mixes incompatible use cases. Proposed split:

**Smart Search Tool** (query-driven discovery):
```typescript
smartSearch({
  query: "photoshop recommendations status",
  returnChunks: true,  // Chunk-level results
  maxResults: 20
})

Signals:
- Semantic (EmbeddingGemma chunks)
- BM25 (keyword matching)
- Recent Notes (edited in last 30 days) - hardcoded into recall set
```

**Graph Browse Tool** (structure-driven exploration):
```typescript
graphBrowse({
  seeds: ["Photoshop Web", "November 15, 2025"],
  depth: 1,           // or 2 for broader exploration
  rankBy: "pagerank" | "recency" | "edgeWeight",
  direction: "both" | "inbound" | "outbound",
  maxResults: 20,
  returnChunks: true
})
```

**Benefits**:
- Clear separation: "find something" vs "explore connections"
- Graph browse is cheap (no embedding/reranking), enables multi-step exploration
- More granular control for Claude (choose depth, ranking, direction per query)
- Removes graph/temporal from search recall set (faster, simpler)

**Agent Workflow Example**:
```
1. smartSearch("photoshop recommendations") → Get initial matches
2. graphBrowse({seeds: ["Photoshop Web"], depth: 1, rankBy: "recency"})
   → Explore recent connections
3. Read specific files with multiple high-scoring chunks
```

**3. Cross-Encoder Reranking Issues**

**Current problem** (line 4485-4515 in main.js):
```typescript
// ❌ Deduplicates to files BEFORE reranking (loses best chunks)
const deduplicatedResults = deduplicateToFiles(results);
await crossEncoderReranker.rerank(query, deduplicatedResults);

// ❌ Inconsistent reranking inputs:
if (result.chunkText) {
  return result.chunkText;  // Semantic: proper chunks ✓
} else {
  return content.slice(0, 2000);  // BM25/Graph/Temporal: truncated docs ✗
}
```

**Best practices** ([Cohere](https://docs.cohere.com/docs/reranking-best-practices), [Galileo AI](https://galileo.ai/blog/mastering-rag-how-to-select-a-reranking-model)):
- Chunk documents before retrieval (~250 tokens / 1000 chars)
- Rerank at chunk level (not document level)
- "Large chunks dilute relevance signals" - need focused context
- Pattern: Retrieve 100 chunks → Rerank to top 20 → Optionally aggregate to documents

**Proposed fix**:
```typescript
// Option 1: Rerank chunks, then deduplicate
const chunkResults = await rrf(semantic, bm25Chunks, graphChunks, temporalChunks);
const rerankedChunks = await crossEncoder.rerank(query, chunkResults);
const topFiles = deduplicateToFiles(rerankedChunks);  // After reranking

// Option 2: Extract chunks for all signals before reranking
for (result in rrfResults) {
  if (!result.chunkText) {
    result.chunkText = extractRelevantChunk(result.file, query);  // Use H2 boundaries
  }
}
const reranked = await crossEncoder.rerank(query, rrfResults);
```

**Impact**: BM25/Graph/Temporal results currently get crude 2000-char truncation vs proper chunk-level reranking for semantic results. This explains why semantic consistently outperforms other signals.

**4. Recent Notes Signal Design**

For the new "Recent Notes" signal in smart search:
- **Window**: 30 days (edited, not created) - shorter than current 120-day temporal
- **Purpose**: Hard-code actively maintained notes into recall set
- **Cross-encoder concern**: Recent full docs could score lower than focused chunks
- **Mitigation**: First 2000 chars likely contain relevant content (title, intro, early headings)
- **Alternative**: Extract chunks from recent notes before reranking for consistency

## Architecture Overview
---

### The Problem
Smart Connections uses **semantic search only**. Query: "What's the status of Lr Agent?" returns `[[Lr Home]]` but misses the last 10 daily notes where the actual current status lives.

**Solution**: Multi-signal ranking combining:
- **Semantic** (EmbeddingGemma) - what is it about?
- **Lexical** (BM25) - exact keywords?
- **Graph** (PageRank + backlinks) - how important is it?
- **Temporal** (recency decay) - how recent is it?

### Recall Set Formation
```
Query → Semantic search (top 100 chunks)
     → Graph expansion (daily notes linking to top 5 seeds)
     → BM25 lexical search (with alias expansion)
     → Merge all candidates (union)
     → RRF ranking (combine all signals)
     → Cross-encoder reranking (optional)
     → Top 20 results to user
```

### Multi-Signal Ranking Formula
```
score = RRF(semantic, bm25, graph, temporal)

RRF = Σ weight[signal] / (k + rank[signal])

Where:
- semantic: EmbeddingGemma 256d embeddings via Python backend
- bm25: MiniSearch with field boosting (title 2x, aliases 2x, etc)
- graph: PageRank + backlink count, weighted by recency
- temporal: exp(-ln(2) * age_days / 30) capped at 120-day window
- k = 60 (RRF parameter)
```

## Phase 1 Implementation Details
---

### Component Configurations

**Python Backend (FastAPI on localhost:8000)**:
- Embedding generation: `POST /api/embed`
- Semantic search: `POST /api/search`
- Matryoshka truncation: 768d → 256d (zero quality loss)
- Persistent NPZ cache (~600 KB for 670 notes)
- Query latency: ~18-20ms

**Graph Expansion**:
```typescript
graphExpansionConfig: {
  enabled: true,
  maxNeighborsPerSeed: 15,    // Per seed note
  traversalDepth: 1,           // 1-hop neighbors
  weightByPageRank: true       // PageRank × log(1 + edges) × recency
}
```

**BM25 Field Boosting**:
```typescript
boost: {
  title: 2.0,      // Filename
  aliases: 2.0,    // Frontmatter aliases
  tags: 2.0,       // Tags
  pageType: 1.5,   // Page type
  h1: 1.5,         // H1 headings
  h2: 1.3,         // H2 headings
  h3: 1.1,         // H3 headings
  content: 1.0     // Body content
}
```

**Query Expansion Strategy**:
1. Semantic search finds top 5 conceptually relevant pages
2. Extract aliases from those pages' frontmatter
3. Build OR query: `"photoshop OR ps OR 'ps web'"`
4. BM25 finds keyword matches using abbreviations

**Temporal Decay**:
```typescript
score = Math.pow(2, -age_days / halfLife)  // Default halfLife = 30 days

Filtering strategy:
- Always include: Notes from last 120 days
- Older notes: Only boost if found by semantic/BM25
```

### Why EmbeddingGemma Outperforms BGE

**Benchmark Results** (32 vault notes, 6 test queries):

| Metric | EmbeddingGemma @ 256d | BGE-M3 | Winner | Improvement |
|--------|----------------------|--------|---------|-------------|
| **Precision@10** | **25.0%** | 18.3% | 🥇 Gemma | +36% |
| **MRR** | **1.000** | 0.563 | 🥇 Gemma | +78% |
| **Recall@10** | **69.2%** | 48.3% | 🥇 Gemma | +43% |
| **NDCG@10** | **0.698** | 0.434 | 🥇 Gemma | +61% |
| **Query Latency** | 18ms | 201ms | 🥇 Gemma | 11x faster |

**Key Finding**: EmbeddingGemma achieved **MRR = 1.0** (perfect first result) across all 6 queries. BGE only 56% of the time (MRR = 0.563).

**BGE's Weakness**: Confused by daily notes with high vocabulary diversity. Example:
- Query: "Recent decisions about Recommendations"
- BGE: Ranked generic "February 05, 2025.md" as #1 (mentions many topics)
- Gemma: Ranked "Recommendations Home.md" as #1 (canonical page)

**Matryoshka Optimization**:
- 768d → 256d: Zero quality degradation
- Storage: 66% reduction (1.9 MB → 0.6 MB)
- Speed: 2.8x faster similarity computation (49ms → 18ms)

## Related Documentation
---

**Deployment & Operations**:
- [[Obsidian RAG - Deployment & Troubleshooting]] - Backend setup, common issues, fixes
- [[Obsidian RAG - Token Efficiency for Claude]] - How to keep token usage low in MCP

**Research & Theory**:
- [[RAG Enhancement Techniques - Reranking and Contextual Retrieval]] - Contextual embedding concepts
- [[Graph Traversal for Recall Enhancement - October 2025]] - Graph-based retrieval research
- [[Evaluation]] - Evaluation methodology

## Roadmap
---

### Phase 2: Tool Redesign + Chunk-Based Results (Priority)

**Goal 1: Split into Smart Search + Graph Browse**

Remove graph/temporal signals from unified search, create dedicated browse tool:

```typescript
// Simplified smart search (query-driven)
smartSearch({
  query: string,
  signals: ["semantic", "bm25", "recentNotes"],  // No graph/temporal
  returnChunks: true,
  maxResults: 20
})

// New graph browse tool (structure-driven)
graphBrowse({
  seeds: string[],        // Starting notes
  depth: 1 | 2,          // Traversal depth
  rankBy: "pagerank" | "recency" | "edgeWeight",
  direction: "both" | "inbound" | "outbound",
  returnChunks: true,
  maxResults: 20
})
```

**Goal 2: Chunk-Based Results for Claude Code**

Return H2 section chunks instead of file-level results:
- **Format**: `{file, heading, chunkText, score}` for each result
- **Token efficiency**: 3-4x reduction (answer from chunks vs Read files)
- **Claude decides**: Use chunk excerpts directly or Read full file
- **No excerpt generation**: Chunks are already perfect size (200-700 chars avg)

**Goal 3: Fix Cross-Encoder Reranking**

Current issues:
- ❌ Deduplicates before reranking (loses chunk granularity)
- ❌ BM25/Graph/Temporal get 2000-char truncation vs proper chunks for semantic

Fix approach:
- Rerank all results at chunk level (not file level)
- Extract chunks for BM25 results (use H2 boundaries + query match)
- Deduplicate to files AFTER reranking (optional, for file-level output)
- Or keep chunk-level results for Claude (preferred)

**Effort**: ~500 lines TypeScript (tool split + chunk return format + reranking fix)

### Phase 3: Intent-Based Search with Adaptive Bias

Preset search modes that auto-adjust weights:

```typescript
search_vault_smart(
  "Lr Agent",
  intent: 'status'  // Boosts temporal 3x, reduces graph 0.5x
)
```

**Intent Modes**:
- `status` - Recent notes (temporal 3x)
- `discovery` - Related topics (semantic 3x, graph 2x)
- `concept` - Canonical explanations (graph 1x, temporal 0.2x)
- `person` - Find who (BM25 3x, graph 3x)
- `timeline` - What happened when (temporal 2x)

### Phase 4: Contextual Retrieval & GraphRAG

- Add LLM-generated context to chunks (precision improvement)
- Full GraphRAG: LLM entity extraction + hierarchical clustering

---

## Development
---

**Local Development**:
```bash
cd /Users/rmanor/obsidianrag
git checkout -b feature/your-feature
npm run dev          # Watch TypeScript
# In another terminal:
./python-backend/start.sh
```

**Build & Deploy**:
```bash
npm run build        # Compiles TS → main.js + esbuild
# Files auto-copy to ~/.obsidian/plugins/obsidian-rag/
# Restart Obsidian to reload
```

**Testing**:
- Manual: Search in Obsidian, check console logs for signal contributions
- Verify graph expansion, query expansion, temporal boosting via debug logs

---

## Repository Structure
---

```
obsidianrag/
├── obsidian-plugin/               # TypeScript plugin
│   ├── src/
│   │   ├── main.ts                # Plugin entry point
│   │   ├── SearchOrchestrator.ts  # Multi-signal ranking + RRF + graph expansion
│   │   ├── CrossEncoderReranker.ts# Mixedbread reranker integration
│   │   ├── GraphAnalyzer.ts       # Graph traversal + PageRank
│   │   ├── MiniSearchIndexer.ts   # BM25 wrapper (MiniSearch)
│   │   ├── QueryExpander.ts       # Query expansion via aliases
│   │   ├── QueryParser.ts         # Tag filter parsing
│   │   ├── TemporalAnalyzer.ts    # Recency scoring
│   │   ├── DocumentChunker.ts     # H2-based chunking
│   │   ├── FileChangeHandler.ts   # Incremental index updates
│   │   ├── SearchModal.ts         # UI
│   │   └── SettingsTab.ts         # Configuration
│   ├── esbuild.config.mjs
│   └── package.json
└── python-backend/                # FastAPI server
    ├── app/
    │   ├── main.py                # FastAPI app
    │   └── models/
    │       ├── embedder.py        # EmbeddingGemma @ 256d
    │       └── reranker.py        # Mixedbread cross-encoder
    ├── requirements.txt
    ├── start.sh                   # Launch script
    └── cache/
        └── embeddings.npz         # Persistent cache (~600 KB)
```

---

## Key Decisions
---

| Decision | Choice | Why |
|----------|--------|-----|
| Embedding model | **EmbeddingGemma @ 256d** | 78% better MRR vs BGE, Matryoshka optimization (zero quality loss, 66% smaller) |
| BM25 library | **MiniSearch** | Battle-tested (powers Omnisearch), fuzzy matching, field boosting |
| Graph algorithm | **PageRank + backlinks** | Simple, effective, pre-computed, query-independent |
| Temporal strategy | **Exponential decay (λ=30d)** + **120d window** | Balances recency without hiding old work |
| Ranking method | **Reciprocal Rank Fusion** | Simple, proven, combines heterogeneous signals without ML |
| Signal weighting | **All weights = 1.0 (equal)** | Start simple, can tune via UI if needed |
| Python backend | **FastAPI on localhost:8000** | Mature, lightweight, future-proofs for ONNX migration |
| **Result format** | **Chunk-level (H2 sections)** | 3-4x token efficiency for Claude Code, natural semantic boundaries, 200-700 char avg |
| **Tool architecture** | **Split: smartSearch + graphBrowse** | Separates query-driven discovery from structure-driven exploration, more granular control |
| **Reranking** | **Chunk-level cross-encoder** | Best practice per Cohere/Galileo AI, prevents diluted relevance signals from full docs |

