---
pageType: daily
aliases:
  - "2025-09-23"
created: "2025-09-23"
---
# [[September 23, 2025]]
# Notes
---





# Meetings 
---

## [[Vic Chen|Vic]] catch up #meetings/1x1 

Contextual recs [[Style Home|style]] ranking, and sending a single asset... 



## Program Q4 Overview #meetings/pgm 

**[[Recommendations Home|Recs]]**
- Combine to one list 
- Make a call out for the optimizations on [[Recommendations Home|recs]] for stuff like deboosting [[Recommendations Home|recs]] people never use, text handling, etc. 

## [[Intent AI Home|CKG]] 4 and [[Intent AI Home|Mint]]  / [[Kosta Blank|Kosta]] & [[Tracy King|Tracy]] #meetings 

Writing the actual wiki page → [[CKG4 productionization planning]]

**Questions from Q4 pgm meeting**
1. How can we groom and validate a useful subgraph of [[Intent AI Home|CKG]] such that we can start using CKG4 in prod in Q4?
	1. What's already been curated
		1. [[Core Affinity Framework|Affinity]]
		2. Getting topics & associations 
			1. start with [[Brian Eriksson|Brian]]'s [[Acrobat|PDF recs]] offline side graph (16k?)
			2. Top hits from current [[Express]] [[Recommendations Home|recs]] 
			3. Offline query analysis for high freq topics and association quality 
2. How can we get the MM model ready for use by capabilities?
	1. MintV2 visual is the eventual solve here
	2. Adding the decoder models
3. Use case specific [[Evaluation|eval]] plan by the capabilities teams?
	1. How do we respond to improvement requests?
		1. Existing pipelines for removing and adding edges and concepts
4. Long term, how do we update and contribute to CKG4 quickly?
	1. Existing pipelines for removing and adding edges and concepts

**Messaging and callouts**
- What do we do about side graphs 
- What is the guidance for adding to 3.5 vs 4
	- Nothing in 3.5
- [[Intent AI Home|Mint]] V2 - what is it, what's it doing? Is it the new MM model? Update to old model?
	- LLM → Embedding similarity to *a* graph (3.5 or 4)
	- Still text only 



One new page for [[Query Understanding|QU]] productionization, following the same 