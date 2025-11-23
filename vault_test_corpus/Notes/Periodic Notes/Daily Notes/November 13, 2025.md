---
pageType: daily
aliases:
  - "2025-11-13"
created: "2025-11-13"
---
# [[November 13, 2025]]
# Notes
---





# Meetings 
---

## [[Lr Home|Lr]] Embedding eval weekly sync #meetings 


## [[Lr Home|Lightroom]] dashboard #meetings 
- Anuj presenting the [[Lr Home|Lr]] dashboard 

![[Screenshot 2025-11-13 at 09.29.12.png]]
- Direct = no filters, keyword only 
- adjust-filter = may or may not have keyword, but will always have a filter 


## AC in [[Lr Home|Lr]] #meetings 

- met with [[Cherag Aroraa|Cherag]] and [[Eshan Trivedi|Eshan]], we can do AC off the same search index in V3. 


## [[Ayush Jaiswal|Ayush]] catchup #meetings/1x1 

- we're stopping modeling and working on more generalized 
- The golden set for MM swimlane 3 isn't correct
	- christian had an [[Evaluation|eval]] set, use this, don't create something new
## [[Ritu Goel|Ritu]] Staff #meetings 

### Q1 planning 
Line of sight we have right now. Basically no new asks. 

1. [[Express]]
	1. AC and HPR, [[Recommendations Home|unified search]]
2. [[Acrobat|Acrobat Studio]]
	1. relevance improvements for [[Acrobat|DC]] and [[express]] files, and natural language in january release
	2. [[PDF2Pres]] improvements 
3. [[Firefly]] / moonlight 
	1. generated history and cloud docs semantic search 
4. [[Lr Home|Lightroom]]
	1. big bang roll out 

## Maria Mora #meetings/interviewer 

- [[2026 Summer Internships - Ritu's Team|2026 interns]]
- Verdict: yes
### 1. Take me through your resume a little bit. 
Art + coding, worked at research lab and graphics. 
Worked at meta on Whatsapp, then medtech. 
AI and analytics club, AI pm training program. 
### 2. What drew you to the Product Management profession?
Thought she likes code running, but actually liked problem definition and seeing the user value. Hell yea. 
### 3. What draw you to the search and AI space?
Seeing the AI in action at the med tech exp was enlightening. 
Likes the feedback loop of data in new model out. 

**whats up recently there**
AB testing with n8n. Knows about testing and personalization practice. Picking a part what apps actually are and what they're doing. 
### 4. Let's do a quick thought exercise, let's say the team has come to you with a new version of a model that they feel is ready to ship. How would you go about evaluating and shipping it?
Dog fooding and having internal testing. Start w hypothesis "will X model reduce friction of Y action things..." completion rate. 

Highlight metrics:
- engagement
- flow analysis 

Dug into the user flow to look at situations where user feedback didn't align with metrics. 
### 5. Any questions for me? 
Asked about how we prioritize across products and teams, how do we handle the legacy code base shit. 

## Sophia Gao #meetings/interviewer 

- [[2026 Summer Internships - Ritu's Team|2026 interns]]
- Verdict: yes
### 1. Take me through your resume a little bit. 
Harvard biz school
Bounced around tiktok. Owned AI apps around internal tooling, and HR. 
### 2. What drew you to the Product Management profession?
Enjoy tech, enjoy cross functional stuff and diverse audience. Been a growth and internal tooling PM. 

### 3. What draw you to the search and AI space?
Enjoys the problem space that AI entails.
AI PM differs from func PM. Talking about building testing and eval data sets. Having to be more adaptable and dealing with uncertainty. 
### 4. Let's do a quick thought exercise, let's say the engineering team has come to you with a new v2 version of an intent understanding model that they feel is ready to ship to users. How would you go about evaluating what they've got, and deciding when it's good enough to ship?
Asking about usage and what data we have for input. told her we could get prompt + art board. 
getting eval set, going back to customer problem scenario and looking for logging. Pulling aggregations of trends within the query set. 
Once you've got this set, and getting the ground truth you might pull behavior data of prompt to action logging, or exporting. Involving some UX and human in the loop annotation. 

Annotations scoring and looking at behavior logs as a ref for this golden set. 

Stats and metrics:
1. precision 
2. What are the pass and failure modes? 
3. Deep dive on the failure modes
	1. Quanitifying the failures by degree or importance 
4.  Answer checking agent, rag thing?
### 5. Any questions for me? 

- role of search PM in the future of AI, etc...
- How does Adobe validate this shit 
