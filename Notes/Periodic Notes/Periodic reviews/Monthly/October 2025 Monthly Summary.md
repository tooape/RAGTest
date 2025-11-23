---
created: 2025-10-31
pageType: claudeResearch
tags:
  - claude
  - reviews/monthlyReview
datelink: "[[October 31, 2025]]"
Related Pages:
  - "[[Intent AI Home]]"
  - "[[Lr Home]]"
  - "[[Recommendations Home]]"
  - "[[Query Understanding]]"
  - "[[Photoshop]]"
---
# October 2025 Monthly Summary
---

## Overview

October 2025 was a pivotal month focused on productionizing [[Intent AI Home|CKG4]], advancing [[Query Understanding]] capabilities, and planning FY26 initiatives. The month culminated with [[Adobe MAX 2025]] and consideration of a potential organizational restructuring and management role.

**Key Dates**: 23 working days (Oct 1-3, 6-10, 13-17, 20-24, 26-28, 30-31)

## Major Workstreams

### 1. CKG 4.0 & Intent AI

**Graph Readiness & Evaluation** (Oct 1, 6-8):
- Established three-tier node classification system for [[CKG 4.0]]:
  - **Tier 1**: Adobe Ecosystem (filters, [[Core Affinity Framework|affinity]], actions)
  - **Tier 2**: Top 20-25k concepts (locations, topics, objects, events, colors)
  - **Tier 3**: Rest of graph
- Defined deliverables: prod-ready graph, tooling (node/edge management, visualizer), and evals
- [[Vipul Dalal|Vipul]]'s feedback on [[Query Understanding|QU]] swimlanes (Oct 14)
- Graph browser launched by [[Asim Kadav|Asim]] (Oct 24)

**Contributor Model & Tooling** (Oct 1, 7-8):
- Developed contributor flow requirements
- Need for opinionated rules document to maintain graph integrity
- Emphasis on strong ownership of cross-use-case graph consistency
- Separate [[Intent AI Home|CKG]] from intent as distinct workstream (retro feedback)

**Team Changes**:
- [[Kosta Blank|Kosta]] transitioning from intent to [[Recommendations Home|recommendations]] (Oct 24)

### 2. Query Understanding

**Swimlane Structure** (Oct 13-15):
- Swimlane 1: Clear
- Swimlane 2: Close out [[SLM]] modeling efforts, move to longer-term foundational work
- Swimlane 3: [[Multimodal intent]] detection, grounding to graph

**Evaluation & Data** (Oct 20, 23):
- Finalized LionBridge annotation allocation: 30k total queries
  - Subprompt extraction: 6,500
  - Semantic intents/topics: 6,000
  - [[NER & SRL|SRL]]: 6,500
  - Asset Affinity: 2,500
  - Core Affinity: 4,000
  - Intent Actions: 4,500
- Cross-surface evaluation strategy discussions
- Coverage analysis needed: DC deep search, Lr autotagger/CAT, Stock vs [[Intent AI Home|CKG]] coverage

**Alignment Issues** (Oct 23):
- Misalignment between leadership on specialization vs platform approach
- Need for clearer distinction between foundational model vs point solutions
- MLE voice needs to come through more strongly

### 3. Lightroom

**Semantic Search** (Oct 2, 9-10, 22-23):
- Multi-file name search broken (Oct 2)
- User feedback from [[Benjamin Warde]] highlighting issues (Oct 9):
  - Good overall performance but edge cases with query disambiguation
  - People labeling integration working well
  - Video indexing needed (use poster frame, not middle/first)
- GA target for web, desktop rollout, possibly mobile

**2026 Roadmap** (Oct 9, 13, 23):
- Triple MAU: 35M → 100M (free + paid)
- Increase [[Firefly|GenAI]] credits usage
- **Specific asks**:
  1. Embedding improvements (RAE, mobile clip, matryoshka comparisons, fine-tuning)
  2. Camera and lens [[NER & SRL|NER]]
  3. Location and people search
  4. Single word improvements (RRF with CAT?)
- **New features**: Location view, Highlights view (Q1 lab project)
- Language support needed for search
- Agentic search demo video shared (Oct 10)

**Photo Styles** (Oct 22-23, 28):
- Canonical style examples identified from triplet set
- Using GPT-5 as judge for evaluation
- Creating 100-250 neutral images with variations per style dimension
- V1 target: January

### 4. Recommendations

**DC Contextual Recs** (Oct 1, 8, 15):
- Deployed new intent system to production (pending legal review)
- Legal sign-off in progress
- Example issue: "Samosa" mapping to "indian curry" instead of proper concept

**Photoshop Web Recs** (Oct 2, 6-7, 16):
- Meeting set for Oct 13
- [[Photoshop|PS Web]] planning for Q1 public launch
- Heads-down development until end of month, evaluation starts Nov 3
- Mid-November kickoff planned
- Rohit obtained API access, needs to export preset data from [[Lr Home|Lr]]

**Enterprise Recs** (Oct 15):
- Decision needed: [[Express]] or [[Photoshop|PS Web]]?
- Need to provide Jeff with [[Lr Home|Lr]] test account credentials

**Express** (Oct 2):
- Asking for better [[Recommendations Home|recs]]
- Question: How much time to back-port [[Acrobat|DC]] work to [[Express]]?

### 5. Multimodal Intent Detection

**Christian's Demo Review** (Oct 14):
- Problem with production [[Intent AI Home|MINT]] model: Averaged embeddings caused "regression-to-mean"
- New LLaVA-based generative architecture:
  - Vision encoder → projection layer → LLM
  - Projected vision tokens bypass text embedding layer
  - Enables true multimodal reasoning vs naive averaging
  - Precision improved from 0.20-0.21 to higher values

### 6. Team & Organizational

**Team Retro** (Oct 7):
- **Wins**: Strong collaboration, client expansion, production progress, leadership alignment
- **Challenges**: Under-resourced, unclear direction, changing priorities, leadership issues, technical challenges
- **Key Takeaways**:
  - SDC written communication needs improvement
  - Better early planning and scoping
  - Hire more people
  - Better feedback loops
  - Clearer POC vs production distinction

**Retro Feedback with Architects** (Oct 8):
- Need triad conversations: architect + PM + team lead/EM
- More rigor on written requirements, decisions, tradeoffs
- Expectation that artifacts are actually read

**Management Consideration** (Oct 31):
- [[Ritu Goel|Ritu]]'s org needs more structure
- Potential to manage: [[Eshan Trivedi|Eshan]] and [[Francois Guerin|Francois]]
- Org would cover: Intent & Language, [[Recommendations Home|Recs]], Disc Guidance, Autocomplete, Evals & relevance
- Might give intent to Rhut for agent/assistant work alignment

### 7. FY26 Planning

**APS** (Oct 6, 9, 17, 31):
- Template development in progress
- One-liners needed for big initiatives:
  1. **C-Pro zone**:
     - [[Lr Home|Lr]] GA
     - Agentic capabilities
     - Semantic search for [[Photoshop|PS]] and Ai
  2. **[[Recommendations Home|Recs]]**:
     - Existing surfaces (multi-lingual, performance)
     - [[Photoshop|PS Web]] recs
- Creating C-Pro capability view for SDC
- [[Lr Home|Lr]] slide completed, [[Photoshop|PS]] slide pending

**Intern Hiring** (Oct 9, 13, 30-31):
- Two start dates: May and June
- Still accepting international students
- Manager commitments: training, weekly 1x1s, event participation
- Evaluation principles: Hire for potential and coachability, avoid bias
- Resume review completed (Oct 30):
  - Liked: Mert, Sean, Maria, Armando, Sophia Gao, Sneha
- Offer target: Before winter shutdown
- Reply sent to recruiter, thinking about project ideas

### 8. Personal Projects: Obsidian RAG Plugin

**Major Development Work** (Oct 26-30):

**Oct 26 - Evaluation & Tag Filtering**:
- Created 23-query ground truth across 7 patterns
- Live plugin evaluation: 37.6% precision, 75.2% recall, 92.4% MRR
- **Critical issue discovered**: Tag filtering completely broken (15% recall for structured queries)
- Fixed tag filtering in QueryParser integration

**Oct 27 - Temporal & Graph Enhancements**:
- Fixed cache persistence (embeddings weren't saving to disk)
- Switched temporal ranking from `mtime` to frontmatter `created` date
- Implemented hybrid temporal strategy: 120-day guaranteed recency coverage
- Fixed chunk-related issues, proper deployment procedures
- Backend startup debugging

**Oct 30 - Memory Optimization & Graph Traversal**:
- Memory analysis: 600MB for EmbeddingGemma-300m
- Optimization options identified: ONNX+int8, lazy loading, FP16
- **Graph traversal for recall** implemented:
  - `getInboundNeighbors()`, `getOutboundNeighbors()`, `expandCandidateSet()`
  - Top-5 semantic results used as seeds
  - Expands to neighbors before multi-signal ranking
  - Configurable: enable/disable, max neighbors (default 15), depth (1 or 2 hops)
- Research documents created:
  - [[Obsidian RAG Memory Optimization - October 2025]]
  - [[Backend Idle Model Unloading - October 2025]]
  - [[Graph Traversal for Recall Enhancement - October 2025]]

### 9. Events

**Adobe MAX 2025** (Oct 28-31):
- Attendance Oct 28
- Followups needed:
  - [[Marc Levoy]]
  - matthew richmond
  - [[Matt Rae]] - roadshow week of [[November 10, 2025]]

## Key Meetings & Decisions

### Strategic Decisions
- **Pilot use case for Intent Testing**: [[Recommendations Home|Contextual recs]] chosen as hero use case (Oct 13)
- **Date [[NER & SRL|NER]] interpretation**: Platform provides "any year", use cases apply specific year constraints (Oct 13)
- **[[Query Understanding]] prioritization**: Focus on coverage and cross-surface capabilities while maintaining use-case specificity

### Important 1x1s
- **[[Ritu Goel|Ritu]]** (Oct 2, 6, 13, 23, 31): APS planning, CKG4 contribution model, [[Photoshop]] planning, [[Query Understanding|QU]] alignment, intern hiring
- **[[Brian Eriksson|Brian]]** (Oct 2, 15, 22, 28): CKG testing, StockFast, [[Style Home|Photo styles]], [[Acrobat|DC]] recs approval
- **[[Subhajit]]** (Oct 1, 7): CKG plan request, retro scope, contributor plan
- **[[Kosta Blank|Kosta]]** (Oct 7, 15, 21): Intent plan, retro, [[Query Understanding|QU]] mission, graph/contributor work
- **[[Asim Kadav|Asim]]** (Oct 7, 24): Intent inference, [[Photoshop|PS Web]] action recs, photo style eval, CKG4 graph browser
- **[[Ayush Jaiswal|Ayush]]** (Oct 8, 22): End-to-end [[Query Understanding|QU]], contribution model, LionBridge allocation

## Action Items & Followups

### Completed
- [x] Reply to intern recruiter (Oct 31)
- [x] [[APS]] slide for [[Lr Home|Lr]] (Oct 31)
- [x] Intern bundle preparation (Oct 31)
- [x] Fixed Obsidian RAG tag filtering (Oct 26)

### Pending from October
- [ ] Think about becoming a manager (Oct 31)
- [ ] MAX followups: [[Marc Levoy]], matthew richmond, [[Matt Rae]] (Oct 31)
- [ ] [[APS]] slide for [[Photoshop|PS]] (Oct 31)
- [ ] Reach out to Katrin and Pei about [[Lr Home|Lr]] at [[MAX 2025]] (Oct 15)
- [ ] Enterprise [[Recommendations Home|recs]] placement decision: [[Express]] vs [[Photoshop|PS Web]]? (Oct 15)
- [ ] Get Jeff credentials for [[Lr Home|Lr]] test account (Oct 15)
- [ ] What is grounding mechanism and post-processing? Ask [[Asim Kadav|Asim]] (Oct 16)
- [ ] Look at LionBridge wiki, talk to [[Jay Manish Sampat|Jay]] about enterprise [[Express]] thing (Oct 22)
- [ ] Language support in Search (Oct 23)
- [ ] [[Query Understanding|QU]] roadshow for [[Lr Home|Lr]] Agent (Oct 23)
- [ ] Create slide/document outlining foundational model vs point solutions for [[Query Understanding|QU]] (Oct 23)
- [ ] Coverage analysis: Run all DC/Lr/Stock tags through [[Intent AI Home|CKG]] (Oct 23)
- [ ] [[Intent AI Home|CKG]] 3.5/4.0 coverage in offline intent set analysis (Oct 23)

### Ongoing Work Items
- Graph work: Manual offline job for filterable fields
- Topic [[Evaluation]] for [[Intent AI Home|CKG]]
- Create wiki page for [[Lr Home|Lr]] embedding models, test queries, problem cases
- Better query list for semantic topic extraction (DC/[[Firefly|FF]] prompts)
- [[Photoshop|PS Web]] recs kickoff mid-November
- Obsidian RAG performance optimization

## Key Metrics & Data

**LionBridge Annotation Allocation**: 30k queries
- Subprompt: 6,500
- Semantic intents: 6,000
- [[NER & SRL|SRL]]: 6,500
- Asset Affinity: 2,500
- Core Affinity: 4,000
- Intent Actions: 4,500

**[[Lr Home|Lr]] 2026 Goals**:
- Triple MAU: 35M → 100M
- Increase [[Firefly|GenAI]] credit usage

**Obsidian RAG Performance** (Oct 26):
- Precision@20: 37.6%
- Recall@20: 75.2%
- MRR: 92.4%
- Failed queries: 4/23 (17%)

## People & Collaboration

**Frequent Collaborators**:
- [[Ritu Goel|Ritu]] - Strategic direction, [[APS]], org planning
- [[Brian Eriksson|Brian]] - Engineering partnership, technical decisions
- [[Asim Kadav|Asim]] - Intent inference, multimodal, tooling
- [[Kosta Blank|Kosta]] - Intent/[[Query Understanding|QU]] work (transitioning)
- [[Subhajit]] - Graph validation, contributor model
- [[Ayush Jaiswal|Ayush]] - [[Query Understanding|QU]], [[NER & SRL|SRL]], subprompt
- [[Jayant Kumar|Jayant]] - Intent architecture, evaluation
- [[Tracy King|Tracy]] - CKG graph design, tooling requirements

**New Connections**:
- [[Benjamin Warde]] - [[Lr Home|Lr]] semantic search feedback
- Intern candidates for 2026

## Technical Highlights

### Innovations
1. **[[Intent AI Home|CKG]] three-tier system** - Clear prioritization framework
2. **Multimodal intent architecture** - LLaVA-based approach vs embedding averaging
3. **Graph traversal for RAG recall** - Bidirectional expansion for daily notes discovery
4. **Temporal ranking strategy** - 120-day guaranteed coverage, frontmatter-based

### Technical Debt & Issues
- Multi-file name search in [[Lr Home|Lr]] (Oct 2)
- [[Style Home|Style]] embeddings for icons/design assets not indexed (Oct 2)
- Obsidian RAG tag filtering (fixed Oct 26)
- Backend startup reliability (Oct 28)

## Cross-Links to Daily Notes

**Week 1** (Oct 1-3):
- [[October 01, 2025]] - CKG testing goals, Vipul's CKG plan request
- [[October 02, 2025]] - [[Lr Home|Lr]] bugs, [[Photoshop]] meeting scheduled
- [[October 03, 2025]] - [[Style Home|Photo styles]] system prompt with [[Maya Davis|Maya]]

**Week 2** (Oct 6-10):
- [[October 06, 2025]] - [[Query Understanding]] checkin, [[APS]] planning
- [[October 07, 2025]] - Team retro, swimlane discussions
- [[October 08, 2025]] - CKG4 eval deliverables, retro feedback
- [[October 09, 2025]] - [[Lr Home|Lr]] & SDC 2026 planning, intern program
- [[October 10, 2025]] - [[Lr Home|Lr]] video indexing, agentic demo

**Week 3** (Oct 13-17):
- [[October 13, 2025]] - Intent swimlanes, internship commitment
- [[October 14, 2025]] - [[Vipul Dalal|Vipul]]'s [[Query Understanding|QU]] feedback, multimodal demo
- [[October 15, 2025]] - Action items, [[Brian Eriksson|Brian]] 1x1
- [[October 16, 2025]] - [[Photoshop|PS Web]] recs timeline, graph analysis
- [[October 17, 2025]] - [[APS]] document review

**Week 4** (Oct 20-24):
- [[October 20, 2025]] - LionBridge allocation, [[Query Understanding]] checkin
- [[October 21, 2025]] - [[Kosta Blank|Kosta]] on [[Query Understanding|QU]] legitimacy
- [[October 22, 2025]] - [[Lr Home|Lr]] ships, photo styles
- [[October 23, 2025]] - Coverage analysis tasks, [[RAG Enhancement Techniques - Reranking and Contextual Retrieval|RAG research]]
- [[October 24, 2025]] - [[Kosta Blank|Kosta]] role transition, graph browser

**Week 5** (Oct 26-28, 30-31):
- [[October 26, 2025]] - RAG app testing, live plugin evaluation
- [[October 27, 2025]] - Cache persistence fix, temporal/graph enhancements
- [[October 28, 2025]] - [[Adobe MAX 2025]], photo styles, backend debugging
- [[October 30, 2025]] - Intern resumes, memory optimization, graph traversal
- [[October 31, 2025]] - Management consideration, MAX followups, [[FY2026 APS]]

## Notes & Observations

### Recurring Themes
1. **Alignment challenges** - Repeated discussions about platform vs specialized approaches
2. **Evaluation complexity** - Balancing use-case specific vs cross-surface evaluation
3. **Resource constraints** - Team under-resourced, hiring needed
4. **Tooling gaps** - Graph browser, contributor tools, debugging capabilities

### Opportunities Identified
- StockFast for semantic search on Stock (Oct 17)
- Community search for [[Lr Home|Lr]] (lower priority)
- Agentic workflows for [[Lr Home|Lr]] photo selection

### Risks & Concerns
- Leadership alignment on [[Query Understanding]] direction unclear
- Changing priorities creating churn
- Requirements often architect-driven vs product-driven
- Coverage expectations vs evaluation constraints

### Personal Growth
- Deep technical work on Obsidian RAG (personal project)
- Consideration of management track
- Strategic thinking on FY26 planning

## Looking Ahead to November

**Immediate Priorities**:
1. MAX followups (Marc Levoy, matthew richmond, Matt Rae)
2. Management decision
3. [[Photoshop|PS Web]] recs kickoff (mid-month)
4. [[Query Understanding|QU]] roadshow for [[Lr Home|Lr]] Agent
5. [[APS]] finalization

**Key Milestones**:
- [[November 10, 2025]] - Matt Rae roadshow week
- Mid-November - [[Photoshop|PS Web]] recs kickoff

**Open Questions**:
- Management role acceptance?
- How to improve leadership alignment on [[Query Understanding]]?
- Enterprise recs placement decision
- Coverage analysis methodology
