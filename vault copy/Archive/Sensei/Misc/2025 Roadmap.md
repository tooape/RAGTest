---
created: 2024-08-22
tags:
  - oldtags/roadmap
aliases:
---

# High level
## New Modalities & content types 
---
[[Express]] has added capabilities for new types of assets, templates, and projects. From simpler elements like animated stickers, and charts, to [[Audio]] and Video modalities. Offering a symmetrical experience across these modalities is important for the user exp in [[Express]]. 

**Impacted User exp:**
- Recs possible for animated video templates
- Able to recommend other asset types 
	- Templates, [[Audio]], [[typography|Fonts]], Animated stickers, etc. 

### Milestone 1: Video template intent inference 

### Milestone 2: [[Audio]] recs 


## [[Personalization Home|Personalization]]  
---
 We'll look to start making an impact on the explore/exploit problem by incorporating user signal for preferences around assets, templates, and other elements in our contextualization. Signals like assets added in my prior projects, or earlier in the current session, things i've added to my favourites, recommendations i've been shown before but never interacted with, etc can be leveraged to create better performing results sets across search and recs. 
Consider the primary KPI as CTR of search and recommendations, with a secondary metric of assets added in sessions which included an export.

### Milestone 1: In session behavior
Leverage Mirai to capture signals like. Geo, query, asset clicks, etc. 
- [x] Slack Tal and ask about the signals they're looking at 

**Use Cases**
1. Ryan logs into [[Express]] and makes a search for "Diwali invite cards". He doesn't see anything he likes and decides to start from blank. He chooses the vertical format canvas and goes to the editor. Once on the editor he makes a search for "lamp" in design assets. *How might we rank results for open flame lanterns and lamps higher than electric desk lamps with lightbulbs in search results?* 
2. Chad googles "halloween party invite" and clicks on an [[Express]] [[Express Traffic Growth - Program Home|SEO]] page containing templates for halloween. He finds one he likes and decides to start editing his specific details into the canvas. He sees "Ideas based on your file" in the photos page and finds one collection called "party".  *How might we display the top asset in this collection as something Halloween related rather than a more generic or non-seasonal party? 


### Milestone 2: Segment
subgroups of EDU (teacher / student, grade range, etc) are the main priority. 
[[B2B]] groupings are behind this. 

**Use cases**
1. Amy is a high school teacher creating a sign up sheet to print out and hand to students for this fall's homecoming dance at her school. She goes to [[Express]] and searches for "sign up sheet". She finds something with some of the fields she needs but it's quite plain and generic. She adds the text "fall dance" as text on the page. She then notices a row of collections called "ideas based on your file" in the design assets tab. The first collection is called "party". *How might we bury results which depict more adult oriented parties, alcohol, and other contextually inappropriate visuals in this collection?*
2. Kaden is a 2nd grade student at Lamar Elementary who has been given an assignment to create a presentation about Biology. He goes to [[Express]] and creates a project from blank and then adds the text "The 5 senses". He then sees a collection in [[Recommendations Home|contextual recs]] for "Eyes". *How might we make the assets in this collection less realistic, and potentially gross or inappropriate for a young child?*
	1. Cecelia is a College Freshman in Bio 201 creating a slide deck for an assignment about the human visual system. *How might we show her more anatomically correct assets than we showed Kaden?*

### Milestone 3: Inter-session behavior
Favs, prior projects

**Use cases**
1. Aiden is a chairperson of their local Out in Tech (a meetup group for LGBTQ tech workers) chapter, and they would like to create an instagram reel with the details about this months happy hour. They've done this for the last few months and have used the "favourites" feature in [[Express]] a few times to save some of their favourite assets. They've added quite a few design assets which all feature bold, bright [[Color|colors]], and depict drinks, disco balls, and speakers. 
	1. *How might we depict assets with a similar visual [[Style Home|style]] in other categories/collections?*
	2. *How might we rank these specific assets higher in the relevant collections as the go through the editor creating this new reel?*
	3. *How might we how them assets with a different "look" in these same thematic categories (drinks, disco balls, etc)?*
2. Every month on the 21st, Tianna needs to create a new pool party poster for the student activities council at the University of Texas in Austin. She regularly uses a collection of assets depicting people in sunglasses laying on pool loungers. She logs into [[Express]] and creates a new project, adds the text "Student activities council Pool party". *How might we boost the assets for the collection "pool" that she used previously?*
3. Fahd is a manager at a fin tech company who sent a "month in review" email to his team at work last month and it was well received. He'd like to keep it up and goes back to [[Express]] to create a new highlights asset for this month. 
	1. *how might we recognize the pattern as he adds inner text and understand what kinds of assets he added last month but alter the specific assets returned within those thematic categories?* Dithering use case etc, he doesn't want to repeat basically the same email

## [[Style Home|Style]] Understanding 
---
Anything which involves creativity will incorporate some [[Style Home|style]]. [[Express]] users are inherently less adept at navigating these visual languages given their relative lower experience with design and creativity than C-Pros. We can augment this lack of knowledge by building [[Style Home|style]] understanding into [[Intent AI Home|MINT]]. 

### Milestone 1: Asset Similarity 
Given a source asset, and a query; rank the results from the query by their visual similarity to the reference asset. 

**Use cases:**
1. Replacing canvas elements
2. [[Style Home|Style]] ranking V1 (just ranking the assets in [[Recommendations Home|contextual recs]] by their aesthetic similarity to the last asset added)

Use cases: *Contextual bar, [[Recommendations Home|contextual recs]]*

### Milestone 2: Hz document visual similarity
Given a set of reference assets, and a query; rank the results of the query by their visual similarity to multiple reference assets. 

**Use cases:**
1. Sorting results in [[Recommendations Home|contextual recs]] by the overall [[Style Home|style]] present on the canvas.

Use cases: *Contextual bar, [[Artemis]], [[Recommendations Home|contextual recs]]*

### Milestone 3: Visual cohesion
Given one instance each of 2 classes of asset (text, image, icon, etc), and a query; rank the results of the query by their compatibility with the reference assets. 
Personal take: *start with [[Color]], then font*

Use cases: *Contextual bar, editor search, [[Recommendations Home|contextual recs]]*

### Milestone 4: Semantic [[Style Home|Style]]
Given a query or prompt containing one or more [[Style Home|style]] tokens, rank the results by their similarity to the [[Style Home|style]] token. 

**aesthetics have been argued since the dawn of time, they are highly subjective, not universally named, and very personal. Our goal here is not to disambiguate "bauhaus" from "early modernism", we're looking to create a way to allow users to use natural language to steer the way their projects look bit by bit.**


Use cases: *Contextual bar, editor search, home search, [[Recommendations Home|contextual recs]]*


## New Surfaces in [[Express]]
---
Once we've proven the safety of contextualization, we will begin expanding it's use and surface area in the product. 

### Milestone 1: All tab
Once the safty and stability of [[Recommendations Home|contextual recommendations]] is shown in production we'll need to expand the ease of use for contextualization. A prime use case is searching and ranking the assets which are displayed in the various sections in the "all" tabs on media and elements panels. 
Users are already expecting to see a wider array of thematic ideas and content here given the tabs's more general use name.

### Milestone 1A: Shapes and animated stickers 
Once in the all tab we should prioritize adding the shapes content type. "Arrow" is one of the top queries in the editor across all segments and we would be well positioned at this point to display that content. 
### Milestone 2: Contextual bar 
Asset replacement suggestions + next best action

### Milestone 3: Mobile editor 
Any new functionality or just scaling of services? 


## Language and Culture 
---
Expanding the languages that the graph is useable in is in essence a user base expansion effort. Translating the graph isn't useful for this. We must solve for the challenge of training culturally relevant associations with less data in T2-T5 regions. 

**Impacted User Exp:**
- [[Recommendations Home|Contextual recs]] useable in non US_EN regions 
- low/null recovery with [[Intent AI Home|CKG]] in non US_EN regions 

## [[Compositional intents|Compositionality]] 
---
The basic value of [[Intent AI Home|MINT]] is it's ability to take the infinite range of creation possible in [[Express]] and map this down to a finite set of canonicalized understood concepts. This value is multiplied if we're able to understand the *combinatorial uniqueness* of pairs of relevant nodes. 

![[Screenshot 2024-08-29 at 12.48.54.png|400]]
Other examples include: 
- "age" + "subject" for EDU 
- "resume" + "Industry" 
- "Logo" + "Industry" for [[B2B]]
- "Region" + "Topic"
etc...
These combinations have specific and unique associations which are distinct from other pairs. 


|          | K                  | 1       | 2          | 3...           |
| -------- | ------------------ | ------- | ---------- | -------------- |
| Math     | 1-10               | +/ -    | mult / div | Basic Algebra? |
| Language | ABCs               | Reading | Books      | Bigger books   |
| Science  | Animals and plants | Gravity |            |                |


**Milestones**


## Unimodal Relevance 
- Exact match 
- Core use cases
- [[Brian Eriksson|Brian]]'s slack 
- [[Jayant Kumar|Jayant]] & [[Ravindra Sadaphule|Ravindra]]'s wiki



## Random notes
---
- [[CKG 2024 Strategy notes|ckg strategy 2024]]


1. Areas of focus:
	1. New modalities 
		1. [[Audio]] + Video
	2. [[Style Home|Style]] 
		1. Asset [[Style Home|Style]] similarity model in [[Intent AI Home|mint]] 
		2. Template [[Style Home|style]] model
	3. [[Compositional intents|Compositionality]] 
		1. Simple use cases combining nodes from different clusters/types for better retrieval of associations
			1. EDU : age + topic
			2. Birthday age + topic
			3. Resume + industry 
	4. [[I2A]]
		1. Unclear 

### Ashok's document

project picasso: 
template variation with [[Style Home|style]] and time of year incorporated. 
Visual cohesion and [[Style Home|style]] understanding 



[Wiki link](https://wiki.corp.adobe.com/display/~rmanor/[[CKG Home|MINT]]+2025+Roadmap+Ideation)


# EOY 2024 Planning 

