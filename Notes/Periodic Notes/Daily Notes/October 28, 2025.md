---
pageType: daily
aliases:
  - "2025-10-28"
created: " 2025-10-28"
---
# [[ October 28, 2025]]
# Notes
---
Today is day one of [[Adobe MAX 2025]]


- [[Subhajit]] has set up a [slack canvas board](https://adobe.enterprise.slack.com/docs/T024KQMLM/F09PC1LQSKA) for stand up notes on intent. 
- [[Matt Rae]] wants to have the roadshow the week of [[November 10, 2025]]
## [[Style Home|Photo styles]] chat with [[Brian Eriksson|Brian]]
- using GPT 5 as a judge to go back to what we were doing two or three weeks ago
- Getting a collection of 100-250 neutral flat ass images and then creating variations for each [[Style Home|style]] dimension.
	- also possibly reducing the number of dimensions?
		- he thinks 67 is okay

## [[Smart Connections Enhancement - Custom RAG|Obsidian RAG]] Plugin Work

Fixed chunk-related issues from yesterday:

**Root Cause Identified:**
- Plugin deployment was incomplete - only copying plugin JS files (main.js, manifest, styles) but missing the entire python-backend directory
- Backend process was stale and running from empty directory
- No cache persistence, embeddings only in memory

**Fixes Applied:**
- Proper deployment: Copy both plugin files AND python-backend directory
- Semantic rank aggregation fix: When file wins RRF (from BM25/Graph/Temporal), aggregate semantic ranks across all chunks from that file for display
- Committed fix in [commit 702f59f](https://github.com/tooape/obsidianrag/commit/702f59f)

**Current Status - Backend Startup Issue:**
- After clean reinstall, backend fails to start on plugin enable
- Plugin loads quickly but embedding backend doesn't initialize
- Need to debug: Check venv paths, backend logs, BackendManager startup sequence

**Next Steps:**
- Debug backend startup failure
- Verify venv configuration in deployed plugin
- Check BackendManager.ts startup logic
- Test manual backend startup to isolate issue



