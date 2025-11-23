---
created: 
tags: 
Related Pages: 
aliases:
---
# Intro

## Key Focus areas
1. In Q3 our major focus is the success of [[Recommendations Home|contextual recs]]. "Success" here shouldn't be thought of as blowing the doors off the building with huge CTR gains in the A/B test. We already know this won't happen based on current designs. Our contribution will mostly be judged based on us not producing any harmful associations, or any really poor relevancy suggestions. 
2. Behind this initial release, we'll look to roll out a series of improvements around [[Style Home|style]] and aesthetic cohesion. 
	1. [[Color]] Harmony 
		1. We don't need millions of [[Color]] nodes, we need some condensed, canonicalized [[Color|colors]] (maybe 2 or 300) which can be used by the [[Color]] team's [[Color]] expansion model 
	2. [[typography|Fonts]]
		1. Even though this isn't [[Vic Chen|Vic]]'s team...we need to avoid a [conway's law](https://arc.net/l/quote/hwbtjyzb) thing where the element and media suggestions are great an visually cohesive and [[Font recs]] are off in space with completely unrelated behavior. This will confuse and frustrate users.  
3. 

# [[Style Home]] 
## Overview
[[Style Home]] work should be grounded in the use case and the user value proposition that they power:
Our target user is not a pro designer. How do we help them get a quality of output that they could not achieve themselves, and that makes them feel like they created something really great?
- [[Recommendations Home|contextual recs]], and [[Style Home|style]] understanding should be thought of as an assisted creation use case

Don't try to solve the universe. We should use the dimensions from stock, and the [[Style Home|style]] taxonomy in [[Express]].
- We need a golden set of [[Style Home|style]] tagged templates from the content design team 
	- 10 Examples of each of the 24 [[Style Home]]
The [[Express]] taxonomy is for templates, and the stock taxonomy is for assets, so we'll need a way to correlate the two and be able to say "heres the assets which go with a minimal whatever template" 

We should try to marry the [[Firefly|FF]] and Stock [[Style Home|style]] dimensions. 

All of this however only covers the broad strokes of [[Style Home|style]], we need to be able to get down to the lower levels. For this I think we're just going to need some embedding similarity. How do we solve that issue of two [[Icons]] or [[typography|fonts]] looking similar? Feeling similar? 

*If we get signal that that the template is "corporate" how do we turn that into the right [[Color|colors]], and the right [[Icons]], and the right [[typography|fonts]]?* 
- We need to bring the creative topic(s) & associations, the [[Style Home|style]], and the assets together into a cohesive whole. 


## [[Style Home|Style]] embeddings Spike
> As a user who is not a pro designer but needs to create content for my business, I would like to be able to easily and quickly create good looking projects in [[Express]]. This way I can get what I need and maintain a high quality visual language with my customers. 

As mentioned in the [vision document page](https://wiki.corp.adobe.com/display/adobesearch/Intent+Services+Strategy+2024), our role is somewhat like a digital art tutor sitting invisibly inside [[Express]] helping non C-Pro users create extremely good looking projects even though they lack expertise. A big part of this is [[Style Home|style]] and we'll need to have a good understanding there. Don't think we need to over rotate on this however! 

[[Style Home|Style]] and aesthetics are something artists and scholars have argued about for literal millennia, and we're not going to "solve" it all of a sudden. *Our mission is just to be able to understand enough aggregate [[Style Home|style]] trends and behavior in the assets created by pro designers, to be able to guide amateur users to a good looking result.* 
Fundamentally, you can think about this as a ranking problem:
> How Might We re-rank the assets of some query based on their stylistic or aesthetic similarity to some given canvas or element?  

This investigation is to understand the viability and efficacy of separating the semantic and stylistic understanding of a collection of elements in embedding space. For example: 
- Consider the topics: Dogs, Cats, People
- and the [[Style Home]]: Pop Art, Anime, Minimalist 

Today we might have: 
![[Screenshot 2024-06-14 at 3.05.20 PM.png]]

Can we get to: 
![[Screenshot 2024-06-14 at 3.05.25 PM.png]]





## Other use cases


# [[Intent AI Home|CKG]] Structure and cleanup
Don't prioritize multi language, we instead need to focus on contextual. 

#### Manual Structure 
We need to create **singular** and **rigid** structures for base level things. Which should be under respective parent nodes to "hold" the structure in question.
1. Numbers 
	1. 0-200
		1. This will be useful as we start to approach [[Compositional intents|compositionality]] and need to be able to have an understanding for things like age of birthday invite, etc. 
2. English letters
	1. A-Z
3. Geography 
	1. Countries
		1.  [alpha-3 abbreviation](https://www.iban.com/country-codes) as metadata
	2. each national capitol city as nodes associated to the right country 
	3. *Move existing nodes into this structure and connect the associations to things like the named location node*


We need to remove any and all copyright nodes: 
- Fictional characters 
- Sports teams 
- Celebrities 
- Brands

Add an element type for [[typography|Fonts]] and draft a proposal on how we can index the data from the [[typography|fonts]] team into [[Intent AI Home|CKG]] so that we can power better/contextual [[Font recs]]. 
- This should be thought of as an aspect of [[Style Home]] 


- **Cleanup**
	- bad nodes
		- De-pluralization 
		- Manual review of nodes with ≥ 3 tokens
		- No brands or copyrights 
			- Fictional characters 
			- sports teams 
			- movies
			- artists/celebrities 
	- Taxonomy / ontology review 
		- We should focus our efforts here and look to accomplish two things: a cleaner graph, and a more dense graph.
			- we can strategize our time here by focusing on the clusters that most users will interact with most frequently upon launch in August. 
				- Do another offline [[Evaluation|eval]] similar to what we were doing in discovery hub earlier this year but using MMv2 and the latest graph. Take the top 1000 templates from prod and get the 1000 most frequent associations across this set. Manually review these 1000 nodes for obvious issues:
					- Dumb names 
					- Irrelevant associations 
						- incl parent nodes 
					- branding/copyright 
					- bad or harmful associations 
			- We're going to have some dumb results when we launch this feature, it's inevitable. How can we save ourselves the worst and most embarrassing misses.
	- Manual Structure 
		- [[Style Home]]
		- wiki page i made once... 

Depth of results [[Evaluation|eval]]: 
- Take top 1000 templates from prod over last 90days and run [[Intent AI Home|MINT]] on them to ensure we have <3 associations over our threshold. 


**MM**
- Video model
	- Video [[Artemis]] 
	- Rec stock videos


**[[Query Intent Type|QIT]]**
-  Clarify the use cases from [[Varun Sunderajan|Varun]]'s PRD

Across all asset types, what are the most relevant elements for contextual? 
Contextual bar use case, where all element clases live together


