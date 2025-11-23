---
pageTitle: FY25 NER and SRL Requirements - Adobe Search - Adobe Wiki
pageLink: https://wiki.corp.adobe.com/display/adobesearch/FY25+NER+and+SRL+Requirements
dateCaptured: 2025-10-14T21:15:30-07:00
pageSource: Adobe Wiki
author:
  - Tracy King
tags:
  - adobeWikis
---
# [FY25 NER and SRL Requirements](https://wiki.corp.adobe.com/display/adobesearch/FY25+NER+and+[[NER & SRL|SRL]]+Requirements)

[[October 14, 2025]] 

## Summary
This document outlines the FY25 requirements for [[NER & SRL|Named Entity Recognition (NER) and Semantic Role Labeling (SRL)]] within Adobe Search. [[NER & SRL|NER]] identifies and types important entities in a query (e.g., \\"paris\\" as a location), while [[NER & SRL|SRL]] interprets the entity's role (e.g., a date's role as `dateSigned`). Together with the [[Recommendations Home|Unified Search]][[Recommendations Home|[[Recommendati]]ons Home| Service (USS)]], these technologies rewrite queries to create more effective search filters, allowing downstream systems to focus on core keywords.

The document details the technical inputs (text, context) and outputs (entity position, type, canonical form) for these systems. It discusses two implementation approaches: rule-based systems for fixed lists (like colors or asset types) and model-based systems for open-ended categories (like dates or names). 

All [[NER & SRL|NER]] and [[NER & SRL|SRL]] services are to be served via a central platform called [[ILUP]], with a target latency of ~500ms. The strategy emphasizes creating single, reusable models for common entity types across various Adobe products. The page includes (now outdated) tables listing specific NER and [[NER & SRL|SRL]] types and provides examples of their application in Document Cloud search queries. 

## Highlights
> 

## Details
- **[[NER & SRL|NER (Named Entity Recognition)]]** identifies and types entities like dates, locations, or people within a text query.
- **[[NER & SRL|SRL (Semantic Role Labeling)]]** determines the semantic role an identified entity plays, such as `dateCreated` or `signedBy`.
- The goal is to improve search by rewriting queries, using [[NER & SRL|NER]]/[[NER & SRL|SRL]] to create filters (e.g., for location or date) and reducing the number of keywords for semantic matching.
- Implementations can be rule-based (for fixed lists like colors) or model-based (for open sets like names).
- All [[NER & SRL|NER]] and [[NER & SRL|SRL]] services are served through a central system called **[[ILUP]]** with a target latency of approximately 500ms.

