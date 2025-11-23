---
creation date: 2024-01-31
aliases:
  - user understanding
  - personalization
  - explore/exploit
Related Pages:
  - "[[CKG 2024 Strategy notes]]"
protected: true
pageType: programHome
---
# Personalization Home
---
- [Wiki link](https://wiki.corp.adobe.com/display/adobesearch/Personalization)

## Personalization v1

### Intro 
"Personalization" is a large topic and it's easy to inflate scope. To start, let's take personalization here to mean:
> Leveraging the behavioral and contextual data we have for a given user and interaction instance in a way that creates a unique experience for them in [[Express]]. 

If you were to ask someone what they're working on, and why they're doing it that way, when they're sitting down at [[express]] their answer will probably contain a few types of information:

- Contextual info about the topic or subject matter of their project
- The [[Style Home|style]] or aesthetic decisions they made
- Their personal capabilities, preferences, and tastes

Currently [[Intent AI Home|MINT]] provides contextual understanding. Which is a good start, but lacks a lot of additional signal. This is because contextualization has more to do with limiting the whole corpus of all assets down to a recall set which is topically related to the user's project, but still leaves the user to sift through many results. [[Style Home|Style]] and personalization will provide significant ranking signal. But what are we re-ranking? This will generally break down into a few categories:
1. Assets within a query result set or contextual rec collection 
2. Collections or topics within [[Recommendations Home|recommendations]] 
	1. You could extend this definition to more general groups of information (*eg: Topical ordering in all tab or explore page.)
3. Components of the UI, like tools like quick actions 

This is a ranked list and we will focus on these categories in the above order of importance. 

### V1 Goals
1. Build the foundational pieces of Mirai required to start delivering personalization in search and discovery use cases 
2. Deliver an experience which gives the user a sense that the app is reacting to what they do, and isn't a boilerplate 
3. Prove our ability to make CTR/Export impacts in [[Express]] with personalization


## Milestone 1: Unused Associations 
Within one editor session, how might we determine the associations in [[Recommendations Home|contextual recommendations]] which despite being topically related to the canvas, are not appealing to the user? 

For the sake of this milestone we can consider an "editor session" as one instance of a particular open canvas. This means that if: 
- a user opens project1, and then opens another [[express]] tab and starts a project2, these would be distinct editor sessions. 
- A user opens project1 and makes changes and then navigates away from the tab long enough that their auth expired and they had to return to [[express]] home to log in the editor session has ended. 

What are the actions which we would say point to an unused association? 
- assoc. in a lower position is clicked consistently 
- user interacts with [[Recommendations Home|recs]] multiple times, but never this one category 


## Milestone 2: User Behavior preferences
How might we use certain key behaviors within a user session, to inform the experience they have with [[Recommendations Home|contextual recommendations]]?

**Use cases**
1. A user comes to [[express]] via the home screen and makes a query for Diwali. They do not like the template results and choose to create their own project from blank. They're eventually shown an association for "Lamp". These lamps are open flame/oil [[Style Home|style]] lamps, and not electric desk and floor lamps.
	1. Entering [[express]] from a Diwali [[Express Traffic Growth - Program Home|SEO]] page is functionally equivalent here
2. A user is in the editor working on a project about a halloween party at their kids' school when they make a query for "party icon" in an element search. The results do not contain images of alcohol. 
3. A user makes a search for "dog birthday instagram post" and then selects a template with no dog content, intending to make a more generic birthday template more dog related. They're shown a [[Recommendations Home|contextual recs]] collection for dog related items like bones and tennis balls once they are in the editor.
4. A user is working on a template about food. We begin by showing a broad range of foods. The user then adds their own photo of a salad. Contextualization should start to bias towards vegetables. 

This query context flow may playout within the editor as well with element queries. 


## Milestone 3: User segmentation preferences 
Based on the user's context, how might we better rank the associations and assets within [[Recommendations Home|contextual recommendations]] for a particular users' segment. 
*We do want to rank assets here.* 

User context/segments:
- Local
- Date
- Entitlement/[[Express]] customer segment
	- EDU, SMB, etc (*I've asked for an exact list here*)

**Use cases:**
- If two users are searching for "party invite" in October but one user is in the US, and another is in India, they are likely creating invites for different parties (Diwali vs Halloween). 
- A query for "instagram" in December might be more christmas/hanukkah related, where as the same query in Feb might be more Valentines related. 
- Young EDU users might prefer a different set of assets within the association for "Biology" than College age EDU users. 

## Milestone 4: Explore / Exploit through a session
How might we adjust the relative diversity of our ranking according to the user's interests in other topics? 

The epsilon will vary across:
- Surface (home vs explore vs editor)
- Element type (Icon, photo, etc)
- Time in editor
	- Users will likely refine and narrow their interest over time


**Scenarios / stories**
- Users getting stuck and dynamically biasing towards explore 
- Explore bias for [[Recommendations Home|recs]] in all tab 
- Exploit bias for [[Recommendations Home|recs]] in element tabs 

**Signals**
- Rate of delete vs add events on editor 
- Number of edits in editor session 
- number of searches vs [[Recommendations Home|contextual recs]] clicks 
- Asset clicks and associations interacted with
- Recency bias in elements added and queries made

