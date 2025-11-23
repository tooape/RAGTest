---
created: 2025-10-31
pageType: claudeResearch
tags:
  - claude
datelink: "[[October 31, 2025]]"
Related Pages:
  - "[[Intent AI Home]]"
  - "[[Lr Home]]"
  - "[[Recommendations Home]]"
  - "[[Query Understanding]]"
  - "[[Photoshop]]"
  - "[[Style Home]]"
---
# September 2025 Monthly Summary
---

## Overview

September 2025 marked the transition from planning to execution for [[Intent AI Home|CKG 4.0]] productionization, with concrete roadmaps emerging for Q4 priorities. The month focused on [[Query Understanding]] architecture, [[Style Home|photo styles]] development, and laying groundwork for FY26 planning.

**Key Dates**: 22 working days (Sep 3-5, 8-12, 15, 17-19, 22-26, 29-30)

## Major Workstreams

### 1. CKG 4.0 & Intent Productionization

**Q4 Planning** (Sep 4, 8, 23, 25, 29-30):
- [[CKG4 productionization planning]] wiki created
- Clarified [[Intent AI Home|CKG]] 3.5 is now KTLO (keep the lights on)
- First use case: [[Acrobat|DC]] [[Recommendations Home|contextual recs]] (~20k concepts)
- [[Intent AI Home|MINT]]v2 confirmed compatible with [[CKG 4.0]]
- Tooling for fast graph modifications to be hardened

**Intent Q4 Prioritization** (Sep 4, 8):
1. P0 Asset [[Core Affinity Framework|Affinity]] L2/L3 (M3) - [[Ayush Jaiswal|Ayush]]/[[Mayank Poddar|Mayank]]
2. P0 Sub prompt logic productionalization - Harha/Arvind/[[Josep]]
3. P0 [[NER & SRL|SRL]] with Sept 30th deadline - Umang/Yuchen
4. P0 Intent action - Suhas (Discovery Agent important to [[Ritu Goel|Ritu]])
5. P1 [[Intent AI Home|CKG]] 4.0 + Better Intent Understanding - [[Anshul Omar|Anshul]]
6. P2 Graph cleanup and testing for current use cases

**Three Swimlanes Defined** (Sep 29):
1. **CKG4 prod ready** (2-3 people)
2. **Query Understanding closure** (5 components: [[SLM]], [[Query Understanding|CAF]], Asset Affinity, Topic Extraction, [[NER & SRL|SRL]])
3. **MM model for [[Intent AI Home|CKG]]**

**Grounding & Tooling** (Sep 30):
- [[Subhajit]] created knowledge graph grounding demo with CODEX KG and t-SNE plot
- Need for step-by-step visualization: Input → [[Intent AI Home|MINT]] → [[Intent AI Home|CKG]]
- [[Intent AI Home|MINT]] needs /explain or debug mode (grounded, top 5 ungrounded, associations)

**Scaling Challenges** (Sep 22):
- Vipul pushed on graph scaling speed: How to add camera types for [[Lr Home|Lr]] in days/weeks vs months
- For new use cases: Collect extraneous concepts, change metadata/edges, add new data fast

### 2. Photo Styles

**Development Workflow** (Sep 3, 18, 22):
- **Training**: 10-20k photos, sync one edit from dimension list, export with filename append
- **Triplets**: Neutral composition, create 3 edited differently, sync across 20-30 others
- **Tag refinements**: Added photo-specific vernacular, film stock examples, Kelvin values
- Simplified grain to High/Med/Low (removed rough vs smooth as too technical)
- Removed "digital noise" (synonymous with grain)

**Style Re-ranking Challenges** (Sep 17, 22):
- Issue: [[Recommendations Home|Contextual recs]] with large recall set ranked by [[Style Home|style]] showed stylistically similar irrelevant results
- Need high precision ranker to cut recall set before [[Style Home|style]] ranking
- No interpretable relevance score currently available
- [[Express]] last asset reference: Jira ticket for sending last added asset as [[Style Home|style]] reference (affects only style, not collections)

**Canonical Style** (Sep 24):
- Discussions with Josh on canonical [[Style Home|style]] approach
- [[Maya Davis|Maya]] providing cleaned up tags list
- Running dummy examples against triplets set for spot checking

**Concerns** (Sep 22):
- Struggling to index STILL
- Running out of hope for [[Style Home|photo styles]] (concerning for SDC)

### 3. Photoshop Web Recommendations

**Planning** (Sep 3, 5, 11):
- **Goals**:
  - Prove SDC can recommend entities beyond stock content
  - Show canvas understanding sufficient for novice user recommendations
  - Demonstrable, not putting user on rails
  - Get deeper into product vs quick completion
- **Recommendation types**:
  - Presets with custom values based on image understanding
  - Atomic edits with recommended values
  - Subject auto-select (darken background, brighten subject, blur background)
  - Gen fill recommendations for empty canvas
- Working within [[Lr Home|Lr]] edit panel framework
- Differentiate PoC (port of old [[Lr Home|Lr]] approach) vs actual implementation

**Timeline** (Sep 11):
- [[Hao Xu|Hao]] OOO Oct 1-11
- Mid-October POC start date
- [[Recommendations Home|Recs]] sub-agent approach: [[Font recs]], tool recs (brushes)

### 4. Lightroom

**CAT vs MINT Decision** (Sep 5, 10):
- CAT looks better but 3x more expensive than [[Intent AI Home|MINT]]
- [[Ritu Goel|Ritu]]'s answer: Just index CAT and move on
- Cost formalization with [[Lr Home|Lr]] team needed

**Relevance Issues** (Sep 11, 30):
- AdobeOne embedding relevance issues (6 Jira tickets tracked)
- Recall is biggest issue
- Only change deliverable by MAX: Bump static threshold (0.25 → 0.26/0.275)
- Query strategy overview page created by [[Chayakanta Dash|Chayakanta]]

**Metadata NER Training** (Sep 24):
- Shooting settings: Need list of known values from prod index
- Equipment: Camera model, lens model
- Challenge: Different variations ("mk2", "mk II", etc.)
- Training model/LoRA head on Mistral 7B / Llama 1B
- Focal length support: Oz buckets, adding to uberfield

**Prod Readiness** (Sep 30):
- Not ready for [[October 10, 2025]]
- CAT slow to scale (5-10 min for new containers)
- Ops long pole: ServiceNow, CSO and DR plans, NewRelic
- Perf/latency testing done by [[October 03, 2025]]

**Agent Work** (Sep 5, 9):
- Part of Ps agent strategy
- MCP exposing metadata and tools (including semantic search)
- Context challenges over 1k images
- Might want different search for MCP than user search

**UXR Questions** (Sep 11):
- Query behavior patterns (single words vs phrases vs metadata)
- Relevance expectations
- Workflow integration
- Failure recovery strategies
- Cross-catalog search needs
- Autocomplete's role in semantic search
- Acute issues around compositional queries and semantic vs exact metadata matching

### 5. Query Understanding

**QU Roadshow Planning** (Sep 8):
- Take QU slides from pt3 product summit deck
- Expand with complexity examples
- SRL examples ("my XYZ", etc.)
- Show: What's possible now, what's in Q4, what's TBD
- Add second level of depth
- Explain relevance not lemmatization

**Product Documentation** (Sep 8, 22):
- Goal: Product docs on prompt processing and QU broadly
- Present to other PMs in other teams
- Wiki page to cover:
  - Readable overview of capability
  - Prod/stage availability
  - Generic vs use case specific capabilities
  - Link to repo/tech wiki with endpoint info

**Affinity Work** (Sep 22):
- Express-specific fine tuning for 5 classes
- Ensure endpoints called out for availability
- [[Core Affinity Framework|CAF]] wiki updates

**Broader Evaluation** (Sep 29):
- [[Vipul Dalal|Vipul]] wants evaluation beyond [[Express]]/[[Acrobat|DC]]
- Targets for next week's review:
  1. Discovery Agent v2 POC - Sameep Solanki
  2. [[Acrobat|Acrobat]] Studio [[Recommendations Home|Unified search]] - [[Ravi]]

**Concerns** (Sep 17):
- Little concrete direction on QU and agents
- [[Ayush Jaiswal|Ayush]] writing intent white paper
- [[Jayant Kumar|Jayant]] doing [[Intent AI Home|CKG]] white paper
- Need scope for action intent/affinity in white papers

### 6. LionBridge Golden Dataset

**Planning** (Sep 29):
- Budget: 30k samples to divide
- Components:
  - Product surface
  - Use cases: [[Recommendations Home|Unified search]], Agents, MCP
  - Tasks: [[NER & SRL|SRL]], Topic extraction, Asset [[Core Affinity Framework|affinity]], [[NER & SRL|NER]], [[Query Understanding|CAF]]
- LionBridge will groom/hand-check generated datasets
- Need clear instructions and 5-10 examples for annotation

### 7. SRL Development

**Model Progress** (Sep 12, 24):
- SRL model evals V3
- Base model: Llama 3.2 1B
- Fine-tune adapter for [[Acrobat|DC]]
- Contribution model: Self-serve with tooling from SDC team
- LoRA adapters approach
- SRL not responsible for sub-prompt, won't predict asset name
- Creates filters instead
- [[Asim Kadav|Asim]]'s nomic embeddings duplicative of SRL, hybrid approach OK

**Testing** (Sep 12):
- Cannot test graph without inference
- Need to test both graph and inference together

### 8. Enterprise & Personalization

**Enterprise Recommendations** (Sep 5, 10, 17):
- "Just fire a 2nd query" approach
- [[Lr Home|Lr]], [[Firefly|FF]] past creations, [[Express]] → unified index
- [[Brian Eriksson|Brian]]'s P0: Enterprise [[Recommendations Home|contextual recs]]
- Relevance without enriching assets challenging

**Personalization** (Sep 10):
- [[Personalization Home|Personalization]] has fracture link deployed
- Method to eval exists but hard to visualize
- [[Josep]] has demo

### 9. Discovery Agent & Tools

**Discovery Guidance** (Sep 19):
- Rhut taking over discovery guidance

**Brian's Corpus Understanding Demo** (Sep 24):
- Bringing in [[Intent AI Home|CKG]] knowledge
- Additional signal from corpus
- Layer in [[Style Home|style]] and personalization
- Goal: Ps as art tutor ("you're too formal, try abstracted colors", "add foreground interest")

### 10. APS & FY26 Planning

**APS Prep** (Sep 8):
- Start PgM doc
- Big bets: CKG4, Agentic stuff
- Organize by segments (C-Pro, etc) or surfaces ([[Photoshop|Ps Web]], etc.)
- SDC Pillars perspective: Unified, Contextual, Agentic
- POV on tech in uber use case sense
- SVP review: [[December 07, 2025]]

**Program Overview** (Sep 23):
- Need "do or die" top 3 must-nails for each program
- [[Recommendations Home|Recs]]: Combine lists, call out optimizations (deboost unused recs, text handling)

### 11. DC Contextual Recommendations

**Use Case** (Sep 10, 22, 29):
- Wiki page created
- Selected as first [[Intent AI Home|CKG]] 4.0 use case (text-heavy, little multimodal, ~20k concepts)
- Barley communicating with DC team
- Unknown use cases
- Don't want to own poor outcomes
- Can't help with text processing
- Leaning in as much as possible

### 12. MAX Preparation

**Materials** (Sep 12):
- Slides for booth/stage folks (don't have deep knowledge)
- [[Peter Baust|Peter]] coordination

## Key Meetings & Decisions

### Strategic Decisions
- **CKG 3.5 → KTLO**: No more contributions to 3.5, focus on 4.0
- **First CKG4 use case**: [[Acrobat|DC]] [[Recommendations Home|contextual recs]] (text-heavy, 20k concepts)
- **CAT for Lr**: Despite 3x cost, decision to index CAT
- **Three swimlanes**: CKG4 prod ready, QU closure, MM model

### Important 1x1s
- **[[Ritu Goel|Ritu]]** (Sep 5, 8, 15, 17, 22): APS, CKG4 productionization, DC concerns, style challenges, QU direction, GPU asks
- **[[Brian Eriksson|Brian]]** (Sep 3, 10, 17, 24): Style disambiguation, CKG associations quality, enterprise recs, corpus understanding demo, P0 priorities
- **[[Kosta Blank|Kosta]]** (Sep 8, 18, 30): Contribution model, intent focus, CKG 3.5 fatigue, graph tooling needs, eval buy-in
- **[[Ayush Jaiswal|Ayush]]** (Sep 12, 24): SRL model evals, LoRA contribution model, graph testing, meeting restructuring
- **[[Tracy King|Tracy]]** (Sep 17): CKG4 evaluation, QU white papers, Express home redesign, style re-ranking

## Action Items & Progress

### Completed
- Intent Q4 prioritization finalized
- Three swimlanes defined
- LionBridge 30k sample allocation
- [[CKG4 productionization planning]] wiki created
- Photo styles tag refinements
- SRL model V3 evals
- Query strategy overview page (Chayakanta)

### In Progress
- APS PgM doc development
- QU product documentation
- Photo styles training data generation
- [[Photoshop|PS Web]] recs POC prep
- Enterprise recs strategy
- [[Lr Home|Lr]] perf/latency testing

### Pending from September
- Graph browser and search tooling
- [[Intent AI Home|MINT]] /explain debug mode
- Style canonical approach finalization
- QU roadshow materials
- Broader CKG4 evaluation plan
- Graph scaling speed improvements

## Key Metrics & Data

**LionBridge Allocation**: 30k samples total (breakdown TBD)

**Intent Priorities**: 6 levels (2 P0s, 1 P0?, 1 P1, 1 P2)

**CKG4 First Use Case**: ~20k concepts for [[Acrobat|DC]] [[Recommendations Home|contextual recs]]

**[[Lr Home|Lr]] Relevance**: Static threshold adjustment (0.25 → 0.26+)

**APS Timeline**: SVP review [[December 07, 2025]]

## People & Collaboration

**Frequent Collaborators**:
- [[Ritu Goel|Ritu]] - Strategic direction, APS, prioritization
- [[Brian Eriksson|Brian]] - Engineering partnership, P0 alignment
- [[Kosta Blank|Kosta]] - Intent/CKG leadership, productionization
- [[Ayush Jaiswal|Ayush]] - SRL, contribution model, evals
- [[Tracy King|Tracy]] - CKG architecture, QU scope
- [[Jayant Kumar|Jayant]] - CKG white paper
- [[Maya Davis|Maya]] - Photo styles tags and testing

**New Collaborations**:
- [[Umang Bista|Umang]] - Former CPF, DC and video understanding
- [[Chayakanta Dash|Chayakanta]] - [[Lr Home|Lr]] query strategy
- [[Subhajit]] - KG grounding demo
- [[Vic Chen|Vic]] - Contextual recs style ranking

## Technical Highlights

### Innovations
1. **Photo styles training workflow** - Systematic approach to dimension-based training
2. **[[CKG 4.0]] three-swimlane architecture** - Clear separation of concerns
3. **LoRA contribution model** - Self-serve approach for use case teams
4. **Knowledge graph grounding demo** - t-SNE visualization by [[Subhajit]]

### Technical Challenges
- [[Lr Home|Lr]] AdobeOne embedding relevance (6 Jira tickets)
- Style re-ranking without interpretable relevance scores
- CAT scaling latency (5-10 min for new containers)
- Graph modification speed for new use cases
- Testing graph without inference coupling

## Cross-Links to Daily Notes

**Week 1** (Sep 3-5):
- [[September 03, 2025]] - Photo styles sets, [[Photoshop|PS Web]] action recs
- [[September 04, 2025]] - Intent Q4 planning, productionization questions
- [[September 05, 2025]] - [[Umang Bista|Umang]] intro, CAT vs MINT decision, enterprise content

**Week 2** (Sep 8-12):
- [[September 08, 2025]] - Intent prioritization, QU roadshow, APS prep
- [[September 09, 2025]] - [[Lr Home|Lr]] agent, semantic search in LrD, photography styles
- [[September 10, 2025]] - CAT for [[Lr Home|Lr]], style sign off, [[Personalization Home|personalization]]
- [[September 11, 2025]] - AdobeOne relevance issues, [[Photoshop|PS Web]] recs, [[Lr Home|Lr]] UXR
- [[September 12, 2025]] - MAX slides, SRL evals V3, graph testing

**Week 3** (Sep 15, 17-19):
- [[September 15, 2025]] - [[Ritu Goel|Ritu]] on style roadmap, [[Lr Home|Lr]] monthly review
- [[September 17, 2025]] - CKG4 evaluation, QU white papers, enterprise recs P0
- [[September 18, 2025]] - Photo style annotations, CKG 3.5 fatigue, intent white paper
- [[September 19, 2025]] - Rhut taking discovery guidance

**Week 4** (Sep 22-26):
- [[September 22, 2025]] - QU checkin, graph scaling, DC concerns, style challenges
- [[September 23, 2025]] - Program Q4 overview, CKG4/MINT planning
- [[September 24, 2025]] - SRL golden set, [[Lr Home|Lr]] metadata NER, corpus understanding demo
- [[September 25, 2025]] - CKG 4.0 plan Q&A, MINTv2 clarifications
- [[September 26, 2025]] - Austin trip

**Week 5** (Sep 29-30):
- [[September 29, 2025]] - LionBridge golden dataset, three swimlanes, broader evals
- [[September 30, 2025]] - KG grounding demo, [[Lr Home|Lr]] roadmap, [[Intent AI Home|MINT]] tooling needs

## Notes & Observations

### Recurring Themes
1. **Productionization pressure** - Moving from R&D to production systems
2. **Evaluation complexity** - Need for broader, more systematic evaluation
3. **Tooling gaps** - Graph browser, debug modes, visualization needs
4. **Cost vs quality tradeoffs** - CAT 3x cost but better results
5. **Communication challenges** - DC team, cross-team alignment

### Opportunities Identified
- Graph scaling speed improvements
- Self-serve LoRA contribution model
- Corpus understanding for creative tutoring
- Cross-catalog search in [[Lr Home|Lr]]
- Autocomplete integration with semantic search

### Risks & Concerns
- Photo styles may not materialize (SDC concern)
- Little concrete direction on QU and agents
- DC team communication issues
- Graph modification speed inadequate
- CAT scaling latency issues

### Transition Points
- **From CKG 3.5 to 4.0**: Clear KTLO declaration
- **From planning to execution**: Q4 priorities locked
- **From broad to focused**: DC recs as first use case

## Looking Ahead to October

**Immediate Priorities**:
1. [[CKG 4.0]] productionization plan completion
2. LionBridge golden dataset finalization
3. [[Photoshop|PS Web]] recs POC kick off (mid-month)
4. [[Lr Home|Lr]] prod readiness (ops, perf testing)
5. APS PgM doc development

**Key Milestones**:
- [[October 03, 2025]] - [[Lr Home|Lr]] perf/latency testing complete
- [[October 10, 2025]] - [[Lr Home|Lr]] GA target (won't make it)
- Mid-October - [[Photoshop|PS Web]] recs POC start

**Open Questions**:
- How to achieve graph modification speed improvements?
- Photo styles viability and path forward?
- Enterprise recs final architecture?
- QU roadshow timing and format?
- Broader CKG4 evaluation strategy beyond DC?
