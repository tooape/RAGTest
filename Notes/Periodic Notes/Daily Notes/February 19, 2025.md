---
pageType: dailyNote
aliases: 
created: "2.19.2025"
---
# Notes
---



https://nlps-playground.stage.cloud.adobe.io/dictionary

## [[Style Home|Style]] release


## [[CKG 4.0]] 

### What is [[Intent AI Home|CKG]] for
The core values of having a [[Intent AI Home|knowledge graph]] in SDC are:
1. A canonical dictionary of linked concepts
	1. Ontology & hierarchy 
	2. Structured exploration 
	3. Grounding of inference systems
2. A legal approved and user safe system for semantic intelligence 
3. A repository of info which is unique to digital creation, and the Adobe ecosystem specifically 

While #1 and #2 are valuable, these can be bought an approved with off the shelf technology, like [[CKG 4.0|Babelscape]]. We see the unique value of investing in [[Intent AI Home|CKG]] as being centered on #3. Things included in this unique data might be:
- Associations between concepts which are useful in content search and discovery, even if the semantic link between them isn't that strong. 
- Knowledge of the tools and products within the adobe ecosystem
- Our user's behavioral signal 
- Creative concepts like color relationships and aesthetics


#### Express flow 
Let's walk through one example where a user might interact with [[Intent AI Home|MINT]] multiple times, each requiring a different use of the graph. 
![[CKG user flow.png|500]]

Once the user is shown the [[Recommendations Home|contextual recommendations]] on the editor, they may choose to navigate to other topics. For instance, they may want more high level content around the "travel" hypernym, or more specific content within sub structures of summer activities or tourism in Japan. I have omitted this from the graphic above due to how many branching paths this may take.

In this flow we've demonstrated several needs of the graph:
- Canonical understanding taken from an image of a plane at an airport 
- An understanding of the specific behavior someone might want to perform with this image
	- Consider an alternate image, of someone's professional headshot on a white background. In this case the user may have only quickly wanted to drop the image square to use on social media, and not invoke artemis for use in a template. 
- An understanding of the topics related to the content of the image, both specifically and more generically. 

This flow also ignores any notion of aesthetic cohesion that might require intelligence, or the user's past experiences on Express being used to understand their current goals. 


### Build vs. Buy
With the recent legal approval to use the [[CKG 4.0|babelscape]] WordAtlas [[Intent AI Home|knowledge graph]], we should investigate using this data set as the base of [[CKG 4.0|CKG4.0]]. This (in theory) provides us a large and robust foundation of generic concepts, with hierarchy and a complete ontology.
Doing so leaves us to focus our effort on the unique and specific Adobe information, and quality improvements. 

**Automated Evaluations**
Evaluations on raw graph data should be done offline. With metrics surrounding the breadth, density, and quality of the graph. 


### Getting that unique adobe data



# Meetings 
---

