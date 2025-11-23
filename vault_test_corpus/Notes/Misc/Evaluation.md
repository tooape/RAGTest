---
pageType: Misc
creation date: 2023-12-12
tags:
  - evals
Related Pages:
  - "[[Intent AI Home]]"
aliases:
  - evaluation thoughts
  - eval
Links:
  - https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=CKG+EOY+Improvements
---
# Evaluations 
---
## Info
 I view Evaluation and graph quality as a pipeline that starts at data ingestion and modeling, and goes all the way through to the inference and ranking on the production surface. 


- new ingestion pipeline 
	- ![[CKG Ingestion Pipeline.png]]


## Eval Playbook 
Evaluation and graph quality are a pipeline that starts at data ingestion and modeling, and goes all the way through to the inference and ranking on the production surface. Here we'll focus on establishing some high level processes and rules for the Online & Offline evals. These evals take place after the pipeline above has been run, and changes to the graph or the inference models have been made. 

### Offline Methodology (Automated)
##### Query 
As outlined [here](https://wiki.corp.adobe.com/pages/viewpage.action?pageId=3049987747), we'll be testing queries across a.com, express, and stock. These scores will be broken up into head, torso, and tail, by dividing the ranked list of all queries (by freq) and taking 5,000 random queries out of the top, middle, and bottom third respectively). These queries will be processed by LLM for semantic completeness. Meaning that none of the semantic meaning of the original query was lost when compared to the resulting nodes that were returned. 
- A query considered covered if the **LLM verifies that more than 100% of semantic information was identified** by the model
- By utilizing hierarchy, metadata, and query preprocessing **the final result will be able to consist of multiple node types** (intent, design type, backgrounds, scene objects, etc ) _instead of top 1 match in current coverage calculations._
- LLM based methods to **quantify the amount of data lost/preserved on average** in large samples, and provide meaningful statistics, to help understand the overall accuracy as well as pinpoint weaknesses in the system.
##### MM 
In order to accurately judge intent usefulness, we utilize GPT4 to do relevance judgements on a set of intents, given the document. We utilize a **1-5 scale** for relevance computation, in line with [existing research](https://arxiv.org/abs/2303.16634). The scale is chosen since GPT was trained on a lot of relevance tasks requiring a score from 1 to 5, hence is claimed to be more adept at assigning scores in that range.

We utilize the following hyperparameters while evaluating:

- p=1 - Most likely token is chosen
- temp=0.5 
- n = 5 - Each row is judged 5 times. We take the average score
- max_new_tokens = 5

### Online Methodology (manual)

#### Internal 
- We'll use the [USS Explorer](https://visual-ckg.corp.adobe.com:8080/) to evaluate template -> intent.  

#### External 

### Data sets 
#### Images 


#### Templates 

**Popular** 
1. Extract the top 30000 templates by popularity for the week of the evaluation.
2. De-Duplicate the overlap with the seasonal 5k
3. Select the top 1500 templates by popularity count.
4. For the remaining 3500 templates, take a stratified sample of all remaining popular templates.
**Random** 

**Seasonal**
1. 
1. De-Duplicate the overlap with the seasonal 5k
  
| Eval sets | Sample size | Eval metric | Priority | Links to eval |
| ---- | ---- | ---- | ---- | ---- |
| Popular EN templates | 5K | Relevance score of top 5 intents | P1 | Appen |
| Seasonal EN templates | 5K | Relevance score of top 5 intents | P1 | Appen |
| Popular FR templates | 5K | Relevance score of top 5 intents | P2 | Appen |


## [[Recommendations Home|Contextual Photos]] [[Evaluation|Eval]] plan (Feb 2024)
What's next after the associations analysis. 

### Week of the 19th 
- Analysis of associations 
- Proposed changes to query 
- Proposed usage of when we would / would not show image  
	- [Wiki](https://wiki.corp.adobe.com/display/adobesearch/C2.2+Template+to+Association+Internal+Evaluations#C2.2TemplatetoAssociationInternalEvaluations-Non-ImageIntentFiltering)
- Plans for next round of evals 
### Week of the 26th 
- Demo to [[Express]] team 
- Collab with Josh and stock / Stock ranker team 
- Finalize changes to query / QIT 
- Prep new eval
	- End to end in ckg uss demo ui 
### Week of March 4th 
- Run next round of evaluation 
### Week of March 11th 
- Go / no Go decision on relevancy 

### Week of March 18th
- go / no go on completion of v1 scope 

### Lessons from evals 
- Need to add intent context to the stock query 
- [Need to think about when we wouldn't use an image](https://wiki.corp.adobe.com/display/adobesearch/C2.2+Template+to+Association+Internal+Evaluations#C2.2TemplatetoAssociationInternalEvaluations-Non-ImageIntentFiltering). 


## Links 
- [[Jayant Kumar|Jayant]]'s [EOY 2023 Ingestion wiki](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=CKG+EOY+Improvements)
- 
