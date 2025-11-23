---
pageType: claudeResearch
tags:
  - claude
  - RAG
  - obsidian-plugin
created: "2025-11-19"
---

# RAG Backend Unhealthy - Diagnosis & Resolution

## Problem
The Obsidian RAG plugin was showing "Backend: unhealthy" in the Indexing Settings, even though search functionality was partially working.

## Root Causes

### Primary Issue: Process Not Running
The Python backend process (`uvicorn` on port 8000) wasn't running. The plugin's auto-start mechanism failed to launch it.

### Secondary Issue: Backend Files Sync
The plugin directory (`~/.obsidian/plugins/obsidian-rag/python-backend/app/`) was empty. The build process in the main project (`/Users/rmanor/obsidianrag/`) is supposed to automatically sync backend files to the plugin directory, but this hadn't been done or was out of sync.

## Logs Analysis

When manually starting the backend, initial errors appeared:
- **ONNX Model Download Failures** (404 errors):
  - Failed to download `google/embeddinggemma-300m` quantized model
  - Failed to download non-quantized ONNX version
  - This is expected - HuggingFace hosting changed, or model path is incorrect

- **Graceful Fallback**:
  - Backend automatically fell back to `sentence-transformers` library
  - Successfully loaded EmbeddingGemma @ 256d using sentence-transformers
  - 2,869 cached embeddings loaded from disk
  - All subsequent health checks pass

## Current Status
✅ **Backend is now healthy**
- Process running on `http://127.0.0.1:8000`
- Model loaded and functional
- All 2,869 embeddings cached and ready
- Search working with BM25 + semantic + graph + temporal signals

## Resolution Taken
Started the backend manually by running:
```bash
cd /Users/rmanor/obsidianrag/python-backend
source venv/bin/activate
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Long-Term Fix Needed
To prevent this from happening again:

1. **Sync Backend Files** from project to plugin directory:
   - Run the build process in `/Users/rmanor/obsidianrag/obsidian-plugin/`
   - This should auto-sync `python-backend/` to the plugin directory

2. **Enable Auto-Start**:
   - Ensure plugin setting "Auto-start backend" is enabled in Obsidian
   - Verify the Python path is correctly set (should be `python3`)

3. **Consider Background Service**:
   - Create a persistent background process or launchd agent for macOS
   - This ensures backend survives system restarts and process crashes

## Architecture Notes
- **Embedding Model**: EmbeddingGemma @ 256d (via sentence-transformers)
- **Cache Location**: `/Users/rmanor/obsidianrag/python-backend/cache/embeddings.npz`
- **Cache Size**: 2,869 embeddings (takes ~1-2 minutes to rebuild if cleared)
- **Fallback Strategy**: Gracefully handles ONNX model unavailability
