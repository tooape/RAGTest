---
pageType: dailyNote
aliases: 
created: "1.22.2025"
---
# Notes
---

- [x] Figure out langauge AI 
	 - [x] Talk to Francois
	 - [x] Wikis 
- [x] Clarify [[Intent AI Home|SLM]] need
- [ ] A tech focused roadmap table 
- [x] Make ajira for this https://adobesearch.slack.com/archives/C05THFJ7A2Y/p1737591508079949?thread_ts=1737587855.379689&cid=C05THFJ7A2Y
- [x] move [[Intent AI Home|ckg]] checkin

# Meetings 
---

## Spellcheck #meetings 

- spellcheck is a null query fall back
- issue is results for misspellings are different than the correct spelling of the word. 

## subAgents #meetings 

[SDC agents and assistant wiki](https://wiki.corp.adobe.com/display/adobesearch/Proposal+%3A+Express+Assistant+SDC+Subagents#Proposal:ExpressAssistantSDCSubagents-OpenQuestions)

- Arch: 
	- ![[Sub Agent.jpg|800]]

Intent to action vs Intent services
I2A is an input to [[Intent AI Home|MINT]], which currently is it's own project. 

## Brian #meetings/1x1 



**Vic**
- i'll discuss: 
	- [[Recommendations Home|Contextual recs]] feature side
	- Style progress
	- Perosnalization sneak 


**Re-org**
- keeping style
	- thread w Ritu
- I2A


## [[Cherag Aroraa|Cherag]] #meetings/1x1 


[[Intent AI Home]] came from stock, as a pre-processor (QPS, query prosses serv)

- Dictionary
- Tokenization
- lemmitization 
- Spacy
- bablescape
	- Multilingual
	- Enriching [[Intent AI Home|CKG]]
	- Linking to [[Intent AI Home|CKG]]
	- [ ] Ask legal about using bablescape for shit 
- Jfast language detection 
	- Detect english 
- Spellchecker
	- Old
- [[Query Understanding|NER]]
	- Span detection
	- Rule based
	- this can be done with [[Intent AI Home|MINT]]
	- Leverage [[Intent AI Home|mint]] to ID exact semantic matches in the string using regex
	- no one uses [[Intent AI Home|CKG]] span
- Adobe one
	- outside [[Intent AI Home]] itself, but we can orchestrate requests over there through the orchestrator
		- Normalizes the A1 outputs into responses which are interpretable to the rest of the SDC stack 
- Orchestration 
	- [[Intent AI Home]] provides broad orchestration to other services, libraries and systems with response normalization which allows for interoperability with USS systems.