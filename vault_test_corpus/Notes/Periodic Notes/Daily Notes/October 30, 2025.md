---
pageType: daily
aliases:
  - "2025-10-30"
created: "2025-10-30"
---
# [[October 30, 2025]]
# Notes
---

[[Anuj Agarwal|Anuj]] has the [[Lr Home|Lr]] dashboard set up ([instructions in slack](https://adobe.enterprise.slack.com/archives/D08FW21C5A4/p1761822298772259))

## 2026 Intern resumes: 
[[R160316 - 2026 MBA Intern - Product Manager_2025-10-29-22-15-40.pdf]]

- people I liked:
	- Mert
	- Sean
	- Maria
	- Armando
	- SOPHIA GAO
	- SNEHA

## [[Smart Connections Enhancement - Custom RAG|Obsidian RAG]] Memory Optimization

Investigated 600MB memory usage for the Python backend. Created comprehensive analysis: [[Obsidian RAG Memory Optimization - October 2025]]

**Key Findings**:
- Current: 600MB for EmbeddingGemma-300m model
- Model on disk: 1.2GB
- Memory breakdown: ~600MB model weights + Python/FastAPI/PyTorch overhead

**Optimization Options**:
1. **ONNX + int8 quantization** (RECOMMENDED): <200MB (67% reduction), same quality
2. **Switch to MiniLM**: ~80MB (87% reduction), lower quality but 5x faster
3. **Lazy loading**: 0MB when idle, start backend on-demand
4. **FP16 optimization**: ~350MB (42% reduction), quick win

**Recommended Approach**: Implement FP16 + lazy loading as quick wins, then migrate to ONNX int8 for production.

### Backend Idle Model Unloading Strategy

Created detailed plan for lazy model loading: [[Backend Idle Model Unloading - October 2025]]

**Approach**: Keep FastAPI backend running but unload model after idle timeout
- **Memory when idle**: ~50MB (just backend server)
- **Memory when active**: 600MB → <200MB with ONNX
- **Reload time**: 2-3 seconds (acceptable, vs 5-10 for full backend restart)
- **Battery friendly**: Minimal CPU usage when model unloaded
- **Cache preserved**: Embeddings cache stays in memory

**Implementation**:
- Add idle timer to Python backend (10 min default, configurable)
- Lazy load model on first search request after idle
- Show loading indicator during 2-3 second reload
- Combine with ONNX for <200MB active memory

**User preference**: Can tolerate 2-3 second delay, not 5-10 seconds.

### Graph Traversal for Recall Enhancement

Explored using graph traversal to expand candidate set, not just rerank: [[Graph Traversal for Recall Enhancement - October 2025]]

**Problem**: Currently graph is only used for ranking (PageRank), not recall
- Query: "Lr Agent status"
- Semantic finds: [[Lr Home]] (hub page)
- Misses: Daily notes linking to [[Lr Home]] with actual status updates

**Solution**: Use graph traversal to expand candidates
- Start with semantic seeds (e.g., [[Lr Home]])
- Traverse inbound links (backlinks) → find daily notes
- Traverse outbound links (forward links) → find related pages
- Add graph neighborhood to candidate pool BEFORE reranking

**Traversal strategies**:
1. **Backlink expansion**: Find notes linking TO high-scoring results
2. **Forward link expansion**: Find notes linked FROM high-scoring results
3. **Bidirectional expansion**: Traverse both directions (most powerful)
4. **Weighted expansion**: Filter by PageRank and edge strength

**Expected impact**: 3-5x larger candidate set, daily notes linking to hubs surface in results

**Implementation**: ~5-6 hours total
- Add traversal methods to GraphAnalyzer
- Integrate with SearchOrchestrator
- Add configuration settings

### Implemented Graph Traversal for Recall

Successfully implemented graph traversal for recall enhancement. See [[Graph Traversal for Recall Enhancement - October 2025]] for full details.

**What was implemented**:
1. **GraphAnalyzer.ts** (GraphAnalyzer.ts:220-382):
   - `getInboundNeighbors()` - traverse backlinks (1 or 2 hops)
   - `getOutboundNeighbors()` - traverse forward links (1 or 2 hops)
   - `expandCandidateSet()` - bidirectional expansion
   - `expandCandidateSetWeighted()` - weighted by PageRank and edge strength

2. **SearchOrchestrator.ts** (SearchOrchestrator.ts:160-185):
   - Added graph expansion after semantic search
   - Top-5 semantic results used as seeds
   - Expands to neighbors before BM25/graph/temporal ranking
   - Graph-expanded notes included in query-relevant set

3. **Settings** (main.ts:30-33, SettingsTab.ts:179-255):
   - Enable/disable graph expansion (default: enabled)
   - Max neighbors per seed (default: 15)
   - Traversal depth: 1-hop or 2-hop (default: 1)
   - Weight by PageRank (default: true)

**How it works**:
```
Query: "Lr Agent status"
    ↓
Semantic search → finds [[Lr Home]] (seed)
    ↓
Graph expansion → adds:
  • Daily notes linking TO [[Lr Home]] (backlinks)
  • Pages linked FROM [[Lr Home]] (forward links)
    ↓
Candidate set: 5 → 30-50 notes
    ↓
Multi-signal reranking → Recent daily notes rank high
```

**Expected results**:
- Queries like "X project status" should now find recent daily notes
- Hub pages will still appear but won't dominate results
- Daily notes linking to hubs get surfaced

**Ready for testing**: Plugin rebuilt and deployed, awaiting user feedback

