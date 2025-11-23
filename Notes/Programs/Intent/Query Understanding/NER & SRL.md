---
aliases:
  - SRL
  - NER
  - semantic role labeling
protected: true
pageType: programHome
---
# NER & SRL Home
---
[[Query Understanding|NER]] (named entity recognition) and SRL (semantic role labeling) are used to rewrite queries and prompts so that they can be more effectively used in search and other applications.

1. [[Query Understanding|NER]]: Identify a token of a query as a match to a particularly important entity type
2. SRL: Interpret this token's role
3. USS: Create an ES query to match it against the relevant metadata and text fields

[[Query Understanding|NER]] and SRL help downstream services by allowing them to not only get these tokens recognized as key to the request, but also subsequent ranking systems can work with a smaller overall query by having these tokens effectively removed from the query by the time they get it. For example, in [[Lr Home|Lightroom]] query "_park picnic in paris 2020_", the query has two named entities in it: "paris" is a location and "2020" is a date. So the actual image search need only pay attention to _park_ and _picnic_, as USS will leverage the [[Query Understanding|NER]]+SRL to filter for location and date. 

**Named Entity Recognition ([[Query Understanding|NER]])** identifies entities that are explicitly mentioned in text. The role of [[Query Understanding|NER]] is to identify and type entities in the text. The [[Query Understanding|NER]] types are from a predetermined set that is specific to the application.  [[Query Understanding|NER]] involves the identification and typing of explicit entity mentions (e.g. "paris" (location) and "2020" (date) in "_park picnic in paris 2020_").

**Semantic Role Labeling (SRL)** identifies the semantic role the entity plays in the query or prompt.  For example, dates may have roles like dateCreated, dateSigned, dateLastModified. For example, the [[Acrobat|DC]] query "_contracts signed in 2024_" has a date [[Query Understanding|NER]] "2024" with a SRL of "dateSigned". However, the query "_contracts 2024_" does not specify the SRL and so there is no SRL for this date entity.

SRL is not [[Query Understanding|NER]] per se. However, SRL is often computed by the same rule- and model-based engines as [[Query Understanding|NER]] and having accurate [[Query Understanding|NER]] can improve SRL quality.

**USS** forms an appropriate ES query based on links the entity (often in its canonicalized form) and its role (if available). How to do this depends on the specific product and feature (e.g. what is done for default search may be different than what is done for search null and low recovery which may be different than what [[Recommendations Home|recommendations]] do).  Consider the "_contracts 2024_" [[Acrobat|DC]] example above, USS will take the canonicalized date and use it as an OR filter across several fields, e.g. the date created, modified, or signed.

**Wiki**
- https://wiki.corp.adobe.com/display/adobesearch/FY25+NER+and+SRL+Requirements
- [[Intent Understanding SRL model wiki]] - Technical details on the SRL model architecture, data generation, and evaluation methodology