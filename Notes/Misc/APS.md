---
pageType: Misc
creation date:
tags:
Related Pages:
aliases:
  - APS Demo
  - APS
  - APS 2023
  - fy2026 aps
Wiki Link:
  - https://wiki.corp.adobe.com/display/adobesearch/Prompt+Intent+Classification+in+DocCloud
---
# Overview
Annual Product Strategy (*APS*) is a series of planning meetings, demos, and inter-team communications that *ideally* gets [[DMe]] teams on the same page for the coming year's priorities and product dev needs.

# FY 2026
---
This is the APS *for* 2026, being planned during November 2025. 

- [Deck link](https://new.express.adobe.com/id/urn:aaid:sc:US:061c895a-3857-5c19-8afa-cda687cc38ab?accept=true&category=search)




# APS 2024
---
## [[Express]]
- [[November 01, 2023#Andrei Stefan Andrei meeting/1x1]]
	- intent from canvas 
## [[Assistive Workflows & Multimedia Processing - Program Home|Assistive workflows]] 
- [[RAG]]
- [Wiki for PDF assist](https://wiki.corp.adobe.com/display/adobesearch/Prompt+Intent+Classification+in+DocCloud)
### Overview 
Annual Product Strategy (*APS*) is a series of planning meetings, demos, and inter-team communications that (ideally ;) ) gets [[DMe]] teams on the same page for the coming year's priorities and product dev needs. The demo portion of these meetings are meant to be a bit aspirational, and demonstrate use cases, tech, and ideas that could be valuable and doable in the coming year if selected. One such case is around the usage of Retrieval Assisted Generation (*[[RAG]]*) in [[Recommendations Home|DocCloud]]. 

This doc is not meant to say that the [[Intent AI Home|CKG]] team or SDC will commit to the features described, or that they're even a priority for [[Recommendations Home]]. The goal of the doc is to evaluate the feasibility of the feature if we decide to prioritize it in 2024. 

### Feature: [[Recommendations Home|PDF]] Assistant
**User Story**
 As a user who is editing a large [[Recommendations Home|PDF]] in [[Recommendations Home|DocCloud]] I would like to be able to quickly get insights about the contents of the document, edit the document, and get help using the [[Recommendations Home]] editor from an AI assistant. This way I can save the time and effort of having to go find specific content in the doc, search HelpX in another tab, or invest time becoming proficient with [[Recommendations Home|PDF]] editor. 

**Use Cases**
- Edit
	- Allow a [[Firefly|GenAI]] chat field to interpret requests to edit the document. 
	- eg. "Redact all numbers from this financial report"
- Search & Understand 
	- Allow the user to query the document or information about the document from the chat. 
	- eg. "In one sentence, what is page 4 about?"
- Help Doc 
	- Allow the user to query HelpX from the chat 
	- eg. "How do I use liquid mode when moving this image?"

**Intent Understanding's Role**
Intent services will assist with this feature by using the Query [[Type of intent|Intent Type]] work to classify prompts in the AI chat window along these 3 classes of request. This will provide prompt refinement for the [[RAG]] system to understand the intent of the request before the document or helpX is queried/edited. 

### Major questions 
1. What taxonomy changes would [[Query Intent Type|QIT]] need to fulfill this intent classification role in the [[Recommendations Home|PDF]] [[RAG]] feature? 
2. Do we have sufficient training data for these kinds of requests to confidently assign a prompt to one of these classes?
	1. if not, where would we get additional training/validation data?
3. What service would best handle these kinds of [[Query Intent Type|QIT]] requests? CGT, or some other service?


