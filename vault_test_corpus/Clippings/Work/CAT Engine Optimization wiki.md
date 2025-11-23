---
pageTitle: "CAT Engine Optimization - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/CAT+Engine+Optimization"
dateCaptured: "2025-10-24T11:31:51-07:00"
pageSource: "Adobe Wiki"
author:
  - "Asim Kadav"
  - "BY Yu"
tags:
  - "adobeWikis"
---
# [CAT Engine Optimization](https://wiki.corp.adobe.com/display/adobesearch/CAT+Engine+Optimization)

[[October 24, 2025]] 

## Summary
This document provides an overview and proposed short-term optimizations for reducing CAT (Content Analysis and Tagging) engine costs. The architecture of the CAT engine involves two main models: Query2Label and AdobeOne-1024.

Query2Label is responsible for predicting the presence of concepts (e.g., \\"dog\ 

## Highlights
> 

## Details
- The CAT engine uses two models: Query2Label (predicts 80 concept probabilities) and AdobeOne-1024 (disambiguates concept meanings).
- Disambiguation is needed because concepts have variants (e.g., \\"dog\\" can be \\"pet dog\\" or \\"hot dog\\").
- Upgrading `sensei_sdk` from 4.15.2 to 4.20.2 reduced median image request latency from 110ms to 47ms.
- A proposed optimization is to change the CAT model to use 768-dim embedding instead of 1024-dim, requiring Stock/LR sign-off.
- Another optimization is to return AdobeOneV2 embeddings with CAT concepts to avoid duplicate API calls for applications.

