---
version: "37"
pageType: claudeResearch
---

This file provides guidance to Claude Code (claude.ai/code) when working with this vault.

**Version Management**: Increment the value of the existing `version` property in the frontmatter each time you edit this document.

## Vault Overview

Personal knowledge management vault for a tech professional working on AI/ML products at Adobe, focused on search, recommendations, and content understanding systems.

## Workflow Principles

- **Search first**: Always use smart search before other approaches
- **Agents for complexity**: Use specialized agents for domain-specific tasks
- **Token efficiency**: Smart search returns excerpts, not full content
- **Read selectively**: Use Read tool on specific files from search results

## Key MCP Commands

MCP Tools Reference: @Claude Artifacts/Memory/MCP-Tools-Reference.md

## Vault Structure

### Core Directories
- **Notes/Periodic Notes/Daily Notes/**: Daily work logs (format: "Month DD, YYYY.md")
- **Notes/Programs/**: Major SDC programs (Intent AI, Lightroom, Recommendations, etc.)
- **People/**: Contact info and working notes about colleagues
- **Clippings/**: AI-generated web clippings requiring post-processing
  - **Clippings/Work/**: Work-related wiki pages and technical documentation
  - **Clippings/Personal/**: Personal articles and reference material
- **Archive/**: Historical projects and completed workstreams
- **Templates/**: Note templates for consistent formatting
- **Claude Artifacts/research/**: Research reports and analysis documents
- **.claude/agents/**: Agent definition files for specialized workflows

### Key Content Areas
- **SDC Programs**: Intent AI, Lightroom, Recommendations systems
- **Query Understanding**: NER & SRL, multi-language support
- **Style Understanding**: Typography, design system work
- **Product Work**: Adobe Express, Photoshop, Lightroom integration

## Daily Notes Structure

Daily notes follow this template:
```markdown
---
pageType: daily
aliases:
  - "{{date:YYYY-MM-DD}}"
created: "{{Date: YYYY-MM-DD}}"
---
# [[{{date: MMMM DD, YYYY}}]]
# Notes
---


# Meetings 
---

```

- **H1 title**: Page title with wikilink to itself in "Month DD, YYYY" format
- **Notes section**: Personal working notes for the day  
- **Meetings section**: Meeting notes with H2 headings ending in #meetings tags
- **Meeting tags**: Use #meetings or #meetings/1x1 for one-on-one meetings


## Heading Hierarchy & Organizational Structure

**Critical Rule**: Headings provide logical hierarchy and context. Preserve this structure when editing.

**Structure**:
- **H1**: Major sections (e.g., "Notes", "Meetings")
- **H2**: Sub-topics within H1 context (e.g., "Team Standup #meetings", "John Smith 1x1 #meetings/1x1")
- **Content**: Inherits the context of its heading

**Daily Notes Hierarchy**:
```markdown
# Notes
---
[Personal working notes]

# Meetings
---

## Team Standup #meetings
[Meeting content]

## John Smith 1x1 #meetings/1x1
[1:1 meeting content]
```

**Editing Rules**:
- Maintain logical organization - don't move content between sections
- Each meeting keeps its own H2 heading
- Content under "Meetings" stays meeting-related

## Linking Guidelines

**WikiLink Patterns**:
- Over-link rather than under-link for better navigation
- Link key topics: [[Evaluation]], [[Query Understanding]], [[Intent AI Home]], [[Lr Home]], [[Recommendations Home]], [[Style Home]]
- Link people by name to their dedicated person pages

**Tagging Rules**:
- Main tags pluralized: `#meetings` not `#meeting`
- Sub-tags singular: `#meetings/1x1`
- Avoid `#oldtags` sub-tags

## Hub-and-Spoke Organization

### Intersectional Topics

When a topic sits at the intersection of Product × Surface × Workstream (e.g., "Photoshop Web Recommendations" = Photoshop × Web × Recommendations):

**Create dedicated page when 2+ criteria met**:
- Different stakeholders/PMs
- Different timelines (>6 months apart)
- Different parent programs
- Content would exceed 300 lines per sub-topic

**Consolidation Rule**: Keep sub-topics under one hub until:
- Sections exceed ~300 lines each
- Independent lifecycles emerge (different launch dates, stakeholders)
- Different success criteria or PRDs

**Structure**:
- Canonical page as single source of truth
- Cross-link from all parent hubs using display text
- Use Related Pages frontmatter for bidirectional discovery
- Comprehensive aliases cover all team terminology

### Frontmatter for Intersection Pages

```yaml
---
created: "YYYY-MM-DD"
pageType: misc
tags:
  - claude
aliases:
  - [Canonical Name]
  - [All team terminology variations]
  - [Abbreviations and shortcuts]
  - [Historical names]
Related Pages:
  - "[[Parent Program Hub]]"
  - "[[Product Hub]]"
  - "[[Technology/Service]]"
---
```

### Link Display Strategy

**Context-dependent linking**:
- **In program hubs**: Use formal display text → `[[Page Name|Display Text]]`
- **In daily notes**: Auto-resolve via aliases → `[[shorthand]]`
- **Meeting headers**: Use team's preferred abbreviation

**Example**: `[[Photoshop Web]]` resolves to "Photoshop Web Recommendations" page via aliases

## File Handling Rules

**Tool Usage**:
- Always use Read tool before Edit (MCP tools don't satisfy this requirement)
- Prefer Read/Edit/Write over MCP tools for file modifications

**Formatting**:
- Add line separator (---) under H1 headings
- Use Title Case for all headings (H1-H6)
- Follow linking patterns: link concepts to existing pages (e.g., "evaluation" → [[Evaluation]])
- Never link to claude.md

**File Operations** (Never without permission):
- Move or rename files (breaks Obsidian linking)
- Delete files

**Creating New Content**:
- Include frontmatter: `pageType`, `created: "YYYY-MM-DD"`, `tags: [claude]`
- Use ISO8601 date format (YYYY-MM-DD)
- Over-link rather than under-link
- Use "Claude Misc Note Template" from Templates/ for miscellaneous notes
- Save research reports in Claude Artifacts/research/ with `pageType: claudeResearch`

**Writing Concise Wiki Pages (Start Small)**:
- **Default to minimal scope**: Start with the essentials only (problem, core requirements, basic success criteria)
- **No speculative details**: Omit implementation specifics, edge cases, technical architecture, or items that "might be useful"
- **User-driven expansion**: Wait for explicit requests to add depth (open questions, detailed workflows, examples, etc.)
- **Why this approach**: Users can quickly copy/paste lean specs into mockups, presentations, or implementation docs without editing down excess content
- **Guideline**: If a section isn't essential for immediate action, it belongs in a follow-up conversation, not the initial page

**Protected Files** (`protected: true`):
- Never delete (ask user to delete via Obsidian UI)
- Ask before major edits (>few lines)
- Examples: Intent AI Home, Lr Home, Recommendations Home

## Search Strategy

### Discovery Approach
1. **Start with smart search** to identify topic areas
2. **Follow wikilinks** from search results
3. **Use semantic browsing** for cross-connections

### When to Use Each Method

**Smart Search (search_vault_smart)** - Default for almost everything:
- **What it is**: Custom RAG system with multi-signal ranking (semantic + keyword + graph + temporal)
- **How it works**:
  - Semantic search via EmbeddingGemma embeddings (understands concepts)
  - BM25 keyword matching (finds exact terms and abbreviations)
  - Graph analysis (prioritizes hub pages and well-connected notes)
  - Temporal boosting (surfaces recent notes for "status" queries)
  - Query expansion (uses aliases to find "PS Web" when you search "photoshop")
- **What it returns**: 200-char excerpts from top 20 results (very token efficient: ~1,000 tokens)
- **Best for**:
  - Initial discovery and exploration
  - Conceptual queries ("what's the status of...", "who's working on...")
  - Time-based searches ("recent notes about X")
  - Finding daily notes with current information
  - Unknown locations or broad topics
- **Token efficiency**: 97.5% reduction vs full content (40,000 → 1,000 tokens)

**Simple Search (search_vault_simple)** - Avoid in most cases:
- **What it is**: Basic keyword search that returns full surrounding context
- **WARNING**: Can return 50,000+ tokens and overload context window
- **ONLY use for**:
  - Exact phrase matching when you know the precise text
  - Finding specific URLs or unique identifiers
  - Locating exact error messages or code snippets
- **When you must use it**: Set `contextLength` ≤ 100 to prevent token overload
- **Avoid for**: General exploration, person names, topic discovery, status queries

**Grep Tool** - For file pattern searches:
- Searching within known file patterns (e.g., "*.md", "Daily Notes/**")
- Finding specific code patterns or technical terms
- Use `output_mode: "files_with_matches"` first, then read specific files
- More token efficient than simple search for keyword queries

**Wikilink Traversal**:
- Exploring established relationships
- Understanding context from known starting points
- Following connections between related notes

### Token Efficiency Rules
- **Always use smart search first** - It's designed for token efficiency
- **Avoid simple search** unless you need exact phrase matching
- **Use Grep** for file pattern searches, not simple search
- **Smart search advantages**:
  - Returns excerpts (200 chars) instead of full content
  - Limits to 20 results by default
  - Multi-signal ranking finds the right notes faster
  - Query expansion catches abbreviations and aliases
- **If you need more context**: Use Read tool on specific files from smart search results

### Query Formulation Best Practices

**Trust the ranking algorithm**:
- Always read top 3-5 results first, even if lower results appear more relevant
- Multi-signal ranking (semantic + BM25 + graph + temporal) is optimized for this vault
- Don't cherry-pick results based on surface patterns (e.g., visible meeting headers)
- The ranker considers recency, semantic relevance, and graph connections

**Keep queries simple and direct**:
- ✅ **Good**: "Brian", "Brian 1x1", "Lr Agent status"
- ❌ **Avoid**: "Brian meeting conversation" (mixed concepts dilute signals)
- Simple queries let each signal (semantic, keyword, temporal) work effectively

**For person searches**:
- Use person name directly: "Brian", "Ritu Goel", "Hao"
- Or with meeting tag: "Brian #meetings/1x1"
- Graph expansion finds notes linking to person pages automatically
- Person pages have high PageRank and serve as graph expansion seeds

**For status/recent information**:
- "X project status" → semantic finds hub, temporal boosts recent daily notes
- "recent Y" → temporal signal surfaces newest mentions
- Graph expansion includes daily notes linking to hub pages

**For structured queries**:
- Tag filters work well: "Ritu staff #meetings", "Intent AI #meetings"
- Query expansion uses aliases ("PS Web" finds "Photoshop Web Recommendations")

## Research Artifacts Workflow

### Creation
- **Location**: Save research artifacts in `claude artifacts/research/`
	- Save only research reports in this directory
- **Frontmatter**: Include `pageType: claudeResearch`, `tags: #claude`, and `created: "YYYY-MM-DD"`
- **Cross-linking**: Link to/from current day's daily note

## Web Clipping Workflow

**Overview**: Clippings created via Obsidian web clipper + Google Gemini 2.5 Flash lack vault context and need cleanup.

**Storage**:
- Clippings/Work/ - Work wikis and technical docs
- Clippings/Personal/ - Personal articles and reference material

**Post-Clipping Cleanup** (think: editor reviewing another writer):

1. **Terminology Alignment**
   - Replace generic terms with vault-specific terminology
   - Update misidentified people, products, concepts to match vault usage

2. **Link Creation**
   - Convert plain text to wikilinks (e.g., "query understanding" → [[Query Understanding]])
   - Link people to their person pages
   - Link to program hubs and key topics (over-link preferred)

3. **Quality Checks**
   - Verify frontmatter has appropriate tags and metadata
   - Ensure accurate representation of source material
   - Confirm consistent vault terminology

**Integration**:
- Cross-reference with related pages (hubs, daily notes)
- Add links to relevant hub pages
- Update related pages if clipping contains important information

**When to Use**: Invoke **web-clipping-curator** agent:
- "Clean up today's clippings"
- "Integrate recent web clippings"
- "Process clippings from [date]"

## Specialized Agents
This vault uses specialized agents for complex workflows with intelligent orchestration for optimal efficiency.
### Agent Coordination Patterns

**Simple Tasks (Direct Routing)**
Single agent handles request end-to-end:
- Vault health checks → obsidian-vault-maintainer
- Content search → Use existing search tools directly
- Task creation → task-master

**Complex Workflows (Orchestrated)**
- **Request Analysis**: Categorizes tasks by complexity and scope
- **Agent Selection**: Routes to appropriate specialist or coordinates multi-agent workflows
- **Context Management**: Maintains session state and prevents duplicate operations
- **Resource Optimization**: Applies token efficiency patterns across all agents
### Quick Agent Reference

**vault-synthesizer**: Create unified summaries from scattered vault content
- *Invoke*: "Synthesize all notes on [topic]", "Create overview of [subject]"
- *Limits*: 150k input, 3k output

**obsidian-vault-maintainer**: Health checks, cleanup, organization
- *Invoke*: "Clean up broken links", "Standardize formatting", "Organize [folder]"  
- *Limits*: 30 file operations per session

**knowledge-graph-architect**: Analyze relationships, create meaningful links
- *Invoke*: "Map note relationships", "Find missing connections", "Link related concepts"
- *Limits*: 20 link operations per session

**web-clipping-curator**: Clean up and integrate AI-generated web clippings
- *Invoke*: "Clean up today's clippings", "Integrate recent web clippings", "Process clippings from [date]"
- *Purpose*: Aligns terminology, creates wikilinks, integrates with hub pages

### Agent Selection Logic

| Task Type         | Agent Route               | Example                            |
| ----------------- | ------------------------- | ---------------------------------- |
| Search/Query      | Direct tools              | "Find notes about X"               |
| Content Analysis  | vault-synthesizer         | "Summarize research on Y"          |
| Vault Issues      | obsidian-vault-maintainer | "Fix broken links"                 |
| Note Connections  | knowledge-graph-architect | "Link related concepts"            |
| Clipping Cleanup  | web-clipping-curator      | "Clean up today's clippings"       |
| Complex Workflow  | Multi-agent pipeline      | "Research + synthesize + organize" |
## Token Efficiency 

All agents follow established efficiency patterns:
- **Parallel Operations**: Mix search types in single messages
- **Targeted Searches**: Lexical for precision, semantic for exploration
- **Context Compression**: Pass summaries between agents, not full content
- **Batch Processing**: Group related operations for optimal resource usage
### Context Handoffs

When agents collaborate:
- **Results + Metadata**: Agents pass processed results, not raw content
- **Relevance Scores**: Help subsequent agents focus efforts
- **Change Tracking**: Monitor what was modified to prevent conflicts
- **Compressed Context**: Maintain session state efficiently
### Usage Guidelines

**Task Classification**:
1. **Read-Only Analysis**: Use existing search tools directly
2. **Content Creation**: vault-synthesizer for synthesis tasks
3. **Organization**: obsidian-vault-maintainer for structural changes
4. **Relationship Building**: knowledge-graph-architect for linking
5. **Clipping Integration**: web-clipping-curator for AI-generated web clippings
6. **External Integration**: task-master for Things3 workflows
