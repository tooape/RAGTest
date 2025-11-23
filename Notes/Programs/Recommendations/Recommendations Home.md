---
creation date: 2023-09-14
tags:
aliases:
  - Unified Search
  - Contextual Discovery
  - contextual search
  - recs
  - recommendations
  - contextual recommendations
  - contextual recs
Links: []
Wiki Link:
  - https://wiki.corp.adobe.com/display/adobesearch/Adobe+Express+Search+and+Discovery+2023+Roadmap
pageType: programHome
Related Pages: []
protected: true
---
# Recommendations Home
---

- Contextual recommendations [program wiki](https://wiki.corp.adobe.com/display/adobesearch/SDC+Program+Adobe+Content+Recommendations+FY25)
- [Contextual recs analytics dashboard](https://app.amplitude.com/analytics/adobe/dashboard/6be35a0y)
- [API Docs](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Express+-+USCD+Integration+API+Calls)

# 2025
---
In 2025 there are 2 major areas of expansion for recommendations, the surfaces we display recs on, and increasing sophisticated these recs are with new tech. 

Recommendations surfaces:
- [[Express]]
	- Search tab & All tabs
- [[Acrobat Contextual Recommendations|Acrobat]] Recommendations
- [[Photoshop]] 

tech investments
- [[Personalization Home]]
- [[Style Home]]
- [[CKG 4.0]]

# Prior Years
---
## 2024
### Tools & Actions
People are fine with recommendations on edits and changes, in part or in whole but it needs to be good. 
- personalized 
- "like it's trained on their own content"

**Links**
- [Prioritization wiki](https://wiki.corp.adobe.com/display/adobesearch/Design%3A+Contextual+Search+and+Discovery)
## Visually cohesive, Contextual editor recs 
### Links
- [[[Vic Chen|Vic]]'s jira ticket](https://jira.corp.adobe.com/browse/CCEX-63145)


- [Eval wiki](https://wiki.corp.adobe.com/display/adobesearch/Evaluation+-+Contextual+Media+and+Elements+Suggestions)
- [Req Wiki](https://wiki.corp.adobe.com/display/adobesearch/Use+Case%3A+Contextual+Media+and+Elements+Suggestions+In+Express)
- [Architecture wiki](https://wiki.corp.adobe.com/display/adobesearch/Design%3A+Contextual+Search+and+Discovery)
- [Andreis photo recs Wiki](https://wiki.corp.adobe.com/display/adobesearch/Express+Editor+Contextual+Browse+and+Search+for+Media+and+Elements)
- [SDC Roadmap wiki](https://wiki.corp.adobe.com/display/adobesearch/Adobe+[[Express]]+Search+and+Discovery+2024+Roadmap)
- [[Andrei Stefan 1|Andrei]]'s [[APS]] deck](https://adobe.sharepoint.com/:p:/s/adobesearch/EVCtFvwxJypFkagfwDaEB_EBW8zO8jpSHrNkpDhwFSwNQw?e=UqH3Q7)
[[Express Editor Media Search.png]]

- [x] Add some info here about the quality of associations and how we might quantify that


### Roadmap

**Feature brief**
[[Express]] makes substantial use of Stock for it's element library. The range and depth of Adobe stock can be overwhelming for C-pros, let alone the [[Express]] persona of Communicators who are less proficient in our tools and design practice generally. This lack of expertise combined with a more limited set of discovery tools in [[Express]], and users find themselves confused and lost looking for content in [[Express]]. This ultimately undermines [[Express]]' value prop as a fast, easy, lightweight creation tool for non-pros to get simple tasks done. 

> How might we improve the discoverability of individual elements within Stock in the [[Express]] editor, so that users do not need to spend time or brain power digging through the ocean of assets available? 


*The below all assumes we're done with working specifically the demo and are looking at building the feature itself.* 
#### Stage 1 - Bare bones Recommending elements 
- NFR
	- Speed up retrieval  
		- Leave the stock query perf to the stock folks, focus on the intent/MM speed
	- Timeouts
		- [[Query Intent Type|QIT]], MM, etc 
- Element classes provided
	- photos, [[Icons]], design assets, *shapes*, and backgrounds 
- *[[Query Intent Type|QIT]] ranking of element classes* 
	- Deploying to [[Intent AI Home|MINT]]

#### Stage 2 - Improving experience & Cohesion
- Better query strategies 
	- intent -> association 
		- thresholding / exploration logic 
		- Better deny list 
	- Template -> Association 
		- Strategy for evaluating signal/understanding gained by going directly to the graph 
- Consistency of exp 
	- As elements change and we refresh intent, how we we keep a logical through line and not confuse 
- Improving relevance & quality of associations 
	- Excel Evaluation 
		- For each of the top 100 templates, return the top 5 associations. For each intent, top 5 intents for each association
			- Deduplicate intents 
			- judge associations as `good` or `not good`
	- Setting up [[Communicator Behavior Signal|user heuristics]] 
		-  What are the user behaviors we expect to correlate to a good result?
			- [[Communicator Behavior Signal]]

##### Canvas to Intent: Second and third order intent
*Manually curating intents/associations which must be returned given some intent (post-processing)*
In any canvas there's likely more than one intent at work. Consider "UT Spanish Language Learners Meetup" where we have a university (UT), a group of people (Spanish Learners), and an activity (Meetup). 

Eg: 
![[Screenshot 2024-04-17 at 11.18.26 AM.png|500x500]]

This same pattern will play out for any [[B2B]] use cases:
![[Screenshot 2024-04-17 at 11.35.56 AM.png]]

In order to provide good results in contextualization, we must be able to show recs for these other intents at work. We'll tip toe into [[Compositional intents|compositionality]] here, by first simply ranking the multiple intents which may be relevant, and then interleaving results. This is a rudimentary approach, but given the use case of contextualizing elements, we can get away with it. 

For example in the running examples above, the ideal exp for users would likely be to have the editor recs show mostly running stuff, then some other more generic sport fashion stuff, then a couple sale/promo things. We should draw the line at 2 or 3 to avoid getting noisy results. This will need some additional thinking for multi-page canvases ([[Express Presentations|presentations]], etc) about how to take the pages in unison vs independently. *Multi-page can be out of scope for now, and we can take each page independently.* 

##### Intent to Association Quality 

**Thresholding**
The preference for this capability right now is towards precision and relevancy. If we do not have many recommendations to show, we shouldn't show random concepts for the sake of filling out a recs list. In the event we cannot get more then X associations of an acceptable quality (*up for discussion on how we define those stats*) we'll either show nothing from our contextualization and fall back to the default collections, or add default collections to the limited number of associations we do have. 

Longer term (ie. out of scope for now), we will develop selective exploration capabilities to consider the confidence/similarity score of an association and when it's below some threshold we'll then navigate up the graph hierarchy to look for broader concepts to show. 

**Deny & Conditional Deny list**

##### Association to Element Quality & [[Color]] Cohesion 
**[[Color]] Cohesion**
Need to understand the difference between background and accent [[Color|colors]]. Given a template like the below, there's a clear [[Color]] pallet at work. Being able to identify this is step one. After we've identified the [[Color|colors]] at work, we'll need to identify the role they play in the overall canvas. For instance here, while there is a lot of yellow in the cavnas, it's a background [[Color]]. Elements like design assets and [[Icons]] will likely be either orange or pale blue. 

![[Screenshot 2024-04-23 at 10.33.38 AM.png|500x500]]

A note on dithering: 
We shouldn't be overly precise here. 

- Avoid naming them or displaying [[Style Home|style]] terminology 
	- Taxonomy/language needs to be worked out, will take time 

#### Stage 3 - Pushing to Prod

- [[Communicator Behavior Signal|MAB]] Schema & Collection pipelines ready 
- Rollout strategy 
	- Feature flagging?
- Infra scale up 
	- Our side

Data capture: 
- segment (EDU, [[B2B]] etc)
- language
- region 
- intent survey 
	- onboarding quiz 
		- 60% completion 
		- Why are you coming here, what are you making, aesthetics 
- CC entitlement 
	- C-pro
- Element additions and editor UI interactions is logged 
	- Might be able to get export rendition 
	- Export is part of doc model 


#### V4+ 
##### Going [[Communicator Behavior Signal|MAB]] 
Optimization engine 

**Addtl. Use cases**
EDU, brand aware, etc. 

- Brand aware is basically just a separate subset of data to draw out of for element query, this is conceptually similar to recommending the users own content from [[Artemis]], GDrive, [[Lr Home|Lr]] Catalog, etc. Our focus will be on solving "How does a user bring their own asset repo into [[Intent AI Home|MINT]]?"
![[Screenshot 2024-04-17 at 11.09.41 AM 1.png]]


**Relevance and exp**
We would expect that that this point improvements in the stock data, [[Express]] data, our models and the graph in other areas ([[Compositional intents|compositionality]], further aesthetic understanding) would improve the experience here almost automatically. 



## Home & SRP
- [[Query Intent Type|QIT]]
	- Quick action
	- tools
	- templates
	- images, etc
- [[Express Category Exploration Pills|Category pills]] 
	- PLG group test 
- [Intent based query suggestion](https://wiki.corp.adobe.com/pages/viewpage.action?pageId=2950819298)
- 
#### User level req for photos 
- [PRD Wiki](https://wiki.corp.adobe.com/display/adobesearch/In-Editor+Contextual+Media+Recommendations+Requirements)

![[Express photos Contextualization_.png]]




## Query suggestion 
[Proposal from [[Josep]] & [[Sanat Sharma|Sanat]] for query suggestion](https://wiki.corp.adobe.com/display/adobesearch/Contextual+In-Editor+Intent+Understanding+and+Recommendations)



## Examples 

Good ones 
- Wedding save the date urn:aaid:sc:VA6C2:daeff84a-419a-42e6-8f5d-70019e978f0b
- NYE party urn:aaid:sc:VA6C2:7ccbc40b-5d23-49e5-81b2-23e6c174e45c
- Fall Fest urn:aaid:sc:VA6C2:186ac659-75e7-4b8b-ada2-4c91cddaedad

[[Style Home]] use case:
- urn:aaid:sc:VA6C2:d7288b0d-4d59-4479-8fb5-8fec9b057142
- urn:aaid:sc:VA6C2:3bf36b59-f0ff-4b7a-9f79-24bad46b0508

[[Compositional intents|Compositionality]] case:
- urn:aaid:sc:VA6C2:43c57a8f-bda8-4155-9717-31350f39dcd7

Semantic ambiguity 
- urn:aaid:sc:VA6C2:db71ee14-2d17-474d-be3f-0423f6109bf3
	- "compact" as in the makeup item, not making something small
	- "face mask" is like a facial peel, not a PPE mask

## Roadmap thoughts 

One of the big ideas in the [[March 26, 2024#Content Roadmap deep dive|2024 content roadmap deep dive]] was the idea of creating delightful content with minimal editing. This is corollary to some of what I've been working on with the [[CKG 2024 Strategy notes|ckg roadmap]]. I think this can get broken down into some constituent pieces: 
- hmw allow for better exploration of ideas






