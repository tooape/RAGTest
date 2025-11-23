---
created: 2024-01-23
aliases:
  - Style
  - color
  - photo style
  - photo styles
tags: []
Related Pages:
  - "[[Intent AI Home]]"
protected: true
pageType: programHome
---
# Style Home
---
# Wikis 
- [Curation team's deck](https://xd.adobe.com/view/8a08fa1f-d628-4e50-ac91-6666c097dcaf-df5b/grid/#access_token=eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE3MDYwNTEzNTg4MDZfN2VhYzZlYmUtZjdjYi00MmJiLTg0YzQtYmRlNDY3MDIzYzQ3X3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJDb21ldFdlYjEiLCJ1c2VyX2lkIjoiRDBGQzBBMjM1QzBGQUM1QzBBNDk1RUNDQGFkb2JlLmNvbSIsInN0YXRlIjoiIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJEMEZDMEEyMzVDMEZBQzVDMEE0OTVFQ0NAYWRvYmUuY29tIiwiY3RwIjowLCJmZyI6IllFTzYzQU5ORlBQNUVERUtGQVFWWUhBQURRIiwic2lkIjoiMTcwNDgxODM3OTkxMF83MGE0MzgxOC1hYTEwLTRhOWUtYmM5MS1kZTM0ZmQ5OTU0ZTlfdWUxIiwibW9pIjoiYzIzMDhlMTIiLCJwYmEiOiJNZWRTZWNOb0VWLExvd1NlYyIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsImNyZWF0ZWRfYXQiOiIxNzA2MDUxMzU4ODA2Iiwic2NvcGUiOiJBZG9iZUlELG9wZW5pZCxjcmVhdGl2ZV9jbG91ZCxzYW8uY2Nwcml2YXRlLHNhby5jY3B1Ymxpc2gsYWIubWFuYWdlLHNhby5jb21ldF9zZXJ2aWNlIn0.HXN2wiQLDrNyws1PrwJ_UwYDm-AIydy5M_V92clQ2Z9dcB5t1HRUcPX2-v3nk3qEl5gc8gQLdA8D5JDKKY2wr48-a96T_Wk0d-YfCswfNJ0E8oKStjq90Pg9bl2rcnSfWMaM1ZcxHAp1eUjlly567OeZL1lpNMD6TcP5SE5BZINPkF1aT0pxodTbcrWrBpx4-IjH3JT4f4l1cEJj7MeeibRl3ZJKPtpPxYit9lKsQvrWMOwlOzlJRRLmu2ac9L-mnG96flt_g120rRJFGvoM7PQzfHbExKeIOMqpKbovD4QCtFeEsRzQYSqr3UBV4mWWdjEAz5iABzK3Ts_u90pLSg&token_type=bearer&expires_in=86399998)
- [Style Wiki home page](https://wiki.corp.adobe.com/display/adobesearch/Style+Understanding+Strategy)
- [Eng Wiki](https://wiki.corp.adobe.com/display/adobesearch/Contextual+Recommendations%3A+Style+Based+Recommendations)

# Style Description
Any time creativity is involved you'll quickly get into the question of style. We therefor view style intelligence as an incredibly valuable signal for any ranking or recall related feature in DMe. This is a very large, ambiguous problem which has been tried several times, by several teams (eg. Content Design, [[FireFly]]). To prevent repeating past mistakes we'll start by drawing some quick scope boundaries: 

- We are not using classification labels or a design taxonomy
- We are not looking to define a new set of dimensions
    - Limitations discussed later in document 
- We are not trying to understand what "minimalism" is or force some standardized definition
    - We are trying to avoid making hard definitions and judgments on the "squishy" parts of this problem 

With this context in mind, we do not think this is a problem that can be ignored. Navigating style is challenging for even experienced designers, but this challenge is multiplied for less design experienced users who may not have a clear vision, or know the design terminology that might return one look or another. This leaves users who have little skill and understanding, and unclear vision of their desired outcome struggling to accomplish a satisfactory result in [[Express]].

## Problem statement
> how might we provide style intelligence which allows Search & Discovery use cases to precisely rank results based on their stylistic qualities? 

Producing a highly relevant, and useful result for any give query or recommendation relies on a few areas of intelligence: 

- **Contextual** info about the topic or subject matter of their project 
- The user's **personal** preferences, and tastes
- The **style** decisions they made in their project

While we have made progress on contextual understanding with [[Intent AI Home|MINT]], and are exploring [[Personalization Home|personalization]] in the [[Recommendations Home|Recommendations]] Program, this provides only a broad understanding of the user's desired result. Delivering real precision requires an understanding of style. We view style as a precision search problem where users are currently struggling to find the correct content because important signals are not being used.
![[Style Understanding Strategy Mar 03 2025.png]]

## Phase 1 Asset Style understanding 
As mentioned above, we are not interested in taxonomies, classification structures, or definition sets. We will avoid these pitfalls and instead **focus on the style similarity between assets**. Where current systems might place all of the previously shown "cartoon burgers" in a similar category we'll provide better signal by creating an embedding space which captures these nuances. Today many embedding spaces are focused on semantic information, and might cluster all of these burgers together since they're all around the same topic or contents. We're interested in creating an embedding space which is trained only on the style qualities of assets, with no regard for subject matter. For instance, while a dog and basketball have nothing in common and would typically be far apart in an embedding space. If both the dog and basketball asset happened to be black and white photos we would expect them to be very close together in this space.

This will allow us to provide supplementary signals around style to search and recommender systems which already have these semantic relationships understood by other embeddings.

## Phase 2 Compositional style 

Expanding on the similarity approach from phase 1, we can leverage this style embedding space to create template-wide understanding of relative style across multiple assets, and asset types.

We see in many projects that assets which are not from the same artist series in the stock index, and aren't as closely related get used together to great effec

# Old color page
---
- [Color guide](https://creativecloud.adobe.com/cc/discover/article/understanding-color-a-visual-guide)
- [Color trends](https://color.adobe.com/trends)
- [Adobe color](https://color.adobe.com/create/color-wheel)


## Use cases 
1. As a communicator working on a project in [[Express]] I would like to be able to see [[Recommendations Home|recommendations]] for new elements ([[Icons]], text effects, images, backgrounds) with appealing colors related to my canvas. This way I don't have to sift through irrelevant suggestions or try to imagine what something might look like in another color. 
2. As a communicator struggling to move forward with a project in [[Express]], I would like to be inspired by new colors, and color combinations for elements in my canvas. This way I can find a new direction or perspective and continue making my project. 
3. As a creator I would like to see a pallet of recommended colors for my selected tool (pen, brush, pencil, HSL tone controls, etc) based on the color composition of my canvas. 

## Elements of color understanding 

### Types of color relationships 
- Analogous 
- Monocrhomatic 
- Triadic 
- Complementary 
- Split complementary 
- Double split complementary 
- Square
- compound
- shades

### Key or primary color within a user canvas or project 





# Photography styles 
---
This page is in scope of the first milestone of our [Style Understanding Strategy](https://wiki.corp.adobe.com/display/adobesearch/Style+Understanding+Strategy) (please read this first). Here, we are only looking at asset:asset similarity. Looking at wider compositions across an entire canvas and complementary style will follow, but is not inscope here. With a solid model for Design assets and Icons now in hand we can incorporate style understanding in photography.

## Near term use cases

Over the next few quarters there are a number of product surfaces, and use cases for style similarity. 

1. Asset [[Recommendations Home|recommendations]] in asset pickers 
    1. [[Photoshop|Ps Web]], [[Express]], PDF
2. [[RAG]] use cases involving generating multi-page or complex creations 
    1. [[PDF2pres]]
3. Editor search results weighting towards more stylistically relevant content
    1. [[Express]], [[Photoshop|Ps Web]]

**Content**

- [Overview](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-Overview)
    - [Near term use cases](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-Neartermusecases)
- [Disambiguations](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-Disambiguations) 
    - [Photo style understanding vs. Photo asset type](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-Photostyleunderstandingvs.Photoassettype)
    - [Style, composition, and mood disambiguation](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-Style,composition,andmooddisambiguation) 
    - [Milestones](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-Milestones) 
        - [Current State](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-CurrentState)
        - [M1 - Creator use cases](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-M1-Creatorusecases) 
        - [M2 Composition understanding](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-M2Compositionunderstanding) 
        - [M3 Eventual goal - C-Pro use cases](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-M3Eventualgoal-C-Prousecases) 
- [Data & Training](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Photography+Styles#PhotographyStyles-Data&Training)

# Disambiguations 

---

## Photo style understanding vs. Photo asset type

Users will want to be able to go between asset types and see [[Recommendations Home|recommendations]] which are similar regardless of our categorization about which assets are what types. When we say "supporting photo styles. We're really discussing improving the model's fine grain understanding of photography, not a specific asset type. 

This distinction is also quite blurry in the asset corpus, as some "design assets" are just photos of things or people with the background removed. 

![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-12%20at%2015.17.41.png?version=1&modificationDate=1755038527203&api=v2)![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-12%20at%2015.15.13.png?version=1&modificationDate=1755038541740&api=v2)

(_left: express design assets, right: [[Photoshop|Ps Web]] Stock content collection)_ 

  

Likewise, in apps like photoshop, the definition of a "photo" will be stretched as creators and C-Pros heavily edit images. 

  

![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/b7579e32305939.5605bbc896c32.jpg?version=1&modificationDate=1755038197450&api=v2) ![](https://wiki.corp.adobe.com/download/attachments/3587106912/Abobe-Photoshop-double-exposure.jpg?version=1&modificationDate=1755038197423&api=v2)

When we say "supporting photo styles, we're really discussing improving the model's fine grain understanding of photography. Photography here should be considered a deep dive on a particularly prevalent style in itself, not a modality. You could make a similar deep dive into other styles which we might think are asset types, for instance Illustration or 3D. 

Since we'll want to be able to jump between different asset types and understand stylistic similarities we're not looking to train something which recognizes photo "style" independently of design asset or icon "style". 

  

## Style, composition, and mood disambiguation 

It's easy to think of things like "meloncholy" or "romantic", or "dreamy" as styles. We consider these things Moods, not style descriptions. Descriptions around "mood" or "vibe" is a byproduct of the subject matter and the visual style of an image like color, and tonality, in combination with it's subject matter or composition. To clarify the distinction let's take an example of two stills from two different movies. 

  

|Still|![](https://wiki.corp.adobe.com/download/attachments/3587106912/in-the-mood-for-love-06-g-2hruizw-1.jpg?version=1&modificationDate=1757024363973&api=v2)|![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-09-04%20at%2015.28.51.png?version=1&modificationDate=1757025129657&api=v2)|
|Mood descriptors|1. romantic<br>2. mysterious <br>3. dreamy<br>4. sensual <br>5. moody|1. melancholic <br>2. nostalgic <br>3. intimate <br>4. tender <br>5. bittersweet|
|Composition descriptors|Vanishing point, golden aspect ratio, use of negative space<br><br>![](https://wiki.corp.adobe.com/download/attachments/3587106912/in-the-mood-for-love-06-g-2hruizw.jpg?version=2&modificationDate=1757024286333&api=v2)|vertical repetition, middle symmetry of subjects<br><br>![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-09-04%20at%2015.23.47.png?version=2&modificationDate=1757025068423&api=v2)|
|Style descriptors|Strong contrast, very warm/red tint, black shadows, underexposed, desharpened|Softer contrast, yellow warm tint, lowered highlights, raised shadows|

  

  

  

  

## Milestones 

### Current State

The style model has some awareness of photography, but very broadly. 

|![](https://wiki.corp.adobe.com/download/attachments/3587106912/441BCCB3-9CB1-4DD8-92FF-9DADD0B481CC.jpeg?version=1&modificationDate=1755100932697&api=v2)|Cat|![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-13%20at%2008.55.45.png?version=1&modificationDate=1755100973197&api=v2)|The model has clearly understood photography as the foundation of the style here (right col of results), and has biased the results away from the illustrations we see on the left side.|
|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/1842039331-R1-E022.jpg?version=1&modificationDate=1755100939660&api=v2)|Dogs|![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-13%20at%2008.58.28.png?version=1&modificationDate=1755100961600&api=v2)|The model seems to have latched onto black and white, but is still returning illustrations.|

  

### M1 - Creator use cases 

Ideally in an initial release we would be able to get some understanding of a photos' color and tonality, and it's texture such that creators can get [[Recommendations Home|recommendations]] which is clearly related to the style of content they're working on, and agents can steer them directionally towards a desired look. 

We will set compositional considerations like rule of thirds, centered subject, depth of field, etc aside for now.

For this release we will totally disregard composition as a stylistic consideration. Placement of the subject(s) within the frame, framing elements like line, light, and shadow will not be given special consideration. 

  

**Color**

We should be able to differentiate between 

1. Different white balance
    1. Cooler / Warmer
2. Saturation & Vibrance 
    1. Raised / Lowered 

|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/DSCF0863.jpg?version=1&modificationDate=1756914985437&api=v2)![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/DSCF9765.jpg?version=1&modificationDate=1756914980233&api=v2)<br><br>![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/DSCF0917.jpg?version=1&modificationDate=1756178769930&api=v2)|![](https://wiki.corp.adobe.com/download/attachments/3587106912/DSCF8616.jpg?version=1&modificationDate=1756914970637&api=v2)<br><br>![](https://wiki.corp.adobe.com/download/attachments/3587106912/DSCF9477.jpg?version=1&modificationDate=1756914960800&api=v2)![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/DSCF0913.jpg?version=1&modificationDate=1756178769577&api=v2)|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/DSCF0660.jpg?version=1&modificationDate=1756914697550&api=v2)<br><br>![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/DSCF0332.jpg?version=2&modificationDate=1756178869263&api=v2)|![](https://wiki.corp.adobe.com/download/attachments/3587106912/DSCF9711.jpg?version=2&modificationDate=1756178877753&api=v2)![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/DSCF3486.jpg?version=2&modificationDate=1756914584117&api=v2)|

  

**Exposure & light**

Here we're looking at

1. Exposure Value
    1. + / - 
2. Contrast
    1. High / Low
3. Shadows
    1. Raised / Lowered
4. Highlights
    1. Raised / Lowered 

  

|Neutral exposure / unedited|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/Screenshot%202025-09-03%20at%2009.01.47.png?version=1&modificationDate=1756915511827&api=v2)|
|Raised (brighter) shadows|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/Screenshot%202025-09-03%20at%2009.02.34.png?version=1&modificationDate=1756915532057&api=v2)|
|Lowered shadows|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/Screenshot%202025-09-03%20at%2009.02.40.png?version=1&modificationDate=1756915546840&api=v2)|
|Raised highlights|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/Screenshot%202025-09-03%20at%2009.02.47.png?version=1&modificationDate=1756915569070&api=v2)|
|Lowered Highlights|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/Screenshot%202025-09-03%20at%2009.02.53.png?version=1&modificationDate=1756915587113&api=v2)|
|Increased highlights + lowered shadows (increase in overall contrast)|![](https://wiki.corp.adobe.com/download/thumbnails/3587106912/Screenshot%202025-09-03%20at%2009.03.04.png?version=1&modificationDate=1756915610357&api=v2)|

  

  

One other note is on "crushed blacks", which is a common stylistic trick where you raise the black point so that the darkest parts of the image go slightly grey. This is loosely related to the above, but we should be able to pick up on this.  

![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-25%20at%2020.49.17.png?version=1&modificationDate=1756180179823&api=v2)![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-25%20at%2020.49.28.png?version=1&modificationDate=1756180180283&api=v2)

  

**Grain** 

We should also understand commonalities in grain:

1. Amount 
2. Size & Roughness 

![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-25%20at%2020.31.03.png?version=1&modificationDate=1756179308280&api=v2)![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-25%20at%2020.30.52.png?version=1&modificationDate=1756179304947&api=v2)![](https://wiki.corp.adobe.com/download/attachments/3587106912/Screenshot%202025-08-25%20at%2020.31.21.png?version=1&modificationDate=1756179309220&api=v2)

  

### M2 Composition understanding 

Understanding of compositional techniques like leading lines, rule of thirds, centered subject, depth of field, etc.

### M3 Eventual goal - C-Pro use cases 

This is out of scope for now.

Ideally we would get to such a fine grain understanding that C-Pros in [[Lr Home|Lightroom]] and photoshop would be able to use style understanding in agentic workflows. For this milestone we would want to be able to support compositional understanding. 

The big changes here are in fine tuning color, with per color channel understanding of Hue, Saturation, and Luminance (**HSL).**

How might we use the XMP data in cooper to be able to understand that across images that visuall present "crushed blacks" that there's a shadow toe curve lift? Then an Lr agent could know how a crushed black look can be added to an image. 

# Data & Training

---

  

The [[Lr Home|Lr]] Applied AI (aka "FutureFotos") team has provided some prior research and datasets for this. 

  

1. [Photoeye](https://openaccess.thecvf.com/content/CVPR2025/papers/Qi_The_Photographers_Eye_Teaching_Multimodal_Large_Language_Models_to_See_CVPR_2025_paper.pdf) - a model for anlyzing aesthetics, composition, and style in a photo. 
    1. Built on the custom made "PhotoCritique" dataset. 
2. [LR aesthetic scoring model](https://git.corp.adobe.com/AdobeMIL/ias2)
    1. [Aesthetic ranking paper](http://users.eecs.northwestern.edu/~xsh835/assets/eccv2016_aesthetics.pdf)
    2. [Personalized Aesthetics](http://users.eecs.northwestern.edu/~xsh835/assets/iccv2017_personalizedaesthetics.pdf)