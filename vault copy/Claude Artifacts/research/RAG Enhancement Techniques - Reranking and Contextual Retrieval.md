---
created: 2025-10-23
pageType: claudeResearch
datelink: "[[October 23, 2025]]"
tags:
  - claude
Related Pages:
  - "[[Smart Connections Enhancement - Custom RAG]]"
  - "[[Evaluation]]"
---
# RAG Enhancement Techniques - Reranking and Contextual Retrieval
---

Technical deep dive on advanced RAG techniques from recent research (2024-2025), focusing on Cohere reranking and Anthropic's contextual retrieval approach.

## Cohere Reranking
---

### What Is Reranking?

Traditional RAG retrieval happens in two stages:
1. **First-stage retrieval**: Fast semantic search (cosine similarity) retrieves top-K candidates (e.g., K=100)
2. **Reranking**: Slower but more accurate model re-scores these K candidates

**Why this works**:
- Semantic search uses **bi-encoders**: Query and documents encoded independently, compared via cosine similarity
  - Fast: Can precompute all document embeddings
  - Limited: Doesn't see query-document interaction
- Reranking uses **cross-encoders**: Query + document processed together
  - Slow: Must process each (query, doc) pair at inference time
  - Accurate: Sees full interaction, captures nuanced relevance

### Cohere Rerank API

**Model**: Cohere Rerank v3.5 (released 2024)
- **Context window**: 4096 tokens per document
- **Language support**: 100+ languages
- **Latency**: ~50-200ms for reranking 100 documents
- **Performance**: 25-35% MRR improvement over semantic-only retrieval

**How it works**:
```python
# After first-stage retrieval (semantic + BM25 hybrid)
candidates = hybrid_search(query, top_k=100)

# Rerank with Cohere
import cohere
co = cohere.Client(api_key="...")

results = co.rerank(
    model="rerank-english-v3.0",
    query=query,
    documents=[doc.content for doc in candidates],
    top_n=20  # Only return top 20 after reranking
)

# Results include relevance scores (0-1) for ranking
for result in results:
    print(f"{result.document.text}: {result.relevance_score}")
```

**Cost considerations**:
- Cohere charges per search (not per token)
- ~$1 per 1000 searches for Rerank v3.5
- For personal vault: negligible cost (<$5/month even with heavy usage)
- For production: Can cache reranking results for repeated queries

### Why Reranking Helps Your Use Case

**Problem**: Semantic search finds `[[Lr Home]]` but misses recent daily notes mentioning Lr Agent

**Reranking advantage**: Cross-encoder sees full context
- Query: "What's the status of Lr Agent?"
- Candidate 1: "Lr Home" page (lots of Lr mentions, but static)
- Candidate 2: "October 16, 2025" daily note: "Lr Agent kick off mid-november"

**Cross-encoder reasoning**:
- Sees "status" + "kick off mid-november" = temporal/current info ✓
- Sees "Lr Home" + comprehensive overview = background info
- Ranks daily note higher for "status" query

**Limitation**: Reranking won't solve the root problem if daily notes aren't in top-100 candidates
- Need hybrid search + graph boosting to get them into candidate set first
- Then reranking polishes the final ranking

## Anthropic's Contextual Retrieval
---

### The Chunking Context Problem

**Traditional RAG chunking**:
```markdown
# Lr Home

## 2025

### Post max
**Tech and Relevance**
- Feedback tweaking based on usage
- Embedding optimization
```

**Chunks created**:
- Chunk 1: "Tech and Relevance: Feedback tweaking based on usage"
- Chunk 2: "Embedding optimization"

**Problem**: Chunk 2 has no context!
- What is "embedding optimization" for? (Lr? Photoshop? Generic?)
- When? (2025? Post-max milestone?)
- Lost all hierarchical context from headings

### Anthropic's Solution: Contextual Retrieval

**Idea**: Prepend each chunk with context before embedding it

**Step 1: Generate context with LLM**
```python
# For each chunk, ask LLM to add context
prompt = f"""
Document: {full_document}

Chunk: "{chunk_text}"

Please provide a brief context (1-2 sentences) that situates this chunk
within the overall document. Include the document title, relevant section
headings, and any important context needed to understand this chunk in isolation.
"""

context = llm.generate(prompt)
# Returns: "This chunk is from the Lr Home page, under the 2025 roadmap,
# specifically the Post-max milestone tech and relevance track."
```

**Step 2: Store chunk with context prepended**
```python
contextual_chunk = f"{context}\n\n{chunk_text}"
embedding = embed(contextual_chunk)
# Store embedding + original chunk (not the context-prepended version)
```

**Step 3: At retrieval time**
- Query embeddings search against contextual chunk embeddings
- Return original chunks (without prepended context) to avoid redundancy

### Anthropic's Research Results

**Baseline performance** (semantic search only):
- Retrieval failure rate: ~15% on their test set

**Improvements**:
- **Hybrid search** (semantic + BM25): 35% reduction in failures → 9.75% failure rate
- **Contextual retrieval** (semantic only): 49% reduction → 7.65% failure rate
- **Contextual + Hybrid**: 67% reduction → 4.95% failure rate
- **Contextual + Hybrid + Reranking**: Mentioned as best approach but specific metrics not disclosed

**Key insight**: Contextual retrieval and hybrid search are complementary
- Hybrid catches keyword misses
- Contextual catches context/semantic misses
- Combined effect is multiplicative, not additive

### Implementation for Your Vault

**Vault-specific context patterns**:

1. **Daily notes**: Already well-scoped (each note is one day)
   ```
   Context: "This is from the daily note for October 23, 2025, under the Meetings section,
   specifically notes from Lr monthly leadership meeting."

   Chunk: "QU roadshow for Lr Agent planned for November"
   ```

2. **Program pages**: Need hierarchical context
   ```
   Context: "This is from the Lr Home program page, under the 2025 roadmap,
   Post-max milestone, Tech and Relevance track."

   Chunk: "Embedding optimization and feedback tweaking based on usage"
   ```

3. **People pages**: Relationship context
   ```
   Context: "This is from Tracy King's person page, under the 'Works on' section."

   Chunk: "Evaluation methodologies and quality assurance for CKG 4.0"
   ```

**Cost analysis**:
- One-time LLM cost to generate context for all chunks
- Your vault: ~670 notes × ~5 chunks/note = ~3,350 chunks
- At $0.25 per 1M tokens (Claude 3 Haiku): ~$0.50 total one-time cost
- Incremental: Only need to generate context for new/modified notes

**Caching strategy**:
- Store context in chunk metadata
- Regenerate when note content changes
- Can reuse context for multiple chunk splits if heading structure unchanged

### Context Generation Management

**Operational Strategy: Smart Auto-Regeneration**

Context generation should be managed intelligently to minimize costs while keeping the index up-to-date.

**Initial Setup** (One-time):
```typescript
async function initialize() {
    const indexExists = await checkIndex();

    if (!indexExists) {
        // First time setup - upfront generation
        await showNotice("Generating contextual index (one-time, ~5 min)...");
        await generateContextForAllNotes();  // $0.50 one-time cost
        await showNotice("Index generation complete!");
    }
}
```

**Automatic Incremental Updates**:

Only regenerate context when actually needed:

1. **New note created** → Generate context for all chunks in that note
2. **Note modified** → Smart detection:
   - Extract heading structure from old and new versions
   - If only content changed (same headings) → NO regeneration needed
   - If headings added/removed/renamed → Regenerate affected chunks only
3. **Daily background sync** → Catch any missed updates from last 24 hours

**Smart Detection Implementation**:
```typescript
// On note modification (Obsidian vault event)
vault.on('modify', async (file) => {
    const oldMetadata = await getChunkMetadata(file);
    const newNote = await vault.read(file);

    if (needsContextRegeneration(oldMetadata, newNote)) {
        // Structure changed - regenerate context (rare)
        await regenerateContextForNote(file);  // ~$0.0005
    } else {
        // Just re-embed with existing context (free, local)
        await reembedChunksWithExistingContext(file);
    }
});

function needsContextRegeneration(oldNote: Note, newNote: Note): boolean {
    // Extract heading structure
    const oldHeadings = extractHeadings(oldNote.content);
    const newHeadings = extractHeadings(newNote.content);

    // Only regenerate if structure changed
    return !deepEqual(oldHeadings, newHeadings);
}
```

**Chunk Metadata Structure**:
```typescript
interface ChunkMetadata {
    chunk_id: string;
    source_note: string;
    chunk_text: string;
    context: string;  // LLM-generated context (cached)
    context_generated_at: string;  // Timestamp
    note_modified_at: string;  // Track source note modification
    heading_structure: string[];  // Cache for change detection
    embedding: number[];  // Contextual embedding
}
```

**Manual Override Commands**:

Always provide manual control for troubleshooting and bulk operations:

```typescript
// Command palette commands
commands.addCommand({
    id: 'regenerate-context-current',
    name: 'Regenerate context for current note',
    callback: async () => {
        const activeFile = workspace.getActiveFile();
        await regenerateContextForNote(activeFile);
        await showNotice('Context regenerated');
    }
});

commands.addCommand({
    id: 'regenerate-context-vault',
    name: 'Rebuild entire contextual index',
    callback: async () => {
        const confirmed = await confirmDialog(
            'This will regenerate context for all notes (~$0.50). Continue?'
        );
        if (confirmed) {
            await generateContextForAllNotes();
            await showNotice('Full index rebuild complete');
        }
    }
});

commands.addCommand({
    id: 'regenerate-context-modified',
    name: 'Sync context for recently modified notes',
    callback: async () => {
        const staleChunks = await findNotesModifiedSince('24 hours');
        await regenerateContextBatch(staleChunks);
        await showNotice(`Synced ${staleChunks.length} notes`);
    }
});
```

**Settings Panel**:
```typescript
// Plugin settings
interface PluginSettings {
    autoRegenerateContext: boolean;  // Default: true
    backgroundSyncEnabled: boolean;  // Default: true
    backgroundSyncInterval: number;  // Hours, default: 24
    llmProvider: 'claude-haiku' | 'local-llm' | 'template';
}

// Settings UI
addToggle({
    name: 'Auto-regenerate context',
    desc: 'Automatically regenerate context when note structure changes',
    value: settings.autoRegenerateContext,
    onChange: (value) => settings.autoRegenerateContext = value
});

addButton({
    name: 'Rebuild Index',
    desc: 'Manually regenerate context for entire vault',
    buttonText: 'Rebuild',
    onClick: () => commands.executeCommandById('regenerate-context-vault')
});
```

**Cost Breakdown**:

| Operation | Frequency | Cost |
|-----------|-----------|------|
| Initial setup | One-time | ~$0.50 |
| New note created | ~1-2/day | ~$0.0002/note |
| Structure change | ~0.5/day | ~$0.0005/note |
| Content-only edit | ~10/day | $0 (no regen needed) |
| **Monthly total** | - | **~$0.02-0.08** |

**Key Benefits**:
- **Mostly free**: Content edits don't trigger regeneration (context still valid)
- **Smart detection**: Only regenerates when heading structure changes
- **Always current**: Index stays up-to-date automatically
- **Manual override**: Full control when needed for troubleshooting
- **Background sync**: Catches any missed updates during daily idle time

**Example Scenario**:
```
User edits "October 23, 2025.md":
1. Added meeting notes under existing "# Meetings" section
2. Plugin detects: same heading structure (# Notes, # Meetings unchanged)
3. Decision: NO context regeneration needed
4. Action: Re-embed chunks with existing cached context (free, local)
5. Cost: $0

User edits "Lr Home.md":
1. Added new "## 2026" section with roadmap
2. Plugin detects: heading structure changed (new H2 added)
3. Decision: Regenerate context for chunks in "2026" section only
4. Action: LLM generates context for ~3 new chunks, re-embeds
5. Cost: ~$0.0003
```

## Betweenness Centrality
---

### Graph Theory Concept

**Definition**: Betweenness centrality measures how often a node appears on shortest paths between other nodes in a graph.

**Intuition**: Bridge notes that connect different topic clusters
- High betweenness = "broker" between communities
- Remove the node → graph becomes disconnected or paths get much longer

### Calculation

**For node *v***, betweenness centrality:
```
C_B(v) = Σ (σ_st(v) / σ_st)
```

Where:
- `σ_st` = number of shortest paths from node *s* to node *t*
- `σ_st(v)` = number of those paths that pass through node *v*
- Sum over all pairs of nodes *s, t* where *s ≠ t ≠ v*

**Example vault graph**:
```
Daily notes:        Program pages:
Oct 20 ──→ Oct 21   Intent AI Home
  ↓          ↓              ↑
  v          v              |
  └─→ [[Query Understanding]] ←─┘
              ↓
              v
        Evaluation ←── CKG 4.0
```

**Betweenness scores**:
- **Query Understanding**: HIGH (bridges daily notes ↔ program pages)
- **Evaluation**: MEDIUM (connects QU and CKG 4.0)
- **Daily notes**: LOW (leaf nodes, no paths go through them)
- **Program pages**: MEDIUM (connect to concepts but not between clusters)

### Why It Matters for Your Use Case

**Problem**: Query "evaluation methodology" should find both:
1. `[[Evaluation]]` page (canonical)
2. Daily notes discussing evaluation work
3. `[[CKG 4.0]]` (uses evaluation)

**Semantic search alone**: Might rank them Evaluation > CKG 4.0 > daily notes

**With betweenness boost**:
- **Query Understanding** gets ranked higher (high betweenness = important connector)
- Signals: "This note is central to understanding relationships between topics"
- Acts as a "hub" that leads to related content

**For your 390 daily notes**:
- Daily notes have low betweenness (mostly leaves in graph)
- BUT their targets have high betweenness
- Strategy: Boost notes that link TO high-betweenness pages
  - "If this daily note links to Query Understanding (high betweenness), it's probably important"

### Other Graph Centrality Metrics

**PageRank**:
- Measures importance by counting incoming links (weighted by importance of linker)
- Good for finding authoritative hub pages
- Your canonical pages (`[[Lr Home]]`, `[[Intent AI Home]]`) would have high PageRank

**Degree centrality**:
- Simple count of links (in + out)
- Your daily notes have high out-degree (link to many concepts)
- Program pages have high in-degree (many notes link to them)

**Local clustering coefficient**:
- Measures how interconnected a node's neighbors are
- High clustering = tightly knit topic cluster
- Useful for detecting communities (Intent AI cluster vs Lr cluster)

**For retrieval ranking, combination strategy**:
```python
graph_score = (
    0.4 * links_to_high_betweenness +  # Daily notes linking to important connectors
    0.3 * pagerank_score +              # Authoritative pages
    0.2 * betweenness_score +           # Bridge notes themselves
    0.1 * local_clustering              # Topic coherence
)
```

## Contextual Chunking Strategies
---

### Chunk Size Trade-offs

**Small chunks (128-256 tokens)**:
- **Pros**: Precise retrieval, less noise, more chunks = better recall
- **Cons**: Lost context, might split semantic units, more chunks to rank

**Large chunks (512-1024 tokens)**:
- **Pros**: More context, fewer chunks to manage, complete thoughts
- **Cons**: Noisy retrieval, harder to pinpoint relevant info, lower precision

**Research consensus (2024-2025)**: 500-800 tokens optimal for most use cases
- With 10-20% overlap between chunks
- Contextual retrieval makes larger chunks more viable (adds missing context back)

### Vault-Specific Chunking Strategy

**Your vault characteristics**:
- Daily notes: ~200-500 tokens each (already good chunk size)
- Program pages: 2000-5000 tokens (need splitting)
- Meeting sections: 100-300 tokens (already well-scoped by H2 headings)

**Proposed chunking approach**:

1. **Daily notes**: Keep as single chunks (or split by H1 sections if >800 tokens)
   ```markdown
   # October 23, 2025
   # Notes
   [treat as one chunk]

   # Meetings
   ## Lr monthly leadership #meetings
   [treat as separate chunk]
   ```

2. **Program pages**: Split by H2 headings + context
   ```markdown
   Chunk 1 context: "From Lr Home page, Overview section"
   Chunk 1 content: [Overview section content]

   Chunk 2 context: "From Lr Home page, 2025 > Post max section"
   Chunk 2 content: [Post max content]
   ```

3. **Hierarchical context preservation**:
   ```python
   def generate_chunk_context(note, heading_path):
       """
       note: "Lr Home"
       heading_path: ["2025", "Post max", "Tech and Relevance"]
       """
       context = f"From {note}"
       if heading_path:
           context += f", under {' > '.join(heading_path)}"
       return context
   ```

### Overlap Strategy

**Purpose**: Prevent semantic units from being split across chunks

**Implementation**:
```python
# 600 token chunks with 100 token (17%) overlap
chunk_1 = tokens[0:600]
chunk_2 = tokens[500:1100]  # Starts 100 tokens before chunk_1 ends
chunk_3 = tokens[1000:1600]
```

**For your vault**: Overlap by one heading level
```markdown
Chunk 1:
# 2025
## Post max
### Tech and Relevance
- Feedback tweaking
[END]

Chunk 2:
### Tech and Relevance  ← Overlap: repeat heading
- Feedback tweaking      ← Overlap: repeat first few items
- Embedding optimization
### Surface Expansion
[END]
```

**Benefits**:
- Semantic units near chunk boundaries appear in multiple chunks
- Retrieval has two chances to find relevant content
- Cost: ~20% more chunks (manageable for 670-note vault)

### Metadata Enrichment

**Beyond just text context**, store structured metadata:

```json
{
  "chunk_id": "lr-home-2025-postmax-001",
  "source_note": "Lr Home",
  "note_type": "programHome",
  "heading_path": ["2025", "Post max", "Tech and Relevance"],
  "created_date": "2025-09-24",
  "last_modified": "2025-10-23",
  "outbound_links": ["[[Evaluation]]", "[[Query Understanding]]"],
  "inbound_link_count": 45,
  "tags": ["claude"],
  "chunk_text": "...",
  "contextual_text": "From Lr Home page, under 2025 > Post max > Tech and Relevance...",
  "embedding": [0.123, -0.456, ...]
}
```

**Use metadata for filtering and boosting**:
- Query: "What's the current status of Lr?"
  - Filter: `last_modified > "2025-10-01"` (recent only)
  - Boost: chunks with `note_type: "daily"` (temporal context)
  - Boost: chunks linking to `[[Lr Home]]` (related content)

## Implementation Recommendations
---

### Prioritized Rollout

**Phase 1: Hybrid Search + Graph Boosting** (Solves your immediate problem)
- Combine semantic + BM25 retrieval
- Boost candidates that link to/from relevant canonical pages
- Boost by betweenness centrality
- **Impact**: Should fix "missing daily notes" issue

**Phase 2: Contextual Retrieval** (Improves precision)
- Generate context for chunks using Claude Haiku (cheap)
- Re-embed all chunks with context
- **Impact**: Better ranking of chunked program pages

**Phase 3: Reranking** (Polish final results)
- Add Cohere Rerank for top-20 results
- Optional: Train custom reranker on your click-through data
- **Impact**: Final 10-20% improvement in result quality

### Cost Analysis (All Phases)

**One-time setup**:
- Contextual retrieval (670 notes × 5 chunks): ~$0.50 (Claude Haiku)
- Re-embedding with context (3,350 chunks): Free (local embeddings) or ~$0.03 (OpenAI)

**Ongoing costs (assuming 50 searches/day)**:
- Cohere Rerank: ~$1.50/month
- LLM context generation for new notes: ~$1/month

**Total**: <$5/month for production-quality RAG

### Performance Targets

**First-stage retrieval** (hybrid search + graph boosting):
- Latency: <50ms
- Implementation: TypeScript plugin (native performance)

**Contextual embedding** (one-time or on note update):
- Latency: Doesn't matter (async background job)
- Implementation: TypeScript or Python (whichever is easier)

**Reranking** (optional Phase 3):
- Latency: 50-200ms (Cohere API)
- Implementation: Python service (better ML ecosystem) or API call from TypeScript

**Total query latency**: <100ms (Phase 1), <300ms (Phase 3)

## References
---

- **Anthropic Contextual Retrieval**: "Contextual Embeddings and Contextual BM25" (2024)
- **Cohere Rerank**: Rerank v3.5 model documentation and benchmarks
- **Graph Centrality**: Newman, M. "Networks: An Introduction" (2010)
- **Chunking Strategies**: Production RAG best practices survey (2024-2025)
- Related vault pages: [[Smart Connections Enhancement - Custom RAG]], [[Evaluation]]
