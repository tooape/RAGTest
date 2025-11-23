---
pageType: dailyNote
publish: false
aliases:
  - 09.30.2024
  - 9.30.2024
created: "9.30.2024"
---
# Notes
---





# Meetings 
---

## [[Intent AI Home|MINT]] unimodal precision 

From [[Brian Eriksson|Brian]]: 
Hi everyone,I chatted with [[Vipul Dalal|Vipul]] last night, and this long-prompt focus is not going away. In addition, it seems he wants to targe[[Artemis|t Artem]]is as the first use case.We should have a deep dive while everyone is in town, but the following are my initial thoughts on how we can accelerate a v1 of this.Given a long prompt from a user, I would like [[Intent AI Home|MINT]] to return four things:  
-Extracted aspect ratio creative intent (e.g., instagram-square-post)  
-Intent related to the template, ideally this would be in the form of a MM vector  
-Template text suggestions (in case our corpus does not have a direct hit for the template intent)  
-Intent related to the desired foreground image of the template, ideally in the form of a MM vector  
-(Stretch goal) MM vector of any background image intentThe first three, [[Artemis]] can leverage today. We are working on Stock integration (helped with the recent [[Intent AI Home|MINT]] indexing) so we will soon be able to leverage the fourth.Examples:  
-I want to create a [[Audio|music]] concert flyer for a ska band  
Type - Flyer  
Template Intent -[[Audio|music]] concert (MM vector)  
Image intent - ska band (MM vector)-Create me a instagram square post of a restaurant menu with an image of a single piece of sushi  
Type - Instagram square post  
Template intent - Restaurant menu (MM vector)  
Image intent - Single piece of sushi (MM vector)


## Improving stock asset collection #meetings 

