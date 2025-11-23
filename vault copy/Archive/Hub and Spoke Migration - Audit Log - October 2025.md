---
pageType: claudeResearch
created: "2025-10-10"
tags:
  - claude
  - vault-organization
  - migration-audit
aliases:
  - Migration Audit Log
  - Hub Spoke Audit
---
# Hub-and-Spoke Migration: Pre-Migration Audit Log
---

## Executive Summary

This document provides a comprehensive audit of all current links and references for projects identified as candidates for hub-and-spoke organizational restructuring. This audit serves as a baseline to ensure no links are broken during migration.

**Audit Date**: October 10, 2025
**Source Document**: [[Vault Organization - Hub and Spoke Model for Intersectional Topics - October 2025]]

**Candidates Identified**:
1. **PS Web Recommendations** - Consolidation needed
2. **Acrobat Studio** - Split into separate initiatives
3. **Express** - Enhancement as product hub (optional)

---

## Migration Candidate #1: PS Web Recommendations

### Current State

**Primary File**: `Notes/Misc/Ps web.md`
- Created: ~August 2025
- Lines: 30
- Status: Minimal stub with scattered content

**Secondary File**: `Notes/Misc/Ps Web Action Recommendations.md`
- Created: September 03, 2025
- Lines: 45
- Status: Separate POC documentation

**Proposed Action**: Consolidate both into `Photoshop Web Recommendations.md`

### Current Aliases

**From `Ps web.md`**:
- ps web contextual recs
- ps web contextual recommendations
- ps web
- psw

**From `Ps Web Action Recommendations.md`**:
- ps web actions
- ps web action recs

**Proposed Comprehensive Aliases** (for consolidated file):
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
  - ps web action recs
  - ps web actions
```

### Link Audit

**Total References Found**: 60 files (via grep search for PS Web variations)

**Key Reference Locations**:

1. **Program Hubs**:
   - `Notes/Programs/Recommendations Home.md` - Line 34 (current: `[[Ps web]]`)
   - `Notes/Programs/CKG 4.0.md` - Lines 83, 100 (current: `[[Ps web|Photoshop web]]`)
   - `Notes/Programs/Style Home.md` - Multiple references

2. **People Pages**:
   - `People/Hao Xu.md` - PM contact page

3. **Daily Notes** (Partial List - Most Recent):
   - October 07, 2025
   - October 06, 2025
   - October 02, 2025
   - September 11, 2025
   - September 08, 2025
   - September 05, 2025
   - September 03, 2025
   - August 28, 2025
   - August 27, 2025
   - August 22, 2025
   - August 20, 2025
   - August 15, 2025
   - August 13, 2025
   - August 07, 2025
   - August 06, 2025
   - August 04, 2025
   - July 22, 2025
   - July 21, 2025
   - July 17, 2025
   - June 23, 2025

4. **Monthly Overviews**:
   - `Notes/Periodic Notes/July 2025 Overview.md`

5. **Other Project Files**:
   - `Notes/Misc/SDC Product Summit.md`
   - `Notes/Misc/CKG4 productionization planning.md`

### Link Patterns Observed

**Common Link Formats**:
- `[[Ps web]]` - Most common (bare link)
- `[[PS Web]]` - Capitalization variant
- `[[Ps web|Photoshop web]]` - With display text
- `[[ps web]]` - Lowercase variant

**Context Usage**:
- Meeting headers: `## [[PS Web]]`
- Inline references: "working on [[Photoshop]] POC"
- Lists: "- [[Photoshop]]"

### Files Requiring Updates Post-Migration

**Critical (Must Update)**:
1. `Notes/Programs/Recommendations Home.md:34` → Change to `[[Photoshop Web Recommendations|Photoshop Web]]`
2. `Notes/Programs/CKG 4.0.md:83,100` → Change to `[[Photoshop Web Recommendations|Photoshop Web]]`

**Optional (Auto-resolve via aliases)**:
- All daily notes will resolve automatically via aliases
- Can optionally update to canonical link format over time

### Related Pages to Link

**Proposed Related Pages frontmatter**:
```yaml
Related Pages:
  - "[[Recommendations Home]]"
  - "[[Photoshop]]"  # Create if doesn't exist
  - "[[CKG 4.0]]"
  - "[[Style Home]]"
```

---

## Migration Candidate #2: Acrobat Studio

### Current State

**Current File**: `Notes/Misc/Acrobat Studio.md`
- Created: Unknown (estimate early 2025)
- Lines: 28
- Status: Currently conflates multiple separate initiatives

**Current Content Structure**:
```
# Acrobat Studio
- Hub PgM Wiki link

## Acrobat AMA
- Sept 2025 launch
- Ask me anything PRD

## Acrobat contextual recs
- Contextual Recommendations wiki
```

**Proposed Action**: Split into three files:
1. `Acrobat Studio.md` - Product hub (keep as overview)
2. `Acrobat Contextual Recommendations.md` - Dedicated recs page (NEW)
3. `Acrobat AMA.md` - Dedicated AMA page (NEW)

### Current Aliases

**From `Acrobat Studio.md`**:
- Acrobat
- pdf recs
- dc recs
- DC
- acrobat studio
- pdf

**Analysis**: These aliases are too broad and conflate multiple concepts:
- "Acrobat" could mean the product, AMA, or recs
- "DC" is ambiguous (product vs. studio vs. specific initiative)

### Link Audit

**Total References Found**: 584 files (via grep for "Acrobat" variations)
- Note: This includes many false positives (generic Acrobat mentions)
- Need to filter for actual wikilinks

**Key Reference Locations** (Based on simple search sample):

1. **Program Hubs**:
   - `Notes/Programs/Recommendations Home.md` - Links to Acrobat contextual recs

2. **Daily Notes** (Recent):
   - October 09, 2025
   - October 08, 2025
   - October 07, 2025
   - Multiple September 2025 entries
   - Multiple August 2025 entries

3. **People Pages**:
   - Multiple team members likely reference Acrobat work

### Proposed Split Strategy

**File 1: `Acrobat Studio.md` (Product Hub)**
```yaml
aliases:
  - Acrobat Studio
  - Acrobat Business Pro
  - DC Studio
Related Pages:
  - "[[Acrobat AMA]]"
  - "[[Acrobat Contextual Recommendations]]"
  - "[[Recommendations Home]]"
```

**File 2: `Acrobat Contextual Recommendations.md` (NEW)**
```yaml
aliases:
  - Acrobat Recs
  - Acrobat Contextual Recs
  - DC Contextual Recommendations
  - PDF Recs
Related Pages:
  - "[[Acrobat Studio]]"
  - "[[Recommendations Home]]"
  - "[[CKG 4.0]]"
```

**File 3: `Acrobat AMA.md` (NEW)**
```yaml
aliases:
  - Acrobat Ask Me Anything
  - DC AMA
Related Pages:
  - "[[Acrobat Studio]]"
  - "[[Intent AI Home]]"
```

### Decision Framework Analysis

**Split Criteria Met** (For Acrobat AMA vs Contextual Recs):
- ✅ Different timelines: AMA = Sept 2025 launch; Recs = ongoing
- ✅ Different initiatives: Distinct PRDs and wikis
- ✅ Different use cases: Q&A assistant vs. content recommendations
- ✅ Would create clutter: Each has substantial content

**Recommendation**: SPLIT - Strong case for separation

### Files Requiring Updates Post-Migration

**Critical**:
1. `Notes/Programs/Recommendations Home.md` → Add link to `[[Acrobat Contextual Recommendations]]`
2. Update any references to "Acrobat" that specifically mean "Acrobat Recs" or "Acrobat AMA"

**Challenge**: Many references to "Acrobat" or "DC" are ambiguous and will require:
- Manual review of context
- Possibly keeping broad aliases on product hub
- Adding specific aliases on initiative-specific pages

---

## Migration Candidate #3: Express (Optional Enhancement)

### Current State

**Current File**: `Notes/Misc/Express.md`
- Created: 2023-08-15
- Page Type: `product`
- Lines: 47
- Status: Exists but may need enhancement as product hub

**Related Files**:
- `Notes/Misc/Express Design Task Hierarchy.md`
- `Notes/Misc/Express Traffic Growth - Program Home.md`
- `Notes/Misc/Express Presentations.md`
- `Notes/Misc/Express Category Exploration Pills.md`

**Current Content**: Strategy pillars for 2023 and 2024, technical notes

**Proposed Action**: EVALUATE - May already function adequately as hub, or may need consolidation

### Current Aliases

**From `Express.md`**:
- express
- adobe express
- CCX
- AX

### Link Audit

**Total References Found**: 290 files (via grep for Express variations)
- High volume indicates heavy usage
- Many references across programs

**Key Reference Locations**:
1. **Program Hubs**:
   - `Notes/Programs/Recommendations Home.md` - Lists Express
   - `Notes/Programs/CKG 4.0.md` - Express integration
   - `Notes/Programs/Style Home.md` - Express use cases

2. **Multiple Program Files**: Recommendations, Intent AI, etc.

3. **Daily Notes**: Extensive references across 2024-2025

### Analysis

**Current State Assessment**:
- ✅ Has dedicated product page
- ✅ Has appropriate pageType: `product`
- ✅ Has good aliases
- ⚠️ May have fragmented related content across multiple files
- ⚠️ May need Related Pages frontmatter added

**Decision Framework**:
- Does NOT need split (already separated)
- May need consolidation of related files
- May need enhancement of Related Pages links

**Recommendation**: LOWER PRIORITY
- Add Related Pages frontmatter
- Consider consolidating related Express files if they're fragmenting information
- Not urgent like PS Web or Acrobat splits

---

## Decision Framework Summary

| Candidate | Split? | Consolidate? | Priority | Rationale |
|-----------|---------|--------------|----------|-----------|
| **PS Web Recommendations** | No | ✅ Yes | **HIGH** | Two separate files covering one program - consolidate Action + Content under one hub |
| **Acrobat Studio** | ✅ Yes | No | **HIGH** | One file conflating distinct initiatives (AMA vs Recs) with different timelines/stakeholders |
| **Express** | No | Maybe | LOW | Already has product page; may need Related Pages enhancement |

---

## Recommended Migration Sequence

### Phase 1: PS Web Recommendations (Priority 1)
**Timeline**: Can execute immediately
**Risk**: Low - well-defined scope, clear aliases

**Steps**:
1. Create comprehensive audit of exact link locations (grep with line numbers)
2. Rename `Ps web.md` → `Photoshop Web Recommendations.md`
3. Update frontmatter with comprehensive aliases
4. Merge `Ps Web Action Recommendations.md` content
5. Update Recommendations Home.md and CKG 4.0.md parent links
6. Validate all links resolve
7. Archive or delete `Ps Web Action Recommendations.md`

**Success Criteria**:
- Zero broken links
- All aliases resolve correctly
- Content from both files integrated
- Parent hubs link to canonical page

### Phase 2: Acrobat Studio Split (Priority 2)
**Timeline**: After PS Web completion
**Risk**: Medium - broader alias ambiguity, more references

**Steps**:
1. Create `Acrobat Contextual Recommendations.md`
2. Create `Acrobat AMA.md`
3. Update `Acrobat Studio.md` to product hub with links to both
4. Distribute content from original file to appropriate new files
5. Update aliases to reduce ambiguity
6. Update Recommendations Home.md to link to Acrobat Contextual Recs
7. Review ambiguous references and update as needed
8. Validate all links resolve

**Success Criteria**:
- Three distinct pages with clear purposes
- Aliases minimize confusion
- Parent hubs link to appropriate pages
- Context-specific links point to correct initiative

**Challenge**: Will require manual review of ambiguous "Acrobat" or "DC" references

### Phase 3: Express Enhancement (Priority 3 - Optional)
**Timeline**: After Acrobat completion
**Risk**: Low - optional improvement

**Steps**:
1. Add Related Pages frontmatter to Express.md
2. Evaluate whether related Express files should be consolidated
3. Enhance cross-linking as needed

---

## Pre-Migration Checklist

### For Each Migration

- [ ] Read current file(s) with Read tool
- [ ] Verify current aliases in frontmatter
- [ ] Run grep search for all link patterns
- [ ] Document exact line numbers of critical parent hub links
- [ ] Create backup/commit current state
- [ ] Draft new frontmatter with comprehensive aliases
- [ ] Draft new content structure
- [ ] Identify all Related Pages to link

### Post-Migration Validation

- [ ] Check Obsidian graph for broken links
- [ ] Test each alias resolves correctly
- [ ] Verify parent hub links work
- [ ] Check backlinks from Related Pages appear
- [ ] Test navigation path from program hubs
- [ ] Spot-check sample daily note references
- [ ] Validate no orphaned content

---

## Detailed Link Tracking (To Be Expanded During Migration)

### PS Web Recommendations - Exact Link Locations

**Parent Hub Updates Required**:
```
File: Notes/Programs/Recommendations Home.md
Line: 34
Current: - [[Ps web]]
New: - [[Photoshop Web Recommendations|Photoshop Web]]

File: Notes/Programs/CKG 4.0.md
Line: 83
Current: - [[Ps web|Photoshop web]] POC development
New: - [[Photoshop Web Recommendations|Photoshop Web]] POC development

File: Notes/Programs/CKG 4.0.md
Line: 100
Current: **[[Hao Xu]]**: [[Ps web|Photoshop web]] POC development
New: **[[Hao Xu]]**: [[Photoshop Web Recommendations|Photoshop Web]] POC development
```

**Daily Notes**: Auto-resolve via aliases (no updates required)
**People Pages**: Auto-resolve via aliases (no updates required)

### Acrobat - Exact Link Locations

*To be populated during Acrobat migration phase*

### Express - Exact Link Locations

*To be populated if Express enhancement proceeds*

---

## Notes & Observations

### Alias Strategy Lessons

1. **Comprehensive is better than minimal**: Including all team terminology variations prevents broken links
2. **Display text variants**: Same link, different context = different display text
3. **Case sensitivity**: Include both capitalized and lowercase variants
4. **Abbreviations**: Team uses shortcuts (ps web, psw, CCX, AX) - must include
5. **Legacy names**: Historical references need aliases for backward compatibility

### Link Pattern Insights

1. **Most common pattern**: Bare wikilink `[[Page Name]]`
2. **Display text usage**: More common in structured documents (program hubs) than daily notes
3. **Meeting headers**: Often use capitalized short form `## [[PS Web]]`
4. **Context switching**: Users type whatever comes to mind - aliases must cover variations

### Risk Mitigation

**Low Risk Actions**:
- Adding aliases (doesn't break existing links)
- Adding Related Pages (enhances, doesn't change)
- Renaming file in Obsidian UI (auto-updates links)

**Medium Risk Actions**:
- Merging content (test that nothing lost)
- Splitting files (ensure parent/child links correct)

**High Risk Actions**:
- Deleting files before validating all links migrated
- Removing aliases before checking usage
- Changing link structure without testing resolution

### Future Considerations

1. **Scalability**: This pattern should work for future intersectional topics
2. **Documentation**: Update CLAUDE.md with this pattern once proven
3. **Templates**: Consider creating a template for intersection pages
4. **Monitoring**: Periodic audits to catch fragmentation early

---

## Appendix: Grep Patterns Used

### PS Web Search
```bash
grep -r "\[\[Ps web|Ps Web|PS Web|psw|ps web" --include="*.md"
```
**Result**: 60 files

### Acrobat Search
```bash
grep -r "\[\[Acrobat|acrobat|DC|dc recs|pdf recs" --include="*.md"
```
**Result**: 584 files (includes many false positives)

### Express Search
```bash
grep -r "\[\[Express|express|CCX|AX\]" --include="*.md"
```
**Result**: 290 files

---

## Version History

- 2025-10-10: Initial audit log created
- TBD: Update after PS Web migration
- TBD: Update after Acrobat migration
- TBD: Final summary and lessons learned
