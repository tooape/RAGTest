---
pageType: dailyNote
publish: false
aliases:
  - 01.3.2024
created: "01.3.2024"
---
# January 03, 2024
---

## stock entities #meetings 
- long term we need stock to be able to return MM intents for stock images 
	- title, image, metadata etc

We don't want to change stock ingestion because we believe we can make good contributions to [[Recommendations Home|contextual search]] without it while allowing CKG to make fast iterations in coverage and evaluation methodologies. 

Hypothesis: 
We believe that we can make meaningful contributions to [[Recommendations Home|contextual search]] use cases without indexing GTs into the stock index. 

this also frees us up to better derive intent at query time based on MM data from the query. 
eventually we might want GT, but not intents 

examples of why we don't want to search for intents but would like to return the associations. 
- does a stock image of a laptop have an explicit and useful intent, or the power of associations with "business" or "technology"
- illustrator "cat", "dog", 
for templates the metadata sucked, for stock the metadata is more mature 


