---
pageTitle: "CKG4 Production Testing - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/CKG4+Production+Testing"
dateCaptured: "2025-09-25T13:51:47-07:00"
pageSource: "Adobe Wiki"
author:
  - "Ryan Manor"
---
[[September 25, 2025]] 

**Summary**
This page outlines the plan for testing, iterating, and using CKG4 (Knowledge Graph 4.0) in production. It focuses on initial text-heavy use cases like DC Contextual Image Recommendations and DC Agent, followed by multi-modal capabilities. The plan addresses how to validate a useful subgraph of CKG4, prepare multi-modal models for use, and enable capabilities teams to evaluate and provide feedback efficiently. 

**Highlights**
> 

**Details**
- No updates will be made to CKG 3.5; development moves to CKG 4.0.
- MINT v2 is a new, separate deployment for intent understanding using Language Models, mapping to CKG 4.0 and is text-only initially.
- Initial CKG4 validation focuses on grooming a subgraph of ~20k high-impact concepts using existing curated data sources and query analysis.
- Text-based use cases can leverage MINT v2 models immediately.
- Multi-modal capabilities (image & image+text) will be addressed by MINT v2 visual capabilities later, adding decoder models and visual embedding components.
- Feedback from capabilities teams will be handled via an existing pipeline for adding/removing edges and concepts, with an SLA for changes.

