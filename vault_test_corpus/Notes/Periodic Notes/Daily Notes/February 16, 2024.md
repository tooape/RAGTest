---
pageType: dailyNote
publish: false
aliases:
  - 02.16.2024
  - 2.16.2024
created: "02.16.2024"
---
# Notes
---
- [x] Get 1x1 with [[Amanda]] 
- [x] Get [[CKG 101]] with Amanda's [list](https://adobesearch.slack.com/archives/C06K39LMPC3/p1708108833887379) going 
- [x] Get other design channel together? 

[Intent Understanding service](https://wiki.corp.adobe.com/display/adobesearch/Contextual+Intent+Understanding+Service)




# Meetings 
---


## Intent Check In #meetings 

- leagla issues 
	- prompts and outputs 
	- User gen data 
- intents which correlate to the user providing their own photos
From Vipul
```[2:09 PM] Vipul Dalal

My thoughts on Fitment Discovery, i.e where we could be heading: 

There are several signals that could be used to power contextual discovery that helps in Fitment to creative intent & content on canvas.

- ContentType (Image/Photo/Illustration/Video/Audio/3D)
- Sub-ContentType

(background/cartoon/clip-art/animated/wallpaper/sketch/drawing/painting/…)

(design/icon/logo/…)

(art/wallpaper/outline/perspective/abstract/perspective/animated/..)

(watercolor/oil-painting/acrylic painting/…)

(Shorts/reel/…)

…

- Style-type:
    - (autumn/fall/winter/spring/winter/night/foggy/…)
    - (Bokeh/b&w/panning/double-shadow/double exposure/ drop shadow/…)
- Aspect ratio
- Orientation 
- Subject orientation
- Color/Hue
- HasText
- Copyspace (co-ordinates)
- Semantics
- DoF
- hasPeople
- Ethnicity
- ….

The above is not a comprehensive list but some of them are very contextual to what kind of content they have and overall intent. The intelligence is about pruning these signals to what is crucial for intent (canvas + session) and then apply it for retrieval. Therefore, we should have these signals in the index and associated with core data-types (mime types) in our Entity structure (regardless of storage). 

For example, I tried seed queries: “cat”, “golden gate”, “wood with two paths”, “Surfing”. And then almost you apply some of these relevant parametric modifiers and discovery results are very different. 

“Cat drawing”, “Cat cartoon”, “Cat clip-art”, “Cat sketch”, “Cat outline”, …

“Golden gate wallpaper”, “Golden gate design”, “Golden gate painting”, “Golden gate watercolor”,  “Golden gate abstract”, “Golden gate in rustic”, “Golden gate at night”, “Golden gate in winter”, .. 

“Wood with two paths background”, “Wood with two paths rainy”, “wood with two paths bokeh”, …
```

Next set of evals: 
- Fix the obvious things 
- Image friendly set 
- All other templates run for other design elements 
- MM work A1 embeddings 
	- visual cohesive results 
	- Query side not understanding side 