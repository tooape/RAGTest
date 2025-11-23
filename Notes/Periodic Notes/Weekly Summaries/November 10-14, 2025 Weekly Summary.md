---
pageType: weekly
created: "2025-11-14"
tags: 
  - claude
  - weeklySummary
aliases:
  - "Week of Nov 10"
  - "Nov 10-14 2025"
---
# November 10-14, 2025 Weekly Summary
---

## Overview

First full week back from leave following marriage. Focused on returning to core initiatives: [[Query Understanding]] (QU) demo work, [[Lr Home|Lightroom]] Desktop planning for 2026, and Q1 planning across products. Conducted 6 internship interviews for 2026 summer cohort.

## Key Initiatives

### [[Query Understanding]] (QU)

**Demo & Interface Work**
- Created [[QU Demo Interface Requirements]] for internal visualization of full QU intelligence outputs (targeting Venkat and Shudakar for review)
- [[NER & SRL]] demo link active for review

**Evaluation & Model Work**
- MM model (swimlane 3) requires formal evaluation strategy
  - Gathering [[express]] templates for eval work
  - Offline eval: stratified 500 templates comparing MM vs MINTv1 (LLM-as-a-judge)
  - Online eval: 100 head templates with side-by-side comparison
- Chat needed with [[Andrei Stefan|Andrei]] and [[Brian Eriksson|Brian]] on swimlane 3 MM evaluation approach

**Adobe Ecosystem Progress**
- [[Anshul Omar|Anshul]] leading unification exercise for big node ingestions
- Tier 1 concepts review with Anshul—need to add [[Intent AI Home|CKG]] service tiering to tracking

### [[Lr Home|Lightroom]] Initiatives

**Agent Kickoff**
- [[Lr Home|Lightroom]] Agent core kickoff meeting completed
- [[Style Home|Style]] understanding work: bounding box approach for overexposed areas

**Reporting & Query Patterns**
- Initial reporting shows strong [[NER & SRL|NER]] performance on dates
- Query patterns: most searches are 1-2 tokens
- `edited` is most popular query—need NER strategy for `edited` and behavioral/culling signals (flags, picks)

**Desktop Language Support Planning**
- Supporting April 2026 launch with 18B assets scope
- Four-tier language support options:
  1. Tier 1: Everything ([[NER & SRL|NER]], embeddings, text)
  2. Everything except [[NER & SRL|NER]]
  3. Everything except [[NER & SRL|NER]] via machine translation (latency cost)
  4. Text match only
- Requested languages: French, German, Spanish, Japanese
- [[Multi-Language 2025|Multi-language]] support via Adobeone expected, [[ILUP]]-side [[NER]] support is an open question

**Semantic Search v2**
- Lightroom Desktop targeting April 2026 release
- Batch processing strategy: offline batching will be faster than real-time (63 days at 10k RPM sync limit in CPF)
- Smart album bug fixes deferred to V3; USS v2 bugs won't be fixed
- Multi-language support scope confirmed

**Dashboard & Technical Work**
- Dashboard presentation: Direct (no filters, keyword only) vs adjust-filter (may/may not have keyword, always has filter)
- Auto-Complete (AC) can use same search index in V3—met with [[Cherag Aroraa|Cherag]] and [[Eshan Trivedi|Eshan]]

**Cost Optimization**
- Cost chat with [[Chhayakanta Padhi|Chhaya]] completed—see [[Lr Home|Lr]] cost optimization guide for details

### [[Style Home|Style]]

- Tracking down Adobe BAM dataset from prior [[behance]] and Adobe Research aesthetic data gathering
- Noted: "no one is on the same page on style"—stakeholder alignment meeting scheduled

### [[Recommendations Home|Recommendations]]

**Photoshop Web (PS Web) Presets**
- Demo staged at http://pr.photoshop.adobe.com/id?PR=70057&flags=acr_presets
- Rohith has demo video available

**Express Design & Icon Recs**
- Design asset/icon [[Style Home|style]] recommendations issue: [[Style Home|style]] isn't persisted to full results list (thumbnail looks good, full results missing signal)

### Q1 2026 Planning

Line of sight reviewed with [[Ritu Goel|Ritu]]. No major new asks. Core planned work:

1. **[[express]]**
   - Auto-Complete (AC) and High-Performance Recommendations (HPR)
   - [[Recommendations Home|Unified search]]

2. **[[Acrobat|Acrobat Studio]]**
   - Relevance improvements for [[Acrobat|DC]] and [[express]] files
   - Natural language support (January release)
   - [[PDF2Pres]] improvements

3. **[[Firefly]] / Moonlight**
   - Generated history semantic search
   - Cloud docs semantic search

4. **[[Lr Home|Lightroom]]**
   - Big bang rollout (April 2026)

### [[APS]] Review

- 2026 deck created
- Key callouts:
  - Contextual discovery for agent
  - Autocomplete rework as part of semantic rollout
  - Need to check on unwanted and preset recommendations v2 status (contact Peter)

## Intern Interview Process

Conducted 6 interviews for [[2026 Summer Internships - Ritu's Team]]:

**Verdicts**:
- Mert Gulsun: ❌ No
- Maria Mora: ✅ Yes
- Sophia Gao: ✅ Yes
- Sean Park: ❌ No (better fit for Subhjait's team)
- Armando: ✅ Yes
- Sneha: ⚠️ Scary (notes indicate concerns; B2B focused, may not be ideal fit)

## People & Leadership

**Feedback for [[Brian Eriksson|Brian]]**
- Doing well: Excellent leader, biased toward action/impact, intentional prioritization
- Do differently: Push more future-facing tech investments now that [[Kosta Blank|Kosta]] is handling day-to-day [[Recommendations Home|recommendations]]
- Overall: Great communicator/collaborator, looking forward to rolling out future bets in [[Style Home|style]] and [[Personalization Home|personalization]] in 2026

**1x1 Highlights**
- [[Asim Kadav|Asim]]: Covered [[Style Home|photo styles]] stakeholder alignment, [[NER & SRL|SRL]] demo, MM model evals
- [[Ayush Jaiswal|Ayush]]: Shifting from modeling work to more generalized approach; golden set for MM swimlane 3 needs validation (use Christian's eval set, not a new one)

## Notes

- [[Personal Knowledge Browser - Cappy]] project mentioned as area of interest
- [[Lr Home|Lightroom]] cost optimization guide now available as resource
- Multi-language implementation strategy for Lightroom Desktop requires cross-functional coordination ([[Adobeone]], [[ILUP]] teams)
