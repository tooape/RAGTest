---
pageType: daily
aliases:
  - "2025-11-12"
created: "2025-11-12"
---
# [[November 12, 2025]]
# Notes
---

## Ps Web preset recommendations demo 
- Stage link
	- http://pr.photoshop.adobe.com/id?PR=70057&flags=acr_presets
- 
## Initial [[Lr Home|Lr]] reporting thoughts
- Date [[NER & SRL|NER]] is working great
- Most queries are 1 - 2 tokens
- `edited` is the most popular query, we need to strategize [[NER & SRL|NER]] for edited, and probably flags/picks. People are searching on these behavioral/culling signals
## [[Lr Home|Lr]] Desktop language support 
out of the [top 10 they want](https://adobesearch.slack.com/archives/C08BALVF7U1/p1762974495497959?thread_ts=1762497926.474059&cid=C08BALVF7U1), what do we do? 
1. Tier 1: everything ([[NER & SRL|NER]], embeddings, text)
2. Everything but [[NER & SRL|NER]]
3. Everything but [[NER & SRL|NER]] via machine translation (will incur latency hit)
4. Text match only 

# Meetings 
---

## [[Asim Kadav|Asim]] #meetings/1x1 

### [[Style Home|Photo styles]]
No one is on the same page on [[Style Home|style]]. Scheduled something. 

### [[Query Understanding|QU]]
- [[NER & SRL|SRL]] [demo link](https://pluto-prod-akadav-asim-qwq-anvexy-0-3000.colligo.dev)

MM model for swimlane 3 needs evals. 

### [[Photoshop|Ps Web]] presets [[Recommendations Home|recs]] demo
Rohith has a [demo video](https://adobesearch.slack.com/archives/C09NNC7SD6V/p1762370885851429) 


## Semantic Search v2 #meetings 

Sagar shared a [wiki with scope](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=OZ&title=Semantic+Search+v2+-+High+Level+Work+Items) asks for the Lr Desktop rollout. [[Lr Home|Lr]] Desktop wants to launch semantic search in April 2026 release. 
- Current est is 18B assets 
- [[Multi-Language 2025|Multi-language]] ask 
	- Requested languages
		- Fr
		- De
		- Es
		- Jp
	- Adobeone should be good here, but [[Query Understanding|NER]] support on the [[ILUP]] side is a question. 
- Smart album bug fixes will happen in V3 only, we'll not be fixing USSv2
- We'll need to understand how fast batch will get, using real-time processing will take 63 days at the sync 10k RPM limit in CPF. Offline batching will be faster. 

## [[Lr Home|Lr]] cost chat with [[Chhayakanta Padhi|Chhaya]] #meetings/1x1  
https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=LR+Cost+Optimization+Guide



## MERT GULSUN Interview #meetings/interviewer 

- [[2026 Summer Internships - Ritu's Team]]
verdict: no
### 1. Take me through your resume a little bit. 
German stem school, exp w google in EU. FinTech exp in prior internship. 

Lot of fintech and strat... 
Assessing data in banking
Loan pricing algo

Hackathon for DeepMind involving nanobanana, where you can sub people into photos.
- postcompose.com
	- segmenting people out of photos and remixing combinations and poses 
### 2. What drew you to the Product Management profession?
Ownership and seeing things end - to - end. Skin in the game. Consulting didn't own outcomes.
Defining metrics for what a V2 would be, before you make that V1. 
Checking back in on metrics and stats over time. 
### 3. What draw you to the search and AI space?
Pulled back in to tech. "Coming back home"
scraped EU regs and used GPT4 platform APIs, and pinecone to make a [[RAG]] app for a consturction project to search for rules and regs. 

### 4. Let's do a quick thought exercise, let's say the team has come to you with a new version of a model that they feel is ready to ship. How would you go about evaluating and shipping it?

- intent for text prompts for PS Assistant

**phase 1 saftey**
Benchmarking this V2 against V1, saftey and regs. 

**phase 2 effectivness**
Customer journey metrics, tractions stats. Have people used it in the past? Assumed an A/B test, but didn't spec it out. 
Are people actually using the intent models. 
Assuming there's UAT and behavioral sets in here... 

What are the signals you'd look for?
1. least words entered that gets to an action choosen 
2. Normalizing by length 

User concern about them having to type a bunch of shit in. 

### 5. Any questions for me? 
1. what's exciting to you about the next 6 months of AI 
2. what's the UX impact of these models taking 30+ seconds to do shit 
