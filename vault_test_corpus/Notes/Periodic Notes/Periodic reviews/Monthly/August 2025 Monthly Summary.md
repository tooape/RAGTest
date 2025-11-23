---
created: "2025-10-31"
pageType: claudeResearch
tags:
  - claude
datelink: "[[October 31, 2025]]"
Related Pages:
  - "[[Intent AI Home]]"
  - "[[Lr Home]]"
  - "[[Recommendations Home]]"
  - "[[Query Understanding]]"
  - "[[Style Home]]"
---
# August 2025 Monthly Summary
---

## Overview

August 2025 focused on establishing foundations for Q4 and FY26 work: [[NER & SRL|SRL]] models reaching production readiness, [[Style Home|photo styles]] roadmap development, and critical organizational decisions about product directions. The month marked the beginning of serious [[Intent AI Home|CKG]] 4.0 discussions and the emergence of agentic workflows as a key theme.

**Key Dates**: 24 working days (Aug 1-8, 10-15, 17-22, 25-28)

## Major Workstreams

### 1. SRL & Query Understanding

**Model Development** (Aug 4-5):
- [[NER & SRL|SRL]] V1.1 deployed with baseline accuracy computed on golden set
- Finalized prompt for generation of training & [[Evaluation|eval]] data
- ~2M rows created with Llama, each creating 3-4 variations → 8M total for training
- Base model decision: Using Llama approach
- V1.1 PoC essentially complete

**Requirements Clarification** (Aug 4-5):
- **Name fields decision**: Rely on client to resolve `@alias` to hexID for [[NER & SRL|SRL]] consumption
- Keep plain text names for internal testing/validation only
- [[Acrobat|DC]] no longer needs semantic/natural language search for Sept release
- Still planning to demo these capabilities

**Challenges** (Aug 4):
- [[NER & SRL|SRL]] PRD thin on detail/examples
- Asset name requirements unclear (file extension? just words?)
- Clarifications coming from informal conversations with Umang, Jay, Tracy
- Getting training data easier than figuring out what to train *for*
- Alignment between use cases and training goals
- Umang perceives Yu Chen and [[Ayush Jaiswal|Ayush]] involvement as turf war

**SRL Architecture** (Aug 4):
- 1-shot approach: Inferring on full query string
- Not leveraging [[NER & SRL|NER]] (e.g., not using people name NER for author names)

**ILUP Integration** (Aug 5):
- API changes required for new global SRL types
- Post-processing moving to [[ILUP]]
- Discovery Hub integration work ongoing

### 2. Intent Action & Core Affinity

**Intent Action Progress** (Aug 4):
- V0 LoRA trained and deployed
- Added to Llama 321B
- Selected 20 tools/actions from 29 available
- 92.5% classification accuracy on single action prediction
- Golden eval set: 500 manually verified samples (Suhas)
- Still need parameter extraction for actions

**[[Core Affinity Framework]] Results** (Aug 5):
- Leaderboard shows significant outperformance vs base models
- Beating GPT-4 mini across various tasks and query lengths
- Early but promising results

### 3. Golden Datasets & Evaluation

**Unified Strategy** (Aug 4):
- [Unified SLM Evaluation Strategy](https://wiki.corp.adobe.com/display/adobesearch/Unified+SLM+Evaluation+Strategy) created
- [Golden datasets](https://wiki.corp.adobe.com/display/adobesearch/Intent+Golden+Datasets) for [[SLM]] [[Evaluation|eval]] established
- New unified wiki for golden datasets with human-verified data and statistics
- Allows comparison between training and golden sets
- Suhas working on unified dashboard

**Multi-Label Tracking** (Aug 4):
- Challenges discussed
- Need precision, recall, F1 metrics for each class

**Data Set Issues** (Aug 4):
- Queries too verbose
- Need to focus on P0 fields
- Preparing new simplified data set for improved accuracy
- Underrepresented samples need addressing
- Weekly progress tracking required

**Asset Affinity** (Aug 4):
- Creating golden eval set
- Addressing shorter query issues
- Plan to include more content queries and retrain model
- [[Express]] use case prioritized

### 4. Photo Styles

**Roadmap Established** (Aug 6):
- [[Style Home|Photo styles]] confirmed as next focus
- More complex than icons/design assets due to richness

**Two-Layer Training Approach** (Aug 6):
- **Technical Layer**:
  - Aspect ratio
  - [[Style Home|Color]] vs B/W
  - Exposure (brightness, contrast)
  - [[Style Home|Color]] (temperature, saturation, tone)
  - Texture & noise
  - Blur (motion blur, depth of field)
- **Compositional Layer**:
  - Composition types (rule of 3rds, 5ths, golden ratio, golden spiral, diagonals, center, frame within frame)
  - Subject placement

**Wikis Created** (Aug 6):
- Aesthetics model documentation
- Style understanding frameworks

### 5. Style Understanding Challenges

**Relevance vs Style Balance** (Aug 4, 6):
- Great directional [[Style Home|style]] understanding achieved
- Problem: Stock recall so long for queries that relevance tanks
- Can't always calculate recall size
- Computing recall offline for all [[Intent AI Home|CKG]] intents

**Next Steps** (Aug 4):
- Getting relevance/recall worked out for topically relevant results
- Path to prod challenges:
  - [[Express]] [[Recommendations Home|contextual recs]] was hero use case but relationship poor
  - [[Vic Chen|Vic]] remains interested but power diminished
  - [[Photoshop]] interested but early, may not have DAU needed
  - [[pdf2pres]] may be best near-term route to prod

### 6. Lightroom

**Agentic Search** (Aug 6):
- Max = PM for creative assistant
- Jeffry Andrew = right contact
- **Current feature**: "Dynamic sky" in pre-release (AI agent decides sky needs and executes)
- **Next feature**: "Suggested edits" (generative preset recommendations)
- **Organizational agent**: Culling on import and catalog management

**Analytics** (Aug 6):
- [[Lr Home|Lr]] team outlined [spec in Amplitude](https://app.amplitude.com/analytics/adobe/dashboard/6be35a0y)
- Key questions:
  - What is token remove?
  - What is search session?
  - When is something an iteration search?
- Missing: Position clicked, AssetID
- Data flow: Captured → Databricks → cleaned/migrated → Redshift or S3
- Dashboard in PowerBI
- Need mock data in Databricks to start dashboarding work
- Clarifying actual rollout with Sanchit and client team

### 7. DC Contextual Recommendations

**AMA Leads Meeting** (Aug 6):
- Not re-using I2A model from [[Express]] agent
- Internal beta: Aug 20th
- Key to Sept release

**Multi-Language** (Aug 6):
- Short term: [[AdobeOne V2]] or machine translation
- Long term: [[Intent AI Home|MINT]]

### 8. pdf2pres & MAX Preparation

**pdf2pres** (Aug 6):
- Mainstage at MAX25
- Takes wall of text PDF doc → "image + text column" slide deck
- Want stylistic similarity across slides
- Opportunity for [[Style Home|style]] integration

### 9. Photoshop Web

**Tool Recs Discussion** (Aug 6):
- Vipul's premise: Different tool recs for foreground vs background asset selection
- [[Ritu Goel|Ritu]]'s concerns:
  - Relationship between clicks and tools is thin
  - Can we actually learn this?
  - Is this unique value for SDC/Ps?
  - Do creators want this?

### 10. Personal & Organizational Development

**Vault Organizational Audit** (Aug 3):
- Conducted comprehensive audit with Claude Code
- [[Vault Organizational Audit - August 2025]] created
- **Key Findings**:
  - Daily note centralization optimal for PM workflows
  - Strong program-centric architecture
  - Advanced linking and discovery capabilities
  - Opportunities for cross-program intelligence synthesis
- **Strategic next steps**:
  - Maintain: Daily note approach, program home architecture, linking framework
  - Evolve: Cross-program intelligence, meeting outcome tracking, enhanced navigation
  - Revolutionary changes not recommended - architecture highly effective

**July 2025 Overview** (Aug 3):
- Created retrospective for previous month

**Agentic Prompting Learning** (Aug 3):
- Using heuristics (budgets, general practices, "how would you tell an intern")
- Tool definition (clearly explain which tasks need which tools, explicit principles)
- Using thinking (prompt agent to use thinking well, interleaved tool calls)
- Loop management ("keep searching until" causes spinning, use "if you don't find perfect source, move on")
- Context window management (compaction, external memory, subagents for compression)

**Interview Process** (Aug 5):
- Alex Hu principal PM interview
- Evaluation methodology discussions
- Ethics and safety considerations
- Metrics identification (clicks, MAU, returning users, thumbs up/down, corpus coverage)
- Influence strategies (showing risk and opportunity, leadership escalation)

### 11. Deployment & Infrastructure

**Pipeline Development** (Aug 4):
- Working on automating training/deployment pipeline for faster iterations
- Need robust pipeline with quality gates
- Multi-version comparison capability
- MintV2 deployment includes latest SRL model and intent action
- Integrating latest [[Intent AI Home|CKG]] release
- Goal: Multiple deployments per week
- AB testing for model version comparison

### 12. Amazon Search Lessons Learned

**Subhajit's Talk** (Aug 6):

**Context & Personalization**:
- Heavy emphasis on context building before processing queries
- Location, language preferences, user history
- Long-term memory (multi-year purchase history) vs working memory (current session)
- Recently shifted to personalizing search based on past purchases
- Challenge: Representing history for downstream systems (raw IDs vs detailed info, payload size vs latency)
- Uses RAG to filter user history based on current queries

**Autocomplete**:
- Unified model for on-focus and prefix-based suggestions
- Candidate generation → ranking
- Maximize user acceptance rates
- Key metrics: offer rate, acceptance rate
- Sub-10ms latency constraints
- Bandit optimization problem - poor training quickly degrades performance

**Query Understanding**:
- Query specificity measured using click entropy
- Broad queries: high entropy, 4+ products
- Specific queries: concentrate on 1-2 products
- Query-to-category affinities using multiple taxonomies (like Adobe's [[Core Affinity Framework|CAF]])
- [[NER & SRL|NER]] uses weakly-labeled + human-labeled data with span identification
- CRF-based extractors

**Matching & Behavioral Signals**:
- Lexical matching on product metadata
- Keyword stuffing challenges → catalog cleanup projects
- Behavioral signals: stored purchase logs (sparsity challenging)
- Query reformulations, order-independent matching
- Significant investments in semantic matching (bi-encoder models)
- Experimental side-loading stack for rapid experimentation
- Future: integrate semantic with ranking, simplify architecture

## Key Meetings & Decisions

### Strategic Decisions
- **SRL name fields**: Client resolves `@alias` to hexID approach
- **Photo styles two-layer training**: Technical + compositional
- **Best path to prod for style**: [[pdf2pres]] over [[Express]]/[[Photoshop]]
- **Deployment pipeline**: Focus on automation for multiple weekly deployments

### Important Meetings
- **[[Query Understanding]] Checkin** (Aug 4): Unified strategy, golden datasets, SRL/Intent Action Sept deadline
- **AI Foundations Program** (Aug 5): SRL V1.1 deployed, [[Core Affinity Framework]] results, ILUP integration
- **[[Recommendations Home|Recs]] Program Sync** (Aug 4): Style eval results, path to prod challenges
- **Subhajit's Search Lessons** (Aug 6): Amazon approach to context, personalization, autocomplete
- **[[Lr Home|Lr]] Agentic Search** (Aug 6): Dynamic sky, suggested edits, organizational agent

### Key 1x1s
- **[[Ayush Jaiswal|Ayush]]** (Aug 4): [[Intent AI Home|CKG]] Alpha 3, QU + Alpha 3, SRL challenges, DC use cases
- **[[Brian Eriksson|Brian]]** (Aug 6): [[Photoshop]] tool recs, pushing [[Style Home|style]] into [[Express]]/[[pdf2pres]]
- **Anuj** (Aug 6): [[Lr Home|Lr]] analytics spec, data architecture

## Action Items & Progress

### Completed
- SRL V1.1 deployed
- Intent Action V0 LoRA trained and deployed
- Unified SLM evaluation strategy created
- Golden datasets established
- Photo styles roadmap defined
- Vault organizational audit completed
- July 2025 overview created

### Key Deliverables
- Unified dashboard (Suhas, ETA: Aug 4)
- New simplified SRL data set (ETA: Wednesday after Aug 5)
- Express golden data set preparation
- End-to-end pipeline automation
- AB testing setup

### Pending
- Parameter extraction for intent actions
- SRL golden set expansion
- Express model evaluation
- [[Lr Home|Lr]] analytics mock data in Databricks
- Rollout clarification with Sanchit

## Key Metrics & Data

**Intent Action**: 92.5% classification accuracy (single action prediction)

**Training Data**: ~8M rows (2M base x 3-4 variations each)

**Golden Set**: 500 manually verified samples (Intent Action)

**Deployment Goal**: Multiple per week with AB testing

**Autocomplete Target**: <10ms latency

## People & Collaboration

**Frequent Collaborators**:
- [[Ayush Jaiswal|Ayush]] - SRL, [[Intent AI Home|CKG]] Alpha 3, QU
- [[Brian Eriksson|Brian]] - Style integration, tool recs
- Suhas - Intent Action, unified dashboard
- Umang - SRL requirements, DC integration
- Yu Chen - SRL development
- [[Subhajit]] - Search lessons, organizational insights
- Anuj - [[Lr Home|Lr]] analytics

**External Insights**:
- Amazon search methodology (via [[Subhajit]]'s talk)

## Technical Highlights

### Innovations
1. **Two-layer photo styles training** - Technical + compositional separation
2. **Unified SLM evaluation strategy** - Cross-model comparison framework
3. **Intent Action LoRA** - 92.5% accuracy, parameter extraction next
4. **Vault organization audit** - Systematic assessment of PM workflow optimization

### Technical Challenges
- SRL PRD clarity and requirements alignment
- Style recall/relevance balance
- Multi-label tracking metrics
- Query verbosity in training data
- Turf war perceptions in SRL team
- Path to prod for photo styles uncertain

### Architecture Decisions
- Client-side `@alias` to hexID resolution
- Post-processing moved to [[ILUP]]
- Automated training/deployment pipeline
- RAG for user history filtering
- Bi-encoder semantic matching

## Cross-Links to Daily Notes

**Week 1** (Aug 1-8):
- [[August 01, 2025]] - (Empty daily note)
- [[August 02, 2025]] - (Empty daily note)
- [[August 03, 2025]] - Vault audit, July overview, agentic prompting learning
- [[August 04, 2025]] - QU checkin, [[Recommendations Home|Recs]] sync, [[Ayush Jaiswal|Ayush]] 1x1
- [[August 05, 2025]] - AI Foundations, Intent sync, SRL requirements, Alex Hu interview
- [[August 06, 2025]] - Photo styles roadmap, [[Lr Home|Lr]] agent, DC AMA, [[Brian Eriksson|Brian]] 1x1, Subhajit's search lessons
- [[August 07, 2025]] - (Likely continued work)
- [[August 08, 2025]] - (Likely continued work)

**Week 2** (Aug 10-15):
- [[August 10, 2025]] - (Empty daily note)
- [[August 11-15, 2025]] - (Content not fully captured in review)

**Week 3** (Aug 17-22):
- [[August 17-22, 2025]] - (Content not fully captured in review)

**Week 4** (Aug 25-28):
- [[August 25-28, 2025]] - (Content not fully captured in review)

## Notes & Observations

### Recurring Themes
1. **Productionization focus** - Moving models from development to deployment
2. **Evaluation rigor** - Golden datasets, unified strategies, metrics frameworks
3. **Cross-team alignment challenges** - Turf wars, unclear requirements, informal clarifications
4. **Path to prod uncertainty** - Multiple potential routes, relationship challenges
5. **Agentic workflows emerging** - [[Lr Home|Lr]] agent, organizational agents, creative assistants

### Opportunities Identified
- [[pdf2pres]] as [[Style Home|style]] integration path
- Automated deployment pipelines for rapid iteration
- [[Lr Home|Lr]] agentic workflows for culling and organization
- Amazon search methodology insights applicable to SDC

### Risks & Concerns
- [[Express]] relationship deteriorated (impact on [[Style Home|style]] rollout)
- SRL PRD lacks detail and examples
- Turf war perceptions on SRL team
- Multi-label evaluation complexity
- [[Photoshop]] too early for meaningful DAU

### Foundation Setting
- **SRL production ready** - V1.1 deployed, training pipeline established
- **Evaluation frameworks** - Unified strategy, golden datasets, leaderboard
- **Photo styles architecture** - Two-layer approach defined
- **Organizational excellence** - Vault audit confirms PM workflow optimization

## Looking Ahead to September

**Immediate Priorities**:
1. SRL golden set expansion and new data prep
2. Intent Action parameter extraction
3. Express model evaluation with golden data
4. Photo styles training execution
5. Automated pipeline completion

**Key Milestones**:
- Aug 20 - DC AMA internal beta
- Sept release - [[NER & SRL|SRL]] and Intent Action critical

**Open Questions**:
- Best path to prod for photo styles?
- How to resolve [[Express]] relationship for [[Style Home|style]] rollout?
- [[Photoshop]] tool recs viability?
- Timeline for [[Lr Home|Lr]] agentic features?
- [[Intent AI Home|CKG]] 4.0 productionization approach?
