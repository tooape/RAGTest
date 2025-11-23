---
pageType: Misc
creation date: 2024-01-31
tags: 
Related Pages:
  - "[[CKG 2024 Strategy notes]]"
aliases:
  - composed intents
  - composing intents
  - compositional intents
  - intent compositionality
  - intent compositions
  - compositionality
---
# Overview  
In the same way that nearly limitless music can be played on the same 88 piano keys, most other forms of creativity are the manifestation of [combinatorial uniqeness](https://www.smithsonianmag.com/innovation/combinatorial-creativity-and-the-myth-of-originality-114843098/). If our graph is going to be useful to creators and communicators, we'll need to be able to understand the combinations of nodes related to a project, even if they fall outside their direct hierarchy. 
Understanding this combinatorial uniqueness is key to delivering the next level user experience in [[Express]], and will be table stakes in any core CC app experience we might power in the future. The best editor experience we could offer would be something contextualized to the specific and unique combination of intents expressed by the user. Take an example of a user doing a search for something specific like "Create Goat Yoga Studio Logo". Currently CKG might offer more generic contextualization with info around yoga, or goats individually. But that's not what the user has specified they're working on. It's not a project about a hot yoga beginners class, or an infographic about goats, or a logo for a goat farm...it's specifically for a business about goat yoga.


### Use Case Examples 

#### Niche Intents 
- [Young business man on Bike](https://adobesearch.slack.com/archives/C05THFJ7A2Y/p1702436182394879?thread_ts=1701902042.990229&cid=C05THFJ7A2Y)

#### [[Intent Seasonality|Seasonal Intents]] 
- [Lunar New year 2024 vs 2023](https://adobesearch.slack.com/archives/C02ULKVAWDQ/p1707159087717789)
- [[Color]] + Season + [[multi-region]] 
	- "red" in China in Feb is Lunary New Year
	- "red" in the US in July is the 4th. 

#### Intent + [[Style Home|Style]] 
As [[Intent AI Home|CKG]] moves into understanding [[Style Home|style]] we'll need to be able to infer style preference in addition to the subject matter of the request or canvas. 



## Building Compositionality 
### Pre-Processing 
We should begin breaking down some request with our QIT model, to being to understand the high level components of a query or action. 

### Node type "Slot Filling" 

In this technique we take a query string and identify for known values of slots or use some form of NN to match for unknown slots. We then use the graph to explore probable associations.

Having this approach will allow you to generalize a lot. For example, under "travel" there are lots of "{location} travel" and one "{season} travel" and one "{location} {season} travel", but you can imagine all the combinations could arise. 
- e.g. "japan spring travel" is popular due to the cherry blossoms but did not show up here yet.
Sometimes the phrasing of the intents does not match even when the slot is effectively the same. We should canonicalize on the intent name and then allow the variations. This may not be a big issue since the ones I noticed had slightly different roles (relations with "'s" for birthday vs people with "for" for birthday)
- eg: "husband's birthday" (relations) vs "birthday for woman" (people)

- Examples of slots: 
	- {age}: when ages appear, allow any age from 1-125 to match; "birthday" related intents are the obvious one here
	- {year}: when years like 2020 appear, allow any reasonable value; "new year" related intents are the obvious one here
	- {relation}: mother/father/wife/etc.; "birthday"
	- {person}: adult/man/woman/child/girl/boy for "birthday", "fashion"
	- {color}: these modify all types of things and which ones we have currently are relatively arbitrary (e.g. "blue plate" vs "red plate"); most of the colors are in the same place and so clearly they are grouped, but this is not actually typed
	- {ethnicity}: for weddings and foods ("restaurant")
	- {location}: this is a big one for things like "travel" which can take almost any location (countries, major cities, major tourist areas) and "mountains" which only has certain values
	- {season}: spring/winter/etc. for "travel", "fashion", "party", "collection" etc.
	- {holiday}: halloween/christmas/etc. for "card", "party", "invitation", "sale", "gift"; most of these already exist, but using slots will let you ensure completeness
	- {school_subject}: english/match/etc. which will allow more complete combination with "lesson", "club"
	- {disease}: cancer/aids/etc; although there are only the disease names and "awareness" currently, I suspec these will later show up with things like "walk-a-thon" and "fundraising"
	- {sports}: volleyball/soccer/etc; these currently should all be under a "sports" intent
	- {food}: fruit salad/etc.; some of these are currently top level; there are both individual foods (fruit salad, bbq) and classes of food (asian food); good for "recipes", "restaurants", "potluck", etc.
	- {zodiac}: gemini/ares/etc.: these are currently top level and will generally group together

Building 



## Old notes  
#### Quality of intent services
- One of the biggest values in doing this is to be able to go "spear fishing". If we can totally accurately nail the intent, even if we have no matches we can back off well. 
	- "Basketball" is useful, and "Community" is useful but "neighborhood Basketball tournament" is most useful
		- This ideally will help us distinguish what's most important here
			- If we don't have anything for this basketball tournament at the local rec center, whats the key piece? Basketball, or community?
	- Similarly we'll need to be able to disambiguate something like "K12 account create". Are they creating an account? Or do they want to generate a [[Firefly|FF]] image on their K12 license?
- Action use cases become much easier where we have [[Type of intent|type of intents]], [[global type|GTs]]
	- Create movie poster 
		- we'll need to correctly match on all 3 of these in order to be useful
#### Growth of the graph
- Long term, how will we maintain the graph? 
	- Functionally 
		- Hosting nodes, query performance, etc 
	- Practically 
		- adding nodes and associations gets more and more complex 
	- "Fewer but better"
		- The number of nodes in the graph can be reduced relative to the amount of knowledge we hold in the graph at any time 
		- The associations will also be more significant 
		- Our current contribution model will work forever 
			- teams will have other priorities and stop contributing
			- quality of the graph is hard to maintain with an open contribution model


“Creativity is combinatorial uniqueness” - kepano
- [Maria Popova Article](https://www.smithsonianmag.com/innovation/combinatorial-creativity-and-the-myth-of-originality-114843098/)

There are only 88 keys on a piano, all graphic artists use the same [[Color]] wheel


# Links 
- [Wiki page](https://wiki.corp.adobe.com/display/adobesearch/Compositional+Intents)
- [Arxiv paper](https://arxiv.org/pdf/2008.04548.pdf) 
- [Tracy's wiki](https://wiki.corp.adobe.com/display/adobesearch/Initial+recommendations+for+CKG+intents+and+compositionality)
- [[[Josep]]'s Wiki](https://wiki.corp.adobe.com/display/adobesearch/Intent+Compositionality+Redux)
