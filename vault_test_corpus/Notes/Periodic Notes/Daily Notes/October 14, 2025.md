---
pageType: daily
aliases:
  - "2025-10-14"
created: "2025-10-14"
---
# [[October 14, 2025]]
# Notes
---


# Meetings 
---
## [[Vipul Dalal|Vipul]]'s takes on [[Query Understanding|QU]] #meetings 

Swimlane 1 is clear
swim lane 2 isn't 
Swimlane 3 mostly is 

For #2 he wants to see what the near term end state is for the [[Query Understanding|QU]] models. 

### General

- Build towards convergence of swimlane 2 and swimlane 3
    - eventually just one swimlane

###  Swimlane 2

- P0 - Close out all [[Intent AI Home|SLM]] modeling efforts in near term
    - Tangible timeline
    - Include these in the list of deliverables (if not already)
- Beyond that, go for longer term foundational efforts
- General vs. specialized flavors of models
    - 0-shot promptable model for early testing
    - retraining to increased scope based on committed use-cases

### Swimlane 3

- [[Multimodal intent|Multimodal]] model should work in both unimodal and [[Multimodal intent|multimodal]] settings
- Grounding to graph should be applicable across the board
- Grounding evaluations needed to prioritize whether current approach is ok or needs to be updated more urgently
## Multi Modal intent detection #meetings 

- [Wiki](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Multi-modal+Intent+and+Content+Understanding)

### Picking back up on Christians demo: 
![[SDC 2025 Intern Showcase 1.pdf]]
#### Problem with Production Model
The existing [[Intent AI Home|MINT]] model used separate vision and text encoders, then **averaged** the embeddings before classification. This caused a "regression-to-the-mean" effect where generic/dominant intents overpowered fine-grained multimodal understanding. Precision: only 0.20-0.21.
#### New Approach: Generation-Based Architecture
Based on LLaVA, replaces embedding averaging with a generative approach:
- **Vision Encoder** → extracts image features as matrix `[num_patches, vision_dim]`
- **Projection Layer** → learned linear transformation mapping vision embeddings to LLM embedding space
	- **Key insight**: The projected vision tokens bypass the LLM's text embedding layer entirely - they're injected directly as "fake text tokens" into the transformer layers. This allows true [[Multimodal intent|multimodal]] reasoning rather than naive averaging.
	- The vision encoder outputs `[256, 768]` dimensional tokens. The projection layer learns a transformation `W: R^768 → R^2048` to match the LLM's embedding dimension.
	- Training: Initially freeze vision encoder and LLM, train only projection on image-caption pairs. Then optionally fine-tune end-to-end on task-specific data ([[Express]]/Stock datasets).
- **Language Model** → processes both projected vision tokens and text embeddings together

