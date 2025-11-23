---
pageType: daily
aliases:
  - "2025-09-22"
created: "2025-09-22"
---
# [[September 22, 2025]]
# Notes
---

[Linear power supply for Laiv uDac](https://www.tekaudiospecialties.com/product-page/lps25va)

## Jira ticket desc. for express to send last added asset
> In order to show contextual recommendations more stylistically aligned with the user's interests and current work, we'll be introducing ranking signal based on the [[Style Home|style]] of the last added asset to the artboard. This way the user can get a more relevant set of recommendations. 

The [[Style Home|style]] model is trained (currently) to look at the similarity of one asset to another asset based only on their [[Style Home|style]] and visual appearance. To get the most out of it, we'll need to pass it one canonical reference to base the similarity off of. 

Currently in contextual recommendations we're sending the whole art board, which reduces the effectiveness of the [[Style Home|style]] model. 

We'll make a change to include the last asset a user added to the intent call to act as this [[Style Home|style]] reference. This [[Style Home|style]] reference effects only the **[[Style Home|style]]** of the recommendations results, not the recommended collections themselves. The [[Style Home|style]] reference asset is used in conjunction with the normal recs query flow, and the signals are blended to produce results. 



# Meetings 
---

## Query Understanding Checkin #meetings 

**Affinity & QU**
Making sure the CAF wiki captures the Express specific fine tuning for 5 classes. 
Making sure the endpoints are called out so that people know where/when this intelligence is available. 

Wiki page to cover:
- Readable overview of capability
- Prod / stage availability
- Generic vs use case specific capabilities
- Link to repo/tech wiki with endpoint info


**CKG4**
Vipul pushed on making scaling up the graph a big question. How do we add camera types or something for Lr. For the clear binary stuff, how can we get faster at manipulating and changing the graph. If we wanted to add some new concepts for Lr, how could we do that in days or weeks, not months. 

For a new use case: 
how do we collect all the extraneous shit already in the graph, and change the node metadata or the edges to whatever new structure makes some use case possible, and add whatever new data is req, fast. 

## [[Ritu Goel|Ritu]] #meetings/1x1 

**DC**
1. I don't want to own their poor outcomes
	1. can't help with tex processing 
	2. barley communicating 
	3. Unknown use cases 
2. We're leaning in as much as we can


**[[Style Home|Style]]**
1. Struggling to index STILL 
2. Running out of hope for [[Style Home|photo styles]] which isn't good for SDC


**Query understanding page**


**The three big things for recs:** 
- [[Style Home|style]] 
- For DC and PDF → pres long text 


## [[Aditya Pathania|Aditya]] #meetings/1x1 

analytics ticket for search and all tabs: 
- differentiate from existing implementation, and form search actions
