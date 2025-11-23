---
created: " 2025-11-11"
pageType: misc
datelink: "[[November 11, 2025]]"
---

# Loresmirth RAG Architecture Design 

**Document Purpose:** Technical design specification for implementing a GraphRAG-based knowledge retrieval system for a Dungeon Master assistance application.

**Audience:** Product Management, Engineering Lead, Implementation (Claude Code)

**Date:** November 1, 2025

---

## 1. Application Context

**Product:** Dungeon Master assistant application enabling DMs to:

- Upload world knowledge documents (official D&D sourcebooks, campaign notes)
- Maintain persistent knowledge of player and world state across sessions
- Plan and execute sessions with intelligent context retrieval

**Core Challenge:** Balancing static world knowledge with dynamic session-to-session state changes in long-running campaigns (20+ sessions).

---

## 2. Foundational Technology: GraphRAG

**Reference Paper:** Microsoft Research - "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"

**Key Concepts:**

- **Entity extraction:** LLM identifies entities (NPCs, locations, factions, items) and relationships from documents
- **Community detection:** Leiden algorithm clusters related entities into hierarchical communities
- **Community summaries:** LLM-generated summaries at multiple abstraction levels
- **Query-time retrieval:** Relevant communities and entities retrieved based on query semantics

**Known Limitation:** GraphRAG papers do not address incremental updates or operational scaling for dynamic knowledge bases.

---

## 3. Architectural Design

### 3.1 Tiered Knowledge Architecture

We implement a three-tier system with different freshness requirements:

```
┌─────────────────────────────────────────────────────┐
│ Tier 1: World Knowledge (GraphRAG)                  │
│ - D&D sourcebooks, campaign world docs              │
│ - Static/semi-static canonical knowledge            │
│ - Rich entity relationships and community structure │
│ - Periodic rebuild cadence based on impact scoring  │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ Tier 2: World State Changelog                       │
│ - Entity mutations (NPC deaths, location destruction)│
│ - Relationship changes (faction hostility)          │
│ - Overrides/augments GraphRAG at query time        │
│ - Triggers GraphRAG rebuilds based on impact       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ Tier 3: Session Context (Semantic Search)           │
│ - High-velocity session-to-session updates          │
│ - Player actions, combat logs, dialogue             │
│ - Semantic + recency-based retrieval               │
│ - Extracted and structured per session             │
└─────────────────────────────────────────────────────┘
```

**Design Rationale:** Separating static world knowledge from dynamic state changes allows us to avoid expensive GraphRAG rebuilds while maintaining accurate current state.

---

## 4. Session Management & Compaction

### 4.1 Problem Statement

Claude's 200K token context window will be exceeded during long sessions, requiring intelligent compaction to preserve critical information without degradation.

### 4.2 Proactive Compaction Strategy

**Implementation:**

```
Monitor token usage per session:
  - Set threshold at ~150K tokens (before API limit)
  - Trigger custom compaction logic (don't wait for API)
  
At compaction trigger:
  1. Extract structured data across categories
  2. Persist full conversation to storage (retain fidelity)
  3. Start fresh context with extracts + recent messages
```

**Structured Extraction Categories:**

json

```json
{
  "combat_log": {
    "encounters": [...],
    "tactics_used": [...],
    "damage_taken": {...},
    "loot_acquired": [...]
  },
  "npc_interactions": {
    "per_character": {
      "NPC_name": {
        "dialogue_summary": "...",
        "relationship_change": "+/-",
        "promises_made": [...]
      }
    }
  },
  "player_decisions": {
    "major_choices": [...],
    "critical_dice_rolls": [...],
    "quest_progress": {...}
  },
  "inventory_state": {
    "items_gained": [...],
    "items_lost": [...],
    "character_conditions": {...}
  },
  "open_threads": {
    "unresolved_hooks": [...],
    "foreshadowing": [...],
    "suspicious_details": [...]
  }
}
```

**Key Principle:** Custom compaction is a feature we build, not something that happens to us. Original data retained in storage enables re-querying with new questions.

---

## 5. World State Change Management

### 5.1 Changelog Architecture

**Design Decision:** Do NOT mutate GraphRAG directly. Maintain separate world state changelog that overrides GraphRAG at query time.

**Changelog Schema:**

json

````json
{
  "session_id": 12,
  "timestamp": "2025-11-01T14:30:00Z",
  "entity_updates": [
    {
      "entity_id": "tavern-redoak",
      "entity_type": "location",
      "status": "destroyed",
      "metadata": {
        "destroyed_by": ["player_1", "player_2"],
        "method": "fire"
      }
    }
  ],
  "relationship_updates": [
    {
      "from": "party",
      "to": "merchants-guild",
      "relationship_type": "allied",
      "new_status": "hostile",
      "reason": "burned guild-owned property"
    }
  ],
  "new_entities": [
    {
      "entity_id": "ruins-redoak",
      "entity_type": "location",
      "derived_from": "tavern-redoak"
    }
  ]
}
```

**Query-Time Application:**
```
Query: "Where can the party rest?"

1. GraphRAG retrieval: [Red Oak Tavern, Green Dragon Inn, ...]
2. Apply changelog filters: Remove/modify based on state changes
3. Return: [Green Dragon Inn, ...]
```

### 5.2 End-of-Session Pipeline
```
Session ends → Trigger extraction pipeline:

1. Structured session extraction (compactor)
2. World state change extraction (separate prompt):
   "Extract CANONICAL world changes from session:
    - Entity state changes
    - Relationship changes  
    - New entities created
    Format as structured JSON"
    
3. Calculate impact score (see Section 6)
4. Append to changelog
5. Check rebuild threshold
````

---

## 6. Graph Update Heuristics: Impact-Based Rebuilds

### 6.1 Problem Statement

"Rebuild every N sessions" is too arbitrary. Need data-driven approach where burning a random tavern triggers no rebuild, but destroying a holy temple triggers rebuild.

### 6.2 Solution: Graph Centrality-Based Importance Scoring

**Core Insight:** The graph structure itself tells us entity importance. Use network analysis metrics weighted by relationship semantics.

**Entity Importance Calculation:**

python

```python
# Computed at GraphRAG construction time
entity_importance = {
    "entity_id": {
        "degree_centrality": float,      # How many connections
        "betweenness_centrality": float, # How many paths through it
        "pagerank_score": float,         # Weighted PageRank
        "community_level": int,          # Hierarchy level (0=top)
        "doc_frequency": int,            # Mentions across source docs
        "composite_score": float         # Weighted combination
    }
}
```

**Weighted PageRank with Relationship Types:**

GraphRAG extracts typed relationships. We assign importance weights:

python

```python
relationship_weights = {
    "sacred_to": 3.0,          # Religious/cultural significance
    "ruled_by": 2.5,           # Political power structure
    "central_location": 2.0,   # Narrative importance (quest-critical)
    "home_of": 1.5,            # Character connection
    "member_of": 1.5,          # Faction membership
    "contains": 1.0,           # Simple containment
    "visited_once": 0.3,       # Weak/transient connection
    "mentioned_by": 0.5        # Reference without direct connection
}

# PageRank with edge weights
importance_scores = weighted_pagerank(
    graph=G,
    edge_attr='relationship_type',
    weight_map=relationship_weights
)
```

**Composite Importance Score:**

python

````python
composite_score = (
    0.4 * pagerank_score +           # Primary: network importance
    0.3 * betweenness_centrality +   # Path criticality
    0.2 * (1 - community_level/max_level) +  # Hierarchy position
    0.1 * normalized_doc_frequency   # Source document prominence
)
```

**Example Scores:**
```
Holy Temple of Wind God:
  - Degree: 22 connections
  - Betweenness: 0.45 (high)
  - PageRank: 0.89 (high, many "sacred_to" edges)
  - Community Level: 0 (top-level summaries)
  - Doc Frequency: 15 documents
  → Composite Score: 0.89

Random Shitty Tavern:
  - Degree: 1 connection
  - Betweenness: 0.02 (low)
  - PageRank: 0.12 (low, only "contains" edge)
  - Community Level: 3 (low-level detail)
  - Doc Frequency: 1 document
  → Composite Score: 0.12
````

### 6.3 Impact Scoring & Rebuild Triggers

**Change Impact Calculation:**

python

```python
def calculate_change_impact(world_change, entity_importance_index):
    """
    Calculate rebuild impact score for a world state change.
    Returns: impact_score (0-100)
    """
    entity_id = world_change['entity_id']
    change_type = world_change['type']  # destroyed, created, modified
    
    base_importance = entity_importance_index[entity_id]['composite_score']
    
    # Change type multipliers
    type_multipliers = {
        'destroyed': 1.5,      # Removal has higher impact
        'created': 1.0,        # New entities
        'status_changed': 0.8, # Modifications
        'relationship_broken': 1.2,
        'relationship_created': 0.9
    }
    
    multiplier = type_multipliers.get(change_type, 1.0)
    impact_score = base_importance * multiplier * 100
    
    return impact_score
```

**Rebuild Decision Logic:**

python

````python
# Accumulate impact across sessions
cumulative_impact = 0
changes_since_rebuild = []

# After each session
for change in session_world_changes:
    impact = calculate_change_impact(change, entity_importance_index)
    cumulative_impact += impact
    changes_since_rebuild.append(change)
    
# Rebuild thresholds
REBUILD_THRESHOLD = 50  # Tunable based on telemetry
MIN_SESSIONS_BETWEEN_REBUILDS = 3
FORCE_REBUILD_THRESHOLD = 100

if cumulative_impact >= FORCE_REBUILD_THRESHOLD:
    trigger_rebuild(priority='high')
elif cumulative_impact >= REBUILD_THRESHOLD and sessions_since_rebuild >= MIN_SESSIONS_BETWEEN_REBUILDS:
    trigger_rebuild(priority='normal')
else:
    # Continue with changelog approach
    append_to_changelog(session_world_changes)
```

**Rebuild Process:**
```
1. Canonicalize changelog into world state updates
2. Merge with original source documents (mark superseded info)
3. Rebuild GraphRAG:
   - Entity extraction
   - Relationship extraction
   - Community detection (Leiden)
   - Community summarization
   - Recalculate entity importance scores
4. Archive old changelog
5. Start fresh changelog
6. Update entity importance index
````

---

## 7. Query-Time Context Assembly

**Pipeline:**

python

````python
def assemble_context(user_query, session_id):
    """
    Assemble context from all three tiers for LLM request.
    """
    # 1. GraphRAG retrieval (world knowledge)
    graph_communities = graphrag_query(
        query=user_query,
        k_communities=3
    )
    
    # 2. Apply world state changelog
    current_world_state = apply_changelog(
        graph_results=graph_communities,
        changelog=get_active_changelog()
    )
    
    # 3. Semantic search recent sessions
    relevant_sessions = semantic_search(
        query=user_query,
        corpus='session_notes',
        recency_weight=0.3,
        top_k=5
    )
    
    # 4. Entity linking (cross-reference)
    mentioned_entities = extract_entities(user_query)
    entity_context = get_entity_cross_references(
        entities=mentioned_entities,
        sources=['graph', 'changelog', 'sessions']
    )
    
    # 5. Recent session continuity (last 3 sessions by default)
    recent_context = get_recent_sessions(
        session_id=session_id,
        lookback=3
    )
    
    # Assemble final context
    context = {
        'world_knowledge': current_world_state,
        'recent_events': relevant_sessions,
        'entity_details': entity_context,
        'session_continuity': recent_context
    }
    
    return context
```

---

## 8. Implementation Roadmap

### Phase 1: Foundation
1. Implement GraphRAG construction pipeline
   - Entity/relationship extraction from source docs
   - Leiden community detection
   - Community summarization
   - Entity importance scoring (centrality metrics)
2. Basic semantic search for session notes
3. Simple query-time retrieval (GraphRAG only)

### Phase 2: Session Management
1. Token monitoring and proactive compaction
2. Structured extraction pipeline
3. Session-to-session persistence
4. Context assembly with multiple sources

### Phase 3: World State Management
1. Changelog schema and storage
2. World state change extraction
3. Query-time changelog application
4. Impact scoring calculation

### Phase 4: Intelligent Rebuilds
1. Graph centrality computation (PageRank, betweenness)
2. Weighted importance scoring
3. Impact-based rebuild triggers
4. Rebuild pipeline with changelog consolidation

### Phase 5: Optimization & Tuning
1. Telemetry: query latency, rebuild frequency, context accuracy
2. Threshold calibration based on real campaign data
3. Geographic partitioning for very long campaigns
4. Changelog retrieval optimization (vector indexing)

---

## 9. Technical Considerations

### 9.1 Entity Importance Index Storage

Store precomputed scores for fast lookup:
```
{
  "index_version": "graphrag_build_20251101",
  "entities": {
    "entity_id": {
      "name": "Holy Temple of Wind God",
      "type": "location",
      "importance_metrics": {...},
      "composite_score": 0.89
    }
  }
}
```

### 9.2 Changelog Scaling (Long Campaigns)

For campaigns exceeding 20+ sessions with hundreds of changes:

**Option A: Periodic consolidation**
- Every 5-10 sessions, consolidate changelog into GraphRAG rebuild
- Archive old changelog
- Keep only "hot" changes (recent 5 sessions) in fast storage

**Option B: Partitioned retrieval**
- Index changelog in vector DB
- Retrieve relevant changes semantically at query time
- Geographic/entity-based partitioning

**Recommended: Hybrid**
- Hot changes (last 5 sessions): in-memory
- Cold changes (older): retrieval-based when relevant
- Scheduled rebuilds incorporate accumulated changes

### 9.3 Graph Construction Details

**Entity Extraction Prompt Pattern:**
```
Extract entities and relationships from this D&D campaign document:

Entity types: character, location, faction, item, quest, event
Relationship types: ruled_by, sacred_to, member_of, contains, 
                    allied_with, hostile_to, owns, created_by

Output format: structured JSON with entity attributes and typed edges
````

**Community Detection:**

- Use Leiden algorithm (available in igraph, networkx)
- Multi-resolution: detect communities at multiple hierarchy levels
- Recommended resolutions: [0.5, 1.0, 2.0] for 3-level hierarchy

**Relationship Weight Assignment:**

- Can be done via LLM classification: "Rate importance of this relationship: low/medium/high"
- Or rule-based mapping from relationship types

---

## 10. Success Metrics

**System Performance:**

- Query latency: <2s for context assembly
- GraphRAG rebuild time: <5 minutes for typical campaign
- Changelog application overhead: <200ms

**Quality Metrics:**

- Context relevance: DM rating after sessions
- Missed connections: tracking when relevant info wasn't retrieved
- Stale data incidents: queries returning outdated world state

**Operational Metrics:**

- Average rebuild frequency per campaign
- Changelog size at rebuild trigger
- Distribution of entity importance scores

---

## 11. Open Questions & Future Work

1. **Relationship weight tuning:** Initial weights are estimates. Need telemetry to optimize.
2. **Multi-party campaigns:** If multiple parties exist in same world, how to handle divergent world states?
3. **Temporal queries:** "What did we know about the temple before session 10?" Requires time-traveling through changelog.
4. **DM override capability:** UI for manually triggering rebuilds or adjusting entity importance.
5. **Graph visualization:** Tool for DMs to visualize entity relationships and community structure.

---

## 12. References

- **GraphRAG Paper:** Edge, D., et al. (2024). "From Local to Global: A Graph RAG Approach to Query-Focused Summarization." Microsoft Research.
- **Leiden Algorithm:** Traag, V.A., et al. (2019). "From Louvain to Leiden: guaranteeing well-connected communities." Scientific Reports.
- **PageRank:** Page, L., et al. (1999). "The PageRank Citation Ranking: Bringing Order to the Web." Stanford InfoLab.

---

**Document Version:** 1.0  
**Last Updated:** November 1, 2025  
**Authors:** Product Team, Engineering Lead