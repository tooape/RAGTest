---
pageType: claudeResearch
created: 2025-10-30
tags:
  - claude
datelink: "[[October 30, 2025]]"
Related Pages:
  - "[[Graph Expansion Analysis - October 28 Brian Meeting - Oct 2025]]"
  - "[[Smart Connections Enhancement - Custom RAG]]"
---
# Graph Expansion Testing Plan
---

## Current Configuration

**File**: `/Users/rmanor/obsidianrag/obsidian-plugin/src/main.ts:48-51`

**Default settings**:
```typescript
graphExpansionEnabled: true,
graphExpansionMaxNeighbors: 15,
graphExpansionDepth: 1,
graphExpansionWeighted: true,  // ← The issue
```

**User-accessible settings** (SettingsTab.ts:184-255):
- ✅ Enable/disable graph expansion
- ✅ Max neighbors per seed (default: 15)
- ✅ Traversal depth (1 or 2)
- ✅ Weighted filtering toggle

## Test Scenarios

### Test 1: Person Search (Current Problem Case)

**Query**: "Brian"

**Expected behavior**:
- Top 5 should include recent meetings with Brian
- Oct 28, 2025 should appear (most recent)
- Oct 22, 2025 should appear (second most recent)

**Test configurations**:

| Config | weightByPageRank | Expected Result |
|--------|------------------|-----------------|
| A (current) | `true` | Oct 28 filtered out by low PageRank |
| B | `false` | Oct 28 included (all neighbors) |

**Evaluation metrics**:
- Position of Oct 28 in results
- Position of Oct 22 in results
- Presence of noise (irrelevant results)

### Test 2: Status Query (Hub + Daily Notes)

**Query**: "Lr Agent status"

**Expected behavior**:
- Hub page ([[Lr Home]]) in top results
- Recent daily notes mentioning Lr Agent in top-10
- Balance between canonical info and recent updates

**Test configurations**:

| Config | weightByPageRank | maxNeighbors | Expected |
|--------|------------------|--------------|----------|
| A | `true` | 15 | Hub page + high PageRank neighbors |
| B | `false` | 15 | Hub page + all recent daily notes |
| C | `false` | 25 | More daily note coverage |

**Evaluation metrics**:
- Hub page position
- Number of recent daily notes in top-10
- Relevance of daily note content

### Test 3: Project Search (Intersection Topic)

**Query**: "Photoshop Web recommendations"

**Expected behavior**:
- Canonical pages ([[Photoshop]], [[Recommendations Home]])
- Recent progress updates in daily notes
- Meeting notes discussing PS Web

**Evaluation metrics**:
- Canonical page ranking
- Recent meeting note inclusion
- Absence of unrelated PS or Web mentions

### Test 4: Noise Sensitivity

**Query**: "Query Understanding"

**Expected behavior**:
- Hub page ([[Query Understanding]]) ranked high
- Relevant sub-topics and workstreams
- Filter out tangential mentions

**Test configurations**:

| Config | weightByPageRank | Expected Noise Level |
|--------|------------------|---------------------|
| A | `true` | Low (strict filtering) |
| B | `false` | Medium-High (all neighbors) |

**Evaluation metrics**:
- Relevance of top-20 results
- Presence of off-topic results
- User perception of quality

## Testing Protocol

### Phase 1: Quick Smoke Test (15 min)

**Goal**: Verify unweighted expansion includes Oct 28

**Steps**:
1. Open Obsidian plugin settings
2. Navigate to "Graph Expansion" section
3. Toggle "Weight by PageRank" to OFF
4. Search "Brian"
5. Check if Oct 28, 2025 appears in results
6. Note position and surrounding results

**Success criteria**:
- Oct 28 appears in top-10
- No obvious noise in results

### Phase 2: Comprehensive Test Suite (1 hour)

**Goal**: Evaluate weighted vs unweighted across multiple query types

**Steps**:
1. **Weighted mode** (`weightByPageRank: true`):
   - Run all 4 test queries
   - Record top-10 results for each
   - Note daily note inclusion rate
   - Assess noise level

2. **Unweighted mode** (`weightByPageRank: false`):
   - Run same 4 test queries
   - Record top-10 results for each
   - Compare daily note inclusion
   - Assess noise increase

3. **Tuning test** (maxNeighbors):
   - Try 10, 15, 20, 25 neighbors
   - Measure recall vs noise trade-off

**Data collection**:
- Screenshots of search results
- Top-10 note paths for each query
- Subjective quality ratings (1-5 scale)

### Phase 3: Long-term Evaluation (Ongoing)

**Goal**: Monitor real-world usage patterns

**Metrics to track**:
- Which queries benefit from unweighted expansion
- Which queries suffer from noise
- User workflow efficiency (time to find info)

**Feedback loop**:
- Note queries where weighted expansion fails
- Identify patterns (person searches, status queries, etc.)
- Propose targeted improvements

## Recommended Configuration

### Immediate Action (Before Further Testing)

**Toggle to unweighted expansion**:
```typescript
graphExpansionWeighted: false,  // Disable PageRank filtering
graphExpansionMaxNeighbors: 15, // Keep moderate neighbor count
```

**Rationale**:
- Fixes Oct 28 problem immediately
- Enables testing of unweighted behavior
- Can revert if noise becomes problematic

### Future Improvements

**Option 1: Temporal-Weighted Hybrid** (recommended long-term)
- Modify GraphAnalyzer.ts to boost recent notes
- Balance PageRank + temporal signal
- See [[Graph Expansion Analysis - October 28 Brian Meeting - Oct 2025#Option 1: Temporal Boosting in Graph Expansion (Recommended)]]

**Option 2: Configurable Strategy**
- Add dropdown in settings: "Weighted", "Unweighted", "Temporal-Hybrid"
- Let user choose based on vault structure and usage patterns

**Option 3: Query-Type Detection**
- Person searches → unweighted (favor recent)
- Hub page searches → weighted (favor quality)
- Auto-detect based on query pattern

## Success Metrics

**Quantitative**:
- Daily note inclusion rate in top-10: >30% for person searches
- Recent note (<7 days) inclusion: >2 in top-10 for status queries
- Noise rate: <20% irrelevant results in top-10

**Qualitative**:
- User finds recent information faster
- Fewer "I know I wrote about this recently" frustrations
- Better balance between canonical and current info

## Next Steps

1. **Run Phase 1 smoke test** (15 min)
   - Toggle `weightByPageRank` to `false`
   - Search "Brian" and verify Oct 28 appears

2. **Document findings** in this note
   - Record before/after results
   - Note any unexpected behaviors

3. **Run Phase 2 comprehensive test** (1 hour)
   - Test suite across multiple query types
   - Collect quantitative data

4. **Decide on permanent configuration**
   - Unweighted if noise is acceptable
   - Temporal-hybrid if noise is problematic
   - Weighted with tuning as fallback

## Related Documents

- [[Graph Expansion Analysis - October 28 Brian Meeting - Oct 2025]] - Root cause analysis
- [[Graph Traversal for Recall Enhancement - October 2025]] - Original design doc
- [[Smart Connections Enhancement - Custom RAG]] - Parent project
