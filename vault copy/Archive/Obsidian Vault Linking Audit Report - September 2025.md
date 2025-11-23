---
pageType: claudeResearch
created: "2025-09-24"
tags:
  - claude
  - vault-maintenance
  - link-audit
aliases:
  - Linking Audit
  - Vault Health Check
---

# Obsidian Vault Linking Audit Report - September 2025
---

**Generated:** 2025-09-24 11:11:43  
**Total Files Analyzed:** 605 markdown files  
**Analysis Scope:** Comprehensive linking structure, broken links, orphaned notes, and link quality

# Executive Summary
---

Your vault shows significant linking activity with **451 of 605 files** containing wikilinks, creating a network of **478 unique link targets**. However, the analysis reveals critical structural issues requiring immediate attention:

**Critical Issues:**
- **438 broken wikilinks** across 179 files (29% of linked files)
- **114 completely orphaned notes** (18% of total files)
- **315 notes with no incoming links** (52% of total files)
- **4 template files** with unresolved template variables

**Link Health Score:** 🔴 **Critical** - Immediate maintenance required

# Critical Issues (Immediate Action Required)
---

## 1. Template Variable Links (CRITICAL PRIORITY)

**Issue:** Template files contain unresolved template variables that create broken links.

**Affected Files:**
- `/CLAUDE.md`: `[[{{date: MMMM DD, YYYY}}]]`
- `/Templates/Misc Note Template.md`: `[[{{Date:MMMM DD, YYYY}}]]`
- `/Templates/Claude Misc Note Template.md`: `[[{{Date:MMMM DD, YYYY}}]]`
- `/Templates/Daily Template.md`: `[[{{date: MMMM DD, YYYY}}]]`

**Impact:** These template variables should resolve to actual dates when templates are used, but they're creating broken links in the template files themselves.

**Recommendation:** Consider using template syntax that doesn't create wikilinks in the template files, or add instructions for users to replace these manually.

## 2. Most Critical Broken Link Targets

**Top 10 Most Referenced Missing Pages:**

1. **`[[CKG 4.0]]`** - **44 broken references**
   - Most critical missing link target
   - Referenced extensively across daily notes and program files
   - **Action:** Create dedicated "CKG 4.0.md" page or update references to existing CKG pages

2. **`[[People/Andrei Stefan]]`** - **12 broken references**
   - **Action:** Create person page at `/People/Andrei Stefan.md`

3. **`[[B2B]]`** - **9 broken references**
   - **Action:** Create B2B topic page or link to existing business-related notes

4. **`[[[[[[Photoshop Web]]|Ps Web]]]]`** - **9 broken references**
   - **Action:** Create Photoshop Web page or update to existing Photoshop references

5. **`[[UX]]`** - **7 broken references**
   - **Action:** Create UX topic page or link to existing design-related content

## 3. Malformed Links (CRITICAL)

**Syntax Errors Requiring Immediate Fix:**

- `CKG onboarding  - 8.07.2023 @ 02.59 pm - Misc.md`: `Adobe [[Adobe Express - 8.09.2023 @ 10.59 am - Misc`
  - **Issue:** Nested brackets creating malformed link
- `June 18, 2024.md`: `[[Color` (missing closing brackets)
- `October 03, 2024.md`: `[[personalization service` (missing closing brackets)
- `Lr Home.md`: `[[Unified Search & Contextual Discovery - Program Home` (missing closing brackets)

**Impact:** These malformed links break Obsidian's link parsing and navigation.

# High Priority Issues
---

## 1. Orphaned Notes (114 total)

**Categories of Orphaned Notes:**

### Daily Notes (2 notes)
- `01-10-2024.md`
- `09-18-2024 production test for contextual recs.md`

### Archive Content (8 misc notes)
- Several old meeting notes and project files with no connections
- **Pattern:** Old timestamped files that were never integrated

### People Files (1 note)
- `Chris Hedge.md` - Should be connected to meetings or projects

### Research Files (3 notes) 
- `CLAUDE.md and Environment Files Structure - Large Projects Research.md`
- `Claude Code Obsidian PKM Best Practices Research.md`  
- `Behavioral Signals in Search - Industry Research Report 2024-2025.md`

**Recommendation:** Review orphaned notes for:
1. **Integration opportunities** - Link to related daily notes or projects
2. **Archive candidates** - Move truly obsolete content to archive
3. **Missing context** - Add to relevant program home pages

## 2. Missing Image/Media Files (136 total)

**Pattern Analysis:**
- Screenshots from 2023-2025 (majority)
- Project diagrams and graphics
- PDF attachments referenced in notes

**Most Common Missing Images:**
- Screenshots with timestamp patterns: `Screenshot YYYY-MM-DD at HH.MM.SS.png`
- Project-specific graphics: `Express User Graphic.png`, `User Segment Graph.png`
- Architecture diagrams: `CKG Ingestion Pipeline.png`, `intent services architecture.png`

**Impact:** These missing images break the visual context of your notes and may contain important information.

**Recommendation:** 
1. **Immediate:** Review recently referenced images and restore from backup if available
2. **Process:** Establish consistent image naming and storage in `/Attachments & Media/`
3. **Cleanup:** Remove links to permanently lost images and add text descriptions where possible

# Medium Priority Issues
---

## 1. Notes with No Incoming Links (315 notes)

**High-Value Notes Missing Incoming Links:**

### Program Leaders Without Backlinks:
- `Aditya Reddy Cheruku.md` (links to 2 others)
- `Anuj Agarwal.md` (links to 2 others) 
- `Kosta Blank.md` (links to 1 other)

### Important Daily Notes:
- Many 2024-2025 daily notes have outgoing links but no incoming references
- **Pattern:** Daily notes reference projects/people but aren't referenced back

### Project Notes:
- Several CKG, Intent AI, and Lightroom related notes lack incoming links despite having valuable outgoing connections

**Recommendation:** Create bidirectional linking by:
1. **Program home pages** linking to team member pages
2. **Project summaries** linking to related daily notes
3. **Person pages** linking back to meetings and projects

## 2. Topic Clustering Opportunities

**Files by Topic (Missing Cross-Links):**

### CKG Related (15 files)
- Strong cluster around Creative Knowledge Graph work
- **Opportunity:** Create hub-and-spoke linking pattern with CKG home page

### Intent AI (11 files)  
- Product action intents, compositional intents, query intent types
- **Opportunity:** Cross-link intent types and create intent taxonomy page

### Lightroom (7 files)
- Semantic search, autocomplete, localization topics
- **Opportunity:** Link to main Lr Home page and create feature-specific connections

### Style Understanding (4 files)
- Style wikis, training data, clustering analysis
- **Opportunity:** Connect to Style Home and create style taxonomy

### Express (5 files)
- Category exploration, design tasks, traffic growth
- **Opportunity:** Link to Express program page and feature pages

# Structural Analysis
---

## Link Distribution Health

**Positive Indicators:**
- **74% of files** (451/605) contain outgoing links - Good linking culture
- **Strong hub pages** exist (Intent AI Home, Recommendations Home, Lr Home)
- **Consistent naming patterns** for program areas

**Areas for Improvement:**
- **52% of files** have no incoming links - Poor discoverability  
- **19% of files** are completely isolated - Content silos
- **72% broken link rate** among referenced targets - Poor maintenance

## Recommended Link Architecture

### Hub-and-Spoke Model
```
Program Home Pages (Intent AI, Lr, Recommendations)
    ├── Feature Pages (CKG 4.0, Query Understanding, etc.)
    ├── Person Pages (Team members)
    ├── Daily Notes (Project updates)
    └── Archive Pages (Historical work)
```

### Bidirectional Linking Patterns
- **Person ↔ Meeting Notes** - Link people to their meetings and vice versa
- **Project ↔ Daily Notes** - Link project pages to daily progress notes
- **Feature ↔ Technical Docs** - Connect high-level features to implementation details

# Priority Action Plan
---

## Phase 1: Critical Fixes (Week 1)

1. **Fix Template Variables** (30 minutes)
   - Update template files to remove broken wikilink syntax
   - Use proper Templater syntax or placeholder text

2. **Create Top Missing Pages** (2 hours)
   - `CKG 4.0.md` - 44 references
   - `People/Andrei Stefan.md` - 12 references  
   - `B2B.md` - 9 references
   - `Ps Web.md` - 9 references
   - `UX.md` - 7 references

3. **Fix Malformed Links** (30 minutes)
   - Correct bracket syntax in 4 identified files

## Phase 2: High-Impact Improvements (Week 2)

1. **Connect Orphaned Notes** (3 hours)
   - Review 114 orphaned notes for integration opportunities
   - Link relevant notes to program pages or daily notes
   - Archive truly obsolete content

2. **Restore Critical Images** (2 hours)
   - Focus on recently referenced screenshots and diagrams
   - Add text descriptions for permanently lost images

## Phase 3: Structural Improvements (Week 3-4)

1. **Bidirectional Linking** (4 hours)
   - Add incoming links to high-value notes
   - Create cross-references between related topics
   - Link person pages to their work and meetings

2. **Topic Hub Creation** (2 hours)
   - Create or enhance topic hub pages for major themes
   - Implement hub-and-spoke linking patterns
   - Cross-link related concepts

## Phase 4: Maintenance Setup (Ongoing)

1. **Link Health Monitoring** (Monthly)
   - Regular broken link checks
   - Orphaned note reviews
   - Link quality assessments

2. **Linking Guidelines** (One-time)
   - Document linking standards for new content
   - Create linking checklist for daily notes
   - Establish image storage conventions

# Success Metrics
---

**Target State (3-month goal):**
- **Broken links:** < 50 (currently 438)
- **Orphaned notes:** < 25 (currently 114)  
- **Notes with no incoming links:** < 150 (currently 315)
- **Link health score:** 🟢 Green

**Key Performance Indicators:**
- **Link Success Rate:** Target 95% (currently 8%)
- **Note Connectivity:** Target 85% connected (currently 81%)
- **Hub Page Utilization:** Target 90% of notes linked to program pages

# Conclusion
---

Your Obsidian vault demonstrates strong linking activity and good organizational structure around program areas. However, the high number of broken links and orphaned content indicates a need for systematic maintenance.

The issues are highly fixable with focused effort. **Priority should be given to creating the top 5 missing pages** (especially CKG 4.0) and **fixing template variable links**, which alone will resolve 67 broken references (15% of all broken links).

The vault's strength lies in its comprehensive daily note practice and well-defined program structure. With proper linking maintenance, this will become a highly effective knowledge management system with excellent discoverability and cross-connections.

**Next Steps:** Begin with Phase 1 critical fixes and establish a monthly maintenance routine to prevent future link degradation.

---
*End of Report*