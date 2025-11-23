---
pageType: programHome
creation date: 2023-08-07
tags:
aliases:
  - Lr
  - Lightroom
  - lightroom home
protected: true
---
# Lightroom Home
---
- [MAX 2025 Wiki Link](https://wiki.corp.adobe.com/display/adobesearch/Lr+Semantic+Search+MAX+2025)
- [LrD GA April 2026 Link](https://wiki.corp.adobe.com/display/adobesearch/Lr+Desktop+Rollout+-+SDC+Planning#LrDesktopRolloutSDCPlanning-Languagesupport)
- [Eval Queries Excel](https://adobe-my.sharepoint.com/:x:/r/personal/rmanor_adobe_com/_layouts/15/doc2.aspx?sourcedoc=%7B7F39A040-7A7D-41F9-83F3-B4E89507827F%7D&file=Lr%20Semantic%20Search%20Evals.xlsx&action=default&mobileredirect=true&DefaultItemOpen=1&wdOrigin=APPHOME-WEB.LOGIN,APPHOME-WEB.FILEBROWSER.RECENT&wdPreviousSession=8fb12408-058e-453b-98e3-6ccea03c5f87&wdPreviousSessionSrc=AppHomeWeb&ct=1754408230109)
- [Search dashboard](https://app.powerbi.com/groups/me/apps/a6a3c37c-acae-463a-86f3-2a8f29c92955/reports/fe510c38-d53f-44c8-ac58-d53cfb4a7062/1ffebe61af88124ae2ab?experience=power-bi) 

# 2025
---
My catalog ID: 
2e23206146d74b928b90b6c54160ef4f


## Links 
- **Lr Search usage dashboards**
	- [Lr Autocomplete Search Usage](https://experience.adobe.com/#/@adobemobiledev/so:adobem9/analytics/spa/index.html?lazyLoadPhpSession=1#/workspace/edit/63e4489d0bea741070c8f178)
	- [Lr Mobile Search Usage](https://experience.adobe.com/#/@adobemobiledev/so:adobem9/analytics/spa/index.html?lazyLoadPhpSession=1#/workspace/edit/617844a6e9d2443854fc8bc3)
	- [Lr Desktop Search Usage](https://experience.adobe.com/#/@adobemobiledev/so:adobem9/analytics/spa/index.html?lazyLoadPhpSession=1#/workspace/edit/60219fc9fc7df953034aeacc)
- [Semantic search discovery Hub eval demo](https://discovery-hub.corp.adobe.com:8080/lightroom-semantic-search)
- [Relevance page](https://wiki.corp.adobe.com/display/adobesearch/Relevance+Planning)


**Terminal curl command to fetch slohia prod test catalog token**
```
curl -X POST "https://testdata.adbephotos.com/v1/ims/uat?indent=1" -H "Content-Type: application/json" -d '{"username":"slohia+prod_semantic_search_1@adobetest.com", "password":"Adobe#123", "client_id":"LightroomMobileOz1"}'
```

Curl for my account 
```
curl -X POST "https://testdata.adbephotos.com/v1/ims/uat?indent=1" -H "Content-Type: application/json" -d '{"username":"ryan.manor@hey.com", "password":"MandarinCranberries,&3", "client_id":"LightroomMobileOz1"}'
```

## Semantic Search at MAX

- [[April 01, 2025]]
- [Wiki page](https://wiki.corp.adobe.com/display/adobesearch/Lr+Semantic+Search+MAX+2025)
- [Test cases wiki](https://wiki.corp.adobe.com/display/lightroom/Semantic+Search+High+Level+Test+Cases)

## Post max

Once the MAX release is launched and stable in production. We'll continue to push development on two tracks: 
1. Tech and relevance 
2. Surface expansion 

### Tech and Relevance 
- First feedback relevance tweaking
	- After launch if there are any major missed in relevance they'll quickly be evident from user behavior, or qual. feedback. We should carve out time to react to these first issues. 
- Embedding optimization 
	- Matryoshka 512/768
	- MobileClip 
- Additional NER and query intelligence 
	- Lens models 
	- Shooting settings 
	- Behavioral 
		- Edited 
		- Picked 

### Surface expansion 
1. Web GA
2. Desktop Release 
	1. This is a big one which will have UX questions to answer like autocomplete, faceted navigation, and other UI/UX changes. 
	2. This is also a cost savings opportunity by replacing the existing Autocomplete
3. Mobile Release 
	1. Once this is complete, we would (in theory) be able to deprecate the legacy index
	2. 


# Prior years

## 2024 
---
- [[Lr 2024]]
- [2024 LR Strategy deck](https://adobe.sharepoint.com/:p:/r/sites/LightroomEcosystemHome/Shared%20Documents/Strat%20Planning/2024/FY24%20Photography%20Category%20Strategy%20Artifacts.pptx?d=wd384898ce5e44f5eb0a9885e615f8aa6&csf=1&web=1&e=x7bKFV)
- 2024 Lr Search: [[USS-Lr Discussion.pptx]]
- [Lr Strategy Deck 2024](https://adobe.sharepoint.com/:p:/s/LightroomEcosystemHome/EYyJhNPk5V5PsKmIXmFfiqYBwwL6mVkWRXBHaEIYEf5_UQ?email=rmanor@adobe.com&e=4:h3VMUY&fromShare=true&at=9&wdLOR=c46274FF9-CC03-2F45-8408-23E3286F26AE)
- [Home Wiki page](https://wiki.corp.adobe.com/display/adobesearch/Adobe+Search+for+Lightroom)


### Post creator summit  
some of the metadata I thought would be important, isn't. 
- These are somewhat more cpro use causes admittedly

When would someone search through their photos: 
- blog posts
- workshops
- instagram posts around some theme 
- client emails and aks for an image


###  [SEARCH-8064](https://jira.corp.adobe.com/browse/SEARCH-8064?src=confmacro "https://jira.corp.adobe.com/browse/SEARCH-8064?src=confmacro")
We know some users have very large catalogs (see below). In order for them to stand a chance at organizing all of this we'll need to give them a way to return large numbers of photos in one search. This presents an issue given the search result limit of 10k records. 

**Story**
> As a user with a very large photo catalog, I would like to be able to automatically add any photo which meets some criteria specified by my filter conditions to an album. This way I can quickly and easily get some organization in my catalog. 

**Details**
 Since this is part of the smart albums feature, we can lay out a few assumptions to make our lives easier. 

1. The user does not need to browse all photos at once. 
2. The user does not need to re-sort the display order. 
3. The user does need to have a complete & correct result count for the search, even if not all results are displayed. 
4. If requested, we mush be able to display any one of the records from the >10k result set. 
5. Albums are not mutually exclusive. A photo may be long to any number of albums. 

Photos

#### Info
User catalog size distribution:
![[Screenshot 2023-12-12 at 1.33.49 PM (1).png]]






## 2023 
---
C# Ramp up
- [2H 2023 plan wiki](https://wiki.corp.adobe.com/display/adobesearch/H2+2023+LR+Search+Plan)
	- Decision: how to handle the migration from model 1 to model 2
		- Shut down model one
		- switch models under the hood 
			- possible data loss 
	- [demo](https://wiki.corp.adobe.com/display/adobesearch/Demo+Video+for+Unwanted+Photos)

### Strategy Notes 2023
- email from rob in feb 2023:
	- I see autocomplete as a core feature of any useful search these days. Apps like Google Photos, Apple Photos, Canva, [[Express]], PicsArt all have some form of autocomplete. The two comparisons that are most relevant for us are Google Photos and Apple Photos (that us, we are compared by photographers to these). In my mind, autocomplete is tables takes. Here is a link to a Miro board that shows various examples of apps that use autocomplete: https://miro.com/app/board/uXjVPj0d2V8=/?share_link_id=314783447339
	- My view is that usage is low because Search is not as visible within our [[UX]]. We are working on a mobile [[UX]] refresh during the second half of this year, and I’m asking our design team to look at bringing search to a more prominent position similar to Apple Photos and Google Photos (for example, as part of the global UI). 
	- I’m curious why autocomplete is so expensive. Is there an opportunity to redesign it in a more cost effective way? Could we rebuild the index less frequently? 
	- New capabilities like CLIP will help make our search more competitive as well. CLIP will also need autocomplete, right? 
	- We are integrating a new capability this year that will enable improved In-App and push notifications on mobile. It’s powered by AJO (Adobe Journey Optimizer). We’ll have opportunities to highlight functionality in more intelligent ways. For example, we could detect customers that haven’t used search and send them a notification that suggests they use it. 
	- Your MAU usage for auto complete. “The % MAU of using AC is  0.17% and 0.22% of using search” but I think you are using free MAU too to calculate that.” It looks like you are including free customers as well. 
	- In terms of user experience, I think it’s probably common that some customers benefit from autocomplete without actually tapping on a specific word. For example, if someone starts typing “Yosem” and they see an autocomplete hint, they may just finish typing the word “Yosemite” because they are already typing. The fact that Yosemite is hinted provides reassurance that they will receive results.
- Lr momentum
	- 54% mobile conversion 
	- 2M mobile only subs 

### Strategy Pillars 
100M MAU and 10M paid MAU

#### 1. GROW MOBILE & WEB  
Continue momentum on Mobile and extend on Web to drive [[adoption]] with photo hobbyists

We believe that by: Building the most advanced and easy-to-use photography app on mobile and web, enabling mobile & web journeys and integrating into 3rd party experiences, we will attract and convert photo hobbyists.
#### 2. BROADEN [[Lr Home|LIGHTROOM]] BRAND  
New [[marketing]] w/expanded value prop targeted to photo hobbyists

We believe that by: Positioning [[Lr Home|Lightroom]] beyond photo editing to serve photo organization and sharing and taking a leadership position in building a vibrant photography community, we will increase awareness and affinity for the [[Lr Home|Lightroom]] brand 
#### 3. INCREASE ENGAGEMENT & RETENTION  
Extend leadership in E&R focused on habit loops and one tap magic

We believe that by: Continually delivering premium value and one-tap magic across the ecosystem, prominently communicating that value and building habit-loops, we will increase usage frequency and retention.

### Specific Asks 

| Feature                             | Notes                                                  |
| ----------------------------------- | ------------------------------------------------------ |
| Maintain Search & Preset Operations | Continue to support features, performance, reliability |
| Complete Clean Up for Lr Web        | With defined path to broader Lr support as well        |
| CLIP/AdobeONE / LLM for Search      | [[[[Unified Search & Contextual Discovery - Program Home]]|[[Unified Search & Contextual Discovery - Program Home|Contextual search]]]] that supports NLP, e.g. “red car”    |
| AND/OR for searches                 | Especially important for People; NOT is nice to have   |
| Improved Discover Feed              | Leverage existing aesthetics data in Lr index          |
| Added Search Language Support       | Continue to keep pace with Lr language adds            |

We may add [[Intent AI Home|CKG]] to this list given the focus on search. 
- [[CKG for Lr Search - 8.29.2023 @ 02.52 pm - Misc]]

### Workstreams
- [[Unwanted Photos in Lr - 9.13.2023 @ 02.19 pm - Misc|Unwanted photos]] 
	- Max 2023 - tech preview 
	- GA Q1 24




### [ML criteria](https://wiki.corp.adobe.com/pages/viewpage.action?pageId=2463830068) for determining what photos to boot:
|                           |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| ------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------- |
| **Field**                 | **Algorithm** | **Description**                                                                                                                                                                                             | **Wiki**                                                                                                       | **Frequency**                                                                                                                                                                                         | **Residence** | **New Capability?** |
| **Unwanted blur**         | ML derived    | Blur quality model outputs 4 scores: undesired, desired, clear and acceptable blur<br><br>Model: [https://git.corp.adobe.com/amisraa/Undesirable-Blur](https://git.corp.adobe.com/amisraa/Undesirable-Blur) |                                                                                                                | Generated for each photo uploaded to OZ?No<br><br>Currently enabled on demand for best photos users in LrW.<br><br>Once the account is enabled , it's generated for each photo uploaded by that user. | OZ            | Existent capability |
| **Aesthetic score**       | ML derived    | Outputs overall aesthetic score + 10 other scores<br><br>- balancing<br>- content<br>- dof<br>- emphasis<br>- harmony<br>- lighting<br>- repetition<br>- rot<br>- symmetry<br>- vivid                       |                                                                                                                | Generated for each photo uploaded to OZ                                                                                                                                                               | OZ            | Existent capability |
| **Bad Exposure**          |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| **Best Photo score**      |               | Multiple models                                                                                                                                                                                             | [Link](https://adobe-my.sharepoint.com/:p:/p/shishett/Ed-2oF9dTvxDsGhVLsYG7psBIxYV-0fviyC31Wvyup-GiA?e=DY7MKC) | Generated on demand for a given album                                                                                                                                                                 | OZ            | Existent capability |
| **Receipt score**         | ML derived    | Integrated with auto tags . Outputs receipt autotag with confidence                                                                                                                                         |                                                                                                                | Generated for each photo uploaded to OZ                                                                                                                                                               | OZ            | Existent capability |
| **Dynamic categories**    | ML derived    | ML model that assigns a category (subject matter) <br><br>to an input JPEG.                                                                                                                                 | [Link](https://wiki.corp.adobe.com/display/SenseiContentFramework/Dynamic+Category+Service)                    | Generated on demand on a subset of images                                                                                                                                                             | USS           | Existent capability |
| **Auto Tags**             | ML derived    | Stock7 (Hashtag2 model)                                                                                                                                                                                     |                                                                                                                | Generate on each photo uploaded to cloud                                                                                                                                                              | USS/OZ        | Existent capability |
| **Stack ino**             |               | is the image part of a stack?                                                                                                                                                                               |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| **Face Detection**        | ML derived    |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       | OZ            | Existent capability |
| **Face Pose**             |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| **Dominant Colors**       |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| **Screen Shot detection** |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| **Pet detection**         | ML derived    | We use Object detection model for identifying animals/pets. Currently, used to improve "dog"/"cat" categories in autotags                                                                                   |                                                                                                                | Generated on subset of assets that has "animal" in it.                                                                                                                                                | OZ            |                     |
| **Eyes open/close**       |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| **Saliency Detector**     |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| **Subject in Focus**      |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| What else?                |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
|                           |               |                                                                                                                                                                                                             |                                                                                                                |                                                                                                                                                                                                       |               |                     |
| 


asdf

---

### Roadmap & work
