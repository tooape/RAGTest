---
pageType: dailyNote
publish: false
aliases:
  - <% tp.file.creation_date("MM.D.YYYY")%>
  - <% tp.file.creation_date("M.D.YYYY") %>
created: "11.21.2024"
---
# Notes
---
- [x] Arvind's slack

[[Brian Eriksson|Brian]] feedback: 

**Doing well**
Brian's leadership is invaluable to our work on [[Intent AI Home|MINT]] and [[Recommendations Home|Recommendations]]. Technically he has a clear sense of where to express his deep insights and give direction in modeling and validation practice, and when to step back and let the team explore and innovate. On the other side of that coin, I would consider him one of the most savvy and well spoken people in the organization. His Emotional Intelligence has helped guide us through difficult meetings and hard conversations. 

Personally I will add the anecdote that in each phase of my time in SDC Brian has been a proactive engineering leadership partner, a trusted collaborator, and a gracious mentor. 


**To improve**
Brian has an excellent reputation among his peers and collaborators in Express; he might think about how to scale this influence as SDC looks to take a larger role in Express' AI and guided creation ambitions. 
It's hardly a secret that bridges between these orgs are few and far between, but our ability to deepen these ties will be do or die over the next few years. Brian's relationship crafting will have to expand beyond these direct product touch points if we're going to be successful there. 

**Other notes**
Sometimes you meet people who have an immediate and obvious sense of being "switched on", Brian is one of them. 


Aditya feedback
**doing well**
Aditya is a very engaged and action oriented collaborator. When building out the data and reporting for [[Recommendations Home|contextual recs]] he not only lead the implementation but helped structure the conversation around what kinds of questions and insights we'd want to cover from a data perspective. I really felt like I was able to structure the product perspective, voice my concerns around data, and leave it to him. 

**could do better**
Not sure this is a practical ask, but I would like a bigger perspective on the data capture and modeling pipeline structure within Express. Not only from the implementation of "how is X stat instrumented and calculated" but organizationally how is Express using this data to make decisions. They seem very data and testing oriented, and I'd like to see things through perspectives more. 

**other notes**
Looking forward to continued collab. with Aditya in [[Recommendations Home|recs]] and search as we scale [[Intent AI Home|MINT]] out to more AX surfaces, and use cases. 
# Meetings 
---

## [[Personalization]] user stories #meetings

If you were to ask someone what they're working on, and why they're doing it that way, when they're sitting down at [[Express]] their answer will probably contain a few types of information:
- Contextual info about the topic or subject matter of their project
- The [[Style Home|style]] or aesthetic decisions they made 
- Their personal capabilities, preferences, and tastes 

Contextualization has more to do with limiting the whole corpus of assets down to a recall set which is topically related to the user's project. From here, aesthetic and personal preferences will provide more useful ranking arguments than topical information. 
The fundamental motivation behind [[Personalization Home|personalization]] is that [[Style Home|style]] alone is not enough to rank a result set of a query or recommendation. 
The easiest way to prove value here then is to think of [[Personalization Home|personalization]] primarily as a ranking mechanism. 

Initial use cases are going to largely break down into two common categories: Associations ([[Recommendations Home|contextual recs]]), and Assets ([[Recommendations Home|contextual recs]] + search). The preference learning will effect the ranking and recall in these areas based on the user's actions in the home, explore, editor screens, as well as their entitlements or segment. 

Generally [[Personalization Home|personalization]] should not be bringing in totally irrelevant results. It's more of a ranking augmentation, parallel to [[Style Home]] (for now :)

### Associations 
For [[Recommendations Home|Contextual Recs]] 

**1. Unused Collections**
> As a user who's working on their project in the [[Express]] editor, I would like for associations in the [[Recommendations Home|contextual recommendations]] which I am not interested in to drop out of the results, so that I can see new ones. This way I can get more associations which I might use, and not take up UI space with things Im not. 

Even if some association is contextually relevant, a user might not want to add that. We should ideally recognize this after a some time in the editor and remove that association. 

**2. Boost and bury**
> As a user who's working on a dog show poster. Associations related to more generic "pets" or "cats" should be ranked below more specific dog, award, and contest related collections. 


**3. navigating explore exploit**
> As a user whos stuck in their project and unsure where to go from here. As associations a dropped off the list of [[Recommendations Home|contextual recommendations]] I would like for the results that are backfilled in the list to be more diverse and less directly related to what I have on my canvas on at the moment. Once I find a direction I want to pursue i would like for the results to get more related to that topic and my selections as I move forward.

### Assets
Applies to [[Recommendations Home|recs]] & search.

**0. Personalized Assets**
> As a user who's adding their n-th orange cat to a canvas. I would like to see orange cats ranked above grey and black cats in queries and contextual associations related to cats.  


**1. Disambiguation**
> As a user who's searched "Diwali" in [[Express]] and then created an invite for a Diwali party in the editor. When I see the association for "lamp" I would like for more relevant, open flame and oil [[Style Home|style]] lamps to be shown higher than electric desk lamps. 

Bat vs bat, etc
"Party" -> Cake and balloons or cocktails and beer? 
+seasonality (stop boosting "diwali" associations after the holiday)
the recontextualization case 

**3. [[Style Home]]**
> As a user who's only interested in hand drawn, illustration [[Style Home|style]] assets. I would like for other [[Style Home]] to be ranked lower in each association's results set, and in search results. 

**4. Embellishments**
> As a user creating a slide deck for my annual report. I would like to see assets which are generally useful, if not contextually related to what I'm working on. Like Arrows and laptops. This way I can add visual appeal to my project. 

If we think about [[Personalization Home|personalization]] as "behavior informed ranking & recall" then this belongs here. 


### Signals 
- query 
	- Contextual associations
- canvas & editor clicks
	- Asset adds
	- text 
	- uploaded assets


**Inter-Session** 


**Segmentation**
Cold start solver, not otherwise very accurate or useful. Individual, EDU, SMB, ENT are the 4 major segments

## [[Express]] [[APS]] #meetings 
![[Screenshot 2024-11-21 at 17.53.18.png]]

![[Screenshot 2024-11-21 at 17.46.50.png]]

![[Screenshot 2024-11-21 at 17.53.38.png]]

