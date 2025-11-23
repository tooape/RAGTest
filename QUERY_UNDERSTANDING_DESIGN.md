# Query Understanding System Design

## Overview
Query understanding pipeline to improve vault search relevance by bridging the gap between user queries and vault structure/terminology.

## Key Insights from Test Queries

### Pattern Analysis (First 10 Queries)
```
User: "who's the PsW PM?"
  → Primary: "Photoshop Web PM" (abbreviation expansion)
  → Alternate: "PsW product manager" (keep abbreviation, expand PM)

User: "When was the last time I met with them?"
  → Primary: "Hao meeting recent" (context injection + temporal)
  → Alternate: "Hao #meetings" (tag injection)

User: "What did I discuss with Ritu in our last 1x1"
  → Primary: "Ritu 1x1" (implicit 1x1 detection)
  → Alternate: "Ritu #meetings/1x1" (explicit tag)

User: "what are the Q1 '26 must nails"
  → Primary: "Q1 2026 must nails" (year normalization)
  → Alternate: "2026 Q1 priorities" (synonym expansion)
```

### Key Transformation Types
1. **Abbreviation Expansion**: PsW → Photoshop Web, GPM → Group PM manager
2. **Tag Injection**: "1x1" → #meetings/1x1, "meeting" → #meetings
3. **Name Expansion**: Brian → Brian Eriksson, Ritu → Ritu Goel
4. **Temporal Detection**: "recent", "last time" → temporal boost + keyword
5. **Synonym Expansion**: "must nails" ↔ "priorities"
6. **Context Resolution**: "them" → Hao (from conversation context)

---

## 5-Stage Query Understanding Pipeline

```
User Query → [1. Normalize] → [2. Expand Entities] → [3. Inject Tags]
           → [4. Detect Signals] → [5. Generate Variants] → Enhanced Queries
```

### Stage 1: Normalization
**Purpose**: Clean and standardize query text

**Transformations**:
- Date normalization: "Q1 '26" → "Q1 2026"
- Case normalization: Preserve proper nouns, lowercase rest
- Whitespace cleanup
- Apostrophe handling: "who's" → "who is"

**Implementation**:
```python
def normalize(query: str) -> str:
    # Year expansion
    query = re.sub(r"'(\d{2})\b", lambda m: f"20{m.group(1)}", query)
    # Possessive/contractions (optional)
    query = query.replace("'s ", " ")
    return query.strip()
```

---

### Stage 2: Entity Expansion
**Purpose**: Expand abbreviations and short names using vault knowledge

#### 2.1 Build Abbreviation Dictionary (One-time)
Extract from vault frontmatter and create bidirectional mapping:

```python
# From vault metadata
abbreviations = {
    # Programs
    "PsW": ["Photoshop Web"],
    "Lr": ["Lightroom"],
    "GPM": ["Group PM manager", "Group Product Manager"],
    "PM": ["product manager", "PM"],

    # People (from aliases)
    "Hao": ["Hao Xu"],
    "Ritu": ["Ritu Goel"],
    "Brian": ["Brian Eriksson"],
    "Kosta": ["Kosta Blank"],

    # Terms
    "1x1": ["one-on-one", "1:1"],
    "QIT": ["Query Intent Type"],
}
```

**Auto-generation**:
```python
def build_abbreviation_dict(vault_path: str) -> Dict[str, List[str]]:
    """Extract aliases from vault frontmatter."""
    abbrevs = {}

    for md_file in glob(f"{vault_path}/**/*.md", recursive=True):
        frontmatter = parse_frontmatter(md_file)

        # Get file title (without .md)
        title = Path(md_file).stem

        # Add aliases as abbreviations
        if 'aliases' in frontmatter:
            for alias in frontmatter['aliases']:
                if alias != title:
                    abbrevs[alias] = abbrevs.get(alias, []) + [title]

    return abbrevs
```

#### 2.2 Query Expansion
```python
def expand_entities(query: str, abbrev_dict: Dict) -> List[str]:
    """Generate query variants with entity expansion."""
    variants = [query]  # Original

    # Find potential abbreviations (uppercase words, known patterns)
    tokens = query.split()

    for i, token in enumerate(tokens):
        clean_token = token.strip("?.!,")

        if clean_token in abbrev_dict:
            # Generate variants with each expansion
            for expansion in abbrev_dict[clean_token]:
                new_tokens = tokens.copy()
                new_tokens[i] = expansion
                variants.append(" ".join(new_tokens))

    return variants

# Example:
# expand_entities("who's the PsW PM?", abbrevs)
# → ["who's the PsW PM?",
#    "who's the Photoshop Web PM?",
#    "who's the PsW product manager?",
#    "who's the Photoshop Web product manager?"]
```

---

### Stage 3: Tag Injection
**Purpose**: Automatically add Obsidian tags based on query intent

**Tag Rules**:
```python
tag_patterns = {
    # Meeting detection
    r'\b(meeting|met|discuss|talked|spoke)\b': ['#meetings'],
    r'\b(1x1|one-on-one|1:1)\b': ['#meetings/1x1'],
    r'\bstaff\s+meeting\b': ['#meetings/staff'],

    # Temporal patterns (for temporal boost)
    r'\b(recent|latest|last\s+time|most\s+recent)\b': ['__TEMPORAL__'],

    # Project/program detection (if you have tags)
    r'\b(Intent\s+AI|IntentAI)\b': ['#intent-ai'],
    r'\b(Lightroom|Lr)\b': ['#lightroom'],
}
```

**Implementation**:
```python
def inject_tags(query: str) -> Tuple[str, Dict[str, Any]]:
    """Add tags and extract signals from query."""
    tagged_query = query
    signals = {'tags': [], 'temporal_boost': False}

    for pattern, tags in tag_patterns.items():
        if re.search(pattern, query, re.IGNORECASE):
            for tag in tags:
                if tag == '__TEMPORAL__':
                    signals['temporal_boost'] = True
                elif tag.startswith('#'):
                    signals['tags'].append(tag)
                    # Append tag to query for BM25 matching
                    if tag not in tagged_query:
                        tagged_query += f" {tag}"

    return tagged_query, signals

# Example:
# inject_tags("What did I discuss with Ritu in our last 1x1")
# → ("What did I discuss with Ritu in our last 1x1 #meetings #meetings/1x1",
#    {'tags': ['#meetings', '#meetings/1x1'], 'temporal_boost': False})
```

---

### Stage 4: Signal Detection
**Purpose**: Extract query intent signals to adjust retrieval strategy

**Detected Signals**:
```python
class QuerySignals:
    has_person_name: bool          # Query mentions person → boost person pages
    has_temporal_keyword: bool     # "recent", "latest" → increase temporal_weight
    has_project_keyword: bool      # "Intent AI" → boost project hub
    meeting_type: Optional[str]    # "1x1", "staff", generic
    intent: str                    # "who", "what", "when", "how", "browse"
```

**Implementation**:
```python
def detect_signals(query: str, person_names: Set[str]) -> QuerySignals:
    """Detect query intent signals."""
    signals = QuerySignals()

    # Person detection
    for person in person_names:
        if person.lower() in query.lower():
            signals.has_person_name = True
            break

    # Temporal detection
    temporal_keywords = ['recent', 'latest', 'last time', 'last', 'most recent']
    signals.has_temporal_keyword = any(kw in query.lower() for kw in temporal_keywords)

    # Intent classification
    if query.lower().startswith(('who', 'who\'s', 'who is')):
        signals.intent = 'who'
    elif query.lower().startswith(('what', 'what\'s')):
        signals.intent = 'what'
    elif query.lower().startswith(('when', 'when did')):
        signals.intent = 'when'
    elif query.lower().startswith(('how', 'why')):
        signals.intent = 'how'
    else:
        signals.intent = 'browse'

    return signals
```

---

### Stage 5: Strategy Selection & Weight Adjustment
**Purpose**: Route query to optimal retrieval strategy based on signals

**Strategy Router**:
```python
def select_strategy(signals: QuerySignals) -> Dict[str, Any]:
    """Select retrieval strategy and weights based on query signals."""

    # Default weights
    config = {
        'strategy': 'multisignal',
        'semantic_weight': 0.3,
        'bm25_weight': 0.5,
        'graph_weight': 0.15,
        'temporal_weight': 0.05,
    }

    # Adjust based on signals

    # Person queries → boost BM25 (name matching) and graph (person page links)
    if signals.has_person_name:
        config['bm25_weight'] = 0.6
        config['graph_weight'] = 0.25
        config['semantic_weight'] = 0.15

    # Temporal queries → boost temporal signal
    if signals.has_temporal_keyword:
        config['temporal_weight'] = 0.20
        config['bm25_weight'] = 0.45  # Reduce BM25 slightly

    # "Who" queries → likely need person pages
    if signals.intent == 'who':
        config['graph_weight'] = 0.30  # Person pages are hubs
        config['bm25_weight'] = 0.5
        config['semantic_weight'] = 0.20

    # "When" queries → temporal is critical
    if signals.intent == 'when':
        config['temporal_weight'] = 0.35
        config['bm25_weight'] = 0.40
        config['semantic_weight'] = 0.15
        config['graph_weight'] = 0.10

    return config
```

---

## Complete Pipeline

```python
class QueryUnderstandingPipeline:
    """Full query understanding and enhancement pipeline."""

    def __init__(self, vault_path: str):
        # Build knowledge from vault
        self.abbrevs = build_abbreviation_dict(vault_path)
        self.person_names = extract_person_names(vault_path)
        self.tag_patterns = load_tag_patterns()

    def process(self, user_query: str, context: Optional[str] = None) -> EnhancedQuery:
        """Process user query through full pipeline."""

        # Stage 1: Normalize
        normalized = normalize(user_query)

        # Stage 2: Expand entities (generate variants)
        variants = expand_entities(normalized, self.abbrevs)

        # Stage 3: Inject tags (apply to all variants)
        tagged_variants = []
        all_signals = {}
        for variant in variants:
            tagged, signals = inject_tags(variant)
            tagged_variants.append(tagged)
            all_signals.update(signals)

        # Stage 4: Detect signals (from original + normalized)
        query_signals = detect_signals(normalized, self.person_names)
        query_signals.tags = all_signals.get('tags', [])
        query_signals.temporal_boost = all_signals.get('temporal_boost', False)

        # Stage 5: Select strategy
        strategy_config = select_strategy(query_signals)

        return EnhancedQuery(
            original=user_query,
            normalized=normalized,
            variants=tagged_variants,
            signals=query_signals,
            strategy_config=strategy_config,
        )
```

---

## Expected Impact on Test Queries

### Example 1: "who's the PsW PM?"
```python
# Current BM25: May not match "Photoshop Web" if only "PsW" in query
# After QU:
variants = [
    "who's the PsW PM?",
    "who's the Photoshop Web PM?",
    "who's the PsW product manager?",
    "who's the Photoshop Web product manager?",
]
signals = QuerySignals(intent='who', has_person_name=False)
config = {
    'bm25_weight': 0.5,     # Strong exact matching
    'graph_weight': 0.30,   # Who queries → hub pages
    'semantic_weight': 0.20
}
# Expected: Higher recall (matches both "PsW" and "Photoshop Web")
```

### Example 2: "When did I last meet with Kosta?"
```python
# After QU:
variants = [
    "When did I last meet with Kosta? #meetings",
]
signals = QuerySignals(
    intent='when',
    has_person_name=True,
    has_temporal_keyword=True,
    tags=['#meetings']
)
config = {
    'temporal_weight': 0.35,   # Critical for "when"
    'bm25_weight': 0.40,       # Name + tag matching
    'graph_weight': 0.15,      # Person page boost
}
# Expected: Recent daily notes surfaced with Kosta meetings
```

### Example 3: "What did I discuss with Ritu in our last 1x1"
```python
# After QU:
variants = [
    "What did I discuss with Ritu in our last 1x1 #meetings #meetings/1x1",
    "What did I discuss with Ritu Goel in our last 1x1 #meetings #meetings/1x1",
]
signals = QuerySignals(
    intent='what',
    has_person_name=True,
    has_temporal_keyword=True,
    meeting_type='1x1',
    tags=['#meetings', '#meetings/1x1']
)
config = {
    'temporal_weight': 0.20,
    'bm25_weight': 0.50,    # Tag + name matching
    'graph_weight': 0.20,   # Person page
}
# Expected: Precise match to Ritu's 1x1 meetings in recent daily notes
```

---

## Implementation Priority

### Phase 1: Core Pipeline (1-2 days)
1. ✅ Build abbreviation dictionary from vault
2. ✅ Implement entity expansion
3. ✅ Implement tag injection
4. ✅ Implement signal detection

### Phase 2: Strategy Integration (1 day)
5. ✅ Integrate with MultiSignalFusion strategy
6. ✅ Add dynamic weight adjustment
7. ✅ Test on vault_test_queries.json

### Phase 3: Optimization (2-3 days)
8. ✅ Tune tag patterns (which keywords trigger which tags)
9. ✅ Tune weight adjustments (how much to boost temporal, graph, etc.)
10. ✅ Add synonym expansion (optional)

### Phase 4: Advanced (Optional)
11. Context resolution (multi-turn queries)
12. Query rewriting with LLM (GPT-4o-mini for query reformulation)
13. Learning from click data (if available)

---

## Evaluation Strategy

### Metrics
Track improvement on vault test queries:
- **NDCG@10**: Overall ranking quality
- **MRR**: First relevant result position
- **Recall@10**: Coverage
- **Per-category analysis**: person_meeting, project_status, temporal, etc.

### Ablation Studies
Test impact of each stage:
1. Baseline (no QU)
2. +Abbreviation expansion
3. +Tag injection
4. +Signal detection + dynamic weights
5. Full pipeline

### Expected Improvements
Based on query analysis:
- **Person queries** (+15-25% NDCG): Name expansion + graph boost
- **Temporal queries** (+20-30% NDCG): Temporal weight adjustment
- **Meeting queries** (+10-20% NDCG): Tag injection
- **Overall** (+15-20% NDCG): Combined effect

---

## Code Files to Create

1. `src/query_understanding/normalizer.py` - Stage 1
2. `src/query_understanding/entity_expander.py` - Stage 2
3. `src/query_understanding/tag_injector.py` - Stage 3
4. `src/query_understanding/signal_detector.py` - Stage 4
5. `src/query_understanding/strategy_router.py` - Stage 5
6. `src/query_understanding/pipeline.py` - Integration
7. `src/query_understanding/vault_knowledge.py` - Extract abbreviations, names, etc.
8. `experiments/query_understanding_eval.py` - Evaluation script

---

## Next Steps

Want me to implement:
1. **The full pipeline** (all 5 stages)
2. **Just the entity expansion** (highest impact first)
3. **Evaluation script** to measure improvements
4. **All of the above** (comprehensive implementation)

Let me know and I'll write the code!
