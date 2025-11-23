---
pageType: claudeResearch
tags:
  - claude
created: "2025-10-30"
---
# Backend Idle Model Unloading Strategy
---

## Objective

Reduce memory footprint when backend is idle by unloading the embedding model while keeping the FastAPI server running. Target: ~50MB idle memory with 2-3 second model reload time (vs 5-10 seconds for full backend restart).

## Problem Statement

**Current Behavior**:
- Backend runs continuously with model loaded in memory
- Memory usage: ~600MB constant (even when idle)
- Impact: Battery drain, memory pressure on system
- User rarely searches continuously - most time is spent idle

**User Preference**: Can tolerate 2-3 second delay on first search after idle, but not 5-10 seconds.

## Proposed Solution: Lazy Model Loading

Keep FastAPI backend running continuously, but unload the embedding model after idle timeout. Model reloads on-demand when search is requested.

### Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI Backend (Always)        │
│         Memory: ~50MB                    │
├─────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────┐    │
│  │   Embedding Model (Lazy)       │    │
│  │   - Loads on first search      │    │
│  │   - Unloads after idle timeout │    │
│  │   - Memory: ~600MB (or <200MB) │    │
│  └────────────────────────────────┘    │
│                                          │
└─────────────────────────────────────────┘
```

### Memory States

| State | Memory Usage | Transition Time |
|-------|--------------|-----------------|
| Idle (model unloaded) | ~50MB | - |
| Loading model | ~50MB → 600MB | 2-3 seconds |
| Active (model loaded) | ~600MB | - |
| Unloading model | 600MB → ~50MB | <1 second |

With ONNX (future):
| State | Memory Usage | Transition Time |
|-------|--------------|-----------------|
| Idle (model unloaded) | ~50MB | - |
| Loading model | ~50MB → <200MB | 1-2 seconds |
| Active (model loaded) | <200MB | - |

## Implementation Plan

### Phase 1: Backend Changes (Python)

**1.1 Modify EmbeddingService** (`app/models/embedder.py`)

Add lifecycle methods:
```python
class EmbeddingService:
    def __init__(self, model_name: str, embedding_dim: int, cache_path: Path):
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        self.cache_path = cache_path

        # Lazy-loaded attributes
        self.model: Optional[SentenceTransformer] = None
        self.is_loaded = False

        # Always load cache (lightweight)
        self.cache: Dict[str, np.ndarray] = {}
        self._load_cache()

    async def ensure_loaded(self):
        """Load model if not already loaded."""
        if self.is_loaded:
            return

        print(f"Loading model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)

        # Truncate embeddings to target dimension
        if self.embedding_dim < 768:
            self.model.max_seq_length = 512

        self.is_loaded = True
        print(f"Model loaded ({self.embedding_dim}d embeddings)")

    async def unload(self):
        """Unload model to free memory."""
        if not self.is_loaded:
            return

        print("Unloading model...")
        self.model = None
        self.is_loaded = False

        # Force garbage collection
        import gc
        gc.collect()
        print("Model unloaded")

    async def embed_texts(self, texts: List[str], note_ids: Optional[List[str]] = None) -> np.ndarray:
        """Generate embeddings. Loads model if needed."""
        await self.ensure_loaded()  # Auto-load on demand

        # ... existing embedding logic
```

**1.2 Add Idle Timer to Backend** (`app/main.py`)

```python
from datetime import datetime, timedelta

# Global state
last_activity_time = datetime.now()
idle_timeout_minutes = 10
idle_check_task = None

async def check_idle_and_unload():
    """Background task to check for idle timeout and unload model."""
    global last_activity_time

    while True:
        await asyncio.sleep(60)  # Check every minute

        if embedding_service.is_loaded:
            time_since_activity = datetime.now() - last_activity_time

            if time_since_activity > timedelta(minutes=idle_timeout_minutes):
                print(f"Idle for {idle_timeout_minutes} minutes, unloading model...")
                await embedding_service.unload()

@app.on_event("startup")
async def startup():
    # Start idle checker
    global idle_check_task
    idle_check_task = asyncio.create_task(check_idle_and_unload())

    # Don't load model at startup - wait for first search
    print("Backend ready (model will load on first search)")

@app.post("/search")
async def search(request: SearchRequest):
    global last_activity_time
    last_activity_time = datetime.now()  # Reset idle timer

    # Model loads automatically in embed_texts if needed
    results = await embedding_service.search(...)
    return results

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": embedding_service.is_loaded,
        "idle_timeout_minutes": idle_timeout_minutes,
    }
```

**1.3 Add Manual Control Endpoints**

```python
@app.post("/model/load")
async def load_model():
    """Manually load model (e.g., for preloading)."""
    await embedding_service.ensure_loaded()
    return {"status": "loaded"}

@app.post("/model/unload")
async def unload_model():
    """Manually unload model."""
    await embedding_service.unload()
    return {"status": "unloaded"}
```

### Phase 2: Plugin Changes (TypeScript)

**2.1 Add Loading Indicator** (`SearchOrchestrator.ts`)

```typescript
async search(query: string, topK: number = 50): Promise<SearchResult[]> {
    // Check if model is loaded
    const health = await this.checkBackendHealth();

    if (!health.model_loaded) {
        // Show loading notice while model loads
        const notice = new Notice('Loading embedding model (2-3 seconds)...', 0);

        // Wait for model to load (triggered by search request)
        // The backend will auto-load when we call /search

        // Remove notice after search completes
        setTimeout(() => notice.hide(), 100);
    }

    // Proceed with search (backend auto-loads model if needed)
    const results = await this.backendManager.search(query, ...);
    return results;
}
```

**2.2 Optional: Preload on Modal Open** (`SearchModal.ts`)

```typescript
class SearchModal extends Modal {
    async onOpen() {
        super.onOpen();

        // Preload model in background when modal opens
        // By the time user types query, model is already loading
        this.backendManager.preloadModel().catch(console.error);
    }
}

// BackendManager.ts
async preloadModel(): Promise<void> {
    try {
        await fetch(`${this.backendUrl}/model/load`, { method: 'POST' });
    } catch (error) {
        console.warn('Failed to preload model:', error);
    }
}
```

### Phase 3: Settings

**3.1 Add Configurable Timeout** (`SettingsTab.ts`)

```typescript
// Add setting
new Setting(containerEl)
    .setName('Idle timeout (minutes)')
    .setDesc('Unload embedding model after this many minutes of inactivity (0 = never unload)')
    .addText(text => text
        .setPlaceholder('10')
        .setValue(String(this.plugin.settings.idleTimeoutMinutes))
        .onChange(async (value) => {
            const minutes = parseInt(value) || 0;
            this.plugin.settings.idleTimeoutMinutes = minutes;
            await this.plugin.saveSettings();

            // Update backend config
            await this.plugin.updateBackendConfig({ idle_timeout_minutes: minutes });
        }));
```

## Benefits

✅ **Memory efficient**: ~50MB when idle (vs 600MB currently)
✅ **Fast reload**: 2-3 seconds (vs 5-10 for full backend restart)
✅ **Battery friendly**: Minimal CPU usage when model unloaded
✅ **Cache preserved**: Embeddings cache stays in memory (lightweight)
✅ **Seamless UX**: Loading indicator provides feedback
✅ **No backend restart**: FastAPI stays running (faster than full restart)

## Trade-offs

⚠️ **First search delay**: 2-3 seconds after idle period
⚠️ **Backend still running**: ~50MB baseline (vs 0MB with full shutdown)
⚠️ **Implementation complexity**: More complex than simple idle shutdown

## Success Criteria

- ✅ Backend starts without loading model
- ✅ Model loads automatically on first search request
- ✅ Model unloads after 10 minutes of inactivity (configurable)
- ✅ Memory usage: ~50MB idle, ~600MB active (or <200MB with ONNX)
- ✅ Reload time: 2-3 seconds (measured)
- ✅ Cache persistence: Embeddings cache survives model unload
- ✅ User feedback: Loading indicator shown during model load

## Timeline Estimate

- **Phase 1** (Backend changes): 2-3 hours
- **Phase 2** (Plugin changes): 1-2 hours
- **Phase 3** (Settings & polish): 1 hour

**Total**: ~4-6 hours

## Future Optimization: ONNX + Lazy Loading

Combining with ONNX quantization (from [[ONNX Implementation Plan - October 2025]]):
- **Idle memory**: ~50MB (same)
- **Active memory**: <200MB (vs 600MB currently)
- **Reload time**: 1-2 seconds (ONNX loads faster)
- **Best of both worlds**: Minimal memory + fast reload

## Related Documents

- [[Obsidian RAG Memory Optimization - October 2025]] - Overview of optimization strategies
- [[ONNX Implementation Plan - October 2025]] - Plan for ONNX migration
- [[Smart Connections Enhancement - Custom RAG]] - Parent project page
- [[October 30, 2025#Obsidian RAG Memory Optimization]] - Today's optimization session

## References

- Sentence-Transformers Lazy Loading: https://www.sbert.net/docs/package_reference/SentenceTransformer.html
- FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
- Python Memory Management: https://docs.python.org/3/library/gc.html
