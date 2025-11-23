---
pageType: Misc
creation date: 2023-10-25
tags: 
Related Pages: 
aliases:
  - EOY plan
  - 8 week plan
---
# 8 week plan
- [Wiki page](https://wiki.corp.adobe.com/display/adobesearch/CKG+Platform+Improvement+-+EOY+2023)
---
## Coverage and Evaluation improvement 
---
[Jira link](https://jira.corp.adobe.com/browse/SEARCH-41140)

Work:
- Automation 
- Coverage level by different thresholds 
- Multi-modal coverage scores 

## Graph Enrichment
---
### Expanding Node count 
[Jira link](https://jira.corp.adobe.com/browse/SEARCH-39273)
- [wiki link to the coverage reporting](https://wiki.corp.adobe.com/display/adobesearch/CKG%2C+Intent+and+Language+Understanding+Platform+Capabilities)
- MISC 
	- We need to focus on quality of these intents, we should not be looking to MISC for arbitrary node growth 
 
### Making the graph more navigable & usable for users 
[Jira link](https://jira.corp.adobe.com/browse/SEARCH-33861)
- Hierarchy (3.4)
- Seasonality (3.4)

### Increasing density of the graph
[Jira link](https://jira.corp.adobe.com/browse/SEARCH-31551)
- intent -> Ingredient (photo, element, fond, textlockup, etc)
- Intent -> Intent 
	- Embedding based similarities
 
### metadata availability at inference time 
[jira link](https://jira.corp.adobe.com/browse/SEARCH-41146)

- Standard metadata fields 
	- Synonyms 
		- top x, based on bablescape 
	- Trending / social score
		- different than the SEO score? could we use the SEO score to do ranked 
	- Legal approved
	- User displayable
	- Punt on language 

## Multi-modal & Template [[Evaluation|eval]] 
---
[Jira link](https://jira.corp.adobe.com/browse/SEARCH-31549)
- Use AdobeOne model
- The focus here is on quality of intents returned, speed is a problem we can fix later if need be. 

## [[Query Intent Type|QIT]]
[Jira link](https://jira.corp.adobe.com/browse/SEARCH-41141)
- Classifying a query by type
- Identifying when CKG is even relevant to the user's need 
	- and if so, what is the categorical purpose of the query 
- Demo Needs 
- Rename

## Compositionally design 
---
- Write user stories here
- as a user I would like to be able to get a more nuanced understanding of my users action's as they navigate 

## AGT/CGT service changes 
---
- Explore function 
	- Hardcoded value where they just say "explore = true"
	- per request where they can specify a value 
