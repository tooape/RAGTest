---
pageTitle: "SDC Query Understanding - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/SDC+Query+Understanding"
dateCaptured: "2025-10-14T21:07:49-07:00"
pageSource: "Adobe Wiki"
author:
  - "Ryan Manor"
tags:
  - "Adobe wikis"
---
# [SDC Query Understanding](https://wiki.corp.adobe.com/display/adobesearch/SDC+Query+Understanding)

[[October 14, 2025]] 

## Summary
This document provides a conceptual overview of the SDC [[Query Understanding]] architecture, designed to align engineering, architecture, and product management teams on a unified strategy. It is a map for future development, not a list of currently implemented features.

The primary focus for Q3 is delivering enhanced search and discovery experiences for DocCloud and the [[Firefly]] app, specifically for unified search, guidance, and assistant features. 

The core of the architecture is composed of two main subsystems:

1.  **[[Intent AI Home|MINT]]**: A comprehensive system for intent intelligence. It includes:
    *   **[[Core Affinity Framework]] ([[CAF]])**: Routes user queries to the most relevant areas (content, tools, products).
    *   **[[NER & SRL|Named Entity Recognition (NER) & Semantic Role Labeling (SRL)]]**: [[NER & SRL|NER]] identifies explicit entities like dates or names, while [[NER & SRL|SRL]] determines their semantic role in the query.
    *   **[[Intent AI Home|SLM]] & MM Model**: Other models housed within [[Intent AI Home|MINT]].

2.  **[[Intent AI Home|Creative Knowledge Graph (CKG)]]**: A database of canonicalized concepts that helps ground the intent of user queries and content.

The document also clarifies the scope and boundaries between these components. For example, [[CAF]] provides high-level [[Core Affinity Framework|affinity]], whereas [[NER & SRL|NER]] handles fine-grained, explicit mentions (e.g., file types, camera models). [[Core Affinity Framework|Affinity]] is defined as a background capability, distinct from the user-facing features it powers. 

## Highlights
> 

## Details
- **Goal**: To align SDC teams on a conceptual architecture for [[Query Understanding]], avoiding one-off solutions.
- **Q3 Focus**: Development is prioritized for DocCloud and [[Firefly]] app experiences, including unified search and assistant features.
- **Core Systems**: The architecture relies on two main subsystems: **[[Intent AI Home|MINT]]** (for intent intelligence) and the **[[Intent AI Home|Creative Knowledge Graph (CKG)]]** (for grounding concepts).
- **[[Intent AI Home|MINT]] Components**: [[Intent AI Home|MINT]] is a comprehensive system that includes the [[Core Affinity Framework]] ([[CAF]]) for high-level query routing and [[NER & SRL]] for identifying specific entities and their roles.
- **Scope Definition**: The document distinguishes between [[Core Affinity Framework|Affinity]] (broad, directional understanding) and [[NER & SRL|NER]] (explicit, fine-grained entity extraction), clarifying that [[Core Affinity Framework|Affinity]] is a backend capability, not a user-facing feature itself.

