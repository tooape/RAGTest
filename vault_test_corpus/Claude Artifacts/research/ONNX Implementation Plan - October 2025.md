---
pageType: claudeResearch
tags:
  - claude
created: "2025-10-30"
---
# ONNX Implementation Plan for Obsidian RAG
---

## Objective

Migrate Python backend from PyTorch/sentence-transformers to ONNX Runtime with int8 quantization, targeting **67% memory reduction** (600MB → <200MB) with zero quality loss.

## Prerequisites

- [x] Research completed: [[Obsidian RAG Memory Optimization - October 2025]]
- [x] Plugin source at: `/Users/rmanor/obsidianrag/`
- [x] Current backend: `python-backend/app/models/embedder.py`

## Implementation Plan

### Phase 1: Setup & Research (30 minutes)

**1.1 Test ONNX Runtime Locally**
- Install onnxruntime: `pip install onnxruntime`
- Test basic model loading with sample code
- Verify tokenizer compatibility with transformers library

**Test Script** (`test_onnx.py`):
```python
from huggingface_hub import hf_hub_download
import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np

# Download model
model_id = "onnx-community/embeddinggemma-300m-ONNX"
model_path = hf_hub_download(
    model_id, 
    subfolder="onnx", 
    filename="model_quantized.onnx"  # int8 version
)

# Load
session = ort.InferenceSession(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Test
text = "This is a test query"
inputs = tokenizer(text, return_tensors="np", padding=True, truncation=True)
outputs = session.run(None, dict(inputs))
embedding = outputs[0][0][:256]  # Truncate to 256d

print(f"Embedding shape: {embedding.shape}")
print(f"Sample values: {embedding[:5]}")
```

**Success Criteria**:
- ✅ Model downloads successfully
- ✅ Inference produces 768d embeddings
- ✅ Truncation to 256d works
- ✅ No errors or warnings

---

### Phase 2: Implementation (2-3 hours)

**2.1 Create ONNX Embedder** (`app/models/embedder_onnx.py`)

```python
"""ONNX Runtime embedding service with int8 quantization."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from huggingface_hub import hf_hub_download


class ONNXEmbeddingService:
    """Service for generating 256d embeddings using ONNX Runtime."""
    
    def __init__(
        self,
        model_id: str,
        embedding_dim: int,
        cache_path: Path,
    ):
        """Initialize ONNX embedding service.
        
        Args:
            model_id: HuggingFace model ID (e.g., "onnx-community/embeddinggemma-300m-ONNX")
            embedding_dim: Target dimension after truncation (e.g., 256)
            cache_path: Path to NPZ cache file
        """
        self.model_id = model_id
        self.embedding_dim = embedding_dim
        self.cache_path = cache_path
        
        self.session: Optional[ort.InferenceSession] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.is_loaded = False
        
        # Cache: note_id -> embedding (256d)
        self.cache: Dict[str, np.ndarray] = {}
    
    async def initialize(self):
        """Load ONNX model and tokenizer."""
        print(f"Loading ONNX model: {self.model_id}...")
        
        # Download ONNX model (int8 quantized)
        model_path = hf_hub_download(
            self.model_id,
            subfolder="onnx",
            filename="model_quantized.onnx"  # int8 version
        )
        
        # Create ONNX session
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        self.session = ort.InferenceSession(
            model_path,
            sess_options,
            providers=["CPUExecutionProvider"]
        )
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.is_loaded = True
        
        print(f"ONNX model loaded ({self.embedding_dim}d)")
        
        # Load existing cache
        if self.cache_path.exists():
            print(f"Loading cache from {self.cache_path}...")
            self._load_cache()
            print(f"Loaded {len(self.cache)} cached embeddings")
    
    async def embed_texts(
        self,
        texts: List[str],
        note_ids: Optional[List[str]] = None,
        use_cache: bool = True,
    ) -> np.ndarray:
        """Generate 256d embeddings for texts.
        
        Args:
            texts: List of text content to embed
            note_ids: Optional note IDs for caching
            use_cache: Whether to use cached embeddings
            
        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        if not self.is_loaded or not self.session:
            raise RuntimeError("Model not loaded")
        
        embeddings_list = []
        
        for i, text in enumerate(texts):
            note_id = note_ids[i] if note_ids else None
            
            # Check cache
            if use_cache and note_id and note_id in self.cache:
                embeddings_list.append(self.cache[note_id])
                continue
            
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="np",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Run inference
            outputs = self.session.run(None, dict(inputs))
            full_embedding = outputs[0][0]  # (768,)
            
            # Truncate to 256d (Matryoshka)
            truncated_embedding = full_embedding[:self.embedding_dim]
            
            # Cache if note_id provided
            if note_id:
                self.cache[note_id] = truncated_embedding
            
            embeddings_list.append(truncated_embedding)
        
        # Save cache periodically
        if note_ids and len(note_ids) > 0:
            self._save_cache()
        
        return np.array(embeddings_list)
    
    async def search(
        self,
        query: str,
        note_ids: List[str],
        top_k: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search for most similar notes to query."""
        if not self.is_loaded or not self.session:
            raise RuntimeError("Model not loaded")
        
        # Embed query
        inputs = self.tokenizer(
            query,
            return_tensors="np",
            padding=True,
            truncation=True,
            max_length=512
        )
        outputs = self.session.run(None, dict(inputs))
        query_embedding = outputs[0][0][:self.embedding_dim]
        
        # Get cached embeddings
        note_embeddings = []
        valid_note_ids = []
        
        for note_id in note_ids:
            if note_id in self.cache:
                note_embeddings.append(self.cache[note_id])
                valid_note_ids.append(note_id)
        
        if not note_embeddings:
            return []
        
        # Compute cosine similarity
        note_embeddings_array = np.array(note_embeddings)
        similarities = self._cosine_similarity_batch(query_embedding, note_embeddings_array)
        
        # Sort by similarity (descending)
        ranked_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Format results
        results = [
            {
                "note_id": valid_note_ids[idx],
                "score": float(similarities[idx]),
            }
            for idx in ranked_indices
        ]
        
        return results
    
    def _cosine_similarity_batch(
        self, query: np.ndarray, documents: np.ndarray
    ) -> np.ndarray:
        """Compute cosine similarity between query and documents."""
        query_norm = query / np.linalg.norm(query)
        docs_norm = documents / np.linalg.norm(documents, axis=1, keepdims=True)
        similarities = np.dot(docs_norm, query_norm)
        return similarities
    
    def _load_cache(self):
        """Load embeddings cache from NPZ file."""
        try:
            data = np.load(self.cache_path, allow_pickle=True)
            embeddings = data["embeddings"]
            note_ids = data["note_ids"]
            
            if embeddings.shape[1] != self.embedding_dim:
                print(f"Warning: Cache dimension mismatch")
                return
            
            for note_id, embedding in zip(note_ids, embeddings):
                self.cache[note_id] = embedding
        except Exception as e:
            print(f"Error loading cache: {e}")
    
    def _save_cache(self):
        """Save embeddings cache to NPZ file."""
        if not self.cache:
            return
        
        try:
            note_ids = list(self.cache.keys())
            embeddings = np.array([self.cache[note_id] for note_id in note_ids])
            
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            
            np.savez_compressed(
                self.cache_path,
                embeddings=embeddings,
                note_ids=note_ids,
                version="1.0",
                model=self.model_id,
                dimension=self.embedding_dim,
            )
            
            print(f"✓ Saved {len(note_ids)} embeddings to {self.cache_path}")
        except Exception as e:
            print(f"✗ Error saving cache: {e}")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_size_bytes = sum(
            embedding.nbytes for embedding in self.cache.values()
        )
        return {
            "num_notes": len(self.cache),
            "size_mb": round(cache_size_bytes / (1024 * 1024), 2),
            "embedding_dim": self.embedding_dim,
        }
    
    async def cleanup(self):
        """Cleanup resources and save cache."""
        if self.cache:
            self._save_cache()
```

**2.2 Update Dependencies** (`requirements.txt`)

```txt
# Before (PyTorch + sentence-transformers)
fastapi==0.109.2
uvicorn[standard]==0.27.1
numpy==1.26.4
sentence-transformers==2.3.1  # REMOVE (includes PyTorch, ~2GB)
pydantic==2.6.1

# After (ONNX Runtime)
fastapi==0.109.2
uvicorn[standard]==0.27.1
numpy==1.26.4
onnxruntime==1.17.0  # ADD (~100MB)
transformers==4.38.0  # ADD (for tokenizer only, no PyTorch)
huggingface-hub==0.20.0  # ADD
pydantic==2.6.1
```

**2.3 Update Configuration** (`app/config.py`)

```python
class Settings:
    """Application settings."""
    
    # Model configuration
    MODEL_ID: str = "onnx-community/embeddinggemma-300m-ONNX"  # Changed
    EMBEDDING_DIM: int = 256
    USE_ONNX: bool = True  # New flag
    
    # ... rest unchanged
```

**2.4 Update Main App** (`app/main.py`)

```python
from app.config import settings

# Conditional import based on USE_ONNX flag
if settings.USE_ONNX:
    from app.models.embedder_onnx import ONNXEmbeddingService as EmbeddingService
else:
    from app.models.embedder import EmbeddingService

# ... rest unchanged, EmbeddingService is now ONNX version
```

---

### Phase 3: Testing & Validation (1-2 hours)

**3.1 Local Backend Testing**

```bash
cd /Users/rmanor/obsidianrag/python-backend

# Create new venv (clean slate)
python3 -m venv venv-onnx
source venv-onnx/bin/activate

# Install ONNX dependencies
pip install -r requirements.txt

# Test backend startup
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Verify in another terminal:
curl http://localhost:8000/health
```

**Expected Output**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "onnx-community/embeddinggemma-300m-ONNX",
  "embedding_dim": 256,
  "cache_size_mb": 0,
  "cached_notes": 0
}
```

**3.2 Memory Benchmarking**

```bash
# Check memory usage
ps aux | grep uvicorn | awk '{print $6/1024 " MB"}'

# Expected: <200MB (vs 600MB with PyTorch)
```

**3.3 Quality Validation**

Reuse existing benchmark from `/Users/rmanor/obsidianrag/Gemma test/beir_benchmark/`:

```python
# test_onnx_quality.py
# Run same 23-query test set with ONNX backend
# Compare metrics to PyTorch baseline

# Acceptable regression: <5% on any metric
# Expected: 0% regression (same model, just quantized)
```

**Metrics to Compare**:
- Precision@10
- MRR (Mean Reciprocal Rank)
- Recall@10
- NDCG@10

**3.4 End-to-End Plugin Testing**

```bash
# Rebuild and deploy plugin
cd /Users/rmanor/obsidianrag/obsidian-plugin
npm run build

# Copy to vault
cp main.js manifest.json styles.css \
   "/Users/rmanor/Library/Mobile Documents/iCloud~md~obsidian/Documents/My Vault/.obsidian/plugins/obsidian-rag/"

# Copy ONNX backend
cp -r ../python-backend \
   "/Users/rmanor/Library/Mobile Documents/iCloud~md~obsidian/Documents/My Vault/.obsidian/plugins/obsidian-rag/"
```

**Test Cases**:
1. Start Obsidian → Backend auto-starts
2. Run search query → Results returned
3. Check memory usage → <200MB
4. Restart Obsidian → Cache loads correctly
5. Multiple queries → Performance consistent

---

### Phase 4: Deployment & Monitoring (30 minutes)

**4.1 Git Commit & Push**

```bash
cd /Users/rmanor/obsidianrag
git add -A
git commit -m "Migrate to ONNX Runtime with int8 quantization

- Replace sentence-transformers with onnxruntime
- Create new ONNXEmbeddingService class
- Update dependencies (remove PyTorch, add onnxruntime)
- Add configuration flag for ONNX vs PyTorch

Results:
- Memory: 600MB → <200MB (67% reduction)
- Quality: Zero regression (same model, QAT-trained)
- Startup: Faster (no PyTorch overhead)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push
```

**4.2 Production Deployment**

- Plugin already deployed to My Vault
- Backend starts automatically via BackendManager
- Monitor console for any errors

**4.3 Monitoring**

Check memory usage after 1 day of normal use:
```bash
# Get backend PID
lsof -i :8000 | grep LISTEN | awk '{print $2}'

# Check memory
ps -p <PID> -o rss,vsz,comm | awk '{print $1/1024 " MB"}'
```

---

## Success Criteria

- ✅ Backend starts successfully with ONNX model
- ✅ Memory usage <200MB (67% reduction from 600MB)
- ✅ Search quality unchanged (<5% regression)
- ✅ Cache persistence works correctly
- ✅ No errors in console logs
- ✅ Obsidian app responsive (no lag)

## Rollback Plan

If issues occur:

1. **Switch back to PyTorch backend**: Set `USE_ONNX = False` in config.py
2. **Restore old venv**: Keep `venv-pytorch` backup
3. **Git revert**: `git revert HEAD` if needed

## Timeline Estimate

- **Phase 1** (Setup): 30 minutes
- **Phase 2** (Implementation): 2-3 hours
- **Phase 3** (Testing): 1-2 hours
- **Phase 4** (Deployment): 30 minutes

**Total**: ~4-6 hours

## Related Documents

- **[[Smart Connections Enhancement - Custom RAG]]** - Main project page
- [[Obsidian RAG Memory Optimization - October 2025]] - Optimization analysis
- [[October 27, 2025#Fixed Obsidian RAG Cache Persistence Issue]] - Cache persistence work
- [[October 30, 2025#Obsidian RAG Memory Optimization]] - Memory investigation session

## Next Steps

1. [ ] Execute Phase 1: Test ONNX locally
2. [ ] Execute Phase 2: Implement ONNXEmbeddingService
3. [ ] Execute Phase 3: Test and validate
4. [ ] Execute Phase 4: Deploy and monitor
5. [ ] Document results and update project pages
