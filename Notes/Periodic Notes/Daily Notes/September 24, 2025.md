---
pageType: daily
aliases:
  - "2025-09-24"
created: "2025-09-24"
---
# [[September 24, 2025]]
# Notes
---


- [Creating SRL golden set data](https://wiki.corp.adobe.com/display/adobesearch/SRL+Golden+Data+Creation+Instructions)
	- [Excel](https://adobe-my.sharepoint.com/:x:/p/ayushjaiswal/ERlPiEwJfnlDiW1oaJ9teMYBss1YnPpbMnk5mF-Xz0gJIw?e=QdET57)

- [list of all SDC legal and ethics reviews](https://wiki.corp.adobe.com/pages/viewpage.action?pageId=3228938871)



# Meetings 
---

## [[Recommendations Home|Recs]] standup #meetings 

[[Josep]] has a [[Personalization Home|personalization]] demo


## [[Lr Home|Lr]] metadata [[Query Understanding|NER]] training #meetings 

- Shooting settings
Should have a list of known vales from prod index

- Equipment
	- Camera model
	- Lens model 

The challenge here is the different variations in the ways the values are indexed, and the ways people can type them. 
"mk2", "mk II", etc.  

they want to train a model or a lora head on mistral 7B / Llama 1B here for the shootings settings. 


## [[Brian Eriksson|Brian]] #meetings/1x1 

**His corpus understanding demo**
how do we bring in the knowledge of [[Intent AI Home|CKG]], how do we get additional signal from the corpus, how do we layer in [[Style Home|style]] and personalization... 

The ultimate goal here is to have Ps as an art tutor sitting there saying "you're too formal, let's try experimenting with more abstracted colors" or "add some foreground interest, here's coral or fish", 

**[[Style Home|Style]]**
[[Style Home|Photo styles]] 
Canonical [[Style Home|style]] 
what was jeff talking about this morning.
How do we get josh bought in 

**recs and CKG4**
traversal vs just topics ID
enterprise assets and decoration of assets 

## Ayush #meetings/1x1  

- SRL isn't responsible for sub prompt, it will not be predicting asset name 
- looks more like creating filters 
[[Asim Kadav|Asim]]'s nomic embeddings are basically duplicative of SRL on intent team, we're ok with they hybrid approach of using both

Restructuring the monday meetings to be more representative of the progress made in the roadmap. 