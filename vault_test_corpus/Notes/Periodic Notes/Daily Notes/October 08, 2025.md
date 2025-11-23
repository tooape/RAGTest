---
pageType: daily
aliases:
  - "2025-10-08"
created: "2025-10-08"
---
# [[October 08, 2025]]
# Notes
---

- [[Obsidian Web Clipper]]



## Aerospace app name list 

```
aerospace list-apps
```


# Meetings 
---

## Working lunch about the graph and CKG4 [[Evaluation|eval]] 

### Deliverable 1 - Prod ready graph 
We'll prioritize by the following levels of service, and index these as node metadata. 

- Tier 1 - Adobe Ecosystem 
	- Filters
	- [[Core Affinity Framework|Affinity]]
	- Actions
- Tier 2 - Top Concepts 
	- Across locations, topics, scene objects, events, colors, etc
	- Top 20-25k by prod usage or importance 
- Tier 3 - Rest of the graph 

### Deliverable 2 - Tooling 
- Node & Edge additions 
- Node & edge remove marker 
- Metadata edits & updates 
- Visualizer
	- search, metadata view, edge traversal 

### Deliverable 3 - Evals 
- [[Evaluation|Eval]] 
	- Use case agnostic evals 
	- Use case specific 
- Grounding and post-processing 
- Edge type conditioned retrieval 
	- Allowing use cases to request edge types of interest 
	- node re-ranking & selection 

## Retro feedback with [[Tracy King|Tracy]] and the architects 
- Separate [[Intent AI Home|CKG]] from intent as a workstream 

### Takeaways 
- A triad conversation between the architect, the PM and the team lead/EM
- More rigor and expectation of well written requirements, decisions, and tradeoffs. And more expectation that these artifacts are read. 

## Legal review for [[Acrobat Contextual Recommendations|DC]] #meetings 

- Mexican fast food and LGBT 

## [[Ayush Jaiswal|Ayush]] #meetings/1x1 

How the use case team ([[Acrobat|DC]] studio) will be making the actual query so that we can understanding the end-to-end in [[Query Understanding|QU]]. 
- What are their evals 
- We can flag issues or gaps 


[[NER & SRL|SRL]] is in good shape, working on v5 of the model. 
Sub-prompt isn't in as good of a place, unclear req. 
Need to talk to [[Jay Manish Sampat|Jay]] and them on where sub prompt is. 

### Contribution model 
The big thing will be getting the tooling right, this solves the easy stuff like dupes, etc.

The bigger issues will be more foundational changes like new or different edge types, where only sanity checks are needed. 
We need a strong, opinionated take here, and changes would require our direct sign off. 

We need a big opinionated document of unbreakable rules. We are the owners of the full view of the graph. 
Changing definitions for one use case would be breaking on other use cases, and we have to own that oversight. 

The expectation needs to be set that the inference and the mapping is still separate from the graph itself...

### Program and structure 
in 2026: creating clear work streams or tracks for the graph, for inference, for other things will help people make things clear. And making the trade offs more clear of what we're not working on. 

Making the trade offs of pivots clear in PgM reviews with leadership. 

Stronger requirements intake and formalization to stop Venkat from seagulling random engineers. 

