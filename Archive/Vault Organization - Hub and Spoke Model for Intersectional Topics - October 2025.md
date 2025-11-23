---
pageType: claudeResearch
created: "2025-10-09"
tags:
  - claude
  - vault-organization
  - information-architecture
aliases:
  - Hub and Spoke Organization
  - Intersectional Topics Strategy
---
# Vault Organization: Hub-and-Spoke Model for Intersectional Topics
---

## Executive Summary

This document analyzes the organizational challenge of representing topics that exist at the intersection of multiple dimensions (Product × Surface × Workstream) and proposes a hub-and-spoke model for consistent, scalable information architecture.

**Core Finding**: The hub-and-spoke pattern already exists successfully in parts of the vault. The issue is inconsistent application, not flawed design.

**Key Recommendation**: Create dedicated pages for intersectional topics as canonical sources, with bidirectional cross-links from all parent hubs. Consolidate related sub-topics under one hub until content exceeds ~300 lines or diverges in lifecycle.

---

## Original Request

> I'd like to better structure my vault. The situation i'm running into is that as we spin up projects like PS Web Contextual recommendations I need to represent the intersection of several different areas. 1. being Ps the product 2. the product surface being web (as opposed to the desktop Ps) and 3. the recommendations workstream. What i'm doing now is creating ps web recs as part of my recommendations page as the canonical reference. My thought is to split this out. I'd create a note for Ps Web Recommendaitons which is seperate from Ps or Recs, and then cross link with a mention of ps web recs in both the ps page and the recs page which links to this new ps web recs specific note.
>
> I'd like you to consider the problem, and the approach here. Then I'd like you to analyze my vault for this case and others, like the different query understanding services vs Mint vs CKG getting all jumbled up, and then the different DC use cases etc. See if this approach is workable, and useful. Come back with some general findings and feedback and we'll discuss from there.

---

## The Problem

As programs expand across multiple products and surfaces, we encounter topics that don't fit cleanly into a single category:

### Example Cases

1. **PS Web Recommendations**
   - **Product**: Photoshop
   - **Surface**: Web (vs. Desktop)
   - **Workstream**: Recommendations
   - **Current state**: Minimal stub page, content scattered

2. **Acrobat Use Cases**
   - **Product**: Acrobat/DC
   - **Multiple initiatives**: AMA, Contextual Recs, Unified Search
   - **Current state**: Single page conflating distinct programs with different timelines

3. **Query Understanding Services**
   - **Technology**: MINT/CKG (underlying platform)
   - **Services**: NER, SRL, CAF (built on platform)
   - **Consumption**: Different products use services differently
   - **Current state**: Actually well-structured, but conceptually confusing

### The Question

How should we organize information when topics sit at intersections? Should we:
- Embed within one "primary" parent? (Doesn't scale)
- Duplicate across parents? (Sync issues)
- Create dedicated intersection pages? (Proposed solution)

---

## Current State Analysis

### Successful Patterns Already in Vault

#### Query Understanding Structure ✅
```
Query Understanding.md (programHome, hub)
├── Pre-processing
├── Core Affinity Framework.md (dedicated page)
├── NER & SRL.md (dedicated page)
├── ILUP.md (dedicated page)
└── Intent Understanding (links to Intent AI Home)
```

**Why it works**:
- Clear hierarchy: one program hub
- Services get dedicated pages when substantial
- Each spoke represents distinct service with own lifecycle
- Cross-links maintain discoverability

#### Intent AI Program ✅
```
Intent AI Home.md (programHome, hub)
├── Technology components
│   ├── CKG 4.0
│   ├── SLM
│   └── MINT
└── Referenced by use cases
    ├── Recommendations Home
    ├── Express
    └── Lightroom
```

**Why it works**:
- Technology stack separated from applications
- Use cases link TO the platform
- Clear boundary: tech vs. product integration

#### Style Home ✅
```
Style Home.md (programHome)
├── Technology (CKG/MINT integration)
├── Use cases
│   ├── Lightroom presets
│   ├── DVA video
│   └── PS Web (mentioned)
└── Cross-cutting concerns
```

**Why it works**:
- Represents cross-product capability
- Links to product-specific implementations
- Consolidated view of distributed work

### Problem Patterns

#### Acrobat Studio ⚠️
**Current**: Single page trying to cover:
- Acrobat AMA (September 2025 launch)
- Acrobat Contextual Recs
- DC Studio unified discovery

**Problem**: Conflating distinct initiatives with different:
- Timelines (Sept launch vs. ongoing)
- Stakeholders
- Technical approaches

**Solution**: Split into:
- `Acrobat Studio.md` (product hub)
- `Acrobat Contextual Recommendations.md` (dedicated)
- `Acrobat AMA.md` (dedicated)

#### PS Web Recommendations (Partially Done)
**Current**:
- `Ps web.md` (minimal stub)
- `Ps Web Action Recommendations.md` (separate POC)
- Content scattered across daily notes

**Solution**: See detailed migration plan below

---

## Proposed Model: Hub-and-Spoke

### Three-Tier Hierarchy

```
Program Home (pageType: programHome, protected: true)
  ├── Product/Surface-Specific Implementation
  │     ├── Cross-links to Program Home
  │     ├── Cross-links to Product Hub (if exists)
  │     └── Specific details, contacts, timelines
  └── Technology/Service Components
        ├── Shared infrastructure
        └── Cross-product concerns
```

### Linking Protocol

**Parent Hub** (e.g., Recommendations Home):
```markdown
Recommendations surfaces:
- [[Express]]
  - Search tab & All tabs
- [[Acrobat Contextual Recommendations|Acrobat]] Recommendations
- [[Photoshop Web Recommendations|Photoshop Web]]
```

**Intersection Page** (e.g., Photoshop Web Recommendations):
```markdown
---
aliases:
  - PS Web Recommendations
  - Photoshop Web Recs
  - ps web
  - psw
Related Pages:
  - "[[Recommendations Home]]"
  - "[[Photoshop]]"
  - "[[CKG 4.0]]"
---
# Photoshop Web Recommendations
---

[Detailed content about PS Web specific implementation]

## Contacts
- PM: [[Hao Xu]]
- Slack: [channel link]

## Related Programs
- Parent: [[Recommendations Home]]
- Technology: [[CKG 4.0]], [[Style Home]]
```

### Frontmatter Standards

**Intersection Pages**:
```yaml
---
created: "YYYY-MM-DD"
pageType: misc  # or productSurface if creating new type
tags:
  - claude
aliases:
  - [All variations team uses]
  - [Abbreviations]
  - [Historical names]
Related Pages:
  - "[[Parent Program]]"
  - "[[Product Hub]]"
  - "[[Technology/Service]]"
protected: false  # unless critical
---
```

**Key principles**:
- Comprehensive aliases cover all team terminology
- Related Pages creates bidirectional discoverability
- pageType distinguishes from pure program hubs

---

## Decision Framework: When to Create Dedicated Pages

### Create Separate Page When 2+ Are True

| Criterion | Weight | Example |
|-----------|--------|---------|
| ✅ Different stakeholders/PMs | High | AMA (Jay) vs Recs (Brian) |
| ✅ Different timelines (>6 months apart) | High | Sept launch vs ongoing |
| ✅ Different parent programs | High | Different org chart branches |
| ✅ Different technical approaches | Medium | Different ML models |
| ✅ Would create clutter on parent (>200 lines) | Medium | Content exceeds section |
| ✅ Has 3+ cross-references from different areas | Low | Multiple programs reference it |

**PS Web Recs qualifies**: ✅ Own timeline, ✅ dedicated PM (Hao Xu), ✅ distinct from desktop PS

**Acrobat AMA qualifies**: ✅ September launch, ✅ own PRD, ✅ distinct from contextual recs

### Keep Consolidated When

| Criterion | Indicator |
|-----------|-----------|
| ✅ Same PM/team | Single owner |
| ✅ Similar timeline | Both in 2025, same phase |
| ✅ Same program | Would appear in same slide deck |
| ✅ User views as one offering | Single product capability |
| ✅ Total content < 500 lines | Manageable in one page |

---

## Critical Test Case: PS Web Action vs Content Recs

### The Challenge

Two concepts that share:
- ✅ Same product: Photoshop
- ✅ Same surface: Web
- ✅ Same workstream: Recommendations
- ✅ Same PM: Hao Xu
- ✅ Same program area: SDC Recommendations

But differ on:
- ❌ **Recommendation type**: Content (assets) vs. Actions (tools/workflows)
- ❌ **Use case**: Discovery vs. Workflow acceleration
- ❌ **Timeline**: Different POC phases
- ❌ **Technical approach**: Different models/strategies
- ❌ **User touchpoint**: Different UI surfaces within PS Web

**Question**: Does this merit separate pages or one consolidated hub?

### Analysis

#### Approach 1: Consolidate Under One Hub ✅ Recommended

**Structure**:
```
Photoshop Web Recommendations.md (THE CANONICAL HUB)
├── Content Recommendations
│   └── Contextual asset/template discovery
├── Action Recommendations
│   └── Workflow/tool suggestions POC
└── Future: [Other rec types]
```

**Rationale**:
1. **User mental model**: "What's going on with PS Web Recs?" → One place to look
2. **Shared infrastructure**: Same PM, same program, same stakeholders
3. **Lifecycle flexibility**: POC can succeed (expand section), fail (archive), or spin out (elevate later)
4. **Analogous to Query Understanding**: Different services (NER vs CAF) under one hub

#### Approach 2: Separate Sibling Pages ❌ Not Recommended

**Problems**:
1. Which one links from Recommendations Home? Both creates clutter
2. Where does shared info go (PM contacts, program overview)? Duplication risk
3. Doesn't scale: Future "Template Recs" = 3rd page, fragmentation multiplies

**When this would work**:
- Completely different stakeholders
- Different programs (not just POCs within one program)
- Never discussed together

#### Approach 3: Hub + Sub-pages (Hybrid)

**When appropriate**:
- Both sub-areas are substantial (>200 lines each)
- Different enough to need separate deep-dives
- Still part of one cohesive program

**Current PS Web state**: Not yet at this threshold

### Decision: Consolidate

**Score against framework**:
- Split criteria: 0/5 (same PM, timeline, program, org chart, content < 500 lines)
- Consolidate criteria: 5/5

**Implementation**:
```markdown
# Photoshop Web Recommendations
---

## Overview
[Program description, shared context]

## Content Recommendations
Contextual discovery of assets, templates, and media.
[Details from current "Ps web.md"]

## Action Recommendations
Workflow and tool suggestions to accelerate creation.

### POC Goals
[Content from "Ps Web Action Recommendations.md"]
1. Prove SDC can recommend non-content entities
2. Help casual creators get into PS Web
3. Deliver POC quickly

### Use Cases
1. Preset Adjustments (similar to Lr preset recs)
2. Subject/Background Manipulation

## Program Information
**Contacts**: [[Hao Xu]], Jasper
**Slack**: [ps-web-in-context-recommendation](...)
**Timeline**: 2025 POCs
**Related**: [[Recommendations Home]], [[CKG 4.0]], [[Lr Home|Lightroom]]
```

**Handling current "Ps Web Action Recommendations.md"**:
- **Option A**: Merge entirely into hub, archive separate file
- **Option B**: Keep as subordinate detail page if >200 lines
  - Rename: "Photoshop Web Action Recommendations POC.md"
  - Frontmatter: `Parent: "[[Photoshop Web Recommendations]]"`
  - Hub links: "For detailed POC docs, see [[Photoshop Web Action Recommendations POC]]"

**Recommendation**: Option A unless Action Recs doc exceeds ~200 lines

### General Principle Derived

> **Consolidation Rule**: When concepts share Product × Surface × Program but differ on implementation/type, create **one hub with sections**. Only split when sections exceed ~200-300 lines or have genuinely independent lifecycles.

**Guiding question**:
> "If someone asks 'What's happening with [Product] [Surface] [Workstream]?', is there ONE place they should start?"

For PS Web Recommendations: **Yes, one place**.

This is like Wikipedia's approach:
- Main article: "Photoshop"
- Sections: Features, History, Versions
- Sub-articles: Only when sections get too large ("History of Photoshop")

---

## Migration Plan: Photoshop Web Recommendations

### Phase 1: Current State

**Existing files**:
1. `Notes/Misc/Ps web.md` - Minimal stub
   - Aliases: `ps web contextual recs`, `ps web`, `psw`
   - Related: `[[Recommendations Home|USCD]]`

2. `Notes/Misc/Ps Web Action Recommendations.md` - Separate POC
   - Aliases: `ps web actions`, `ps web action recs`
   - ~45 lines of content

**References** (44 files found):
- Link variations: `[[Ps web]]`, `[[PS Web]]`, `[[Ps web|Photoshop web]]`
- Locations: Recommendations Home:34, CKG 4.0:83,100, ~15 daily notes
- People: Hao Xu (PM)

### Phase 2: Canonical Naming

**Decision**: "Photoshop Web Recommendations"

**Rationale**:
- Matches pattern: "Acrobat Studio", "Recommendations Home"
- Clear, professional, searchable
- Avoids abbreviation in file name
- Display via aliases: "Photoshop Web" or "PS Web"

**Comprehensive alias list**:
```yaml
aliases:
  - PS Web Recommendations
  - Photoshop Web Recs
  - PS Web Recs
  - ps web contextual recs
  - ps web contextual recommendations
  - ps web
  - psw
  - Photoshop Web
  - PS Web
  - PS Web Content Recs
  - ps web action recs  # covers action variant
```

### Phase 3: File Structure

**Action**: Rename `Ps web.md` → `Photoshop Web Recommendations.md`

**Updated frontmatter**:
```yaml
---
created: "2025-08-XX"  # Use original creation date
pageType: misc
tags:
  - claude
aliases:
  - PS Web Recommendations
  - Photoshop Web Recs
  - PS Web Recs
  - ps web contextual recs
  - ps web contextual recommendations
  - ps web
  - psw
  - Photoshop Web
  - PS Web
Related Pages:
  - "[[Recommendations Home]]"
  - "[[Photoshop]]"  # when created
  - "[[CKG 4.0]]"
  - "[[Style Home]]"
protected: false
---
```

**Content structure**:
```markdown
# Photoshop Web Recommendations
---

Contextual recommendations for Photoshop Web, bringing content discovery and workflow assistance to web-based creative workflows.

## Overview
[Program description]
[Value proposition]
[2025 focus areas]

## Content Recommendations
Contextual discovery of assets, templates, and media for PS Web users.

### Current State
[Content from existing "Ps web.md"]

### Use Cases
- Asset recommendations in picker
- Template suggestions based on canvas

## Action Recommendations
Workflow and tool suggestions to accelerate creation.

### POC Goals
[Merge from "Ps Web Action Recommendations.md"]
1. Prove SDC can recommend non-stock, non-content entities
2. Prove action intelligence integration
3. Prove content intelligence required

### Target User
Help casual/novice creators get into PS Web without forcing them into templates.
Goal: "Draw them deeper" into product capabilities.

### POC Use Cases
1. **Preset Adjustments**: Recommend PsW adjustment configurations (similar to Lr presets)
2. **Subject/Background Manipulation**: Recommend subject vs background edits

### Timeline
- 2025 POC phase
- Quick delivery leveraging existing SDC intelligence

## Contacts & Links
- **PM Contacts**:
  - [[Hao Xu]]
  - [Jasper](https://adobe.enterprise.slack.com/team/WC4RU0GG7)
- **Slack**: [ps-web-in-context-recommendation](https://adobe.enterprise.slack.com/archives/C0967S972VC)
- **Program Wiki**: [link when available]

## Technical Approach
- Leverage canvas intelligence from [[CKG 4.0]]
- [[Style Home|Style understanding]] for visual analysis
- Explore action intelligence as incremental layer

## Related Work
- [[Lr Home|Lightroom]] preset recommendations (similar pattern)
- [[Express]] contextual recommendations
- [[Recommendations Home]] (parent program)
```

### Phase 4: Update Parent Hub Links

**File**: `Notes/Programs/Recommendations Home.md` (line 34)

**Current**:
```markdown
- [[Ps web]]
```

**Updated**:
```markdown
- [[Photoshop Web Recommendations|Photoshop Web]]
```

**File**: `Notes/Programs/CKG 4.0.md` (lines 83, 100)

**Current**:
```markdown
- [[Ps web|Photoshop web]] POC development
- **[[Hao Xu]]**: [[Ps web|Photoshop web]] POC development
```

**Updated**:
```markdown
- [[Photoshop Web Recommendations|Photoshop Web]] POC development
- **[[Hao Xu]]**: [[Photoshop Web Recommendations|Photoshop Web]] POC development
```

### Phase 5: Execution Steps

#### Step 1: Backup
```bash
# Optional but recommended
git commit -am "Pre PS Web Recs migration snapshot"
```

#### Step 2: Rename File (in Obsidian UI)
1. Right-click `Notes/Misc/Ps web.md`
2. Rename to: `Photoshop Web Recommendations.md`
3. Obsidian auto-updates all `[[Ps web]]` links

#### Step 3: Update Frontmatter & Content
1. Add comprehensive aliases
2. Add Related Pages links
3. Merge content from both existing files
4. Structure with clear H2 sections

#### Step 4: Handle "Ps Web Action Recommendations.md"
**Recommended**: Merge into main hub
1. Copy content into "Action Recommendations" section
2. Archive or delete original file
3. Update any direct links (shouldn't be many)

**Alternative**: Keep as subordinate if substantial
1. Rename: "Photoshop Web Action Recommendations POC.md"
2. Add frontmatter: `Parent: "[[Photoshop Web Recommendations]]"`
3. Hub page links to it for details

#### Step 5: Update Parent Hubs
1. Edit `Recommendations Home.md` line 34
2. Edit `CKG 4.0.md` lines 83, 100
3. Use display text: `[[Photoshop Web Recommendations|Photoshop Web]]`

#### Step 6: Validate
1. Check for broken links in Obsidian graph view
2. Search for `[[ps web]]` - should resolve to new page
3. Verify aliases resolve correctly
4. Check Related Pages backlinks appear
5. Test navigation from Recommendations Home

#### Step 7: Optional Cleanup (Low Priority)
- Daily notes can remain as-is (aliases resolve)
- Incrementally update to canonical links over time
- Update meeting headers: `## [[Photoshop Web Recommendations|PS Web]]`

### Phase 6: Link Strategy

**Strategy A: Minimal Updates (Recommended Phase 1)**
- Rename file only
- Update parent hubs only
- Leave daily notes as-is
- Aliases auto-resolve `[[Ps web]]` → "Photoshop Web Recommendations"

**Pros**: Fast, low risk, no broken links
**Cons**: Inconsistent link text across vault

**Strategy B: Comprehensive Updates (Future)**
- Update all 44 references to canonical link
- Use display text variants: `[[Photoshop Web Recommendations|PS Web]]`
- Complete consistency

**Recommendation**: Start with Strategy A, gradually adopt Strategy B

### Display Text Convention

**Context-dependent linking**:
- **In program hubs**: Formal → `[[Photoshop Web Recommendations|Photoshop Web]]`
- **In daily notes**: Casual → `[[Photoshop Web Recommendations|PS Web]]` or `[[ps web]]`
- **In person pages**: Match their usage → `[[PS Web]]`

---

## Migration Checklist

```markdown
### PS Web Recommendations Migration

- [ ] Backup/commit current vault state
- [ ] Decide on handling Action Recs file (merge vs subordinate)
- [ ] Rename "Ps web.md" → "Photoshop Web Recommendations.md" (in Obsidian)
- [ ] Update frontmatter with comprehensive aliases
- [ ] Update frontmatter with Related Pages
- [ ] Merge or link to Action Recommendations content
- [ ] Expand page with Overview, Contacts, Timeline sections
- [ ] Update Recommendations Home.md link (line 34)
- [ ] Update CKG 4.0.md links (lines 83, 100)
- [ ] Check for broken links in graph view
- [ ] Verify aliases resolve correctly
- [ ] Test backlinks from Related Pages
- [ ] Test navigation path from Recommendations Home
- [ ] (Optional) Update daily notes incrementally
```

---

## Broader Recommendations

### Immediate Actions

1. **Acrobat/DC Restructuring**
   - Split `Acrobat Studio.md` into:
     - Keep as product hub
     - Create `Acrobat Contextual Recommendations.md`
     - Create `Acrobat AMA.md`
   - Update `Recommendations Home.md` to link to dedicated recs page

2. **PS Web - Execute Migration**
   - Follow plan above
   - Consolidate Action + Content under one hub

3. **Query Understanding Clarity** (Nice to have)
   - Add architecture diagram in `Query Understanding.md`
   - Show layers: Technology (MINT/CKG) → Services (NER, SRL, CAF) → Products

### Medium-Term Actions

4. **Create Missing Product Hubs**
   - `Photoshop.md` (referenced but doesn't exist)
   - `Express.md` (highly referenced, should be hub)
   - Consider `Firefly.md` hub

5. **Document the Pattern**
   Add to `CLAUDE.md`:
   ```markdown
   ## Intersectional Topics

   When a topic sits at the intersection of Product × Workstream × Surface:

   **Create dedicated page when 2+ criteria met**:
   - Different stakeholders/PMs
   - Different timelines (>6 months)
   - Different parent programs
   - Content would exceed 300 lines

   **Structure**:
   - Canonical page as single source of truth
   - Cross-link from all parent hubs
   - Use Related Pages frontmatter
   - Comprehensive aliases for discoverability

   **Consolidation rule**: Keep sub-topics under one hub until:
   - Sections exceed ~300 lines each
   - Independent lifecycles emerge
   - Different stakeholder ownership
   ```

---

## Organizational Principles

### One Entry Point Per Product×Surface

**Principle**: Users should have ONE place to start for any Product×Surface×Workstream combination.

**Example**: "What's going on with PS Web Recs?"
- ✅ One canonical page with complete picture
- ❌ Not: Multiple pages requiring assembly

### Technology vs Application Separation

**Principle**: Separate underlying technology platforms from product applications.

**Example**:
- Technology: `Intent AI Home.md` (MINT, CKG, SLM)
- Applications: `Recommendations Home.md`, `Express.md`, `Lightroom.md`
- Links: Applications link TO technology

### Lifecycle-Based Splitting

**Principle**: Don't split preemptively. Consolidate until lifecycle divergence.

**Lifecycle indicators**:
- Different launch dates (>6 months)
- Different stakeholders taking ownership
- One initiative sunsets while other continues
- Different success metrics

**Example**: PS Web Action Recs
- Currently: POC within broader program → Consolidate
- If succeeds: May spin out → Can elevate to sibling
- If fails: Archive section → No orphaned page

### Content Threshold

**Principle**: Size matters, but context matters more.

**Guidelines**:
- < 200 lines per sub-topic: Keep consolidated
- 200-300 lines: Evaluate against other criteria
- > 300 lines per sub-topic: Strong signal to split
- > 500 lines total page: Consider restructuring

**But**: 500 lines of tightly related content (same PM, program, timeline) beats 5 pages of 100 lines each with sync issues.

---

## Success Criteria

### Discoverability
- ✅ Can find via product navigation OR workstream navigation
- ✅ Aliases cover all team terminology
- ✅ Related Pages create bidirectional discoverability

### Maintainability
- ✅ Single source of truth, not duplicated content
- ✅ Clear ownership and update responsibility
- ✅ Changes don't require updating multiple pages

### Scalability
- ✅ Pattern works for 3 intersections or 30
- ✅ Growth doesn't bloat parent pages
- ✅ New initiatives follow clear template

### Context Preservation
- ✅ Dedicated page maintains full context
- ✅ History and evolution tracked in one place
- ✅ Related work and dependencies clear

---

## Lessons Learned

### Pattern Already Exists
The hub-and-spoke model is not new to this vault. Query Understanding and Intent AI already use it successfully. The issue was recognizing the pattern and applying it consistently.

### Start Consolidated, Split Deliberately
Premature splitting creates fragmentation. It's easier to split a large page than to merge scattered content.

### Aliases Are Powerful
Comprehensive aliases mean you can rename files without breaking mental models. Team can keep using "ps web" while vault structure uses "Photoshop Web Recommendations".

### Decision Frameworks Beat Ad-Hoc Choices
Having explicit criteria (same PM? same timeline? >300 lines?) turns subjective decisions into objective evaluation.

### Test Cases Reveal Edge Cases
The Action vs Content Recs case forced articulation of the consolidation principle. Without testing the model, this nuance would have remained implicit.

---

## Related Documentation

- Implementation: Execute PS Web Recs migration per this plan
- Pattern Documentation: Add to `CLAUDE.md` (see section above)
- Future Migrations: Use this as template for Acrobat split, Express hub, etc.

---

## Appendix: Link Patterns

### Parent Hub Link Format
```markdown
# In Recommendations Home.md
- [[Photoshop Web Recommendations|Photoshop Web]]
```

### Intersection Page Frontmatter
```yaml
---
created: "YYYY-MM-DD"
pageType: misc
tags: [claude]
aliases:
  - [All team terminology]
  - [Abbreviations]
  - [Historical names]
Related Pages:
  - "[[Parent Program]]"
  - "[[Product Hub]]"
  - "[[Technology]]"
---
```

### Subordinate Page (if needed)
```yaml
---
created: "YYYY-MM-DD"
pageType: misc
tags: [claude]
Parent: "[[Photoshop Web Recommendations]]"
aliases: [...]
---
# Photoshop Web Action Recommendations POC
---

**Parent**: [[Photoshop Web Recommendations]]

Detailed POC documentation...
```

---

## Version History

- 2025-10-09: Initial analysis and migration plan
- Future: Update after PS Web migration execution
- Future: Update after Acrobat restructuring
