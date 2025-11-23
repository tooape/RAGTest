---
pageType: daily
aliases:
  - "2025-09-17"
created: "2025-09-17"
---
# [[September 17, 2025]]
# Notes
---





# Meetings 
---

## [[Tracy King|Tracy]] #meetings/1x1 

- Evaluating CKG4

**[[Query Understanding|QU]]**
- [[Core Affinity Framework|action affinity]]
	- https://wiki.corp.adobe.com/display/adobesearch/Proposal%3A+Intent+Action
	- https://wiki.corp.adobe.com/display/adobesearch/Intent+Action+Requirements
- sub prompt 
- topic Extraction 

Putting the [[Query Understanding|QU]] work into the white papers: 
- intent white paper from [[Ayush Jaiswal|Ayush]] 
- [[Jayant Kumar|Jayant]] is doing [[Intent AI Home|CKG]] 

putting the scope for action intent / [[Core Affinity Framework|affinity]] etc into these papers ^ 


**[[Express]] home screen redesign**
- for "coffee shop flyer" the [[Core Affinity Framework|affinity]] will be 99% templates but we'll want to show [[Icons]] or something, but we wouldn't want to just blast the query into [[Icons]] corpus directly, what we actually want is kind of a contextual rec where you just want mugs and lattes 

**[[Style Home|Style]] re ranking in contextual [[Recommendations Home|recs]]**
- we had an issue with [[Style Home|style]]-ranking by [[Style Home|style]] because the [[Recommendations Home|contextual recs]] query had such large recall that ranking this recall set by [[Style Home|style]] would show stylistically similar irrelivant results. mixing the [[Style Home|style]] signal with the textual relevance 

high precision ranker for fetching a specific recall set.
We'd need an actual relevance score, some way to cut a recall set to then throw over to [[Style Home|style]] ranking. We do not have an interpretable relevance score. 


## [[Brian Eriksson|Brian]] #meetings/1x1 

For [[Style Home|style]] what is the prod experience? We wouldn't be able to cache 

P0s for [[Brian Eriksson|brian]] 
- Enterprise [[Recommendations Home|contextual recs]] 
- Migrating away from [[Intent AI Home|MINT]]

## [[Ritu Goel|Ritu]] #meetings/1x1 

- [[Query Understanding]] and agents
	- I'm concerned about having so little concrete direction

GPU asks: 
- do I need to mention [[Style Home|style]] more?

**Lightroom** 
Formalizing the cost w Lr team