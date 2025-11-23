---
pageType: Misc
created: 2023-11-10
tags:
  - oldtags/vision
  - oldtags/CKG
Related Pages:
  - "[[CKG 2024 Strategy notes]]"
aliases:
  - CKG Vision
  - CKG Scope
  - CKG Mission
  - CKG roadmap doc
---
# Outline
- Context 
- Pie in the sky 
	- Mission & Vision 
	- Phases / Pillars of this 
		- Defining the core parts 
- 1H 
	- Define by problems we're looking to solve over the first half 
	- Break out by Cycle 
		- 6 -8 wk 
	- Explorations for 2H
- 2H Ideas 
	- Note about things changing 
- Scope limits and call outs. 

# Doc
## Context

### Understanding Creativity 
A [[Intent AI Home|knowledge graph]] is a structured representation of information, consisting of entities, and the relationships connecting them. Within SDC we've developed a graph known as the "Creative [[Intent AI Home|Knowledge Graph]] ([[Intent AI Home|CKG]])" as a way to better understand our users and how they work in our ecosystem. 

CKG is best thought of as a platform connecting three pillars of understanding:
1. Understanding of the creation, asset, or canvas that the creator is working on 
2. Understanding of the creator or communicator's behavior within one of our apps
3. Understanding around the applications, data, and services in Adobe a user has at their disposal 
#### Intent Services
All of this understanding and structured knowledge is just one part of the "Intent Services" which helps us understand our user's interests, actions, and intents. The platform consists of several services like:
1. **CKG (browse API)** is the graph itself, and can be viewed and queried from Elastic. This allows apps to navigate the structure of the graph and view the relationships between the different nodes, known as GlobalTypes (GTs). 
2. **Context -> GlobalType (CGT)** is a model for understanding intent and related assets or info based on contextual user information like searches, time of year, and location. 
	1. *adding MM here*
3. **Asset -> GT (AGT)** is a model for understanding intent based on Multi-Modal inputs like the colors, text, and icons placed on the canvas. 
4. **Query Intent Type (QIT)** is a model which helps us understand what the nature of a text query is from areas like information retrieval, help documentation, or creating a new document. 
5. **Query Product Intents Engine (QPIE)** is another model gives context about what products or features within the Adobe ecosystem are most related to the user's query. 

Together these constituent pieces add up to a platform which helps us understand the whole creative process. This understanding allows us to offer a superior experience, reduce the mental overhead and friction of creating, and allow for more exploration and ideation for creatives and communicators. While having this wide range of services is great for determining the intent of a user, but it creates a usability problem for internal teams. How to use what service, when to use them, and exactly how they interact is unnecessary compilation. To ease this load on internal dev teams, we've put them inside the **Intent and Language Understanding Platform (ILUP)**, formerly called "Morpheus".  This creates a somewhat opaque orchestration layer that gives teams a simple in I/O for getting intent understanding for their use case. ILUP also contains services like spell checker, named entity recognition, and language detection. The specifics of ILUP or all it's underlying capabilities aren't important for this document, but it is important to understand it's role as the orchestrator in our intent understanding system. 

![[Express User Graphic (5).png]]
[You can learn more about this platform here](https://wiki.corp.adobe.com/display/adobesearch/Intent+Understanding+Platform+-+Morpheus#IntentUnderstandingPlatformMorpheus-Components)


### Creator vs. Communicator
![[Screenshot 2023-12-04 at 11.04.45 AM.png]]
*Add contrast on user segment labels*


## Vision & Strategy 
### Long term 
#### Mission: 
Our mission represents the goal we intend to drive towards as a project. This creates a guidepost for us to refer back to when making hard decisions, faced with conflicting direction, and answering design questions. 

>To become Adobe's canonical source of understanding the creative process. 

I've specifically included all of Adobe in scope, but limited the mission to creative process. If a DX use case requires understanding of some creative process, we should in theory have that knowledge within intent services and we should be available for use in that case. But if that same DX team wanted us to get [[Personalization Home|user understanding]] in a context not related to creation, like admin tasks or data analysis, we would defer them to another team. 

#### Vision:
Adobe's vision is to "change the world through digital experiences". Adobe's brand has been synonymous with creation, art, and imaging for decades, and this vision statement speaks to that level of impact. Intent services' vision will need to rise to that same scale of opportunity since our mission statement leads us to a position of cutting across Adobe. In our vision statement we take a moment to consider "what will the state of Adobe once we accomplish our mission"?

> Our vision is to make creation with Adobe seamless, joyful, and nearly effortless.

If we had a perfect understanding of all three of the types of understanding laid out above; we would be able to create an ecosystem where the effort and skill required to complete a creative task within Adobe apps is dramatically reduced, if not completely eliminated. The world will never need less art or fewer creative voices tomorrow than it does today. As that demand and breadth of creative need continues to expand, Adobe's offerings will need to become not only more powerful but also much easier to use. Intent services has a critical role to play in maintaining Adobe's position as the foremost platform for creation in the coming years and decades. 

### In 2024
The two statements above a multi-year goals that we'll work toward over time. More specifically in 2024 there are a few key strategic decision that will help shape the roadmap that moves us in that direction. 

#### 1. [[Express|CCX]] will remain our primary focus 
As stated in our mission, we will have a future outside of [[Express]] as a more broad Adobe technology platform. The immediate future however will still be focused primarily on [[Express|CCX]] use cases, and will not invest substantial effort or energy in seeking out use cases in the core/flagship apps. There's a few reasons for this, but most importantly is that the Express use cases are relatively easier and less nuanced than the very granular and complex workflows and seasoned users of the flagship apps. Sticking to Express will help us focus our energy, and will allow us to look into the more simplistic use cases across disciplines that Express offers, before we try to tackle very complex use cases in the flagship apps. 

#### 2. Express caters to a wide (and growing) range of user segments, we will narrow focus on certain pseudo personas for 2024
Even when narrowing down from all of Creative Cloud, and setting aside the more advanced Creative Pro segments the range of users and expectations is huge. Express is also looking to expand the kinds of users it can handle in 2024 with improvements like Enterprise support for larger organizations to enable brand assets, and K-12 education users. Likewise, the kinds of creation possible in express is growing to include pdf and painting. To keep us focused and unblock us from ambiguity we'll focus on Communicators and some casual creators, rather than Creative pros. Solving for these users will give us a stepping stone to the more complex cases in enterprise user segments, and flagship app users. These users are also in the best position to be impacted by our work, since they're less likely to be highly proficient in Express itself, and are less likely to have a very crisp and specific vision for what they're working on. Any contextualization we can offer in the UI or asset exploration and discovery will be of huge value to them. This isn't to say we'll outright ignore other segments, and our work will be valuable to all Express users. This is just to say our energy will be focused on some sub-segments in order to narrow our focus. 

> “We discover how even the many good opportunities we pursue are often far less valuable than the few truly great ones." 
> - Excerpt from "Essentialism", *Greg Mckeown*


![[Paid CC Segmentation Next Gen.png]]
- [user segment wiki](https://wiki.corp.adobe.com/display/GMI/Paid+CC+Segmentation%3A+The+Next+Generation#PaidCCSegmentation:TheNextGeneration-AdobeCreatorSegmentation)

![[User Segment Graph.png]]

#### 3. Investing in ourselves
Intent understanding will require a very diligent and ongoing investment in our graph and models. While this comes at the tradeoff of not being able to work on as many production use cases, we view this time spent on our modeling, our graph, and our services as key to our becoming an essential part of CC as we stated in our mission. The graph and the services around it are like a flywheel we're putting energy into, and drawing energy out of over time. 

## Roadmap 
### 1H 
- 6 - 8 wk cycles of 3-4 sprints 
	- 1 core issue being solved in each 
		- A few things to hang our hat on 
	- 2nd tier of [[issues]] below that 
		- Use cases
		- Improvements 
		- ops excel. 
	- Platform investments 
		- data we want 

**Where will accomplishing these points leave us?**

**How will we manage KTLO of prod use cases?**


*Cycles of 6 wks ( 2 per qtr) *

|                                                          | Cycle 1 (Jan - Mid Feb)             | Cycle 2 (mid Feb - march) | Cycle 3 (march - Mid April) | ... |
| -------------------------------------------------------- | ----------------------------------- | ------------------------- | --------------------------- | --- |
| ** One win we're taking to Production**                  | recs                | In editor media recs                          |                             |     |
| **Problems we're looking to invest in solving Big Bets** | Coverage                               | [[Style Home]], usability                          |                             |     |
| **Internal improvements & platform evolution **          | Multi-modal | Multi language                           |                             |     |


### 2H 
- Themes 
- Touch back on our 2024 strategy points from above. 

