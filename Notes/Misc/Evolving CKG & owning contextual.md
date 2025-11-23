---
creation date: 
tags: []
Related Pages: 
aliases:
---
based on conversations with [[Ritu Goel|Ritu]] and [[Brian Eriksson|Brian]] on [[March 18, 2024|3.18.2024]]



Owning contextual would allow me to push more of the tech agenda we want into [[Express]]. It would also give me a position to better instruct the direction of the tech, since I would be more connected to the use cases and customers involved. Rebranding [[Intent AI Home|CKG]]. 

If I owned contextual today I would start by taking stock of where the pieces of the experience we care about are, and what the capabilities of [[Intent AI Home|CKG]] are there. 

Where do we see having an outsized impact on the experience in [[Express|ccx]]?

CKG has to evolve beyond it's own graph. I've stumbled around this problem of how to use the graph in things like styles, where we have massive amounts of information we'd need to cram into the graph. On the flips side we've been worried about the graph being too much of a generalist to make significant impact in things like contextual photo recs. 
The graph itself may shift over time to become a more "behind the scenes" technology that acts as a focusing or limiting guardrail in helping us understand more about the user. 

For instance consider a user going to the editor with some template. We might break the document down in CML, but then intent understanding service would break it down, and return embedding spaces relative to certain neighborhoods in embedding space that [[CPT]] or something would then use for returning deeper contextualization. Intent service and it's semantic embedding approach is the real money maker here. The graph is primarily used for limiting the field of options. 



## Notes on models and retrieval
From [Sanat's wiki](https://wiki.corp.adobe.com/display/adobesearch/Contextual+Search+GT+Detection+Process)

Currently, contextual search workflows start with intent detection and then utilize the graph for serving associations for contextual search. While this is generally a useful approach as it provides diverse suggestions, there is often information loss from the original query to the associations.

Now that the multimodal model is trained to predict all node_types, we propose a hybrid approach of generating contextual categories, some coming from the model and some coming via associations.

Everything is ultimately an info retrieval problem. We need to look for the most specific understanding we can 

**Diverging Exploration** Suppose a user gave an image of a poodle in front of the empire state building. When we extract understanding here we might end up with nodes like `poodle, Empire State Building` and a user will want to explore things related to these in different directions. For insance they may be more interested in seeing things related to "Poodles in big cities" or "dogs in NYC". In some instances they may explore both and arrive at "pets in big cities". This branching 