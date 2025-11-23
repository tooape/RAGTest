---
tags:
  - claude
created: 2025-09-29
---
- [Wiki link](https://wiki.corp.adobe.com/display/adobesearch/CKG4+Production+Testing)

# One off graph curation 
---

Adding a node type for adobeMetadata. 

What are the use cases or products that we care about, what are the fields within each. 
1. [[Lr Home|Lightroom]]
	1. Camera
	2. Etc...
2. [[Express]]
	1. Type 
	2. 
3. [[Acrobat|DC]]


# Intro
---

This page outlines our plan for testing, iterating, and using CKG4 in production use cases.

## Test plan
### Initial Use cases
We'll target text heavy use cases because we currently only have the modeling required to map into the graph for text. 

1. [[Acrobat|DC]] Contextual Image [[Recommendations Home|recommendations]]
2. [[Acrobat|DC]] Discovery Agent
3. [[Acrobat|DC]] [[Recommendations Home|Unified search]]

**Image & Image+Text**
The [[Multimodal intent|multimodal]] model readiness will be addressed through [[Intent AI Home|MINT]] v2 visual capabilities as the eventual solution. This involves adding decoder models to the existing text-only pipeline and developing the visual embedding components that can map visual content to graph concepts, transitioning from the current LLM-based embedding similarity approach to a more comprehensive [[Multimodal intent|multimodal]] understanding.

Evaluating [[Multimodal intent|multi-modal]] performance will be run later on once we have this model in hand. 
### Reducing topical scope of [[Evaluation|eval]]
CKG4 is very large and includes knowledge from a variety of sources. We have basic health stats and intrinsic [[Evaluation|evals]] for the graph already. However, evaluating it for use cases has not yet been done. We will not be looking to evaluate the general world knowledge of CKG4 at this time. Instead we will focus on [[Intent AI Home|CKG]] 4.0's applicability to the use cases above. To do this quickly we'll narrow down to a few key clusters of data within the graph, and we'll expand from there later on. This reduction in scope will help to be able to quickly respond to gaps or changes for the use cases to start using CKG4. 

This initial "subgraph" will be:
1. The [[Core Affinity Framework|affinity]] hierarchy that is already been curated in [[Intent AI Home|CKG]] 4
2. The topic list that the [[Recommendations Home|contextual recs]] and [[PDF2Pres]] teams have pulled from CKG3.5 as an offline topic list (~16k concepts)
3. Top 1000 most used topics in [[Express]] [[Recommendations Home|recommendations]]
4. (nice to have) Conducting offline [[Query Understanding|query]] analysis to identify high-frequency topics with quality associations from [[Express]] and Stock search logs.

With these methods we can quickly zero in on a short list of ~20k concepts which we will ground in CKG4 as a high impact, high quality sub-graph that can quickly be integrated into production features.
### How do we respond to feedback quickly?
Capabilities teams will conduct case-specific [[Evaluation|evaluations]] plans tailored to their particular applications. 
We will leverage the existing pipelines for adding and removing edges and concepts as feedback comes in from these teams. Both [[Evaluation|evaluation]] feedback and long-term maintenance will be handled through this tooling. There will be a ticketing queue with an SLA to make these changes in [[Intent AI Home|CKG]] 4.0.

