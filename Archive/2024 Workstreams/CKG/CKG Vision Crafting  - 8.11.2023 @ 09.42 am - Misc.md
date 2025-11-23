---
pageType: Misc
created: 2023-08-11
modification date: {}
tags:
  - oldtags/CKG
Related Pages:
  - "[[Intent AI Home]]"
Things Link: things:///show?id=Qv1nzsSFNio1VL25ELfpq4
---
---
# [[Intent AI Home|CKG]] Vision Crafting  OLD - 8.11.2023 @ 09.42 am - Misc
- [Deck link](https://adobe-my.sharepoint.com/:p:/r/personal/rmanor_adobe_com/Documents/CKG%20Vision.pptx?d=wf47e415b4b9f4ead8e6b271081933498&csf=1&web=1&e=AwVHi7)

# Old doc
- Sections: 
	- [x] ID that you're better at user than constraints, and only ok at the tech 
	- [x] Break out OKRs
	- [x] Move the feature ideation shit to its own section
		- [x] Rethink the groupings by user flow- they blend together 
		- [x] Speak more directionally 
			- [x] App teams will fill in the specifics
	- [x] List examples
	- [x] Mission/vision statement crafting 
		- [x] draft something 
	- [x] pillars

## Intro 
---
[[Intent AI Home|CKG]] (Creative [[Intent AI Home|Knowledge Graph]]) is a platform for understanding the contextual intention of a user's specific interaction with the Creative Cloud & Document Cloud suite of services and apps. This platform is part of a wider collection of capabilities for giving us a detailed and nuanced understanding of what a user is looking for, trying to do, or may be interested in doing next. In this doc I'll break down the strategic direction for the platform, with considerations for user goals, business objectives, and engineering advancement. I will also outline some hypotheses to validate & confirm the direction, and list some specific feature capabilities in these areas. I will **not** go into functional or requirement level detail here. Nor will this list be exhaustive of everything we might do with [[Intent AI Home|CKG]]. The focus here is outlining the strategic direction, and core tenets of CKGs design going forward. 


This is a living document which will be updated as we learn more about our users’ interactions with [[Intent AI Home|CKG]] and our business goals; so Feedback/comments are helpful and encouraged :)

## Business Goals & user definitions
---
I've found 3 [[Intent AI Home|CKG]] major OKRs for 2023. While i'm mindful it's currently Q3 and we're likely to get new OKRs in the coming months, I would guess they're going to be thematically similar. So I will continue to use these as a baseline for high level planning and strategy in [[Intent AI Home|CKG]] and adjust as needed next quarter. 

### 1. Unlock [[adoption]] of [[Express]] with Communicators 
#### Details
[[Express]] is very intentional in giving it's user proto-personas a different title than the core CC app portfolio. By calling these users "communicators" we establish a clear delineation in their desired outcome compared to the core CC app "creators" persona. The value prop of our services to communicators stops at the output they achieve within the app in any given user session. With this in mind we can consider the impact that having a contextual understanding of this user's desired output might have. 

If mastery of the tool or improvement of their craft is not a goal to communicators (as it might be among "creators" in one of the flagship CC apps, discussed below) then a reduction in time spent in the tool and/or proficiency required to arrive at a certain quality of output are the predominant factors to optimize for. 
#### Use cases in canvas
- Layout & content understanding 
	- HMW understand intent based on the content type and arrangement of elements on the canvas (text, images, graphics, etc) 
		- Arrangement details  
			- Posters likely have some common layout differences than ig posts
			- Brand guidelines
			- Personal style of doing things
			- 
	- This way we can power experiences like:
		- moving elements based on readability, brand guidelines 
		- Suggesting new elements to add 
			- invite,RSVP, "find out more at..." -> add QR code
- Aesthetics suggestions 
	- HMW understand intent based on the look/feel/character of the elements used on the canvas
		-  Element metadata 
			- [[Color]] 
			- font 
			- keywords
	- This way we can power experiences like: 
		- Better curation of suggestions/recs to add
			- Blues, snowflakes -> winter, christmas etc
			- Red, white -> valentines 
			- Yellow, fireworks -> Diwali 
			- Green, yellow, blue -> Summer beach party
			- Why am I getting winter photos for my summer template?
				- photo: ![[Screenshot 2023-08-15 at 2.28.33 PM.png]]
		- theming and [[Color]] coordination recommendations
			- you could create a family photo card/poster with a collage of images and "theme" it Wintery, Summery, Camping, etc and we could understand the elements, filters, etc to add
			- [[Artemis]] 
- Template understanding 
	- Purpose
	- Format 
		- video, post, flyer, etc
	- Theme
	- Event 
	- Context
- Image understanding 
	- theme, subject
- Social understanding 
	- HMW link the implicit intent of a user interaction (searching for some term) with the assets, templates, etc that they ended up using on the canvas and exporting 
		- "Barbie" -> pink, shiny
- Workflow assist 
	- Inspo generator 
		- HMW understand when a user is stuck or lacking inspiration in editing something 
			- use A1 or FF to generate some ideas with intent context 
				- "As a user who has been struggling for some time on how I should make a change to the wording in a section on a resume i'm editing in [[Express|AX]], I would like [[Express|AX]] to give me some ideas with how I might word the section. This way I can take some inspiration or get new ideas about how to write my document. "
					- this could be for just about any content type 
					- Could be enriched with [[Intent AI Home|CKG]] intent 
						- resume template, boring font, limited color pallet -> cut and dry
						- Lots of graphics, bright colors -> fun and wacky
	- Repetitive workflow recovery / variation 
		- "As a communicator using [[Express|AX]] for work, I am frequently using the app in consistent ways to generate updated assets like newsletters and announcement posts", I would like to save time in doing this by having [[Express|AX]] suggest these action without me having to recover them, and suggest some variations."
			- HMW understand the intent of a regular newsletter and prompt the user to create a new newsletter, possibly with a new suggested template but to auto fill some info
				- team name, product name, date, company assets etc
			- HMW augment the suggested assets based on document understanding? 
				- eg. if a user is creating a newsletter about "last week at summer science camp" can we suggest their [[Lr Home|Lr]] photos from the related album, filtered by capture time in the last week ranked by the quality of the photos?
					- we already have scoring around in focus, faces, expo, etc
	- 

#### Use cases in [[Express]] home 
- [[Express|AX]] -> flagship app prompt based on intent
	- HMW use our understanding of intent to prompt the user when they need to launch one of the flagship apps, and give them a CTA to do so. 
		- As users give more signal about intent in a given session (eg. crop a photo, make an ig post, edit a [[Recommendations Home|PDF]]) can we understand when the capability is within [[Express|AX]]'s bounds and when it isn't. 
- 
#### Test cases to think about 
- I'm designing an invite for my Diwali party
	- "Diwali" is likely to appear in a text field 
	- [[Color]] associations 
		- yellow
		- red
	- Graphic associations 
		- Lanterns 
		- fireworks
		- candles 
	- Time of year
- I'm making a social post for my house show 
	- Understand that the purpose is to meet up
		- there's likely to be a QR code, RSVP link, date/time/location 
	- "music", "comedy" etc likely to appear in text fields 
	- 
- I'm creating an image to post on the running channel in slack for a group run on Saturday
	- Understand that the purpose is to meet up
		- there's likely to be a QR code, RSVP link, date/time/location 
	- imagery of Shoes, running, outdoor as photos or graphic elements  

### 2. Dive a step function change in CC flagship engagement and retention 
#### Details
Here our user is known as a "Creator", and depending on their context and experience with the given CC app they're using, can have a wider range behaviors, desires, and motivations than the previous case of "communicators". For instance, newer users may be motivated to They actually be interested in mastery of the tool, and the improvement of their craft. These users aren't uniform however and likely comprise individual creators, and those working as part of a professional studio. 
 
 
 **Rewrite this- too self congratulatory:** 
I've previously spent some time looking into this user with (then) [[Lr Home|Lr]] product leader Josh Haftel in 2021. In short the document outlines why a user moves from first usage and being primarily motivated by wanting "better" photos (or illustrations, animations, etc), to gradually being interested in the art/craft itself and therefor continuing to use CC as an enthusiast/pro creator.

- User journey diagram:
	-  ![[image 1.png]]
	- **Typical ig user**
		- Extrinsically motivated, focused on results
		- *low pain tolerance*  
			- This is [[Intent AI Home|CKG]]'s opportunity  
		- low motivation 
		- Our goal here is to build excitement and interest 
	- **Emerging / Enthusiast user**
		- Some interest in photography
		- Some knowledge of [[Lr Home|Lr]]/Ps
		- Medium motivation
		- Our goal here is to deepen learning 
	- **Pro Photog**
		- Intrinsically motivated, focused on mastery 
		- High knowledge of CC
		- "Less time in post is money saved"
			- This statement likely applies to pro users of all CC apps
			- Similar motivation to "communicators" in this way
		- Our goal here is to accelerate common steps/patterns in the tool

[[Intent AI Home|CKG]] stands to have substantial impact on the number of users we're able to migrate up this curve and how long it takes them to do so. By giving users a more contextually aware and intent driven experience we can quickly move through early phases of this model and reach higher engagement by entrenching ourselves as *the* destination for their creative process. 
#### Use cases - Novice  
- As a new user to [[Lr Home|Lightroom]], i would like to understand how I change the photo i captured into what I see on my social timelines. This way I can post better images to my feed. 
	- Next step suggestion in edit flow 
		- Might mitigate "well now what"
	- Look or over all aesthetic suggestion 
	- inspo panel 
		- Display list of photos from discover that make use of similar photo elements as user's catalog 
- User proficiency classification 
	- Can we intuit they're a novice and then recommend different tutorials?
	- We can confirm this with the user after some level of confidence 
		- adherence to our predicted set of actions within that user group 
##### Enthusiasts
- Pre-expand 
	- expand the curve tool or crop or something bc we know they usually follow a flow 
		- Crop -> Curve -> color correct -> effects 
##### Pro photogs
- Import session understanding 
	- If they're coming from a portraiture session they'll have 900 of the same composition 
		- If they make one edit here with any consistency, we can apply that to the rest
			- Crop, WB adjust etc 
	- 
- [[Assistive Workflows & Multimedia Processing - Program Home|Assistive workflows]] 
	- Crop
	-  
		- Screenshots w annotation 
### 3. Set the foundation for CC growth for next 3 years ( change to [[Recommendations Home|DC]])
#### Details 
Already largely in progress with the creation of [[Intent AI Home|CKG]]. As outlined here that investment can/will be leveraged in numerous ways. The additional work to be done here for more [[global type|GTs]], improved intent taxonomy, etc will be explored later.

#### [[Intent AI Home|CKG]] Usage 
- Examples 
	- Screenshots w annotation 
- 
## Product Hypotheses
---
### **Hypothesis 1** - We believe that by deploying personalized experiences relevant to a given users understood intent, that we can alter/impact user experience such that they will take an expected set of additional or alternate actions than they otherwise would.
- [x] proof or rejection statement 

### **Hypothesis 2** - We believe that we have a sufficiently nuanced understanding, or can build the complexity of understanding of user actions to be impactful motivate this change in behavior in the creative or communication process.
- [x] define helpful 
	- People's ideas of AI 
		- time saver
		- force multiplier 
- [x] proof or rejection statement 

### **Hypothesis 3** - We believe that this change in user behavior will result the in the desired business outcomes of increased usage and continued engagement across CC surfaces. 
- [x] proof or rejection statement 




## Appendix 
---
- Mission statement 
	- unlock the power of creators and communicators 
	- Eliminate the friction of using the tool from the creative process 
	- 
- link to my doc for Josh 
- Call out my limited tenure 
	- Establishing a clear, concise, and cogent vision is a function of three thematic areas of knowledge: 
		- Knowledge of relevant Users 
		- Knowledge of current and emerging Technologies 
		- Knowledge of applicable Constrains 
	- my knowledge of each is limited
- What is the technical purpose of [[Intent AI Home|CKG]]
	- Is it the end all be all graph?
	- Or one component in intent understanding 

- Thinking through ![[Ritu - 8.20.2023 - 1x1 Meeting#CKG capabilities]]

## Input → Intent 

In order to give a meaningful output relative to the user's intended task or actions we'll need to be able to understand what their intent is. The first phase is centered on correctly understanding the user's intent. 

|User Inputs|Details|
|---|---|
|Query|- query term|
|User Context|- Geo  <br>- time  <br>- account type|
|Tool Context|- App|
|Project metadata|- Project name|
|Ingredients(?)|- Media, fonts, colors used|

## Intent → Ingredient & elements

With an understanding of the users intent, we can boost, suggest, and display more relevant ingredients and elements when the user is looking to add to their project.
- Would this extend to FF usage? 
	- Eg. based on an understood intent to make a Halloween party invite, might we be able to give better prompts to FF for image/font generation, or A1 for text gen?

## Intent → Tools & Actions


# Notes 
- What is [[Intent AI Home|CKG]] and who is it for 
	- "creative [[Intent AI Home|knowledge graph]]" means what exactly? 


