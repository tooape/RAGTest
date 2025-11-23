---
pageType: dailyNote
publish: false
aliases:
  - 01.5.2024
created: "01.5.2024"
---
# January 05, 2024
---

## [[Recommendations Home|USCD]] & [[Intent AI Home|CKG]] Sync #meetings 
- currently stage isn't using the latest MM model 
	- 


## [[Recommendations Home|Contextual Search]] [[Evaluation|Eval]] plan 
Wiki link 

Overview 
As a first step in our strategy to power [[Recommendations Home|contextual search]] and disc. use cases, we're going to provide contextually relevant media recommendations. This will give users collections of images from stock, based on the inferred intents from their template. 
Over the past couple months we've created Demo UIs to work on this: 
- [[Evaluation|Eval]] UI in the USS Explorer 
	- This allows us to browse templates from production (including dynamic collections like Seasonal and popular) and judge the intents for each, as well as see the image results from stock for the given intent. 
- POC UI 
	- This is an integration of intent understanding built into the staging [[Express]] UI, and allows us to better understand how the systems work together. 

This page outlines how we'll use the [[Evaluation|Eval]] UI to run manual scoring of template -> intent results. It should be noted that this manual evaluation (aka online evaluation) will be done in parallel with automated evals using GPT on larger sets of templates (aka offline [[Evaluation|eval]]). 

Methodology
Data sets
Since manual [[Evaluation|eval]] is time consuming, we'll focus on the seasonal and popular sets of templates. These are templates that get used in production by communicators every day and a good test set for us to understand the experience. 

Scoring 
We're looking to get [[Evaluation]] on two things: 

Relevance 
"Out of the top 5 intents, how many are relevant to the template?" (1 - 5)

Ranking 
"Is the top intent the most relevant out of the 5?" (y / n)

## [[Ravindra Sadaphule|Ravindra]] #meetings/1x1 

- Tactical stuff
	- I'm working on the plan for the eval doc
	- I'll review your edits/comments on the stock entities stuff 
- how do we best work together
	- I feel like I’m chasing engineering
		- By the time I get a plan on paper or req for some project number 1, engineering is asking about project 2 
	- trying to get out ahead more by putting a vision and a strategy around the whole intent mission with a roadmap doc 
	- Mind if I add a recurring 1x1? 
- QIT on roadmap around assistive generation / assistive creation 

- helping on evals 



## CC spending : 
![[UFCU transactions.csv]]
- **Uncategorized**: $124.00
- **Food & Dining**: $1,110.91
- **Transfer**: $147,690.12
- **Home**: $10,582.48
- **Bills & Utilities**: $1,161.39
- **Financial**: $12,700.75
- **Shopping**: $130.18
- **Auto & Transport**: $13,810.91
- **Health & Fitness**: $651.00
- **Taxes**: $26,150.00
- **Fees & Charges**: $0.32
- **Business Services**: $27.92
- **Personal Care**: $2.00
- **Travel**: $25.27

These totals represent the cumulative spending across different categories based on the provided transaction records.