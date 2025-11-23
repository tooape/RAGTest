---
pageType: claudeResearch
created: 2025-11-11
tags: [claude, rag, obsidian, backend, architecture]
aliases:
  - RAG Backend Structure
  - Obsidian RAG Plugin Backend
---

# RAG Plugin Backend Architecture Summary

**Project**: Obsidian RAG Plugin with Multi-Signal Semantic Search
**Repository**: `/Users/rmanor/obsidianrag/`
**Backend Location**: `/Users/rmanor/obsidianrag/python-backend/`
**Status**: Active (Phase 3: Search Quality Improvements)

---

## Quick Start: How to Start the Backend

### Option 1: Using Shell Script (Recommended)
```bash
cd /Users/rmanor/obsidianrag/python-backend
./start.sh
```

### Option 2: Manual Start
```bash
cd /Users/rmanor/obsidianrag/python-backend

# Activate virtual environment (if not already active)
source venv/bin/activate

# Start uvicorn server
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Option 3: Direct Python Module
```bash
cd /Users/rmanor/obsidianrag/python-backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Success Indicator**: Server is ready when you see:
```
Uvicorn running on http://127.0.0.1:8000
```

Visit `http://localhost:8000/health` to verify the server is running.

---

## Backend Directory Structure

```
python-backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── models/
│   │   ├── embedder.py           # EmbeddingGemma service with lazy loading
│   │   └── cross_encoder.py      # Cross-encoder service (lazy load)
│   ├── routes/
│   │   ├── embed.py              # POST /api/embed endpoint
│   │   ├── search.py             # POST /api/search endpoint
│   │   ├── rerank.py             # POST /api/rerank endpoint (cross-encoder)
│   │   └── cache.py              # Cache management endpoints
│   └── storage/
│       └── cache.py              # Embedding cache manager (if exists)
│
├── cache/
│   └── embeddings.npz            # Cached 256d embeddings (2.5 MB currently)
│
├── venv/                          # Python virtual environment
│   └── lib/python3.9/site-packages/  # Installed dependencies
│
├── requirements.txt               # Python dependencies
├── start.sh                       # Shell script to start backend
└── README.md                      # Backend documentation
```

---

## Core Backend Components

### 1. Main Application (`app/main.py`)

**Responsibilities**:
- FastAPI application initialization
- CORS middleware configuration
- Application lifecycle management (startup/shutdown)
- Health check endpoints
- Idle timeout and model unloading (10 minutes of inactivity)
- Route registration

**Key Features**:
- **Lazy Model Loading**: EmbeddingGemma model loads on first use, not at startup
- **Idle Detection**: Background task checks every 60 seconds for 10-minute idle timeout
- **Graceful Shutdown**: Saves embeddings cache and cleans up resources
- **CORS Configuration**: Allows requests from Obsidian (`app://obsidian.md`) and localhost

**Startup Flow**:
1. `lifespan()` context manager runs on startup
2. Cache directory is initialized
3. EmbeddingService is created and cache is loaded (lightweight)
4. CrossEncoderService is initialized (models not loaded yet)
5. Idle checker background task is started
6. Server begins accepting requests

### 2. Configuration (`app/config.py`)

**Settings**:
```python
MODEL_NAME = "google/embeddinggemma-300m"  # Embedding model
EMBEDDING_DIM = 256                         # Matryoshka truncation (from 768d)
HOST = "127.0.0.1"                         # Server host
PORT = 8000                                 # Server port
CORS_ORIGINS = ["app://obsidian.md", "http://localhost"]
CACHE_DIR = Path("./cache")                # Cache directory
EMBEDDINGS_FILE = "embeddings.npz"         # Cache file name
MAX_BATCH_SIZE = 32                        # Batch size for embeddings
CACHE_SIZE_MB = 100                        # Max in-memory cache
HF_TOKEN = os.environ.get("HF_TOKEN")      # HuggingFace authentication token
```

**Cache Storage**:
- Path: `/Users/rmanor/obsidianrag/python-backend/cache/embeddings.npz`
- Current size: 2.5 MB (670 notes cached)
- Format: NumPy compressed array (.npz)

### 3. Embedding Service (`app/models/embedder.py`)

**Core Features**:
- **Lazy Loading**: Model loads on first embed/search request
- **ONNX Runtime Support**: Efficient inference with int8 quantization (when available)
- **Sentence-Transformers Fallback**: Falls back to pure Python if ONNX unavailable
- **Embedding Cache**: In-memory cache + persistent NPZ file storage
- **Matryoshka Truncation**: Truncates 768d embeddings to 256d
- **Automatic Cache Persistence**: Saves embeddings after each batch

**Key Methods**:
- `async initialize()`: Loads cache from disk (lightweight, model loads later)
- `async ensure_loaded()`: Auto-loads ONNX or sentence-transformers model
- `async embed_texts()`: Generates embeddings for text list
- `async search()`: Semantic search within cached embeddings
- `_save_cache()`: Saves cache to embeddings.npz
- `_load_cache()`: Loads cache from embeddings.npz
- `async unload()`: Frees model memory (cache preserved)
- `get_cache_info()`: Returns cache statistics

**Embedding Dimensions**:
- Full model: 768d
- Truncated (Matryoshka): 256d
- Memory per note: 256 × 4 bytes = 1 KB
- Total for 670 notes: ~670 KB (compressed to 2.5 MB in NPZ)

### 4. Cross-Encoder Service (`app/models/cross_encoder.py`)

**Lazy Loading Pattern**:
- Model NOT loaded at startup
- Loads only on first rerank request if enabled
- Can be unloaded after idle timeout

**Model**: `cross-encoder/ms-marco-MiniLM-L6-v2`
**Latency**: ~550ms for 200 documents
**Status**: Implemented but disabled by default (RRF works better)

### 5. API Routes

#### `/api/embed` (POST)
**Purpose**: Generate embeddings for texts

**Request**:
```json
{
  "texts": ["Note content 1", "Note content 2"],
  "note_ids": ["note1.md", "note2.md"],
  "use_cache": true
}
```

**Response**:
```json
{
  "embeddings": [[0.1, 0.2, ...], ...],
  "model": "google/embeddinggemma-300m",
  "dimension": 256,
  "cached": 0,
  "latency_ms": 45.2
}
```

#### `/api/search` (POST)
**Purpose**: Semantic search within cached embeddings

**Request**:
```json
{
  "query": "search query",
  "note_ids": ["note1.md", "note2.md"],
  "top_k": 100
}
```

**Response**:
```json
{
  "results": [
    {"note_id": "note1.md", "score": 0.95},
    {"note_id": "note2.md", "score": 0.82}
  ],
  "latency_ms": 18.5
}
```

#### `/api/rerank` (POST)
**Purpose**: Cross-encoder reranking (optional, for precision refinement)

**Request**:
```json
{
  "query": "search query",
  "documents": ["text 1", "text 2"],
  "top_k": 20
}
```

**Response**:
```json
{
  "results": [
    {"index": 0, "score": 0.95},
    {"index": 5, "score": 0.82}
  ],
  "latency_ms": 550.0
}
```

#### `/health` (GET)
**Purpose**: Health check and service status

**Response**:
```json
{
  "status": "healthy",
  "embedding_model_loaded": false,
  "embedding_model_name": "google/embeddinggemma-300m",
  "embedding_dim": 256,
  "cross_encoder_loaded": false,
  "cross_encoder_model": "cross-encoder/ms-marco-MiniLM-L6-v2",
  "cache_size_mb": 2.5,
  "cached_notes": 670,
  "idle_timeout_minutes": 10
}
```

#### `/` (GET)
**Purpose**: Root endpoint with basic service info

#### `/api/cache/` (Multiple endpoints)
**Purpose**: Cache management (info, save, clear, etc.)

---

## Dependencies & Requirements

**File**: `requirements.txt`

```
fastapi>=0.115.0              # Web framework
uvicorn[standard]>=0.32.0     # ASGI server
onnxruntime>=1.17.0           # Optimized inference (if available)
transformers>=4.38.0          # HuggingFace model loading
huggingface-hub>=0.20.0       # HuggingFace API
numpy>=2.0.2                  # Numerical computing
pydantic>=2.9.0               # Data validation
python-multipart>=0.0.12      # Form/multipart handling
sentence-transformers>=5.1.2  # Fallback embedding model
```

**Python Version**: 3.9+

**Virtual Environment Status**: 
- Location: `/Users/rmanor/obsidianrag/python-backend/venv/`
- Python version: 3.9
- All dependencies installed

---

## Configuration & Environment Setup

### Environment Variables

```bash
# Optional: HuggingFace token for model downloads
export HF_TOKEN="hf_your_token_here"

# Optional: Python path (used by plugin auto-start)
export PYTHON_PATH="python3"
```

### HuggingFace Setup (One-time)

```bash
# Authenticate with HuggingFace
huggingface-cli login

# Paste token from https://huggingface.co/settings/tokens
# Token gets saved to ~/.huggingface/token
```

### Cache Directory

- **Location**: `./cache/` (relative to python-backend/)
- **Created**: Automatically on startup if doesn't exist
- **Contents**:
  - `embeddings.npz`: Cached embeddings (2.5 MB currently)
- **Writable**: Must be writable by Python process

---

## Startup Process & Lifecycle

### 1. Initial Startup

```
start.sh
  └─> Activate venv/bin/activate
  └─> python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
      └─> FastAPI startup
          └─> lifespan() context manager
              ├─> Initialize cache dir
              ├─> Create EmbeddingService
              ├─> Load embeddings.npz (if exists)
              ├─> Create CrossEncoderService (models not loaded)
              ├─> Start idle checker task
              └─> Server ready on port 8000
```

**Time to Ready**: 1-2 seconds (just cache loading, model loads lazily)

### 2. First Search/Embed Request

```
POST /api/search
  └─> ensure_loaded()
      ├─> Download EmbeddingGemma model from HuggingFace (if first time)
      └─> Initialize ONNX session or sentence-transformers
          └─> Perform embedding/search
```

**First Request Latency**: 30-60 seconds (model download + load)
**Subsequent Requests**: <50ms

### 3. Idle Timeout (10 minutes)

```
Background idle_check_and_unload() task
  └─> Every 60 seconds, check if idle > 10 minutes
      └─> If yes:
          ├─> Unload model (frees 300MB memory)
          ├─> Save cache to embeddings.npz
          └─> Keep cache in memory
```

### 4. Shutdown

```
SIGTERM signal
  └─> lifespan() context manager cleanup
      ├─> Cancel idle checker task
      ├─> Save embeddings cache
      └─> Clean up resources
```

---

## Health Checks & Monitoring

### API Health Endpoint

```bash
# Check if backend is running
curl http://localhost:8000/health

# Expected response (JSON):
{
  "status": "healthy",
  "embedding_model_loaded": false,  # Model not loaded until first use
  "cached_notes": 670,              # Embeddings in cache
  "cache_size_mb": 2.5              # Cache file size
}
```

### Status Indicators

- **Model Loaded Status**: `embedding_model_loaded` field
  - `false`: Model hasn't been used yet (normal on startup)
  - `true`: Model was used and is in memory
- **Cache Status**: `cached_notes` field
  - Number of embeddings in NPZ file
  - Should grow as plugin indexes notes
- **Idle Timeout**: `idle_timeout_minutes` field
  - Currently set to 10 minutes
  - Model unloads after 10 minutes of no requests

### Common Status Scenarios

| State | Model Loaded | Meaning |
|-------|---|----------|
| Just Started | false | Normal; model loads on first request |
| After First Search | true | Normal; model in memory for fast queries |
| After 10min Idle | false | Normal; model was unloaded to save memory |
| service not initialized | N/A | Error; restart backend |

---

## Error Handling & Troubleshooting

### Backend Won't Start

1. **Check Python/venv**:
   ```bash
   cd python-backend
   source venv/bin/activate
   python --version  # Should be 3.9+
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test manually**:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

### Model Download Fails

1. **HuggingFace Authentication**:
   ```bash
   huggingface-cli login
   # Paste token from https://huggingface.co/settings/tokens
   ```

2. **Verify token**:
   ```bash
   huggingface-cli whoami
   ```

3. **Set HF_TOKEN environment variable**:
   ```bash
   export HF_TOKEN="your_token_here"
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

### Port Already in Use (8000)

```bash
# Find process using port 8000
lsof -i :8000

# Kill process (if needed)
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

### Cache Corruption

```bash
# Backup corrupted cache
mv cache/embeddings.npz cache/embeddings.npz.backup

# Backend will recreate cache on next use
# Plugin will re-index all notes
```

---

## Performance Characteristics

### Memory Usage

| Component | Memory |
|-----------|--------|
| EmbeddingGemma model (loaded) | ~300 MB |
| Embeddings cache (670 notes) | ~670 KB |
| Python/FastAPI overhead | ~50-100 MB |
| **Total Idle** | ~50-100 MB |
| **Total with Model** | ~350-400 MB |

### Latency

| Operation | Latency |
|-----------|---------|
| /health check | <5ms |
| Semantic search (cached) | <20ms |
| First request (model load) | 30-60s |
| Cross-encoder rerank (200 docs) | ~550ms |
| Cache load on startup | <2s |

### Scaling

| Metric | 670 notes | 5000 notes |
|--------|-----------|-----------|
| Embeddings cache size | 2.5 MB | 19 MB |
| Search latency | <20ms | <50ms |
| Model memory | 300 MB | 300 MB |

---

## Integration Points

### Obsidian Plugin Integration

The plugin (`obsidian-plugin/`) connects to the backend:

1. **Auto-Start**: Plugin spawns Python process on Obsidian launch
2. **File Changes**: Plugin sends updated note content to `/api/embed`
3. **Searches**: Plugin sends queries to `/api/search`
4. **Optional Reranking**: Plugin calls `/api/rerank` for cross-encoder

### MCP Integration (Claude Code)

The plugin implements Smart Connections v3.0 API for Claude Code:
- `search_vault_smart` MCP tool queries the backend
- Results use multi-signal ranking (semantic + BM25 + graph + temporal)

---

## Development & Testing

### Running in Development Mode

```bash
cd python-backend
source venv/bin/activate

# With auto-reload on code changes
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Testing Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Embedding (requires model to load first)
curl -X POST http://localhost:8000/api/embed \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello world"],
    "note_ids": ["test.md"],
    "use_cache": true
  }'

# Search
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test query",
    "note_ids": ["note1.md", "note2.md"],
    "top_k": 10
  }'
```

### Viewing Logs

```bash
# In terminal running the backend
# Logs appear directly on stdout

# Common log messages:
# "Cache directory initialized: /path/to/cache"
# "Loading ONNX model: google/embeddinggemma-300m..."
# "Model loaded successfully (256d)"
# "Idle for 10 minutes, unloading embedding model..."
```

---

## Important Files & Locations

| File | Purpose |
|------|---------|
| `/Users/rmanor/obsidianrag/python-backend/start.sh` | Startup script |
| `/Users/rmanor/obsidianrag/python-backend/requirements.txt` | Python dependencies |
| `/Users/rmanor/obsidianrag/python-backend/app/main.py` | FastAPI application |
| `/Users/rmanor/obsidianrag/python-backend/app/config.py` | Configuration settings |
| `/Users/rmanor/obsidianrag/python-backend/app/models/embedder.py` | Embedding service |
| `/Users/rmanor/obsidianrag/python-backend/cache/embeddings.npz` | Cached embeddings |
| `/Users/rmanor/obsidianrag/ARCHITECTURE.md` | Detailed system architecture |
| `/Users/rmanor/obsidianrag/README.md` | Installation & usage guide |

---

## Key Design Decisions

1. **Lazy Model Loading**: Model loads on first use, not at startup, for fast server start
2. **10-Minute Idle Timeout**: Automatically unloads model after 10 minutes with no requests
3. **NPZ Cache Format**: Compressed NumPy arrays for efficient storage and fast loading
4. **256d Matryoshka**: Truncates full 768d embeddings to 256d with no quality loss (85% storage savings)
5. **ONNX Runtime with Fallback**: Attempts ONNX for efficiency, falls back to sentence-transformers
6. **Cross-Encoder Disabled by Default**: RRF fusion works well without additional latency
7. **Per-File Debouncing**: Plugin waits 5 minutes before re-indexing changed notes

---

## Next Steps

If you need to:
- **Start the backend**: Use `./start.sh` or manual Python command
- **Test connectivity**: Visit `http://localhost:8000/health`
- **Debug issues**: Check `/Users/rmanor/obsidianrag/python-backend/` logs
- **Understand architecture**: See `/Users/rmanor/obsidianrag/ARCHITECTURE.md`
- **Check code details**: Explore `/Users/rmanor/obsidianrag/python-backend/app/`

Generated with [Claude Code](https://claude.com/claude-code)
