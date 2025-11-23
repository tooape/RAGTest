---
created: 2025-01-10
pageType: misc
tags:
  - claude
  - vibe-code-project
Related Pages:
  - "[[Smart Connections Enhancement - Custom RAG]]"
aliases:
  - unified capture
  - knowledge browser
  - personal clipper
Status: Ideation
---
# Personal Knowledge Browser - Cappy 
---

A vibecode project to build a unified "save for later" system that centralizes bookmarks, watch later lists, and saved content from all platforms into Obsidian, with entity-aware discovery inspired by Tidal's credits browsing.

**GitHub Repository**: https://github.com/tooape/cappy
**Local Path**: `/Users/rmanor/cappy/`

## The Vision
---

**Problem**: Every platform has its own "save for later" feature - YouTube watch later, Twitter bookmarks, Reddit saves, browser bookmarks, Amazon wishlists, GitHub stars, etc. These become information silos that are hard to search, connect, or browse holistically.

**Solution**: Centralize all "this is interesting" moments into Obsidian as **knowledge objects** with rich metadata and entity relationships, enabling discovery through people, topics, and connections - not just chronological lists.

### Inspiration

**Tidal Credits Browsing**: In Tidal, you can discover music through album credits - see all albums mixed by Serban Ghenea, or songs featuring a specific session musician. This creates discovery through **entity relationships**.

**Apply this to knowledge capture**: If I clip a YouTube video from Casey Neistat, a tweet from @caseyneistat, and a blog post he wrote, I want to:
- See them all connected through the entity [[Casey Neistat]]
- Discover patterns (topics he talks about, collaborators, related creators)
- Browse my knowledge through people/topics/publications like browsing music through credits

**Similar Products**:
- [MyMind](https://mymind.com) - Visual bookmarking with AI tagging
- [Fabric](https://fabric.so) - Personal internet library
- Pinterest - Visual discovery through boards
- Pocket - Read later with tagging

**Key Difference**: We're building on Obsidian's native strength (wikilinks + graph) rather than creating a separate silo.


## Architecture
---

### Three Main Components

**1. Capture Layer** - Get content into Obsidian with rich metadata
- Browser extension (active clipping while browsing)
- API integrations (bulk import from platform "saves")
- LLM-powered entity extraction (people, topics, publications)
- Auto-linking to person/topic pages

**2. Entity System** - Obsidian's wikilinks as "credits"
- Person pages (creators, authors, thinkers)
- Topic pages (concepts, themes)
- Publication pages (Medium, NYT, YouTube channels)
- Auto-created on first mention
- Backlinks show "all content from this person"

**3. Discovery Plugin** - Browse and explore captured content
- Card wall view (Pinterest/MyMind style)
- Entity browse (all content from [[Person X]])
- Semantic search (integrated with existing RAG)
- Related content suggestions (using embeddings)
- Works on mobile (Obsidian mobile app)

### Why Obsidian Plugin vs Separate App?

**Advantages**:
- ✅ Wikilinks provide entity relationships natively
- ✅ Works on mobile via Obsidian mobile app (no separate build)
- ✅ Integrated with existing RAG for semantic search
- ✅ Single source of truth (personal vault)
- ✅ Simpler maintenance (one plugin vs web app)
- ✅ Already have graph visualization

**Disadvantages**:
- ⚠️ Obsidian UI constraints (can't fully replicate MyMind aesthetic)
- ⚠️ Plugin development learning curve
- ⚠️ Limited to Obsidian ecosystem

## Content Types and Metadata
---

### Example: Video Clip

```yaml
---
contentType: video
title: "Making a Film in NYC"
creator: [[Casey Neistat]]
channel: [[Casey Neistat]]
platform: YouTube
duration: 12:34
topics: [[Filmmaking]], [[NYC]], [[Cameras]]
url: https://youtube.com/watch?v=...
thumbnail: https://...
clipped: 2025-01-10
---

# Making a Film in NYC

[LLM-generated summary]

## Key Points
- [Extracted highlights]
```

### Example: Tweet

```yaml
---
contentType: tweet
author: [[Casey Neistat]]
platform: Twitter
topics: [[Filmmaking]], [[Gear]]
url: https://twitter.com/...
clipped: 2025-01-10
likes: 1.2k
---

# Tweet about camera gear

[Tweet text and thread context]
```

### Example: Article

```yaml
---
contentType: article
title: "On Creativity"
author: [[Casey Neistat]]
publication: [[Medium]]
byline: "Casey Neistat is a filmmaker..."
publishDate: 2024-12-15
readingTime: 8 min
topics: [[Creativity]], [[Storytelling]]
url: https://...
coverImage: https://...
clipped: 2025-01-10
---

# On Creativity

[LLM-generated summary + highlights]
```

### Example: Product

```yaml
---
contentType: product
title: "Sony A7S III"
vendor: [[B&H Photo]]
price: $3,498.00
category: [[Cameras]]
topics: [[Video Production]], [[Gear]]
url: https://...
productImage: https://...
clipped: 2025-01-10
---

# Sony A7S III

[Product description + key specs]
```

### Entity Page: Person

```yaml
---
pageType: person
name: Casey Neistat
twitter: @caseyneistat
youtube: @casey
website: https://caseyneistat.com
topics: [[Filmmaking]], [[Vlogging]], [[NYC]]
---

# Casey Neistat

Filmmaker, YouTuber, entrepreneur.

## Bio
[LLM-generated bio on first creation]

## Content
[Backlinks automatically show all clips from/about this person]
```

## Capture System Design
---

### Browser Extension

**Option A: Fork Obsidian Web Clipper**
- Pros: Already has templates, markdown conversion, existing user base
- Cons: Need to understand codebase, limited by upstream changes
- Repo: https://github.com/obsidianmd/obsidian-clipper

**Option B: Build Custom Extension**
- Pros: Full control, tailored to entity extraction
- Cons: More work, duplicate effort from Obsidian Clipper

**Decision**: TBD - Need to evaluate Obsidian Clipper's extensibility

### Entity Extraction Flow

```
User clips page
    ↓
Browser extension sends to LLM (Gemini/Claude)
    ↓
LLM extracts:
    - Content type (video/article/tweet/product)
    - Entities (people, topics, publications)
    - Metadata (author, date, price, etc.)
    - Summary + highlights
    ↓
Extension creates note with frontmatter
    ↓
Auto-creates person/topic pages if they don't exist
    ↓
Wikilinks connect everything
```

### LLM Prompts by Content Type

**Article**:
```
Extract from this article:
- Title
- Author (create as [[Author Name]])
- Publication (create as [[Publication Name]])
- Byline/author bio
- Publish date
- Reading time
- Main topics (as wikilinks)
- 3-sentence summary
- Key quotes/highlights
```

**Video (YouTube)**:
```
Extract from this video page:
- Title
- Creator/channel (create as [[Creator Name]])
- Duration
- Topics covered (as wikilinks)
- Transcript summary (if available)
- Key timestamps
```

**Tweet/Thread**:
```
Extract from this tweet:
- Author (create as [[Author Name]])
- Thread context (if part of thread)
- Main topics (as wikilinks)
- Engagement metrics
- Summary (if thread)
```

**Product**:
```
Extract from this product page:
- Product name
- Vendor (create as [[Vendor Name]])
- Price
- Key specifications
- Category/topics (as wikilinks)
```

### API Integrations (Bulk Import)

**Priority platforms** (TBD with user):
- YouTube Data API → Watch later playlist
- Twitter API → Bookmarks
- Reddit API → Saved posts
- GitHub API → Starred repos
- Pocket API → Saved articles
- Raindrop.io API → Browser bookmarks
- Amazon Wishlist (scraping, no official API)

**Flow**:
```
Scheduled script (daily/weekly)
    ↓
Fetch new saves from each platform
    ↓
For each item:
    - Fetch page content
    - Run LLM extraction
    - Create Obsidian note
    - Link entities
```

## Discovery Plugin Design
---

### Core Views

**1. Card Wall View** (Default)
- Masonry layout like Pinterest/MyMind
- Cards styled by contentType:
  - Videos: Thumbnail + title + creator + duration
  - Articles: Cover image + title + author + publication
  - Tweets: Tweet text + author + engagement
  - Products: Product image + title + price
- Click card → Open note or original URL
- Hover → Quick preview
- Filters: Type / Date / Entity / Topic

**2. Entity Browse View**
- Left sidebar: List of people/topics/publications
- Click entity → Show all related clips (like Tidal credits)
- Example: Click [[Casey Neistat]] → See all his videos, tweets, articles
- "More from this entity" suggestions

**3. Timeline View**
- Chronological scroll
- Group by day/week/month
- Mixed content types

**4. Graph View Enhancement**
- Overlay on Obsidian's native graph
- Highlight entity clusters
- Filter by contentType

### Search Integration

**Leverage existing RAG system**:
- Semantic search across all clips
- Search by entity: "show me all content from [[Person X]]"
- Search by topic: "show me all [[Filmmaking]] clips"
- Combined search: "filmmaking videos from Casey Neistat"

**New search features**:
- Filter by contentType (videos only, articles only, etc.)
- Date range filtering
- Platform filtering (YouTube, Twitter, etc.)

### Discovery Features

**"More Like This"** (using embeddings):
- Click "Related" on any clip → Show semantically similar clips
- Powered by existing EmbeddingGemma RAG system

**"People Also Clipped"**:
- If you clipped [[Person A]], show other people who appear in similar contexts
- Graph-based discovery (neighbors in knowledge graph)

**"Topics You Might Like"**:
- Cluster analysis of your clips
- Suggest under-explored topics

**"From the Same Creator"**:
- Click creator name → See all their content
- Tidal credits experience

### Mobile Experience

**Capture**:
- iOS: Share sheet → Send to Obsidian
- Android: Share intent → Same
- Or: Mobile web version of extension

**Browse**:
- Plugin works in Obsidian mobile app
- Simplified card view (single column)
- Swipe gestures for filters
- Search integrated

## Implementation Plan
---

### Phase 0: Research and Scoping (Week 1)

**Questions to Answer**:
1. Which platforms are top 5 "save for later" sources?
2. Which entity types are most important? (People, Publications, Topics, Products)
3. Should we fork Obsidian Clipper or build custom extension?
4. Is mobile capture critical for v1?
5. What's the primary browse mode? (Card wall, entity-first, timeline)

**Technical Evaluation**:
- Review Obsidian Clipper extensibility
- Evaluate Obsidian plugin API for custom views
- Test LLM entity extraction on sample pages
- Assess API availability for target platforms

### Phase 1: Capture System (Week 2-4)

**Tasks**:
1. **Browser Extension**:
   - Fork/build extension with LLM entity extraction
   - Implement content type detection
   - Create type-specific extraction prompts
   - Auto-create entity pages (people/topics/publications)
   - Save to personal vault with rich frontmatter

2. **Entity Auto-Creation**:
   - Template for person pages
   - Template for topic pages
   - Template for publication pages
   - LLM enrichment (pull bio, social links on creation)

3. **API Integration (Pick 2-3 platforms)**:
   - Script to pull saves from APIs
   - Transform to Obsidian notes
   - Schedule periodic sync

**Deliverables**:
- Working browser extension
- 2-3 API integrations
- Entity pages auto-created
- 50-100 clips in personal vault for testing

### Phase 2: Discovery Plugin (Week 5-8)

**Tasks**:
1. **Obsidian Plugin Setup**:
   - Create plugin scaffold
   - Register custom views
   - Read vault files with contentType frontmatter

2. **Card Wall View**:
   - Masonry layout component
   - Card designs for each contentType
   - Filtering UI (type, date, entity)
   - Click handlers (open note/URL)

3. **Entity Browse View**:
   - Entity list sidebar
   - "All clips from X" display
   - Integration with backlinks

4. **Search Integration**:
   - Connect to existing RAG backend (EmbeddingGemma)
   - Semantic search within Discovery view
   - Filter by contentType, entity, date

**Deliverables**:
- Obsidian plugin with Card Wall + Entity Browse views
- Semantic search integrated
- Works on desktop Obsidian

### Phase 3: Polish and Mobile (Week 9-10)

**Tasks**:
1. **Mobile Capture**:
   - Share sheet integration (iOS)
   - Share intent (Android)
   - Or: PWA version of clipper

2. **Mobile Browse**:
   - Test plugin on Obsidian mobile
   - Optimize card layout for mobile
   - Swipe gestures

3. **Discovery Features**:
   - "More like this" using embeddings
   - "From the same creator" links
   - Graph cluster visualization

**Deliverables**:
- Mobile capture working
- Plugin works on Obsidian mobile
- Discovery features live

## Open Questions
---

### Product Questions

1. **Top 5 platforms for capture**?
   - YouTube watch later?
   - Twitter/X bookmarks?
   - Reddit saved posts?
   - Browser bookmarks?
   - GitHub stars?
   - Amazon wishlists?
   - Academic papers (arXiv, PubMed)?

2. **Primary entity types**?
   - People (creators, authors, thinkers) - High priority?
   - Publications/Companies (NYT, Medium, YouTube channels) - High priority?
   - Topics/Concepts (Filmmaking, AI, Design) - High priority?
   - Products/Brands - Lower priority?

3. **Primary browse mode**?
   - Card wall (Pinterest style)
   - Entity-first (browse by people/topics)
   - Timeline (chronological)
   - Mix of all three

4. **Mobile capture priority**?
   - Critical for v1 (can't launch without it)
   - Nice to have (desktop first, mobile later)

5. **Discovery features priority**?
   - "More like this" (semantic similarity)
   - "From the same creator" (entity relationships)
   - "Topics you might like" (clustering)
   - Graph visualization

### Technical Questions

1. **Browser extension approach**?
   - Fork Obsidian Clipper (leverage existing work)
   - Build custom (full control)
   - Depends on: Clipper's extensibility for entity extraction

2. **LLM for entity extraction**?
   - Gemini (free tier, fast)
   - Claude (better quality, costs money)
   - Mix (Gemini for initial, Claude for enrichment)

3. **Entity linking strategy**?
   - Automatic (LLM decides all wikilinks)
   - Semi-automatic (LLM suggests, user confirms)
   - Learn from patterns (LLM improves over time)

4. **API sync frequency**?
   - Real-time (webhook-based if possible)
   - Periodic (daily/weekly script)
   - Manual (user triggers import)

5. **Obsidian plugin architecture**?
   - Single plugin with multiple views
   - Multiple plugins (Capture + Discovery separate)
   - Integrate with existing plugins (Dataview, Graph View)

## Success Metrics
---

**Qualitative**:
- [ ] "I can find that article from that person I follow" in <10 seconds
- [ ] "Browsing my clips feels like browsing Pinterest" (engaging, visual)
- [ ] "I discovered new content through entity connections I didn't expect"
- [ ] "I stopped using platform-specific bookmarks" (YouTube watch later, Twitter saves, etc.)

**Quantitative**:
- [ ] 500+ clips imported from existing "save for later" silos
- [ ] 50+ person pages auto-created with backlinks
- [ ] Semantic search returns relevant clips (MRR > 0.8)
- [ ] Mobile capture works (can clip from phone)
- [ ] Plugin launch time <2s on 1000-clip vault

## Related Work
---

**At Adobe**:
- [[Query Understanding]] - Entity extraction, NER
- [[Recommendations Home]] - Discovery algorithms
- [[Smart Connections Enhancement - Custom RAG]] - Semantic search, embeddings

**Could Apply**:
- Entity extraction from Query Understanding work
- Graph-based discovery from Recommendations
- RAG search from Smart Connections project

## References
---

**Inspiration Products**:
- [MyMind](https://mymind.com) - Visual bookmarking
- [Fabric](https://fabric.so) - Personal internet library
- [Tidal](https://tidal.com) - Music credits browsing
- [Obsidian Web Clipper](https://github.com/obsidianmd/obsidian-clipper)

**Technical**:
- [[Smart Connections Enhancement - Custom RAG]] - RAG backend
- [[Evaluation]] - Testing methodologies
- Obsidian Plugin API docs

## Next Steps
---

1. **Answer scoping questions** (see Open Questions above)
2. **Evaluate Obsidian Clipper** for entity extraction feasibility
3. **Prototype entity extraction** with LLM on sample pages
4. **Design entity page templates** (person, topic, publication)
5. **Start Phase 1**: Build capture system
# Capture System Design
## Web Clipper Insights & Requirements
---

### Capture Goals

**Primary Goal**: Mirror some of the intelligence in MyMind using the Obsidian web clipper and its ability to integrate with Google Gemini.

**Desired Behavior**: Have the clipping respond to the kind of page being clipped with resilience to different layouts and div names across sites.

### Content Types & Metadata Requirements

Different page types require different metadata extraction:

**Products**:
- Price (not captured by default, needs LLM)
- Short description (needs LLM)
- Main image

**Blog Posts, Tweets, Newsletters**:
- Summary (LLM-generated)
- Tags

**Essays & Whitepapers**:
- Summary (LLM-generated)
- Tags

**Videos**:
- Title
- Creator
- Tags

**Images**:
- Tags

**Universal Metadata** (captured across all types):
- Link/URL
- Date of clipping
- Page source

### Challenges & Constraints

#### 1. Limitations of Page Metadata
Obsidian doesn't capture things like price or short description by default as a page property. The AI needs to be prompted to extract and capture these supplementary details from the page content itself.

#### 2. Template Selection Problem
**Challenge**: Don't want to manually select which template to use every time
**Tradeoff**: Using a generic template avoids manual selection but requires longer, more complex prompts to extract content-specific metadata

**Solution Needed**: 
- Auto-detection of page type via LLM (video vs article vs product vs tweet)
- Content-type-specific prompts that are complex enough to capture all needed metadata
- Trade off: slightly longer processing time for better metadata quality

#### 3. Vault Organization Issues
Current state (as of 2025-11-18 audit):
- 23 loose clipping files in `/Clippings/` root directory (unorganized)
  - Personal interest articles: Lamps, gardening, knitting guides
  - Work/technical content: Claude docs, photography references
- Non-standard frontmatter on all clipping files
  - Current: `pageTitle`, `pageSource`, `dateCaptured`
  - Standard should be: `pageType`, `created` (ISO format), `tags: [claude]`
- Orphaned `/Notes/Misc/Untitled.md` file

**Required Actions Before Integration**:
1. Organize loose files into `Clippings/Work/` and `Clippings/Personal/` subdirectories
2. Run web-clipping-curator agent to standardize frontmatter across all clipping files
3. Verify clipping quality and vault terminology alignment

---

# References

### Existing Obsidian Plugins & Tools

**[Obsidian Social Archiver](https://github.com/hyungyunlim/obsidian-social-archiver-releases)**
- Obsidian plugin that archives social media posts into the vault as formatted Markdown notes
- Supports 12+ platforms: Twitter/X, Instagram, TikTok, Facebook, LinkedIn, YouTube, Reddit, Threads, Bluesky, Mastodon, Pinterest, Substack
- Key features:
  - Instant note creation with background media downloading (automatic retry up to 3 attempts)
  - Customizable media handling (text only, images only, or complete content)
  - Timeline view with Pinterest-style media gallery
  - Full-text search and filtering by platform/date/status
  - Web sharing with public timelines at custom URLs (preview or full content)
  - Local storage, passwordless auth, GDPR/CCPA compliant
  - Free beta (unlimited archiving)
- **Comparison to Cappy**: Focused specifically on social media archiving with built-in platform integrations. Cappy is broader (any content type) with emphasis on entity relationships and discovery. Social Archiver could be complementary for social media capture layer.
# Existing Obsidian Plugins & Tools
### Existing Obsidian Plugins & Tools

**[Obsidian Social Archiver](https://github.com/hyungyunlim/obsidian-social-archiver-releases)**
- Obsidian plugin that archives social media posts into the vault as formatted Markdown notes
- Supports 12+ platforms: Twitter/X, Instagram, TikTok, Facebook, LinkedIn, YouTube, Reddit, Threads, Bluesky, Mastodon, Pinterest, Substack

**Capture Architecture:**
- **Two-Phase Model**: 
  - Phase 1: Instant note creation with basic metadata (appears immediately)
  - Phase 2: Background processing downloads full content asynchronously
- **Scraping Backend**: Uses **BrightData's web scraping API** rather than direct platform APIs
- **Infrastructure**: Svelte frontend, Cloudflare backend/CDN, passwordless magic link auth
- **Retry Logic**: Automatic retries up to 3 attempts on failure
- **Media Modes**: Configurable capture (text only, images only, or complete with videos)

**Platform-Specific Extraction:**
- **Twitter/X**: Thread unrolling
- **TikTok**: Transcript extraction (DRM fallback to URL)
- **YouTube**: Raw + formatted transcript options
- **Reddit**: Nested comment preservation
- **Mastodon**: Instance-aware parsing with link cards
- **Bluesky**: Quote-rich capture with embed extraction

**Features:**
- Timeline view with Pinterest-style media gallery
- Full-text search and filtering by platform/date/status
- Web sharing with public timelines at custom URLs
- Local storage, passwordless auth, GDPR/CCPA compliant
- Free beta (unlimited archiving)

**Design Implications for Cappy:**
- Outsources scraping complexity to specialized BrightData service rather than building custom parsers
- Two-phase capture pattern enables good UX (instant feedback) while handling async processing
- Platform-specific extractors show how to handle varied content structures elegantly
- Could fork/borrow: Social media capture layer (using BrightData backend), two-phase UX pattern, platform-specific extraction templates

**Comparison to Cappy**: Social Archiver is focused specifically on social media with built-in platform integrations. Cappy is broader (any content type - videos, articles, products, etc.) with emphasis on entity relationships and semantic discovery. Potential synergy: use Social Archiver's scraping infrastructure + extraction patterns for the social media capture layer, then layer Cappy's entity system and discovery on top.