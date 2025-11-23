---
pageType: Misc
created: 2023-08-28
tags: []
Related Pages:
  - "[[August 25, 2023]]"
aliases:
  - graph coverage
  - ckg coverage
---
---
# [[Intent AI Home|CKG]] Baseline - [[August 28, 2023|8.28.2023]] @ 10.00 am - Misc
---
## Defining coverage 
This doc outlines the methods and data we'll use to evaluate the variety as well as the complexity/nuance of user intents that [[Intent AI Home|CKG]] is capable of assigning. This effort is meant to serve two purposes:
1. A confidence score of productionalizing some new use case in one of our apps/surface
2. A consistent set of criteria to measure iterative improvements made to the graph over time

### Intent Criteria 
- A query is considered covered if we can connect it to a known intent in our graph, with a score >0.X 
	- Multi-Intent: if we can return 2+ intents with a score >0.X 
	- We should only be considering `INTENT` nodes
		- not others (`DESIGN_TYPE` , `BACKGROUND` , etc.)
## Context -> GT Evaluation
We should evaluate using the top 10k query terms on each: [[Express]], Stock, and a.com, [[Lr Home|Lightroom]]
- Coverage will be measured with a few stats, described below in the reporting section

### Reporting
This evaluation should be run every week (or at least month), and we should be able to recall any given prior report. This will allow us to evaluate the performance of the graph, and the improvements over time. As well as give us an indication of when the graph is diverging from user behavior and corrective actions are needed in response. 

The report should address the below data:
- Total % covered 
	- We should be able to sub divide this into 3 buckets in order to make better decisions and not simply take a high total % as "good enough"
		- Head % covered 
		- Torso % covered
		- Tail % covered
- Multi-Intent 
	- The % of cases where we were able to assign 2 or more intents over our score threshold 
- w/w Change in overall intent assignment %
	- Do we really need per score change? For graph regression/divergance alerting maybe? 


| Query Surface | Overall Intent assignment % | Head % | Torso % | Tail % | Multi intent % (overall) | w/w Change % |
| ------------- |:---------------------------:|:------:|:-------:|:------:| ------------------------ | ------------ |
| [[Express]]  queries |             x%              |   x%   |   x%    |   x%   | x%                       | +/- x%       |
| Stock         |                             |        |         |        |                          |              |
| Lightroom     |                             |        |         |        |                          |              |
| a.com         |                             |        |         |        |                          |              |
|         **Overall**      |                             |        |         |        |                          |              |

## Asset -> GT Evaluation
Take top 10k Templates (by remix count?) and run a similar report on the number of templates we're able to get a highly confident intent for. 

| Query Surface | Overall Intent assignment % | Head % | Torso % | Tail % | Multi intent % (overall) | w/w Change % |
| ------------- |:---------------------------:|:------:|:-------:|:------:| :------------------------: | :------------: |
| [[Express]] Templates  |             x%              |   x%   |   x%    |   x%   | x%                       | +/- x%       |

## Evolution of the process 
Over time we'll add more rich reporting here to cover these areas in more detail, and to cover new areas of the graph. 
- Using popular / trending templates for evaluation 
- User meta-intent 
	- Quick actions, etc 
- Temporal data 
	- Holidays 
	- other 
- Composed intents 

## Appendix 
What this score is not: 
- a guarantee of completness 
- a replacement for A/B testing in prod
- a scope to be burned down 
	- 100% coverage is not in and of itself something that might be valuable 
	- These metrics are indicators of a good graph, not the end all goal, or something to be exhaustively pursued to completion 

### Social Benchmarking 
In addition to understanding our ability to confidently assign intent within our platform we should also be evaluating outside

Channels: 
- Google Trends 
	- Canva queries 
- FB/Twitter

Need to specify query set here