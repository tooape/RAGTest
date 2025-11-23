---
pageType: dailyNote
publish: false
aliases:
  - 01.4.2024
created: "01.4.2024"
---
# January 04, 2024
---
aintitAboutTime67^

## [[Stock entities]] [[indexation ]]position 
- Yesterday's meeting
	- ![[January 03, 2024#stock entities meeting]]

Context
Stock is the repository of most of the ingredients that are available in express, and we would there for like to be able to use as much of our intelligence as possible when searching for these assets in Express. In recent weeks the idea of using CKG's nodes (GTs) as additional metadata to index into stock has come up as a way to improve our ability to return assets relevant to a user's intent. 

Hypothesis:  
We believe that we can leverage intent services' intelligence to make meaningful contributions to [[Recommendations Home|contextual search]] use cases without indexing GTs into the stock index, and instead performing the intent inference at query time. 

Details 

Issues with indexing
We've found a few key issues with the indexation approach: 
- Indexing the GTs would capture a single version of the the graph, which would quickly be outdated as we iterate on the nodes and structure of CKG.
- Indexing GTs into stock would be relatively expensive and time consuming. 
- Stock images in and of themselves may have many or ambiguous intents (eg. what is the intent of an image of a dog sitting under a tree?). This makes the other types of GTs more valuable, which may be duplicative of CAT tags, and isn't the design goal of CKG. (Content tagging vs. intent understanding)
- The metadata in stock is already quite robust (as opposed to templates)

Proposal 
We're proposing that we run intent inference at query time instead of index time. This has several advantages:
- We can use more MM signal including the query corpus or canvas in the inference 
- We'll always be using the latest deployed version of the graph, and the inference models 


## Grooming #meetings 
- [[Recommendations Home|Contextual search]] demo 
	- Getting evals going 

Sneha, Jayant don't know what is going on or what's in progress