---
pageType: daily
aliases:
  - "2025-10-26"
created: " 2025-10-26"
---
# [[ October 26, 2025]]

# Rag app testing
- [[Smart Connections Enhancement - Custom RAG]]
## Test case descriptions

### 1. "photoshop"
Here' i'd expect to get the Photoshop web home page, my most recent meetings (H2 lines) about this, and then other recent mentions. 
Specifically looking for it to hit the meeting on [PS Web recs I had on Oct 16th](obsidian://open?vault=My%20Vault&file=Notes%2FPeriodic%20Notes%2FDaily%20Notes%2FOctober%2016%2C%202025).
### 2. "ps web"
I'd expect mostly similar results to case number one here

### 3. "Hao"
I'd expect to get his personal page, and then recent days where I mentioned him or had meetings with him. 

### "What's the most recent activity on X"
This would be the prompt I would send into claude and then the search would get made from MCP. Similar here, X would be some project or questions, or ask, and then I would expect the canonical page, meetings which had the topic named in the H2 line, and then meetings where it was mentioned in plain text returned. 

### Exact match for page names 
- "Coffee"
- Ritu Goel 

###  "Ritu staff #meetings"
Here I want the most recent few days where we had ritu's staff returned in reverse chronological order. 
  



## Links
- [[beir-cellarbeir A Heterogeneous Benchmark for Information Retrieval. Easy to use, evaluate your models across 15+ diverse IR datasets.|Test data]]
  - [https://www.pinecone.io/blog/cascading-retrieval/](https://www.pinecone.io/blog/cascading-retrieval/)




## Next Steps: Vault-Specific RAG Evaluation

After BEIR benchmark completes:

1. **Create ground truth file** (23 queries across 7 patterns)
   - Pattern 1: Topic/Project Search (photoshop, intent ai, recommendations, mint)
   - Pattern 2: Abbreviations (ps web, lr, qu, ps)
   - Pattern 3: Person Search (Hao, Ritu Goel, Kosta)
   - Pattern 4: Temporal Queries (recent activity on X)
   - Pattern 5: Exact Match (Coffee, Ritu Goel, Evaluation, ILUP, MCP-Tools-Reference)
   - Pattern 6: Structured Queries (Ritu staff #meetings, Intent AI #meetings, Brian #meetings/1x1, qu #meetings)
   - Pattern 7: Directional/Semantic ("vibe code rag" → Smart Connections Enhancement page)

2. **Manually identify top 10 results** for each query
   - Use current vault search to gather candidates
   - Rank based on relevance + recency + context (H2 vs body)

3. **Build vault evaluation script**
   - Run top 3 BEIR models (Cross-Encoder, Hybrid RRF, Current RAG App) against vault
   - Plus BM25 baseline for exact match comparison

4. **Generate comparison report**
   - Metrics per query: NDCG@10, MRR, P@5, Hit Rate@1
   - Analyze which model wins for which pattern
   - Make production recommendation

5. **Implement winning approach** in Smart Connections enhancement


## Live Plugin Evaluation Results

Completed full 23-query evaluation of live Obsidian plugin via MCP.

### Overall Performance
- **Average Precision@20**: 37.6%
- **Average Recall@20**: 75.2%
- **Average MRR**: 92.4%
- **Failed Queries** (Recall < 50%): 4/23 (17%)

### Performance by Pattern
- ✅ **Abbreviations**: 90% recall - ps web, lr, qu all work
- ✅ **Person Search**: 90% recall - Finding people and mentions
- ✅ **Topic/Project**: 87.5% recall - General topics work well
- ✅ **Exact Match**: 88% recall - Direct page names work
- ✅ **Directional Semantic**: 90% recall - Conceptual matches good
- ⚠️ **Temporal Queries**: 80% recall - Recency ranking issues
- ❌ **Structured Queries (#meetings)**: **15% recall** - TAG FILTERING BROKEN

### Critical Issues

#### ~~1. Tag Filtering Completely Broken~~
All 4 structured queries failed:
- "Ritu staff #meetings": 30% recall
- "Intent AI #meetings": 20% recall  
- "Brian #meetings/1x1": **0% recall** (complete failure)
- "qu #meetings": 10% recall

**Problem**: QueryParser #meetings filtering not being applied. Plugin returns daily notes mentioning the topic but WITHOUT #meetings tags on headings.

#### 2. Temporal Signal Too Weak
For "recent activity on photoshop web":
- Hub pages rank #1 instead of recent daily notes
- August/June 2025 dates mixed with September dates
- Temporal decay not strong enough vs semantic+BM25

#### 3. Graph Signal Unknown
Hub pages rank very high - could be PageRank working OR just strong semantic/BM25 scores.

### Action Items
- [x] Fix tag filtering in SearchOrchestrator.ts - QueryParser integration
- [ ] Investigate temporal signal strength - consider increasing weight or reducing half-life
- [ ] Verify graph signal is contributing to rankings

Results saved to:
- `beir_benchmark/live_plugin_results.json`
- `beir_benchmark/live_plugin_eval.log`  
- `beir_benchmark/live_plugin_eval_summary.json`
