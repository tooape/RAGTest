---
pageType: dailyNote
publish: false
aliases:
  - 11.18.2024
  - 11.18.2024
created: "11.18.2024"
---
# Notes
---

- [x] Get a test photo set for Lr semantic search 



# Meetings 
---

## [[Lr Semantic Search PRD draft|Lr Semantic search]] catch up

- Next iteration of req this week
- Finalized by when? 
- POC expectations and ETA?

Scope:
- write some test queries 
- Scene info
- Apple kids and woodworking add

Date: Over the next month

Right now they're ok. 

Working plan from [slack](https://adobesearch.slack.com/archives/D05NGV9HCV8/p1728076583059499): 
- We had a workshop with USS team in August. For now, we wanted to do a POC for semantic search for one account in Lightroom to start with. For that we will require
    - Some help from USS team for onboarding
    - Dedicated sessions on the semantic search and ingestion pipeline
- Based on POC, further assistance might be required for enabling the semantic search feature on Lightroom for all account
- We also would need  help in understanding how [[Intent AI Home|CKG]] (Creative [[Intent AI Home|Knowledge Graph]]) is implemented at their end and how it can be leveraged in LR. Dedicated sessions would help here as well.

[Jira project](https://jira.corp.adobe.com/browse/OZ-15060) for lr semantic search POC. 

This is for 2H, MAX '25 launch 
- Q2 code complete


Changes on their side: 
- people recognition improvements 
- location data in exif for semantic as a p2

Duplicate detection

Current indexing work: 
- USS bugs 
	- Continue to consult model
- adding "not"operator for smart albums
- On device vs cloud service 
- Populating auto-complete
	- Jing's re-architecture 
	- UX issues are too severe 

### [[Peter Baust|Peter]]'s query list
Ryan,

Here’s a quick take on requests for Search.  Since I solicited feedback, it kindof grew beyond what I had in mind for the Prototype.

It’s OK if we cut off some near the bottom, though ideally we could do all of these via Search UI.

A red boat

Alexa riding in a red boat

Alexa in a white dress

Alexa wearing a white dress

Alexa wearing an off-white dress

Alexa trägt ein weißes Kleid (if UI is German, same for other languages)

Alexa and Siri riding bikes

Alexa or Siri riding a bike

Alexa and Siri at the lake

Alexa and Siri at the lake, without Claude

Alexa and Siri at Lake Tahoe

Alexa or Siri with puppies

Alexa or Siri with the 3 puppies

Allexa wearing a white dress (Offer or show Alexa wearing a white dress, with correction)

Alexa wedding photos

Birthday photos in the past year where people are smiling

Diwali photos from the past 10 years

**Will need some (new) LR assistance for these**

Our family in Seattle 

Our family photos from the Seattle area – Mapbox has offered to work with us on on this, if needed

Our family on Seattle trip 

Alexa or Siri with family dog 

**We want to do this, maybe with or without USS**

Show me my best photos in the last six months 

Similar pictures to this one

Pictures from the same shoot as this one 

Photos in this album/folder that meet a certain criteria

I am sure I missed some important cases here.

-[[Peter Baust|Peter]]