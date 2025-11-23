---
pageType: claudeResearch
tags:
  - claude
created: "2025-10-30"
---
# Graph Traversal for Recall Enhancement
---

## The Problem

**Current behavior** (as noted in project motivation):
- Query: "What's the status of the Lr Agent project?"
- Semantic/BM25 finds: `[[Lr Home]]` ✓
- **Misses**: Last 10 daily notes mentioning "Lr Agent" where actual current status lives ✗

**Root cause**: Graph is only used for **ranking** (PageRank), not **recall** (expanding candidates).

### Current Retrieval Flow

```
Query: "Lr Agent status"
    ↓
Semantic Search → finds [[Lr Home]] (0.87 similarity)
    ↓
BM25 Search → finds [[Lr Home]] (keyword match)
    ↓
Graph Signal → ranks [[Lr Home]] higher (high PageRank)
    ↓
Result: Only [[Lr Home]] returned
```

**Missing**: All the daily notes that:
- Link TO [[Lr Home]] → "Today's update on [[Lr Home]]"
- Link FROM [[Lr Home]] → Hub page links to recent updates
- Are connected via 2-hop paths → Daily note → [[Lr Home]] → Another daily note

## The Solution: Graph Traversal for Recall

Use graph structure to **expand the candidate set**, not just rerank existing candidates.

### Enhanced Retrieval Flow

```
Query: "Lr Agent status"
    ↓
Semantic Search → finds [[Lr Home]] (initial seed)
    ↓
Graph Traversal → expands to neighbors:
    • Inbound links: Daily notes linking TO [[Lr Home]]
    • Outbound links: Pages linked FROM [[Lr Home]]
    • 2-hop connections: Daily note → Hub → Daily note
    ↓
Expanded Candidate Set: 50 notes instead of 5
    ↓
BM25 + Graph + Temporal → rerank with multi-signal
    ↓
Result: Recent daily notes with status updates ranked high
```

## Graph Traversal Strategies

### 1. Backlink Expansion (Inbound Links)

**Concept**: Notes linking TO high-scoring results are likely relevant

**Example**:
```
Query: "Lr Agent"
Semantic finds: [[Lr Home]]
Backlink expansion adds:
  - [[October 30, 2025]] → links to [[Lr Home]]
  - [[October 27, 2025]] → links to [[Lr Home]]
  - [[Lr Agent Kickoff]] → links to [[Lr Home]]
```

**Code**:
```typescript
getInboundNeighbors(nodeId: string, maxDepth: number = 1): string[] {
    const neighbors = new Set<string>();

    // Direct backlinks (1-hop)
    this.graph.forEachInEdge(nodeId, (edge, attributes, source) => {
        neighbors.add(source);
    });

    // 2-hop backlinks (if maxDepth > 1)
    if (maxDepth > 1) {
        const firstHop = Array.from(neighbors);
        for (const neighbor of firstHop) {
            this.graph.forEachInEdge(neighbor, (edge, attributes, source) => {
                neighbors.add(source);
            });
        }
    }

    return Array.from(neighbors);
}
```

### 2. Forward Link Expansion (Outbound Links)

**Concept**: Notes linked FROM high-scoring results are likely relevant

**Example**:
```
Query: "PS Web recommendations"
Semantic finds: [[Recommendations Home]]
Forward expansion adds:
  - [[PS Web Implementation]] ← linked from Recommendations Home
  - [[Search Ranking Algorithms]] ← linked from Recommendations Home
  - [[Photoshop Web]] ← linked from Recommendations Home
```

**Code**:
```typescript
getOutboundNeighbors(nodeId: string, maxDepth: number = 1): string[] {
    const neighbors = new Set<string>();

    // Direct outbound links (1-hop)
    this.graph.forEachOutEdge(nodeId, (edge, attributes, target) => {
        neighbors.add(target);
    });

    // 2-hop outbound links (if maxDepth > 1)
    if (maxDepth > 1) {
        const firstHop = Array.from(neighbors);
        for (const neighbor of firstHop) {
            this.graph.forEachOutEdge(neighbor, (edge, attributes, target) => {
                neighbors.add(target);
            });
        }
    }

    return Array.from(neighbors);
}
```

### 3. Bidirectional Expansion (Most Powerful)

**Concept**: Traverse both directions to find the "neighborhood" around seed results

**Example**:
```
Query: "Intent AI progress"
Semantic finds: [[Intent AI Home]]

Bidirectional expansion:
  Inbound (daily notes referencing Intent AI):
    - [[October 30, 2025]]
    - [[October 27, 2025]]
    - [[Intent AI Roadmap]]

  Outbound (pages Intent AI Home links to):
    - [[Query Understanding]]
    - [[NER and SRL]]
    - [[Recommendations Home]] (shared tech)

  2-hop connections:
    - [[October 30, 2025]] → [[Intent AI Home]] → [[Query Understanding]]
    - [[Lr Home]] → [[Query Understanding]] ← [[Intent AI Home]]
```

**Code**:
```typescript
expandCandidateSet(
    seedNoteIds: string[],
    maxNeighbors: number = 20,
    traversalDepth: number = 1
): string[] {
    const expanded = new Set<string>(seedNoteIds);

    for (const noteId of seedNoteIds) {
        const nodeId = this.pathToNodeId(noteId);

        if (!this.graph.hasNode(nodeId)) continue;

        // Get inbound neighbors (backlinks)
        const inbound = this.getInboundNeighbors(nodeId, traversalDepth);
        inbound.slice(0, maxNeighbors).forEach(n => expanded.add(this.nodeIdToPath(n)));

        // Get outbound neighbors (forward links)
        const outbound = this.getOutboundNeighbors(nodeId, traversalDepth);
        outbound.slice(0, maxNeighbors).forEach(n => expanded.add(this.nodeIdToPath(n)));
    }

    return Array.from(expanded);
}
```

### 4. Weighted Expansion (Smart Filtering)

**Concept**: Not all neighbors are equally relevant - weight by PageRank and edge count

**Example**:
```
Query: "PS Web"
Semantic finds: [[Photoshop Web]]

Unweighted expansion (naive):
  - [[Random Meeting Note]] (mentioned PS Web once)
  - [[Unrelated Daily Note]] (tangential mention)

Weighted expansion (smart):
  - Filter neighbors by:
    • High PageRank (important notes)
    • Multiple edges (strong connection)
    • Recent modification (temporal signal)
  - Keep only top-scoring neighbors
```

**Code**:
```typescript
expandCandidateSetWeighted(
    seedNoteIds: string[],
    maxNeighborsPerSeed: number = 10
): Array<{noteId: string, score: number}> {
    const candidates = new Map<string, number>();

    for (const noteId of seedNoteIds) {
        const nodeId = this.pathToNodeId(noteId);
        if (!this.graph.hasNode(nodeId)) continue;

        // Get all neighbors (inbound + outbound)
        const neighbors: Array<{id: string, edgeCount: number}> = [];

        // Count inbound edges for each neighbor
        this.graph.forEachInEdge(nodeId, (edge, attr, source) => {
            const existing = neighbors.find(n => n.id === source);
            if (existing) {
                existing.edgeCount++;
            } else {
                neighbors.push({id: source, edgeCount: 1});
            }
        });

        // Count outbound edges for each neighbor
        this.graph.forEachOutEdge(nodeId, (edge, attr, target) => {
            const existing = neighbors.find(n => n.id === target);
            if (existing) {
                existing.edgeCount++;
            } else {
                neighbors.push({id: target, edgeCount: 1});
            }
        });

        // Score each neighbor by PageRank × edge count
        for (const neighbor of neighbors) {
            const pagerank = this.pagerankScores.get(neighbor.id) || 0;
            const score = pagerank * Math.log(1 + neighbor.edgeCount);

            const path = this.nodeIdToPath(neighbor.id);
            candidates.set(path, Math.max(candidates.get(path) || 0, score));
        }
    }

    // Return top-K weighted neighbors
    return Array.from(candidates.entries())
        .map(([noteId, score]) => ({noteId, score}))
        .sort((a, b) => b.score - a.score)
        .slice(0, maxNeighborsPerSeed * seedNoteIds.length);
}
```

## Integration with Current Search Flow

### Option 1: Expand After Initial Retrieval (Conservative)

```typescript
async search(query: string, topK: number = 50): Promise<SearchResult[]> {
    // Phase 1: Get initial candidates (semantic + BM25)
    const semanticResults = await this.getSemanticResults(query, 50);
    const bm25Results = this.getBM25Results(query, 50);

    // Phase 2: Graph expansion on top semantic results
    const topSeeds = semanticResults.slice(0, 5).map(r => r.noteId);
    const expandedCandidates = this.graph.expandCandidateSet(topSeeds, 20, 1);

    // Phase 3: Add expanded candidates to ranking pool
    const allCandidates = new Set([
        ...semanticResults.map(r => r.noteId),
        ...bm25Results.map(r => r.noteId),
        ...expandedCandidates
    ]);

    // Phase 4: Multi-signal reranking on expanded set
    return this.rerankWithMultiSignal(Array.from(allCandidates), query, topK);
}
```

### Option 2: Expand Before BM25 (Aggressive)

```typescript
async search(query: string, topK: number = 50): Promise<SearchResult[]> {
    // Phase 1: Semantic search (initial seeds)
    const semanticResults = await this.getSemanticResults(query, 30);

    // Phase 2: Graph expansion (add neighborhood)
    const topSeeds = semanticResults.slice(0, 5).map(r => r.noteId);
    const graphExpanded = this.graph.expandCandidateSet(topSeeds, 15, 1);

    // Phase 3: BM25 search on expanded candidate set
    // This helps find daily notes mentioning key concepts
    const expandedSet = [...semanticResults.map(r => r.noteId), ...graphExpanded];
    const bm25Results = this.bm25.searchWithinCandidates(query, expandedSet, 50);

    // Phase 4: Multi-signal reranking
    return this.rerankWithMultiSignal(bm25Results, query, topK);
}
```

## Expected Impact

### Before Graph Traversal

```
Query: "Lr Agent status"
Candidates: 5-10 notes
  - [[Lr Home]] (semantic: 0.87)
  - [[Lightroom]] (semantic: 0.65)
  - [[Query Understanding]] (semantic: 0.62)

Result: Static hub page ranked #1
```

### After Graph Traversal

```
Query: "Lr Agent status"
Initial seeds: [[Lr Home]] (semantic: 0.87)
Graph expansion adds:
  - [[October 30, 2025]] (backlink to Lr Home)
  - [[October 27, 2025]] (backlink to Lr Home)
  - [[Lr Agent Kickoff]] (backlink to Lr Home)
  - [[Query Understanding]] (forward link from Lr Home)

Candidates: 30-50 notes
Multi-signal reranking:
  - [[October 30, 2025]] → high temporal + graph signal
  - [[October 27, 2025]] → high temporal + graph signal
  - [[Lr Home]] → high semantic + PageRank

Result: Recent daily notes with status updates ranked high
```

## Implementation Plan

### Phase 1: Add Graph Traversal Methods (GraphAnalyzer.ts)

**Estimated time**: 2-3 hours

1. **Add traversal methods**:
   - `getInboundNeighbors(nodeId, maxDepth)`
   - `getOutboundNeighbors(nodeId, maxDepth)`
   - `expandCandidateSet(seedNoteIds, maxNeighbors, depth)`
   - `expandCandidateSetWeighted(seedNoteIds, maxNeighbors)`

2. **Helper methods**:
   - `pathToNodeId(path: string): string`
   - `nodeIdToPath(nodeId: string): string`

3. **Unit tests**:
   - Test 1-hop expansion
   - Test 2-hop expansion
   - Test weighted filtering

### Phase 2: Integrate with SearchOrchestrator (SearchOrchestrator.ts)

**Estimated time**: 2-3 hours

1. **Add configuration**:
   ```typescript
   interface GraphExpansionConfig {
       enabled: boolean;
       maxNeighborsPerSeed: number;
       traversalDepth: number;
       weightByPageRank: boolean;
   }
   ```

2. **Modify search flow**:
   - Get top-5 semantic seeds
   - Expand with graph traversal
   - Add expanded candidates to ranking pool
   - Rerank with multi-signal

3. **Add telemetry**:
   - Log expansion statistics
   - Track how many graph-expanded results make top-10

### Phase 3: Settings & Tuning (SettingsTab.ts)

**Estimated time**: 1 hour

1. **Add settings**:
   - Enable/disable graph expansion
   - Max neighbors per seed (default: 15)
   - Traversal depth (1 or 2 hops)
   - Weight by PageRank (default: true)

2. **Provide presets**:
   - Conservative: 10 neighbors, 1-hop, weighted
   - Balanced: 15 neighbors, 1-hop, weighted
   - Aggressive: 20 neighbors, 2-hop, weighted

## Success Criteria

- ✅ Graph traversal expands initial candidate set by 3-5x
- ✅ Daily notes linking to canonical pages appear in top-10 results
- ✅ Query "X project status" returns recent daily notes, not just hub page
- ✅ No significant performance degradation (<100ms added latency)
- ✅ User can configure expansion aggressiveness

## Trade-offs

### Benefits
✅ **Improved recall**: Finds daily notes and context missing from semantic search
✅ **Leverages vault structure**: Uses existing wikilink relationships
✅ **Temporal awareness**: Recent daily notes linking to hubs get surfaced
✅ **No training required**: Pure graph traversal, no ML needed

### Costs
⚠️ **Increased candidate set**: More notes to rerank (performance impact)
⚠️ **Potential noise**: Loosely related neighbors might get included
⚠️ **Configuration complexity**: More parameters to tune

### Mitigations
- **Weighted expansion**: Filter by PageRank and edge strength
- **Depth limiting**: 1-hop by default, 2-hop optional
- **Max neighbors**: Cap at 15-20 per seed
- **Smart presets**: Provide good defaults, allow tuning

## Related Documents

- [[Smart Connections Enhancement - Custom RAG]] - Parent project page
- [[Obsidian RAG Memory Optimization - October 2025]] - Memory optimization
- [[ONNX Implementation Plan - October 2025]] - Model optimization
- [[Backend Idle Model Unloading - October 2025]] - Idle memory strategy

## References

- Microsoft GraphRAG Paper: https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/
- Graph Traversal Algorithms: https://en.wikipedia.org/wiki/Graph_traversal
- Graphology Library Docs: https://graphology.github.io/
- PageRank + Graph Features: https://github.com/graphology/graphology/tree/master/src/metrics
