---
pageType: claudeResearch
created: 2025-10-30
tags:
  - claude
datelink: "[[October 30, 2025]]"
Related Pages:
  - "[[Smart Connections Enhancement - Custom RAG]]"
  - "[[Graph Traversal for Recall Enhancement - October 2025]]"
---
# Graph Expansion Analysis: October 28 Brian Meeting
---

## The Problem

**User query**: "When was the last time I spoke with Brian and what did we discuss?"

**Expected**: October 28, 2025 note (most recent Brian conversation)

**What happened**:
1. Initial search "Brian meeting conversation" returned October 26 at top (wrong)
2. Person page "Brain Eriksson" ranked #5
3. **October 28 note completely missing from results**

## Root Cause Analysis

### Why Oct 28 Was Missing

**Oct 28 note structure** (Notes/Periodic Notes/Daily Notes/October 28, 2025.md:15):
```markdown
## [[Style Home|Photo styles]] chat with [[Brain Eriksson|Brian]]
```

**Problem**: Non-standard pattern
- **Standard**: `## Brian #meetings/1x1`
- **Actual**: `## [[Style Home|Photo styles]] chat with [[Brain Eriksson|Brian]]`

**Impact**:
- BM25 doesn't strongly match "Brian" (buried in wikilink markup)
- No `#meetings/1x1` tag for pattern matching
- Semantic similarity likely lower (heading about "Photo styles")

### Graph Expansion Logic

**Current implementation** (GraphAnalyzer.ts:366-369):
```typescript
const pagerank = this.pagerankScores.get(neighborNodeId) || 0;
const score = pagerank * Math.log(1 + edgeCount);
```

**Scoring breakdown**:
- **Daily notes**: Low PageRank (not hubs, fewer incoming links)
- **Oct 28 → Brian link**: edgeCount = 1
- **Score**: `low_pagerank × log(2) = low_pagerank × 0.693`

**Comparison to hub pages**:
- **Hub page neighbor**: High PageRank × log(1 + many_edges) >> daily note score
- **Result**: Daily notes filtered out in favor of hub pages and frequently-linked notes

### The Fundamental Trade-off

**Weighted expansion optimizes for**:
✅ High-quality neighbors (well-connected, important notes)
✅ Filtering noise (random mentions)

**But filters out**:
❌ Recent daily notes (low PageRank but high temporal value)
❌ Single mentions (edgeCount = 1 but potentially relevant)

## Evidence: Graph Expansion is Working (But Filtering Too Aggressively)

**From SearchOrchestrator.ts:162-184**:
```typescript
if (this.graphExpansionConfig.enabled && semanticResults.length > 0) {
    const seedNotes = semanticResults.slice(0, 5).map((r) => r.noteId);

    if (this.graphExpansionConfig.weightByPageRank) {
        const expandedWeighted = this.graph.expandCandidateSetWeighted(
            seedNotes,
            this.graphExpansionConfig.maxNeighborsPerSeed  // default: 15
        );
        graphExpandedNoteIds = expandedWeighted.map((e) => e.noteId);
    }
}
```

**Process**:
1. Top-5 semantic seeds include "Brain Eriksson" person page ✓
2. Graph expansion finds all backlinks (including Oct 28) ✓
3. **Weighted scoring filters Oct 28 out** (low PageRank × low edgeCount) ✗

## Solutions

### Option 1: Temporal Boosting in Graph Expansion (Recommended)

**Concept**: Boost recent notes in graph expansion scoring

**Modified scoring** (GraphAnalyzer.ts):
```typescript
const pagerank = this.pagerankScores.get(neighborNodeId) || 0;
const temporal = this.getTemporalScore(neighborNodeId);  // 2^(-days/30)
const score = (pagerank + temporal * 0.5) * Math.log(1 + edgeCount);
```

**Impact**:
- Recent daily notes get temporal boost even with low PageRank
- Oct 28 (2 days old): temporal ≈ 0.95, significant boost
- Old notes: temporal decays, no unintended boost

**Trade-offs**:
- ✅ Surfaces recent daily notes for people searches
- ✅ Maintains quality filtering (temporal + PageRank combined)
- ⚠️ Requires TemporalAnalyzer integration in GraphAnalyzer

### Option 2: Special Handling for Daily Notes

**Concept**: Lower PageRank threshold for daily notes pattern

**Modified filtering**:
```typescript
const isDailyNote = notePath.includes('Daily Notes/');
const threshold = isDailyNote ? 0.001 : 0.01;
if (pagerank < threshold && !isDailyNote) continue;
```

**Impact**:
- Daily notes bypass strict PageRank filtering
- Non-daily notes still need high PageRank

**Trade-offs**:
- ✅ Simple, pattern-based approach
- ❌ Hard-coded heuristic (breaks if structure changes)
- ❌ Doesn't distinguish recent vs old daily notes

### Option 3: Unweighted Expansion (Aggressive)

**Concept**: Disable weighted filtering (`weightByPageRank: false`)

**Current fallback** (SearchOrchestrator.ts:175-179):
```typescript
graphExpandedNoteIds = this.graph.expandCandidateSet(
    seedNotes,
    maxNeighborsPerSeed,  // 15
    traversalDepth  // 1
);
```

**Impact**:
- All neighbors included (up to 15 per seed)
- Oct 28 would be included ✓

**Trade-offs**:
- ✅ Maximum recall
- ❌ Includes noise (loosely related mentions)
- ❌ Larger candidate set (performance impact)

### Option 4: Hybrid Approach (Best of Both)

**Concept**: Include top-K weighted + recent daily notes

**Implementation**:
```typescript
// Get top-K weighted neighbors
const weighted = this.expandCandidateSetWeighted(seeds, 10);

// Add recent daily notes (last 30 days) linking to seeds
const recentDaily = this.getRecentDailyNeighbors(seeds, 30);

return [...weighted, ...recentDaily];
```

**Impact**:
- Weighted expansion for quality
- Guaranteed inclusion of recent daily notes

**Trade-offs**:
- ✅ Best of both: quality + recency
- ✅ Configurable (days threshold, count limit)
- ⚠️ More complex implementation

## Recommended Action Plan

### Phase 1: Immediate Fix (30 min)
**Enable unweighted expansion for testing**:
- Set `weightByPageRank: false` in SearchOrchestrator config
- Test "Brian" query → verify Oct 28 appears
- Monitor for noise in results

### Phase 2: Smart Temporal Boosting (2-3 hours)
**Implement Option 1 (Temporal + PageRank)**:
1. Pass TemporalAnalyzer to GraphAnalyzer constructor
2. Modify weighted scoring to include temporal signal
3. Tune weights (e.g., `pagerank + temporal * 0.5`)
4. Test with various queries

### Phase 3: Evaluation (1 hour)
**Test queries**:
- "Brian" → should rank Oct 28 high
- "Lr Agent status" → should surface recent daily notes
- "Photoshop Web" → should balance hub + recent mentions

**Metrics**:
- Top-10 inclusion rate for recent daily notes
- Noise level (irrelevant results)
- User satisfaction (qualitative)

## Related Issues

### Non-Standard Meeting Headers

**Oct 28 used**: `## [[Style Home|Photo styles]] chat with [[Brain Eriksson|Brian]]`
**Standard**: `## Brian #meetings/1x1`

**Should standardize?**
- **Pro**: Better BM25 matching, clearer structure
- **Con**: "chat" may be intentionally informal vs "meeting"

**Recommendation**: Ask user about meeting header conventions

### Query Formulation

**Original query**: "Brian meeting conversation"
- Mixed concepts dilute signals
- Better: "Brian", "Brian 1x1", "recent Brian meetings"

**Fix**: Added to CLAUDE.md query best practices (v36)

## Success Criteria

After fixes:
- ✅ "Brian" query returns Oct 28 in top-5
- ✅ Person searches surface recent daily notes
- ✅ Status queries balance hub pages + recent updates
- ✅ No significant increase in noise (irrelevant results)

## Files to Modify

1. **SearchOrchestrator.ts**: Toggle `weightByPageRank` config
2. **GraphAnalyzer.ts**: Add temporal boosting to weighted expansion
3. **Settings**: Add graph expansion strategy toggle (weighted/unweighted/hybrid)
