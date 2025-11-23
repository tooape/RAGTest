---
created: " 2025-11-12"
pageType: misc
datelink: "[[November 12, 2025]]"
Related Pages:
  - "[[Lr Home]]"
---
# Overview 
Targeting April 2026. 

# Relevance 

## Embedding testing 
- [[Chhayakanta Padhi|Chhaya]]'s [wiki](https://wiki.corp.adobe.com/pages/viewpage.action?pageId=3640037052)

### Candidates
LLM as a judge testing the quantized and unquantized versions of: 
1. [[AdobeOne V2]] 768
2. RAE
3. Matryoshka 
	1. 768
	2. 512

Once we do this, we'll select 2 or 3 candidates for online / human evals. 

**Callout on mobile clip**
We should index the test catalog on mobile clip and load this as a separate exp directly in discovery hub. 

### Eval set 
Continue to use test catalog and query sets from prior evals. 
- Single and Multi-token queries 

## [[NER & SRL|NERs]]
Camera model and Lens model [[NER & SRL|NERs]] are currently in progress. Once these are complete we should work on Edited, exported, and picked. 

## Recall 
The feedback that our recall is too large has come multiple times, we need to close down the recall more elegantly. 

## Fine tuning failure cases from A1V2 768
- ID the queries and catalogs that failed and fine tune on selected embedding strategy above. 

# Engineering & Cost
Migration of ~20B existing user assets as one-off migration from V2 → V3 
https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=LR+Cost+Optimization+Guide


# Bugs and Smart Album improvements 
- [SEARCH-41514](https://jira.corp.adobe.com/browse/SEARCH-41514) - Search by incomplete filename finds 2 results, not 3 or more
- [SEARCH-45611](https://jira.corp.adobe.com/browse/SEARCH-45611) - Search: IMG filters properly, but only for two images.
- [SEARCH-45612](https://jira.corp.adobe.com/browse/SEARCH-45612) - Search: Behavior different for files that start wit 5D4 vrs IMG
- [SEARCH-45613](https://jira.corp.adobe.com/browse/SEARCH-45613) - Search: File extension must be removed to find file.
- [SEARCH-43225](https://jira.corp.adobe.com/browse/SEARCH-43225) - P: Allow Search By Year/Month/Day

# AutoComplete

We'll need to continue to support autocomplete as it is in [[Lr Home|Lr]] today. 

![[Screenshot 2025-11-12 at 15.02.24 1.png]]
>How might we support Autocomplete from the normal V3 index, and not a separate one? 
> Would [[Lr Home|Lr]] team be ok with a search-as-you-type implementation instead?

The existing autocomplete is more of a facet value browser than anything. Could we replicate or replace this functionality? 

# Language support 

[[Lr Home|Lightroom]] supports multiple languages via [external docs](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=photo&title=Lightroom+Ecosystem+Language+Support). The [top 10 are](https://adobesearch.slack.com/archives/C08BALVF7U1/p1762974495497959?thread_ts=1762497926.474059&cid=C08BALVF7U1): 
1. English
2. German
3. French
4. Japanese
5. Portuguese
6. Spanish
7. Korean
8. Dutch
9. Italian
10. Polish

There are 3 questions to answer here: 
1. What is [[AdobeOne V2|AdobeOne]]'s support for these 10?
	1. Can we show NDCG for non-english vs. english to quantify the relevance drop for each?
2. What data is req'd to support [[NER & SRL|NERs]] for these languages? 
3. For languages not supported by [[AdobeOne V2|AdobeOne]], or [[NER & SRL|NER]], what is the best mitigation? 
	1. MTS at query time 
	2. Text matching only 
	3. Tagging
	4. other
