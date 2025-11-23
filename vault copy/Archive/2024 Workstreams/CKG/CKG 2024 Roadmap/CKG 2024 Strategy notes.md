---
pageType: Misc
created: 2023-09-27
aliases:
  - ckg roadmap
  - ckg strategy 2024
  - roadmap 2024
  - 2024 strategy
  - 2024 roadmap
  - 24 roadmap
tags:
  - oldtags/misc/product
Related Pages:
  - "[[Intent AI Home]]"
  - "[[CKG Vision Crafting  - 8.11.2023 @ 09.42 am - Misc]]"
  - "[[CKG Vision Doc]]"
Wiki Link:
  - https://wiki.corp.adobe.com/display/adobesearch/Intent+Understanding+Strategy
---

# Use case & Eng themes 
---
These product focus areas are in ranked order of impact and importance, and represent the rubric for evaluating our work on [[Intent AI Home|CKG]] and intent understanding. 

## Use case themes
### 1.  Relevance & Recovery 
First and foremost we'll be looking for use cases which allow us to improve the relevancy and the recall of queries in [[Express|CCX]]. This extends beyond the home page search, and just template search. 

#### Relevance & Recovery Use cases
- Template search expansion 
	- As a communicator trying to create a new file in [[Express|CCX]], when I search for a template and see that there are no available results, I would like to be shown search results for related queries for related concepts that do have results. This way I can see if there's anything close enough to my desired template that I may be able to customize myself and continue with my creation journey. 
		- "College swimming tourney" -> swimming, college, sports, pool, etc
- Files search
	- 85% of CC users are on a personal license, and are unlikely to have good file structure in their cloud storage. 
- Collection ranking 
	- a query for "dog image" should be recognizable as a query for an image asset, and templates and video [[collections]] should be displayed lower on the page. 

### 2. Recommendation & Suggestion


#### Recommendations & Suggestion Use Cases
- As a communicator working on a project but struggling to find the correct elements to put on my chosen template I would like to see contextually relevant backgrounds, videos, graphics, textlockups, and media that will give me quick access to relevant assets in making my project.
-  [[Element and media search demo - 8.30.2023 @ 02.32 pm - Misc]]

### 3. Action 
Finally we have scenarios where we might be able to intuit an action or desired outcome the user is looking to accomplish, and shortcut their navigation of the app to achieve it. Here, we see the "search box" getting turned into something closer to a command palette once we've understood the intent as some action. 

#### Action use cases
- As a communicator who's looking to find a project file I was recently working on, i would like to be able to use the search field to quickly jump to the projects matching my search without having to scan through results for new templates, images, etc. 
- As a communicator looking to understand when I will be billed for my premium membership next, I would like to be able to use the search box to ... 
- As a Communicator who would like to generate a new image, I would like to be able to input my prompt as a request in the search and not have to navigate to a specific prompt input for this. 
- As a Creator who is looking to perform an action in a core app, outside of the capabilities of [[Express|CCX]], I would like to be able to search for my desired action from [[Express]], and be taken to the related functionality directly in the core CC app. This way I can perform 


## Engineering themes 
---
### 1. Expanding and improving the graph 
As the number of use cases that intent understanding supports expands, and the need for more nuance in intent understanding grows, the graph will need to improve commensurately. The data in the graph, the schema it uses, and the associations between nodes is worth investing in heavily as the quality of this graph becomes an asset we'll use in every new use case we enable. Like an investment that requires some initial deposits, but pays out over time and returns more than was put in. 

### 2. [[Multimodal intent|Multi-Modal]] 
The DMe product portfolio extends across many asset types and modalities of creation. We'll need to factor these into our understanding of intent in order to sufficiently understand what it is the user might be looking to do. Text, photos, illustrations, videos, [[Audio]], and 3D will all need to become part of our intent understanding. 

Text and image remain the top two, video is fast approaching as a need. 

### 3. Contextual understanding 


## Intersections of work
---

|                             | Expanding the graph | Contextual understanding |  multimodal embeddings |
| --------------------------- | ------------------- | ------------------------ | ---------------------- |
| **Relevancy & recovery**        |    By improving the quality of our nodes, and associations we can have a positive impact on the precision or recall of more queries.                  |                          |                        |
| **Suggestion & Recommendation** |                     |                          |                        |
| **Action**                      |                     |                          |                        |


# Vision Ideation 
---
This doc will need to speak to things bigger than individual surface integrations. Or at least offer some framework for codifying those integrations into ranked thematic buckets.
- The matrix of the eng tasks and the product use case pillars below will help establish this. 

Describe the roadmap in 8 six week segments instead of quarters? 
need to include scope limits and team charter 

- [[Chris Hedge Mentorship - 11.9.2023 - meeting]]

### Notes from the [[CKG EOY 8 week plan|8 week plan]] meeting on [[November 03, 2023|11.3.2023]]
- We're unlikely to escape our prod commitments being large time sinks for us 
- We're unlikely to avoid shifts in direction and priority coming at us from production or from [[Express]] 

I'm kind of lead to believe that an annual or quarterly roadmap will not be successful here. In order to handle these conditions we're going to need to remain stable in our vision towards the future for [[Intent AI Home|CKG]], but we'll need to be flexible in how we're working to get there. 
- A series of 6 and 8 week plans that speak to how [[Intent AI Home|CKG]] might need to evolve 
- A vision doc or team charter statement


### Needed docs
- Problem definitions / OKRs/ etc
- Major investments / bets we want to make long term 
- series of Cycle over cycle accomplishments 
- Vision 



Scope of the document: 
Just [[Intent AI Home|CKG]] stuff, not all of ILUP 

- Think about the vision and goal setting 
	- in scope
		- The graph 
		- Intent Services 
		- Production support 
			- Escalation path through [[Intent AI Home]]/AIO etc. 
		- APIs
	- out of scope
		- ILUP functionality 
		- non-[[Express]] app specific functionality 
			- I'll talk about non [[Express]] use, but not individual apps. More of a high level thing across the portfolio 
	- Our future inside and outside of [[Express]] 

- [[Intent AI Home|CKG]] Is the official user intent/context understanding platform for [[Express]]
	- Productionalized high value use cases 
		- Some flagship feature we can “hang our hat on” 
	- Regression A/B tests where we remove [[Intent AI Home|CKG]] from certain queries? 
- *We maintain a high degree coverage* / association density even as node counts grow and user query behavior shifts around 
- [[Intent AI Home|CKG]] should be an engine of understanding. 
	- The graph itself might always need manual curation but it should not require constant management and curation to be effective in prod 


## Mission and Vision 
> The brain, like arms and legs, consumes caloric energy. Before computers, _computer_ was an occupation. Humans were employed to compute. We asked these humans to eat food, so they could power brains, so they could run mathematical calculations, so that… so that…
> Now we use electric energy instead of caloric energy to move atoms and compute bits.
> The things that only calories can do are becoming fewer. We choose to delegate more of the caloric work to the electric muscle and brain.
> The caloric world is beautiful. We choose to freely live in the caloric world. We enjoy hand-kneaded artisanal bread. We enjoy running through the woods to work off those calories, mostly.
> Electric energy gives us the power to make things that no muscles were ever tireless enough to make. That no brains were tireless enough to compute.
> Electric energy gives us the freedom to choose how we use caloric energy, because caloric energy is precious.

### Mission Statement Ideation 
- Be the designated standard for user intent understanding for [[DMe]]. 
- Serve as the canonical source of truth for understanding user intent in DMe. 
- Give DMe apps and services a nuanced and accurate understanding of what their users want to do. 
- Provide understanding of user intent to DMe through a portfolio of AI powered services and data mode
- To become the canonical source of understanding user action and creative intent in DMe. 

### Vision Statement 
What will the state of the business be after you accomplish your mission?
- Once we accomplish this mission, creating with Adobe apps will be accessible, joyful, and nearly effortless.

### Breaking down the mission statement
How do we get to "*a nuanced and accurate understanding of what their users want to do*"? What are the elements of a system that does this?
- Powerful and easy APIs
	- Low friction for implementation by surface teams 
	- High availability 
- Clear, convenient, and concise data 
	- Intents are easily consumed by surface teams 
	- Intents are appropriate/useable for the given use case 
	- Associated data is relevant 
- A rich/complete graph 
	- A graph that covered the breadth, and depth of creative work. 
	- A graph that has enough metadata to power complex surface app experiences 
	- A graph that has the kind of density needed to explore and inspire the user of the surface app
- Accurate results 
	- Here "accurate" means our returned intent is true to the user's actual intention in that specific interaction 
- Functionally relevant 
	- Surface app teams will need to be able to adapt, or extend what we have to suit their more specific needs. 



## [[Express Roadmap - 11.14.2023 - meeting|Express roadmap deck]] 
- 

## Discussions with [[Vipul Dalal|Vipul]] & [[Ritu Goel|Ritu]] 

### [[Vipul Dalal|Vipul]] 
![[November 15, 2023#Notes]]


### Thoughts on our convergence with Art 
![[November 28, 2023#Stock thing meeting]]

In recent discussions with [[Vipul Dalal|Vipul]] we're starting to converage on what [[Intent AI Home|CKG]] is in an abstract sense and what it represents to adobe. As quoted above [[Intent AI Home|CKG]] is, in essence, an interpretive platform connecting three pillars of understanding:
1. the creator or communicator's behavior
2. the applications and services of Adobe 
3. the creation the creator/communicator is working on 
[[Intent AI Home|CKG]]'s maturation then can be thought of as improving our intelligence along these three axis. Services like CGT would align with the user behavior, [[Query Intent Type|QIT]] and [[Product Action intents - 9.26.2023 @ 01.45 pm - Misc|PAI]] along the Adobe platform, and AGT within the creation space. 
In maturing these 3 pillars we'll run into a wide range of questions, issues, and decisions about how to process. For instance, right now [[Query Intent Type|QIT]] might have knowledge of [[Lr Home|Lightroom]] but does it understand when a user might want to apply an exposure curve? Is it even important that it knows this? 
To address these questions we'll need to consider what it is [[Intent AI Home|CKG]] will be, or what we might want it to be. Thinking about our mission/vision above we have very lofty goals. While we consider only the communicator use case right now (communicators being a less sophisticated, and sometimes orthogonal persona to a creator), our mission will eventually put us in front of creators, themselves being varying degrees of hobbyist to serious artists. 

![[Express User Graphic v2.png]]
Adding [[Recommendations Home|PDF]] here ^ 

Our understanding completness or nuance will vary for each of these disciplines 

The first and second pillars are relatively easier, or at least more deterministic and quantifiable. Pillar 3 is where we'll need to put more consideration, as this eventually becomes a discussion about art and culture.

Pro birthday card designer case (explore vs. exploit )



# Roadmap Ideation 
[Andrei's photo recs Wiki](https://wiki.corp.adobe.com/display/adobesearch/Express+Editor+Contextual+Browse+and+Search+for+Media+and+Elements)
[Express Roadmap wiki](https://wiki.corp.adobe.com/display/adobesearch/SDC+Express+Project+X+Prioritization+FY24)
[Andrei's APS deck](https://adobe.sharepoint.com/:p:/s/adobesearch/EVCtFvwxJypFkagfwDaEB_EBW8zO8jpSHrNkpDhwFSwNQw?e=UqH3Q7)
## Production use cases & Powering contextual disc 
[Andrei's req wiki](https://wiki.corp.adobe.com/display/adobesearch/Express+Editor+Contextual+Browse+and+Search+for+Media+and+Elements)

#### In editor contextualization - Media Collections
- Powering Media contextualization 
	-  >5 collections 
	- [[Audio]], Video are secondary 
	- First 3 or 4 photo results will be displayed when the collection is collapsed 
- Powering the other ingredient tabs are secondary 
	- Design assets
	- Shapes
	- Icons 
#### [[Recommendations Home|Contextual search]] and browse
- [Andrei's PRD](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Express+Editor+Contextual+Browse+and+Search+for+Media+and+Elements)
- [[Query Intent Type|QIT]]
	- Quick action
	- tools
	- templates
	- images, etc
- [[Express Category Exploration Pills|Category pills]] 
	- PLG group test 

#### [[CKG Query Suggestions|Query suggestions]] 
- [Intent based query suggestion](https://wiki.corp.adobe.com/pages/viewpage.action?pageId=2950819298)
	- SEARCH-43342

#### [[Artemis]] (from your content)

#### Text to template

#### Category browse pills 

#### Intent aware autocomplete
- [[Intent Autocomplete]]


## The big bets in our future 
- [[Product Action intents - 9.26.2023 @ 01.45 pm - Misc|QPIE]] / [[Query Intent Type|QIT]]
- [[Personalization Home]]
- [[Style Home|Style]] 
- [[Compositional intents|Compositionality]] 
- [[UG graph updates]]
	- Nodes & training assoc. 
	- Trending nodes
	- [[Color]] or [[Style Home|style]] trends
- Model service 
	- rolling CGT & AGT up into one service 
- [[Multi-Language 2025]] 
	- Ideas from a conversation with [[Tracy King|tracy]]
		- ![[November 17, 2023#Tracy King Tracy conversation meeting/1x1]]
- [[Exploration]] / Multi-armed bandit
	- Inspiration
- 


A lot of the long term stuff seems to be the graph improvements or at least related to beefing up the platform. 

Short term wins: 
- [[Recommendations Home|Contextual photos]] 
- Contextual ingredients
- [[Express Category Exploration Pills|Exploration pills]]

