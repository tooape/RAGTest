---
pageTitle: "FY25 Core Affinity Framework Requirements - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/FY25+Core+Affinity+Framework+Requirements"
dateCaptured: "2025-10-14T21:15:03-07:00"
pageSource: "Adobe Wiki"
author:
  - "Ryan Manor"
  - "Ravindra Sadaphule"
  - "Venkat Barakam"
tags:
  - "Adobe wikis"
---
# [FY25 Core Affinity Framework Requirements](https://wiki.corp.adobe.com/display/adobesearch/FY25+Core+Affinity+Framework+Requirements)

[[October 14, 2025]] 

## Summary
This document outlines the requirements for a **[[Core Affinity Framework]] ([[Query Understanding|Core Affinity]])**, a system designed to understand and route user queries within Adobe's SDC (Search, Discover, and Content) ecosystem. [[Query Understanding|CAF]] acts as a routing mechanism, analyzing a user's request based on three key inputs: their current **Surface** (e.g., Express Home), their **Query**, and their **Context** (e.g., region, user entitlements, past behavior).

The framework uses a cascading, multi-level classification system (L1, L2, L3) to categorize the user's intent with increasing specificity. At the highest level (L1), all requests are sorted into four universal categories: **Content** (assets like photos or templates), **Tools & Actions** (features like 'crop tool'), **Products** (e.g., Photoshop), and **HelpX** (support documentation).

[[Core Affinity Framework|Affinity]] is calculated as a multi-label probability score (0-1) for each category, meaning a single query can have a high affinity for multiple categories. For instance, a search for \\"background\\" in Express could relate to both 'Content' (an image) and 'Tools' (the 'remove background' quick action).

The document clarifies that [[Query Understanding|CAF]]s scope is limited to this categorization and does not handle tasks like distinguishing between search vs. generative AI prompts or [[NER & SRL|NER (Named Entity Recognition)]]. The initial Q3'25 priority is to implement the L1 and L2 categories for critical surfaces like DC and Firefly. 

## Highlights
> 

## Details
- **[[Core Affinity Framework]] ([[CAF]]):** A routing mechanism to understand user intent based on their surface, query, and context.
- **Key Inputs:** The framework leverages three inputs: 1) Surface/Experience, 2) Query, and 3) User Context.
- **Hierarchical Categorization:** Uses a multi-level structure (L1, L2, L3) to classify requests into broad and then more specific categories.
- **L1 Categories:** The four universal top-level categories are Content, Tools & Actions, Products, and HelpX.
- **Q3'25 Prioritization:** The initial focus is on implementing L1 and L2 categories for P1 surfaces like DC and Firefly.

