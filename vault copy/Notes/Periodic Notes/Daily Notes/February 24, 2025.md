---
pageType: dailyNote
aliases: 
created: "2.24.2025"
---
# Notes
---

## Style doc 
[Wiki page](https://wiki.corp.adobe.com/display/adobesearch/Aesthetics+and+style+understanding+Strategy)

Goals to convey in the opening:
1. What is the pie in the sky
	1. few examples
	2. What kinds of use cases we're looking at 
		1. Near term use cases
			1. phases 1 and 2 in express [[Recommendations Home|recs]]
			2. Stock "similar look" [[Recommendations Home|recs]]
		2. more distant use cases
			1. assistant/query etc
		3. Visionary use cases
2. Why is style hard
	1. Imprecise
	2. no ground truth 
		1. Adobe research about style language 
	3. What we're not doing 
		1. solving art
		2. taxonomy
		3. etc.
3. 

**Intro**
Any time creativity is involved you'll quickly get into the question of style and aesthetics. This is challenging for even experienced users who don't always know how to achieve a certain look they may have in mind.  This challenge is multiplied for less design experienced users who may not have a clear vision, or know the design terminology that might return one look or another. 
All of this creates a very difficult environment for the SDC team. Users with little skill and understanding, and unclear vision of their desired outcome are struggling to accomplish a satisfactory result in Express. On top of this, design is highly subjective, with little or no widely agreed upon or understood terminology or categorization, and the structures of design language that do exist vary substantially over time and culture.

All of this to say style and aesthetic understanding is a large and challenging problem with a range of use cases we might prioritize, as well as technical directions for solutions. This page outlines our primary use cases, areas we're specifically keeping out of scope at different stages, and our strategy to address these concerns. 

**Vision**
Based on our research team's findings we know that many express users are not design experts, and lack language to articulate what stylistic aspects they're interested in. Likewise we've also learned that these users rarely understand why some asset (or their project project as a whole) doesn't align with their ideal. 
Our ultimate vision is to level this playing field. Put simply our challenge is:"how might we allow users to easily explore, and clearly direct the aesthetic aspects of creation in an understandable way?". Firstly we believe bringing foundational aesthetic intelligence to market massively improves the value and usability of products like Express and Stock for non-CPros. They'll be able to quickly and easily get inspiration, guidance, [[Recommendations Home|recommendations]], and assisted creation, but more than that they'll end up with a project that looks better and more interesting than they imagined. 
Longer term we see this underpinning CC apps as well, by providing c-Pros with clear and actionable inspiration for tools and assets as they move through their projects. 

This problem of aesthetics has been tried several times, by several teams (eg. Content Design, [[Firefly]]). Their approaches most commonly relied on creating either a taxonomy of styles by category, or a matrix of dimensions which describe some assets' individual style. This involves assuming some ground truth, drawing lines between categories, and creating ridged taxonomies based on these assumptions. These teams looked at the problem with the idea of creating a specific set semantic classes which would describe style, and users would then be able to use this to find or generate the appropriate content. 

**Early Strategy - Style Similarity** 
Instead of trying to solve a very complex and subjective language problem, we're looking to provide some value very quickly by looking at style as a similarity problem. 

Consider the images below: 
![[Aasheerb_a_calming_minimalist_Japandi_living_room_with_an_empha_31d470e5-1edb-4c64-b0ca-b2d53ed021e3.png|200]]
![[image148546.jpg|200]]

One of these living rooms is decorated in a "Japandi" style, and the other in a "Minimalist modern" style. Even if you're confident in your answer, do you believe most users would agree with your assessment? With all of this in mind we view trying to label which is which as a fruitless exercise, and not required to start delivering value around style. If you swapped the chairs between these two living rooms they would still look good and relatively cohesive. 

Consider a user making a flyer for their furniture store, if they uploaded either of these example images they might expect similar fonts, colors, design assets, and templates to be recommended to them, even if they have no idea what "Japandi" means. 

"Burger, fires and milkshake example"
- show the difference between just "cartoony" and the same set of assets 

Focusing on the near term Express & Stock user, some use cases we envision might include: 
- A user adds several images they've saved from instagram or twitter to the canvas.
- A user 

Scope callouts: 
- Semantics and language
	- we know this is important for assistant, but we aren't there yet
- Taxonomy and classifications 
	- we're looking to avoid this as much as possible

**Looking further out - Cohesion & Semantics**

Looking even further out to C-Pros:
-  Photoshop user is stuck in the middle of making an painting. They feel their canvas is off some how, but they aren't sure what's causing them to doubt their work. We may show them 





Some examples include: 

1. A user provides multiple pictures which they've saved from twitter and instagram with interior decor they find inspiring. 
2. A user asks assistant for "more contemporary" assets to replace something on their canvas
3. A user searches for "Japandi decor ideas"
4. A user has favourited several assets in express in prior visits. 




**Overview**
Any time creativity is involved you'll quickly get into the question of styles and visual cohesion. Visual cohesion is complex, subjective, often culturally informed, and difficult to describe. It's so hard in fact, that Many Express users cannot articulate in a search what they're looking for stylistically at all. Likewise with some users of Adobe products having considerably more design and art education than others, any ridged taxonomy or set of dimensions trying to quantify style is unlikely to be successful. 



When building intelligence and capability related to aesthetics, we should keep a few goals in mind:

Allow users of varying design skill to interact with aesthetics in an understandable way.
Avoid hard and fast taxonomies, definitions, and categorization. 
Design for uniformity across features, apps, and platforms. 
  

While 2025 is going to be mostly or wholly about express, we should mention of a future beyond express even up into the core CC apps. 

 We see this as foundational tech, which will have impact across:

[[Recommendations Home|Contextual recs]]
Template and asset search 
Assistant 
etc. 


**Phase 1...**
