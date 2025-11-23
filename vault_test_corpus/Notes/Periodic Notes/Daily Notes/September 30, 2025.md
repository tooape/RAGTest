---
pageType: daily
aliases:
  - "2025-09-30"
created: "2025-09-30"
---
# [[September 30, 2025]]
# Notes
---





# Meetings 
---

## CKG4 and Grounding #meetings 
 
 [[Subhajit|Subhajit]] has made a knowledge graph grounding demo with CODEX KG demo project and t-SNE plot 

generative retrieval, passing gradients 
## [[Lr Home|Lightroom]] Roadmap #meetings 

**Relevance roadmap**
- Recall is biggest issue
	- only change we can deliver by max is bumping the static threshold up a bit (0.25 → 0.26, 0.275, etc) 
 
**Prod readiness**
We'll not be ready for [[October 10, 2025]]
CAT is slow to scale up (5-10 min for new containers)
- Ops is the long pole
	- service now, CSO and DR plans, NewRelic, etc. 
- Perf testing and latency testing will be done by [[October 03, 2025]]

## [[Kosta Blank|Kosta]] #meetings/1x1 

- We got [[Ravi]]'s buy in on evaluating [[Acrobat|DC]] [[Recommendations Home|unified search]]. 
- Sameep said there's no real [[Evaluation|eval]] strat worked out for disc agent, but they do have demo UI. 
- I need to get some time with [[Francois Guerin|Francois]], [[Tracy King|Tracy]], and [[Jay Manish Sampat|Jay]] to talk about [[Evaluation|eval]] design 


**Needs**
A way to visualize the step by step: 
1. Input → [[Intent AI Home|MINT]] ([[SLM]]) → [[Intent AI Home|CKG]] 
	1. being able to triage where a crappy result is coming from 
2. navigating the graph 
	1. Visualizing the graph
	2. searching the graph 
3. [[Intent AI Home|MINT]] should have an /explain or some debug mode
	1. grounded, top 5 ungrounded, and a level or two of associations 


## AI Foundations #meetings 

