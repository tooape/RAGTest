---
pageType: daily
aliases:
  - "2025-10-13"
created: " 2025-10-13"
---
# [[ October 13, 2025]]
# Notes
---

In general as the NER & Query Understanding platform starts to take more shape in production, the foundational intelligence will be design to bias for recall. Meaning that in a query like beaches in the summer the expected date NER would be Jun - Sept for any prior year, and then it's up to the use case team to take those results and cut down to 2025 if they want current year only. 

## Lightroom roadmap 
Directionally: 
1. Embedding improvements 
	1. Comparison (RAE, mobile clip, matryoshka, etc.)
	2. Fine tuning 
2. Camera and lens NER
3. Location and people 
4. Single word improvements 
	1. RRF with CAT and embeddings? 

# Meetings 
---

## Intent Swimlanes #meetings 

Swimlane
![[Screenshot 2025-10-13 at 10.55.41 1.png]]


## [[Ritu Goel|Ritu]] #meetings/1x1 

**Managing the Internship**
- Hiring and interviewing kick off 
- I'm on board
- I'll start thinking about projects 
Trying to close it fast... we'd want to send an offer before winter shutdown. 


**Intent Testing**
We want a pilot use case to target, we're going to pick contextual [[Recommendations Home|recs]]. 
We understand the mission of building for everything but in order to give focus and get something shipped we need that pilot case. 


Start with testing everything. Then go down to "what are we going to do in Q4?" Don't communicate hero use case first. 

To have cross surface evals, you need cross surface sets. 

EG: 
What if we were going to power:  
- MM search (find similar)
- Contextual recs
- Agentic

If we wanted to go across C-Pro, Creator, etc segments, how would we prepare the data? 


Cross use case eval is the point... 
^ this may not be sufficient for going to prod, and we'd want to eval for an individual feature to ship, but we're going to do broad coverage. 


Making sure we have data for the date conflict thing with Jay, where "summer" could be any year vs this eyar. 

INtent team will provide any year, and then the use case team will need to probvide their specific interpretations. 


