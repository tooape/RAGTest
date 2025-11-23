---
pageTitle: "Multi-modal Intent and Content Understanding - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/Multi-modal+Intent+and+Content+Understanding"
dateCaptured: "2025-10-14T21:11:04-07:00"
pageSource: "Adobe Wiki"
author:
  - "Asim Kadav"
tags:
  - "Adobe wikis"
---
# [Multi-modal Intent and Content Understanding](https://wiki.corp.adobe.com/display/adobesearch/Multi-modal+Intent+and+Content+Understanding)

[[October 14, 2025]] 

## Summary
This document outlines a proposal for a [[Multimodal intent|multi-modal]] language model designed for intent and content understanding. The model will serve as a foundational component for other [[Query Understanding]] models in [[Intent AI Home|CKG4]] and will support downstream tasks like LoRA fine-tuning, automatic tagging, and [[Multimodal intent|multi-modal]] content retrieval.

The project roadmap consists of four key milestones with target completion dates in late 2025:
1.  Recover and re-deploy an existing model (AdobeOneV1 + LLAMA1.8B).
2.  Ground the model in [[Intent AI Home|CKG4]], ensuring it doesn't require retraining for graph changes.
3.  Iterate on the model's performance and accuracy.
4.  Deliver the updated model as a production-ready service for use in [[Intent AI Home|MINT]].

The initial design specifies an architecture using AdobeOneV1 as the encoder and a Llama-1.8B model as the decoder. It also explores three potential approaches for grounding the model to [[Intent AI Home|CKG]]. 

## Highlights
> 

## Details
- **Objective**: Develop a [[Multimodal intent|multi-modal]] language model for intent and content understanding, grounding other [[Query Understanding]] models in [[Intent AI Home|CKG4]].
- **Roadmap**: A four-milestone plan to deliver a production-ready service by November 28, 2025.
- **Milestone 1**: Recover and re-deploy the existing model (AdobeOne+LLAMA1.8B) by October 17, 2025.
- **Technology Stack**: The initial model (M0) combines the AdobeOneV1 encoder with a Llama-1.8B decoder.
- **Key Challenge**: Grounding the model to [[Intent AI Home|CKG4]] in a way that avoids the need for retraining when the [[Intent AI Home|knowledge graph]] changes.

