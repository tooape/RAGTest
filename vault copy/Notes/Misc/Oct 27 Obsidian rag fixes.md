---
created: " 2025-11-11"
pageType: misc
datelink: "[[November 11, 2025]]"
---
## Fixed [[Smart Connections Enhancement - Custom RAG|Obsidian RAG]] Cache Persistence Issue

Last night successfully debugged and fixed the embedding cache persistence problem in the [[Smart Connections Enhancement - Custom RAG|obsidian rag ]]plugin. Embeddings were being computed but not saved to disk, causing ~3-5 minute re-indexing on every Obsidian restart.

**Root Cause**:
- Cache directory didn't exist, causing `np.savez_compressed()` to fail silently
- Python 3.9 compatibility issue (used `| None` instead of `Optional`)
- Circular import issues in route files

**Fixes Implemented**:
- Added cache debugging endpoints: `GET /api/cache/info` and `POST /api/cache/save`
- Enhanced cache save logging with detailed error traces
- Ensured cache directory creation on startup (config.py:34)
- Fixed Python 3.9 compatibility in embed.py and search.py (replaced `| None` with `Optional`)
- Fixed circular imports by using `app.main.embedding_service` reference

**Results**:
- ✅ Embeddings now persist to disk at `.obsidian/plugins/obsidian-rag/python-backend/cache/embeddings.npz`
- ✅ Cache file: 204KB for 210 notes
- ✅ Startup time: ~0s (loads from cache) vs ~3min (re-indexing)
- ✅ Backend fully operational in My Vault

**Repository**: All changes committed and pushed to `tooape/obsidianrag` [commit 85344d1](https://github.com/tooape/obsidianrag/commit/85344d1)

**Location**: Plugin now installed in My Vault at `.obsidian/plugins/obsidian-rag/` (RAGapp vault no longer needed)

## Open Questions on Temporal Ranking

### Question 1: What Field Is Being Used for Date Ranking? ✅ ANSWERED

**Answer**: The temporal analyzer uses **file modification time (`file.stat.mtime`)**, NOT frontmatter fields.

**Code location**: main.js:834512-834546

**Implementation details**:
```javascript
getScore(file) {
  const now = Date.now();
  const mtime = file.stat.mtime;  // ← Uses file modification time
  const ageMs = now - mtime;
  const ageDays = ageMs / (1000 * 60 * 60 * 24);
  const score = Math.pow(2, -ageDays / this.halfLifeDays);  // Exponential decay
  return score;
}
```

**Key parameters**:
- **Half-life**: 30 days (default) - score decays to 0.5 after 30 days
- **Decay function**: Exponential decay using `2^(-age_days / 30)`

**Implications**:
- ✅ Every file edit updates the temporal score (including typo fixes)
- ✅ Works for all files regardless of frontmatter
- ❌ Doesn't reflect true "creation date" from frontmatter
- ❌ Editing old notes makes them appear "recent" even if content is historical

**Alternative option**: Could modify to use frontmatter `created` field (via `vault.metadataCache.getFileCache(file).frontmatter.created`) for more accurate temporal signals, but this would require all notes to have consistent frontmatter.

## ✅ Implemented Frontmatter Created Date for Temporal Ranking

Switched temporal ranking to use frontmatter `created` date with fallback to `mtime`. This provides better separation of concerns between ranking signals.

**Changes made**:
- Modified `TemporalAnalyzer.ts` to accept `MetadataCache` parameter
- Updated `getScore()` to check `frontmatter.created` first, fallback to `file.stat.mtime`
- Updated `getAgeDays()` with same logic for consistency
- Modified `main.ts` to pass `metadataCache` to TemporalAnalyzer constructor

**Architecture benefits**:
- **Graph ranking** handles hub pages (high PageRank, many backlinks)
- **Temporal ranking** handles truly recent content (daily notes, meetings)
- Editing hub pages no longer gives false recency boost
- Daily notes correctly ranked by meeting/writing date, not typo fix date

**Implementation**:
```typescript
// Try to get created date from frontmatter first
const cache = this.metadataCache.getFileCache(file);
const createdStr = cache?.frontmatter?.created;

let timestamp: number;
if (createdStr) {
  timestamp = new Date(createdStr).getTime();  // Use frontmatter
} else {
  timestamp = file.stat.mtime;  // Fallback to mtime
}
```

**Repository**: Committed and pushed to `tooape/obsidianrag` [commit b195668](https://github.com/tooape/obsidianrag/commit/b195668)

**Deployed**: Plugin rebuilt and installed in My Vault - restart Obsidian to activate

### Question 2: Temporal Recall Problem - Are Recent Notes Missing from Candidate Set? ✅ CONFIRMED

**Hypothesis**: Is temporal (date) ranking getting crushed because it only re-ranks pages already returned by lexical+semantic search?

**Answer**: YES - the hypothesis is confirmed. The code explicitly filters temporal results to only boost query-relevant items.

**Code location**: SearchOrchestrator.ts:154-166

**The filtering logic**:
```typescript
// Production mode: filter graph/temporal to only boost query-relevant items
const queryRelevantNotes = new Set<string>();
semanticResults.forEach((r) => queryRelevantNotes.add(r.noteId));
bm25Results.forEach((r) => queryRelevantNotes.add(r.noteId));

finalGraphResults = graphResults.filter((r) =>
    queryRelevantNotes.has(r.noteId)
);
finalTemporalResults = temporalResults.filter((r) =>
    queryRelevantNotes.has(r.noteId)
);
```

**What's happening**:
1. Temporal analyzer searches ALL notes and ranks them by recency
2. But in production mode, temporal results are FILTERED to only include notes already found by semantic OR BM25
3. If a recent daily note has poor semantic/BM25 scores, it gets excluded from RRF fusion entirely
4. Temporal signal can't help because the note was filtered out before RRF

**Example failure**: "recent activity on photoshop web"
- Most recent daily notes mentioning "PS Web" have weak semantic scores (not enough context)
- They don't make top-100 from semantic+BM25
- Temporal filter removes them (not in `queryRelevantNotes` set)
- Hub pages win because they have strong semantic/BM25 scores + graph boost

**Debug mode exists**: Lines 149-153 show there's a debug mode that disables this filtering:
```typescript
if (this.debugMode) {
    // Debug mode: graph/temporal are full RRF candidates (no filtering)
    console.log('[DEBUG MODE] Using unfiltered graph/temporal signals');
    finalGraphResults = graphResults;
    finalTemporalResults = temporalResults;
}
```

**Potential Solutions**:
1. **Enable debug mode for temporal queries** - Detect "recent", "current", "status" keywords and disable temporal filtering
2. **Remove temporal filtering entirely** - Let temporal be a full RRF signal (may surface irrelevant recent notes)
3. **Hybrid approach** - Always include top-N most recent notes in candidate set, regardless of semantic/BM25 scores
4. **Query expansion** - Expand queries with date-related terms to improve BM25 recall for daily notes

Related to evaluation findings from [[October 26, 2025#2. Temporal Signal Too Weak]].

## Next Steps: Test Temporal Filtering Strategies

Created comparison framework to test two approaches empirically using 23-query test set:

**Option 2: Remove temporal filtering** (use existing debug mode)
- Already implemented via `debugMode` setting
- When enabled, temporal/graph signals participate fully in RRF without filtering
- Easy to test: toggle setting, reload plugin, run queries

**Option 3: Hybrid approach** (always include recent notes)
- Would require code modification
- Always add top-30 days of notes to candidate set before RRF
- More conservative than Option 2

**Testing Plan**:
1. Test key queries with current production mode (filtering ON):
   - "ps web" - expect hub page to rank higher than recent daily notes
   - "qu" - similar issue
   - "recent activity on photoshop web" - expect hub pages instead of daily notes
2. Enable debug mode, reload plugin
3. Test same queries with debug mode (filtering OFF)
4. Compare which approach surfaces more expected daily notes from ground truth
5. Choose winning approach based on results

**Key Questions**:
- Does debug mode improve recall for recent daily notes?
- Do irrelevant recent notes pollute results (noise from no filtering)?
- Which queries benefit most from removing the filter?

**Test script created**: `/RAGapp/Gemma test/beir_benchmark/compare_temporal_strategies.py`

## Testing Environment

**Evaluation data**:
- Ground truth: `beir_benchmark/vault_ground_truth.json` (23 queries, 7 patterns)
- Focus queries: "ps web", "qu", "recent activity on photoshop web"
- Expected behavior: Recent daily notes (Aug-Sep 2025) should rank highly

**Plugin settings location**: `.obsidian/plugins/obsidian-rag/`
- Debug mode toggle available in plugin settings
- Requires plugin reload to take effect

## ✅ Implemented Option 3: Hybrid Temporal Strategy

Successfully implemented guaranteed recency coverage for temporal ranking:

**Implementation**: SearchOrchestrator.ts:155-193
- Always includes notes from last **120 days** in RRF candidate set (covers ~393 daily notes)
- No longer filters out recent daily notes due to weak BM25/semantic scores
- Older notes still filtered to query-relevant items only
- Performance impact: negligible (~300 extra candidates, microseconds to process)

**Key insight**: Daily notes WERE getting BM25 matches for abbreviations (e.g., "QU"), but scored too low to make top-100 due to high document frequency. Temporal boost needs them in candidate set to work effectively.

**Architecture**:
- Temporal ranking: Handles last 120 days (guaranteed coverage for all daily notes)
- Graph ranking: Handles well-connected hub pages (filtered to query matches)
- BM25/Semantic: Primary discovery signals

**Rationale for 120 days**:
- Covers full quarterly work cycle (~4 months)
- Temporal score at 120 days: 2^(-120/30) = 0.0625 (6% of today's score, still meaningful)
- Performance negligible: 393 vs 97 candidates, microseconds to process
- Effectively means "all daily notes participate" in temporal ranking

**Next Steps**:
- Test with "qu" and "ps web" queries after Obsidian restart
- Monitor actual performance with 120-day window
- Consider indexing/embedding optimization for faster startup

## TODO: Performance & Optimization Investigation

- [ ] Profile embedding generation performance (currently ~3-5 min for 210 notes)
- [ ] Investigate EmbeddingGemma model optimization opportunities (currently 256d)
- [ ] Benchmark cache loading time vs re-indexing time
- [ ] Consider incremental indexing strategies for large vaults
- [ ] Evaluate impact of 30-day temporal inclusion on search latency
- [ ] Test with larger vault sizes (1000+ notes) to identify bottlenecks


# Meetings
## Semantic Search Failure Analysis - "Semantic=undefined"

**Observation**: After implementing chunking and fixing null check bug, semantic search returns `undefined` in signal ranks while BM25 and Graph work correctly.

**Console output**:
```
Signal Ranks: Semantic=undefined, BM25=0, Graph=3, Temporal=undefined
Search scope: 680 files, 1879 chunks
```

### Top 5 Most Likely Root Causes

**1. Chunk ID Mismatch Between Plugin and Backend** ⭐ MOST LIKELY
- Plugin sends chunk IDs like `Notes/Daily/Oct 27.md#chunk-0` to backend
- Backend's embeddings.npz was rebuilt and may have different IDs
- Search endpoint receives chunk IDs that don't exist in cache
- Returns empty results → semantic signal becomes `undefined`
- **Diagnostic**: Check backend logs for search requests with 0 results
- **Fix**: Verify cache has chunk IDs, not file paths

**2. Empty Embeddings Cache After Reinstallation**
- Plugin was deleted and reinstalled multiple times
- Cache file (`embeddings.npz`) may have been cleared
- Backend loads successfully but has 0 cached embeddings
- Search always returns empty because no embeddings exist
- **Diagnostic**: Check `/api/cache/info` endpoint
- **Fix**: Wait for full reindex to complete

**3. Backend Not Receiving Search Requests**
- Frontend fetch to `http://localhost:8000/api/search` failing silently
- Error caught but semantic results set to `undefined` instead of `[]`
- BM25/Graph work because they're local to the plugin
- **Diagnostic**: Check browser Network tab for failed requests
- **Fix**: Verify backend is running and responding to health checks

**4. Async Race Condition - Search Before Embeddings Complete**
- Index rebuild triggers search immediately
- Search executes before embeddings are fully cached
- First few queries get `undefined` until cache is populated
- **Diagnostic**: Try query again after waiting 30 seconds
- **Fix**: Add loading state or delay initial search

**5. NaN/Inf Values Returning from Backend**
- Despite sanitization fixes, edge case still producing invalid JSON
- Fetch succeeds but JSON.parse() fails
- Error handler sets semantic results to `undefined`
- **Diagnostic**: Check backend logs for 500 errors or serialization failures
- **Fix**: Add more comprehensive NaN checks in score computation

### Next Steps
1. Check backend logs for incoming search requests
2. Verify embeddings cache contains chunk IDs (not file paths)
3. Test `/api/cache/info` to confirm embeddings exist
4. Check browser Network tab for failed API calls
5. Try query after waiting for full index rebuild

**Related**: This is different from the previous temporal filtering issue - semantic was working then, now it's completely broken.---



