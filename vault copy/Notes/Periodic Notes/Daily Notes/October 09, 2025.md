---
pageType: daily
aliases:
  - "2025-10-09"
created: "2025-10-09"
---
# [[October 09, 2025]]
# Notes
---

[[Benjamin Warde]] had some [[Lr Home|Lr]] [semantic search issues](https://adobe.enterprise.slack.com/archives/C09J00HAEJE/p1760040807511329): 
```
Hello Semantic Search team!  I've been trying it out for the past couple days and I'm very happy, it works better than I was expecting.  I've had several real world uses cases where I was easily able to immediately find a picture I was looking for using Semantic Search, when I had been unable to find it using our legacy search tools.  Great work, everyone, I can't wait to get this rolled out across the ecosystem!I've hit a few weirdnesses, feedback is below.  I believe my catalog ID is 38945240f1854e3480c3db15169d595c but if that doesn't seem right, maybe someone can tell me how to find my catalog ID (ideally without needing to go into Spider).

- Searching for "golden gate bridge" does (eventually) return photos of the Golden Gate Bridge, but they are buried beneath a bunch of pictures of my daughter on a ferris wheel.
- Semantic Search seems to take into account the names of people that I've labeled in the People section.  Awesome!  When I search for "nalani with a dog and a city skyline in the background" I get pictures of Nalani with a dog (and no skyline), and I get pictures of Nalani with a skyline behind her (but no dog).  I want that search to prioritize pictures of Nalani with a dog and a skyline behind them both.
- Searching for "lego" or "legos" returns zero results.  But searching for "lego box" returns lots of results, including pictures of Legos with no box, which surely should have been found when searching for "lego" or "legos".
- It doesn't seem to work on videos.  Is it possible to include videos?  Even if we're not searching within the video, but simply indexing the poster frame?
- Does it read text in images?  I searched for "pig roasting on a spit" and it found the photo I was looking for (great!) but it also found a picture that clearly had no pigs in it, but which did have a prominent sign which said, "Pork Chops".
```
# Meetings 
---

## Semantic Topic Extraction and [[SLM]] #meetings 

We need to create a new and better list of queries. Right now we only have like stock or [[express]] queries.
- scene object
- background 
- [[color]]
- etc

We want more complex queries from shit like [[Acrobat|DC]] prompts and [[Firefly|FF]] prompts.

### Ask
For Contextual [[Recommendations Home|Recs]] (PS, [[Express]], and [[Acrobat Contextual Recommendations|DC]]) what are the kinds of use cases for topic extraction, and where might we get the examples. 


## [[Lr Home|Lr]] & SDC 2026 #meetings 

### Vision
Explore anyone to create stunning photos and explore... 

### Top line goals 
- triple MAU
	- 35M (mobile) → 100M (free + paid)
- Increase usage of [[Firefly|GenAI]] credits

### Next level goals
- finish 2025 goals 
- mobile 
	- onboard and activate
	- Engage and retain
		- community commitment 
	- sharing and virality 
- Edit 
	- incorporating new [[Firefly|GenAI]] models 
- Project Stratus 
	- adding to [[Lr Home|Lr]] desktop 
	- including NOT operator in smart albums 
- Agentic assistants 
### Specific asks 
- GA for semantic search in web 
	- Rollout for semantic search on Desktop 
	- *maybe* mobile 
- Bug fix
	- >2 file name search 
### Special ask - retiring auto tags 
At ingestion, we run a bunch of old shitty taggers which is indexed with the metadata. 
if a photo is updated, all metadata must be resent. 

Fixing the old tagging flow, and designing our new future. 
### Lower priority / TBD
- [[Lr Home|Lightroom]] Web Maps 
- Community search 
- agentic workflows
	- photos selection 
## [[Ritu Goel|Ritu]] staff #meetings 

[[APS]] template is getting worked out in the [checklist here](https://adobe.sharepoint.com/:w:/s/DMESLCReviewArtifacts/EYB7WM7osnRNlb9lNJFlQqMBmmx2r0HANp5R2UbmF0DBoA?e=UBzSpc&xsdata=MDV8MDJ8cm1hbm9yQGFkb2JlLmNvbXw5NDE3MjExZWVjMWU0MmNkZTU4MTA4ZGUwNzY5MzY2NXxmYTdiMWI1YTdiMzQ0Mzg3OTRhZWQyYzE3OGRlY2VlMXwwfDB8NjM4OTU2MzQ1NjM4NzQ5MzIwfFVua25vd258VFdGcGJHWnNiM2Q4ZXlKRmJYQjBlVTFoY0draU9uUnlkV1VzSWxZaU9pSXdMakF1TURBd01DSXNJbEFpT2lKWGFXNHpNaUlzSWtGT0lqb2lUV0ZwYkNJc0lsZFVJam95ZlE9PXwwfHx8&sdata=TDRvRTZ3Vnp4MWczN0ZldXpvWEtrZ042RnVnUDZ5MS9BazE3Qkljb1hCbz0%3d).

## Intern program #meetings 

- two start dates 
	- One in May one in june 

They're still taking INTL students 

They're going to send you a resource page with interview notes and shit.
### Manager asks 
1. Commit to the program 
2. they'll give you training 
3. Weekly 1x1
4. Encourage them to go to events 

### Evaluating candidates 

Hire for potential, not demonstrated credentials. 

**Avoid bias**
1. Pedigree 
2. [[Core Affinity Framework|affinity]] and similarity 
3. Gender 
4. halo / horn effect - focusing only on positives, or only negative 

Look for specific skills, set biases aside, and hire for potential. 
- hire for coachability 

anchor on core values 

## Sign-off: Subprompt requirements #meetings 

[[Acrobat|DC]] is launching MCP. They've given us conditional sign off, but a few notable queries failing. 

