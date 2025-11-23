---
aliases:
  - ps web contextual recs
  - ps web contextual recommendations
  - ps web
  - psw
  - ps web action recs
  - ps action recs
  - ps recs
  - PS Web Recommendations
  - Photoshop Web Recs
  - PS Web Recs
  - Photoshop Web
  - PS Web
Related Pages:
  - "[[Recommendations Home]]"
  - "[[CKG 4.0]]"
  - "[[Style Home]]"
---
# Photoshop Mobile 
---

- Pm: [Michael Lewis](https://adobe.enterprise.slack.com/team/W4W9YQRA7)
Interested in stock content [[Recommendations Home|recs]], but REALLY interested in filters/effect/etc.

# Photoshop Web [[Recommendations Home|Recommendations]]
---

## Content [[Recommendations Home|Recommendations]] 
- Ps PM Contacts:
	- [[Hao Xu]]
	- [Jasper](https://adobe.enterprise.slack.com/team/WC4RU0GG7)
- Slack Channel: [ps-web-in-context-recommendation](https://adobe.enterprise.slack.com/archives/C0967S972VC)

## Action [[Recommendations Home|Recommendations]] 
 - [Wiki](https://wiki.corp.adobe.com/display/adobesearch/ML+approach+for+PsWeb+Presets+Recommendation)

## Goals
### 1. Prove SDC Can 
1. Prove we can Recommend non stock, and non content entities 
2. Prove we can incorporate the action intelligence where needed
3. Prove we have the content intelligence required 

### 2. Help casual/novice creators get into Ps Web

![[Screenshot 2025-08-28 at 10.47.58.png|500]]
^ 
> Be the best destination for Creators to quickly make quality, core images edits, while also giving them the control they need to go beyond template-/filter-based image editing. 
> Agentic workflows will help users accelerate their creation, and when blended with manual controls will help them [[express]] their authentic voice.

The goal here is to bring creators into the product, and help them accomplish their desired outcome in a way that does not force them into a box, or abstract the whole product away from them. We want to "draw them deeper" into the product and show what all can be done in an assisted way. 

### 3. Deliver a POC quickly 
We should not spend months modeling and designing systems from scratch here. The goal is to take foundational understanding that exists in SDC, and if need be layer in incremental new intelligence to deliver a new experience. 

## POC use cases 
Given the info above we'll prioritize use cases which we may be able to quickly power leveraging our canvas intelligence, while we explore action intelligence as a possible next step. 
### 1. Preset Adjustments  
> How might we understand the visual content of the canvas, and recommend different suitable and appealing configurations of the PsW adjustments to users so that they can quickly "try on" different looks for their artboard. 

Similar to the [[Lr Home|Lr]] preset [[Recommendations Home|recs]] feature. We will analyze the canvas contents and recommend PsW Adjustments with different configurations which would improve the visual interest of the canvas. 

### 2. Subject / Background manipulation 
> How might we recognize when a user might want to improve a subject driven scene with enhancements to the subject or background independently of each other. 

When a canvas has a strong subject in the foreground, recommend darkening or blurring the background, brightening, saturating, or adding contrast to the subject, etc. 

![[Screenshot 2025-09-05 at 08.10.45 1.png]]

![[Screenshot 2025-09-05 at 08.10.53.png]]

Recommending quick actions and filters 
"We've detected a person here's select background, blur background, select subject brightn subject, etc."
"we've detected the image is dark, here's autoboost shadows"

"we've detected it's a photo not a drawing, here's stylize or filters" 


→ think about creator journey, going back to the doc you made for Josh Haftel:  ![[August 28, 2025#Creator segments meetings]]

