---
pageType: daily
aliases:
  - "2025-10-07"
created: "2025-10-07"
---
# [[October 07, 2025]]
# Notes
---

Today I kind dove into using a [tiling window manager](https://nikitabobko.github.io/AeroSpace/guide) to go full nerd mode. 

## Graph work
- [[October 06, 2025#Query Understanding checkin meetings]]
- manual offline one off job of getting all the filterable fields in
- Topic [[Evaluation]] 


# Meetings 
---

## Team retro #meetings 

- [Easy retro link](https://easyretro.io/publicboard/2T4gVeIdcmh1GXwkOc47fAj3cAQ2/7772a7c8-1cf5-40bd-af58-84e3c1c0911a?list=false&sort=votes)

![[Screenshot 2025-10-07 at 21.33.18.png]]

![[Screenshot 2025-10-07 at 21.33.30.png]]

```
  Things That Went Well:
  - Internal team Collaboration & Delivery: Strong teamwork, collaborative culture, and successful delivery of multiple technical achievements (SRL for MCP, LoRAs, etc.)
  - Client Expansion: Onboarding new clients beyond Express
  - Production Progress: Fully transitioned to Pluto, increased production usage of Intent/CKG, and good incremental progress with Alpha releases
  - Leadership Alignment: Frequent sync with leadership on priorities and decision-making that enabled fast iteration

  Challenges and Lowpoints:
  - Resource & Staffing Issues: Team is highly under-resourced, needs hiring, staffing perception vs reality mismatch
  - Unclear Direction: Lack of clarity on goals, requirements, timelines, PRD, scope (especially for SRL), unclear end use-cases making evaluation difficult
  - Changing Priorities: Constant priority shifts, project churn, stop/start of new projects
  - Leadership & Collaboration Problems: Leadership & Architecture not taking responsibility for mistakes, not collaborative, unrealistic expectations, urgent requests without forethought
  - Technical Challenges: Extreme churn, architecture relationship difficulties, tech debt in graph and query understanding, GPU resources, issues with Mint
  - Process Gaps: Wins not celebrated, unclear NFR/SLA for productionization, requirements often architect-driven rather than product-driven

  Take Aways:
  - Communication Improvements: SDC's written communication and critical reading culture needs substantial improvement
  - Planning & Scoping: Early project planning needs better definition, clearer POC vs production feature distinction, alignment with PM/Arch on requirements before building
  - Resource Needs: Hire more people
  - Process Improvements: Better feedback loops (SRL client integration), project ownership per geo works better than cross-geo, aligning with PM/Arch on requirements speeds progress
  - Evaluation Challenges: Difficulty showing value when failures don't appear in larger eval results
```


## [[Asim Kadav]] #meetings/1x1 

- **Intent inference** 
	- multi modal modeling 
	- Grounding in the graph 
Swim lane 3 is going to be squarely on the intent team. There is a current model using data from [[stock]], [[express]] and MintV1. Evaluating pick up on christians work: 
- Updating from AdobeOne V1 → V2 
- We need to get the evals structured 
	- What is the current evals set and the current [[Evaluation|eval]] mechanism

- **[[Photoshop|PS Web action recs]]** 
	- Needs help from [[Lr Home|Lr]] side 
	- Rohit has gotten API access for [[Photoshop]] and now needs to export the preset data from [[Lr Home|Lr]]. 
	- There's a demo

- **Photo [[Style Home|style]]** 
	- Re-training for a side 
	- [[Evaluation|Eval]] on [[October 09, 2025]]

- **[[Lr Home|Lightroom]] Embedding evals** 
	- Getting the test bench built and starting to run the evals 
	- I need to make a wiki page for 
		- what models we want to test
		- our test queries 
		- the problem cases from [[Lr Home|Lr]] focus day 

## [[Subhajit]] #meetings/1x1 

1. Getting the one off adobe ecosystem data & Merging all the random off shoots into the main graph (new wiki)
2. Define Contributor flows
3. Validations and evals 
	1. Graph tiers
	2. End to end 
		1. do no harm, don't break existing use cases 
	3. On going validation as people add / change things 
	4. Running regression for the Tier 1 / tier 2 nodes after a change

## [[Kosta Blank|Kosta]] #meetings/1x1 

- For retro, what is the actual time scope? Since Q2 ([[February 28, 2025]] on?)
	- starting from [[SLM]] & [[Intent AI Home|CKG]] 4 

- Intent plan 
	- contributor plan 
		- tooling & automation 
	- graph plan 
		- Manual structures, metadata, top 20k intents 

- manual 
	- Making a node type for filters (metadata fields)
	- [[Core Affinity Framework|Affinity]] 
		- Intent Actions & [[Acrobat|DC]] verbs 

