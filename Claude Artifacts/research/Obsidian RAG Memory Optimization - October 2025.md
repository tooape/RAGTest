---
pageType: claudeResearch
tags:
  - claude
created: "2025-10-30"
---
# Obsidian RAG Memory Optimization Analysis
---

## Current State

**Memory Usage**: 600MB for Python backend
**Model**: `google/embeddinggemma-300m` (300M parameters)
**Disk Size**: 1.2GB
**Output**: 256d embeddings (Matryoshka truncation from 768d)
**Framework**: sentence-transformers with PyTorch

### Memory Breakdown
- **Model weights**: ~600MB (fp32/fp16)
- **Runtime overhead**: Python, FastAPI, uvicorn, numpy, PyTorch
- **Embedding cache**: ~204KB for 210 notes (negligible)

## Optimization Strategies

### Option 1: ONNX + Quantization (RECOMMENDED)
**Target Memory**: <200MB (~67% reduction)
**Quality Impact**: Minimal (QAT-trained model)

**Implementation**:
- Switch from `google/embeddinggemma-300m` to `onnx-community/embeddinggemma-300m-ONNX`
- Use int8 or uint8 quantized version
- Replace sentence-transformers with onnxruntime

**Advantages**:
- Same model quality (quantization-aware trained)
- 3x memory reduction (600MB → <200MB)
- Faster inference (ONNX optimizations)
- Cross-platform compatibility

**Code Changes Required**:
```python
# Current: sentence-transformers
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("google/embeddinggemma-300m")

# New: ONNX Runtime
import onnxruntime as ort
from transformers import AutoTokenizer
session = ort.InferenceSession("model.onnx")
tokenizer = AutoTokenizer.from_pretrained("onnx-community/embeddinggemma-300m-ONNX")
```

**Available Quantized Models**:
- `onnx-community/embeddinggemma-300m-ONNX` (fp32, q8, q4)
- `electroglyph/embeddinggemma-300m-ONNX-uint8` (uint8 specialized)

**References**:
- https://huggingface.co/onnx-community/embeddinggemma-300m-ONNX
- https://huggingface.co/electroglyph/embeddinggemma-300m-ONNX-uint8

### Option 2: Switch to MiniLM
**Target Memory**: ~80MB (~87% reduction)
**Quality Impact**: Moderate (trade-off for size)

**Implementation**:
- Replace with `sentence-transformers/all-MiniLM-L6-v2`
- 22M parameters, 384d embeddings
- 5x faster inference than current model

**Advantages**:
- Minimal memory footprint (22MB model)
- 5-14k sentences/sec on CPU
- Well-established model with good quality
- No code changes required (drop-in replacement)

**Disadvantages**:
- Lower quality than EmbeddingGemma
- No multilingual support (100+ languages → English-focused)
- Not ranked as high on MTEB benchmark

**When to Choose**:
- Desktop app responsiveness is critical
- Vault is primarily English content
- Willing to trade some quality for speed/memory

### Option 3: Lazy Loading Backend
**Target Memory**: 0MB when idle, 600MB when active
**Quality Impact**: None (same model)

**Implementation**:
- Start backend on-demand (first search query)
- Shutdown after 5-10 minutes of inactivity
- Show loading indicator during startup

**Advantages**:
- Zero memory cost when not searching
- No model quality trade-off
- Simple implementation (modify BackendManager.ts)

**Disadvantages**:
- First search has 5-10 second delay (model loading)
- Increased latency for intermittent searches
- More complex lifecycle management

**Code Changes**:
```typescript
// BackendManager.ts
async search(query: string) {
    await this.ensureRunning();  // Start if not running
    this.resetIdleTimer();       // Reset shutdown timer
    // ... existing search code
}

private resetIdleTimer() {
    clearTimeout(this.idleTimer);
    this.idleTimer = setTimeout(() => this.shutdown(), 600000); // 10 min
}
```

### Option 4: PyTorch FP16 Optimization
**Target Memory**: ~350MB (~42% reduction)
**Quality Impact**: Minimal

**Implementation**:
- Explicitly use `torch.float16` for model
- Enable `torch.inference_mode()`
- Disable gradients computation

**Advantages**:
- Easy to implement (configuration change)
- No external dependencies
- Preserves model quality

**Disadvantages**:
- Only 2x reduction (vs 3x for ONNX quantization)
- Still using sentence-transformers overhead

**Code Changes**:
```python
# embedder.py
import torch
self.model = SentenceTransformer(self.model_name)
self.model.half()  # Convert to FP16
self.model.eval()  # Inference mode
```

## Comparison Matrix

| Option | Memory | Quality | Speed | Complexity | Recommended For |
|--------|--------|---------|-------|------------|----------------|
| ONNX + int8 | <200MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium | **Production** |
| MiniLM | ~80MB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Low | English-only vaults |
| Lazy Loading | 0-600MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Medium | Intermittent use |
| FP16 | ~350MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Low | Quick win |

## Recommended Implementation Plan

### Phase 1: Quick Wins (1-2 hours)
1. **Enable FP16 optimization** → immediate 42% reduction
2. **Add idle timeout** → 0MB when not in use
3. **Test memory usage** → verify improvements

### Phase 2: ONNX Migration (4-6 hours)
1. **Implement ONNX backend** → replace sentence-transformers
2. **Use int8 quantized model** → <200MB target
3. **Benchmark quality** → ensure no regression vs current

### Phase 3: Alternative Models (Optional)
1. **Benchmark MiniLM** → test quality vs memory trade-off
2. **User configuration** → allow model selection in settings
3. **Document trade-offs** → help users choose

## Implementation Priority

**Highest ROI**: Option 1 (ONNX + int8)
- Best balance of memory, quality, and speed
- 67% memory reduction with same quality
- Future-proof (ONNX standard, quantization-aware trained)

**Quick Win**: Option 4 (FP16) + Option 3 (Lazy Loading)
- Can implement immediately
- Combined: 42% reduction + 0MB when idle
- No quality trade-off

**Alternative**: Option 2 (MiniLM)
- Only if memory is critical constraint
- English-focused vaults
- Willing to sacrifice some quality

## Next Steps

1. ✅ Research completed
2. [ ] Implement FP16 optimization (quick win)
3. [ ] Add idle timeout for backend
4. [ ] Prototype ONNX backend with int8
5. [ ] Benchmark quality regression (if any)
6. [ ] Deploy optimized version
7. [ ] Monitor memory usage in production

## Related Pages

- **[[Smart Connections Enhancement - Custom RAG]]** - Main project page
- [[ONNX Implementation Plan - October 2025]] - Implementation plan for this optimization
- [[October 27, 2025#Fixed Obsidian RAG Cache Persistence Issue]] - Cache debugging work
- [[October 30, 2025#Obsidian RAG Memory Optimization]] - Memory investigation session
- [[Evaluation]] - Evaluation methodologies

## References

- EmbeddingGemma ONNX: https://huggingface.co/onnx-community/embeddinggemma-300m-ONNX
- ONNX Quantization: https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html
- Sentence-Transformers Quantization: https://sbert.net/docs/package_reference/sentence_transformer/quantization.html
- MiniLM Model: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
