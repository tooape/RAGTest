---
aliases:
  - NER
  - CAF
  - Core Affinity
  - user action intent
  - QU
  - Pre-processing
pageType: programHome
---
# Query Understanding Home
---

Lead by myself, [[Subhajit]], and [[Jayant Kumar|Jayant]].


**Links**
- [[SDC Query Understanding wiki]]
	- [[Multi-modal Intent and Content Understanding wiki]]
	- [[CKG4 Production Testing wiki]]
	- [[Query Understanding Planning wiki]]


# Overview
Query Understanding encompasses 6 main models, or systems. 
## 1. [[Core Affinity Framework]] 
Gives directional understanding of a queries affinity to content, products, tools, or Help at 3 levels of granularity. 
- [[FY25 Core Affinity Framework Requirements wiki]]
## 2. [[NER & SRL]] 
Identifies tokens which are explicit mentions of key data like Date, People name, and more. These are use case specific but all are served from [Intent Services](app://obsidian.md/Intent%20AI%20Home).
- [[FY25 NER and SRL Requirements wiki]]

##  3. [[Intent AI Home| Intent Understanding]] 
Canonicalization of user intents and concepts within the query, document, artboard, or prompt.
- [CKG 4.0](https://wiki.corp.adobe.com/display/adobesearch/Node+and+Edge+evaluations+task+tracker)  
- [MINT](https://wiki.corp.adobe.com/display/adobesearch/FY25+Mint)

## 4. Intent Action
Classifies natural language queries into predefined tool actions (e.g., COMBINE_FILES, REMOVE_BACKGROUND) and extracts refined subprompts by removing metadata to isolate core search terms.
- [[Query Understanding - Intent Action and Subprompt Extraction Using SLMs wiki]]

## 5. Semantic Topic Extraction
Extracts structured semantic intent from user queries, organizing them into categories like Topic, Design type, Background, and Color to better understand user needs.
- [[Intent Understanding Semantic Topic Extraction model wiki]]

## 6. Multi-modal Model
A foundational multi-modal language model for intent and content understanding that supports downstream tasks like LoRA fine-tuning, automatic tagging, and multi-modal content retrieval, grounded in [[Intent AI Home|CKG4]].
- [[Multi-modal Intent and Content Understanding wiki]]

