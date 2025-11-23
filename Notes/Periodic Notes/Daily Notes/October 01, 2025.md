---
pageType: daily
aliases:
  - "2025-10-01"
created: "2025-10-01"
---
# [[October 01, 2025]]
# Notes
---

Email reply to [[Acrobat|DC]]

Hi Vikas, 

We've been running some evaluations on a new intent system to better handle the Acrobat workflow. We've completed a few rounds of evals now and the improvements look like they're working, so we're deploying these changes to production. We'll still need legal approval however, and are working through the PLA for this change currently. We will update you later this week with our progress on the deployment and the legal sign off.

Best, 
Ryan Manor



# Meetings 
---

## [[Subhajit]] #meetings/1x1

[[Vipul Dalal|Vipul]] wants:
- [[Intent AI Home|CKG]] plan 

## [[Tracy King|Tracy]] #meetings/1x1 

Putting the node tier in the metadata.
Considering adding [[Express]] [[Recommendations Home|recs]] to the use case list
- since we only care about the graph and not mapping in 
- Take the top concepts and the associations as a sub graph and test it 
	- We know we're going to want to move this use case over, start testing the graph before we have the inference 

For additions and edits to the graph 
- What are our SLAs,
If someone wants a new affinity hierarchy, how would we respond to that. 
Where does this fit in, what is this new concept? What are the correct edges? 
"This connection is just wrong"
Who is the sign off for this? [[Francois Guerin|Francois]] and I? Venkat? [[Jayant Kumar|Jayant]]? 

For spotting wonky (lake mountains) nodes we could look at the occurrence of that exact phase within the query logging. 

**Graph tooling**
We have atomic adds, edits, and deletes of nodes and edges but we do not have: 
- Inference debug 
- Graph search 
- Graph association nav
- Metadata view


Write the spec for a V1 graph browser & search 
V2 - bubblespace node name, and the visualizer 

## Recommendations standup #meetings 

- we're deploying to prod today for the new intent system
	- Still pending legal review 
- IBM issue 
	- Where are the assets? AEM? Stock?
	- What do you want? 

## [[Intent AI Home|CKG]] testing #meetings

better call out the goal of bringing people back into [[CKG 4.0|CKG4]] and validating the graph is ready for prime time. 

Call out Mintv2 testing, and MINTv1 vs V2

Calling out the secondary goals 
- of figuring out inference strategies for different use cases / text lengths 
- Mintv2 testing
	- and MINTv1 vs V2


**Goals**
Quickly get [[Intent AI Home|CKG]] ready for the "prime time", with secondary goals of understanding the optimal strategies for difference use cases like short vs long text.

Here, "prime time" means that we're able to certify that for the high touch, critical parts of the graph which are used in use cases like [[Recommendations Home|contextual recs]] or unified search topic extraction are accurate and high quality. 

We're not looking to evaluate the whole graph, or test it's completeness of world knowledge. Testing the graph on the whole is going to follow this exercise. 

3 tiers of nodes
1. top 1k hand checked 
2. top 20k semi-automated 
3. --Scope line for this project-- 
4. Automated graph maintenance

