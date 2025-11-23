---
title: "FY25 Core Affinity Framework Requirements - Adobe Search - Adobe Wiki"
source: "https://wiki.corp.adobe.com/display/adobesearch/FY25+Core+Affinity+Framework+Requirements"
tags:
  - "clippings"
created: 2025-09-23
---
This document outlines the requirements for Adobe's FY25 [[Query Understanding|Core Affinity]] Framework ([[Query Understanding|CAF]]) for Search, Discovery, and Content AI (SDC) query and intent understanding. [[Core Affinity Framework|CAF]] acts as a routing mechanism, or \\"air traffic controller,\\" for user requests by categorizing them into broad (L1), then more specific (L2, L3) topical categories based on the user's surface, query, and context. It is designed to improve relevance and user experience but has specific scope limitations, not covering areas like search vs. generation or Named Entity Recognition ([[NER & SRL|NER]]).

- The [[Query Understanding|Core Affinity]] Framework ([[Core Affinity Framework|CAF]]) leverages three inputs: User's Surface/Experience, Query (including prompts), and Context (region, language, entitlements, behavior).
- It employs a cascading analysis with three levels of categories: Level 1 (universal, broad categories like Content, Tools, Products, HelpX), Level 2 (more fine-grained understanding), and Level 3 (most granular).
- [[Core Affinity Framework|Affinity]] is a multi-label task, assigning a probability (0-1) to each category independently, meaning scores do not necessarily sum to 1.
- Product surface acts as a prior, biasing [[Core Affinity Framework|affinity]] scores for queries like \\"crop\\" differently on [[stock|Stock]] (images) vs. [[Express]] (quick action).
- Q3'25 prioritization focuses on building out the first two levels of categories for critical surfaces like Document Cloud ([[Acrobat|DC]]) and [[Firefly]], aiming for high-level relevance and demoability before expanding deeper and broader.