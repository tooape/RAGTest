---
created: 2025-01-10
pageType: misc
tags:
  - claude
  - vibe-code-project
Related Pages:
  - "[[Smart Connections Enhancement - Custom RAG]]"
  - "[[Personal Knowledge Browser - Cappy]]"
aliases:
  - vibe code projects
  - personal code projects
  - side projects
---
# Code Projects Home
---

Personal vibecode projects - side projects exploring search, knowledge management, and information discovery.

## Active Projects
---

### [[Personal Knowledge Browser - Cappy]]

**Status**: Planning (Started January 2025)

A unified "save for later" system that centralizes bookmarks, watch later lists, and saved content from all platforms into Obsidian, with entity-aware discovery inspired by Tidal's credits browsing.

**Key Features**:
- Centralize YouTube watch later, Twitter bookmarks, Reddit saves, browser bookmarks, etc.
- Entity extraction (people, topics, publications) via LLM
- Tidal-style discovery: Browse content by creator/topic relationships
- Card wall UI for visual browsing
- Obsidian plugin for discovery and search

**Tech Stack**: Browser extension (or fork Obsidian Clipper), Obsidian plugin, LLM entity extraction, existing RAG backend

**Next Steps**: Scoping questions, evaluate Obsidian Clipper extensibility, prototype entity extraction

## Completed Projects
---

### [[Smart Connections Enhancement - Custom RAG]]

**Status**: ✅ Phase 1 Complete (October 2025)

Obsidian RAG plugin with hybrid search, graph-aware retrieval, and multi-signal ranking for improved vault discovery. Replaces Smart Connections with better recall for daily notes and temporal content.

**Key Achievements**:
- **EmbeddingGemma @ 256d**: 78% better MRR than BGE, 66% storage reduction via Matryoshka optimization
- **Multi-signal ranking**: Semantic + BM25 + Graph (PageRank) + Temporal with RRF fusion
- **Graph expansion**: Finds daily notes via backlinks to canonical pages (3-5x candidate set expansion)
- **Token efficiency**: 200-char excerpts reduce Claude integration cost by 97.5% (40K → 1K tokens)
- **Sub-100ms queries**: Actual latency ~40-50ms on M4 Pro

**Tech Stack**: Python backend (FastAPI, EmbeddingGemma), TypeScript Obsidian plugin, MiniSearch (BM25), graphology (PageRank)

**Repository**: https://github.com/tooape/obsidianrag (`/Users/rmanor/obsidianrag/`)

**Phase 2 Options**: Contextual Retrieval, GraphRAG with LLM entities, or Evaluation framework

## Common Themes
---

**Search & Discovery**:
- Semantic search (embeddings, RAG)
- Multi-signal ranking (semantic + keyword + graph + temporal)
- Entity-based discovery (people, topics, relationships)
- Graph-aware retrieval (backlinks, PageRank, clustering)

**Knowledge Management**:
- Obsidian as platform (wikilinks, graph, markdown)
- LLM-powered enrichment (summaries, entity extraction)
- Token efficiency for AI integration
- Personal vault as single source of truth

**Tech Stack Patterns**:
- Python backends for ML (embeddings, LLMs)
- TypeScript for Obsidian plugins
- Local-first processing (privacy, offline capability)
- API integrations (platform data, LLM services)

## Potential Future Projects
---

**Ideas to Explore**:
- GraphRAG for Obsidian (LLM-extracted knowledge graph + hierarchical clustering)
- Evaluation framework for RAG quality (ground truth labeling, automated metrics)
- Multi-vault semantic search (search across personal + work vaults)
- Contextual retrieval for long notes (heading-aware chunking)
- Mobile-first knowledge capture (voice notes, photo OCR, quick clips)
- Social graph extraction (meeting notes → org chart understanding)

## Resources
---

**Related Vault Concepts**:
- [[Evaluation]] - Testing methodologies from Adobe work
- [[Query Understanding]] - Entity extraction, NER concepts
- [[Recommendations Home]] - Discovery algorithms
- [[Intent AI Home]] - Knowledge graphs

**External Inspiration**:
- [MyMind](https://mymind.com) - Visual bookmarking
- [Fabric](https://fabric.so) - Personal internet library  
- [Tidal](https://tidal.com) - Music credits browsing
- [Microsoft GraphRAG](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)
- [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

**Technical References**:
- [Obsidian Plugin API](https://docs.obsidian.md/Plugins/Getting+started/Build+a+plugin)
- [Obsidian Web Clipper](https://github.com/obsidianmd/obsidian-clipper)
- [EmbeddingGemma](https://huggingface.co/google/embeddinggemma-300m)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [[Anthropic – AI prompt engineering A deep dive]]
