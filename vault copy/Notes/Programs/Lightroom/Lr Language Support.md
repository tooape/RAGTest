---
created: "2025-11-12"
pageType: misc
tags:
  - claude
aliases:
  - Lr language support
  - Lightroom language support
  - Lr multilingual
Related Pages:
  - "[[Lr Home]]"
  - "[[Semantic Search v2]]"
  - "[[Query Understanding]]"
  - "[[Multi-Language 2025]]"
---

# Lightroom Language Support
---

## Context
[[Lr Home|Lightroom]] Desktop April 2026 release requires [[Semantic Search v2|semantic search]] support for multiple languages. Current supported user base spans 16 languages, with top 10 by usage:

1. English
2. German  
3. French
4. Japanese
5. Portuguese
6. Spanish
7. Korean
8. Dutch
9. Italian
10. Polish

**Immediate request**: French, German, Spanish, Japanese

## Key Constraint: Query Understanding Dependency
While adobeOne V2 model covers embeddings and basic multilingual support, **[[Query Understanding|NER & SRL]] requires separate implementation** for each language.

This creates four implementation tiers:

1. **Tier 1** (Full support): Everything ([[NER & SRL|NER]], embeddings, text)
2. **Tier 2** (Embeddings only): Everything but [[NER & SRL|NER]]
3. **Tier 3** (With translation): Everything but [[NER & SRL|NER]] via machine translation (latency tradeoff)
4. **Tier 4** (Text match only): No semantic features

## Open Questions
- NER support timeline for requested languages on [[ILUP]] side
- Fallback strategy for unsupported languages (English default? Machine translation?)
- Scope line for NER updates given 18B asset migration requirement
