---
pageType: Misc
created: 2023-08-07
modification date: {}
tags:
  - oldtags/CKG
Related Pages: "[[Intent AI Home]]"
---
---
> Unbounded learning will take too much time. I learn by doing so just start with some ticket/task somewhere and learn what you need for that - KC

> A knowledge graph is a structured representation of facts, consisting of entities, and relationships among entities.

# Resources 
- [[Jayant - 8.7.2023 - 1x1 Meeting#Links]]
- [Project wiki](https://wiki.corp.adobe.com/display/adobesearch/Creative+Knowledge+Graph)
- [Query Intent Service](https://wiki.corp.adobe.com/display/adobesearch/Query+Intent+Service+Overview)
- [Morpheus?](https://wiki.corp.adobe.com/display/adobesearch/Query+and+Text+Processing+Services)
- [CKG new hire](https://wiki.corp.adobe.com/display/adobesearch/CKG+-+New+Hire+Onboarding)
- [Arch video](https://adobe-my.sharepoint.com/personal/sadaphul_adobe_com/_layouts/15/stream.aspx?id=/personal/sadaphul_adobe_com/Documents/Recordings/Placeholder%20Workshop_%20High%20Level%20Architecture%20Review%20for%20Unified%20Search%20%26%20Contextual%20Discovery-20230803_144153-Meeting%20Recording.mp4&ga=1)
- [Graph generation video](https://adobe-my.sharepoint.com/personal/jaykumar_adobe_com/_layouts/15/stream.aspx?id=/personal/jaykumar_adobe_com/Documents/CKG/demo_videos/CKG_graph_generation.mp4&ga=1)

---
# Notes 
- GT -> [[global type]] 
	- CGT -> context [[global type]] 
		- query to predict [[global type]] 
	- AGT -> asset [[global type]] 
		- service to perform asset matching 
	- intent, background, color, design type 
- going from intent to color 
	- "Birthday" -> blue , pink 
- "birthday flyer"
	- Birthday -> intent
	- flyer -> design type 

## Graph Theory 
Networks are made up of: 
- Nodes 
	- Different entities 
- Edges 
	- Convey info about the links between the nodes
	- 3 types 
		- Undirected
		- Directed 
			- a tree is a directed graph 
		- Weighted 
- graphs are represented as **G = (V, E)**
	- Graph = (vertices/nodes, edges)
		- Vertices and edges are *sets* of data 
- Graphic:
	- ![Graphic:](https://miro.medium.com/v2/resize:fit:700/1*goT8sipQbDIoogV6Kc_3KA.jpeg)
- 
## CKG SDK README
This is the official release of Creative [[Intent AI Home|Knowledge Graph]], with associated tools. For information on the CKG API, see the [Graph API Spec](https://wiki.corp.adobe.com/display/adobesearch/Graph+API+Specs).
### Taxonomy
For the complete taxonomy, see the [CKG taxonomy file](https://git.corp.adobe.com/adobesearch/ckg-sdk/blob/main/taxonomy.json).

### Graph
The graph is represented as JSON in the following three files:
1. [Nodes](https://git.corp.adobe.com/adobesearch/ckg-sdk/blob/main/nodes_without_associations.json)
2. [Edges/Associations](https://git.corp.adobe.com/adobesearch/ckg-sdk/blob/main/edges.json)
3. [Nodes with associations](https://git.corp.adobe.com/adobesearch/ckg-sdk/blob/main/nodes_with_associations.json)

#### Nodes
##### Stats
|Node|Count|change|diff_count|
|:--|--:|:--|--:|
|ACTION|220|+0/-0|0|
|BACKGROUND|356|+0/-0|0|
|COLOR|260|+0/-0|0|
|COMMAND|1627|+0/-0|0|
|DESIGN_TYPE|230|+66/-2|64|
|EVENT|136|+0/-0|0|
|FILTER|13|+0/-0|0|
|FONT|770|+0/-0|0|
|ICON|877|+0/-0|0|
|INTENT|3247|+0/-0|0|
|LOCATION|120|+0/-0|0|
|MISC|9583|+0/-0|0|
|PANEL|63|+0/-0|0|
|PRODUCT|70|+0/-0|0|
|SCENE_OBJECT|738|+0/-0|0|
|TOOL|156|+0/-0|0|
|VIEW|2|+0/-0|0|

##### Source
|**Node Type**|**Data Source**|
|:--|:--|
|INTENT|Mined from 200k [[Adobe [[Adobe Express - 8.09.2023 @ 10.59 am - Misc|Express]] - 8.09.2023 @ 10.59 am - Misc|[[Adobe Express - 8.09.2023 @ 10.59 am - Misc|AX]]]] queries + AX Project Topics|
|FONT|AX|
|DESIGN_TYPE|AX|
|BACKGROUND|Stock Backgrounds Dataset + GPT3|
|EVENT|Stock 50M + AX|
|SCENE_OBJECT|Stock 50M + AX + GPT3|
|LOCATION|Stock 50M + AX|
|MISC|Stock 50M|
|ACTION|Stock 50M + AX|
|COLOR|Common colors|
|ASSET_TYPE||
|ICON|Stock 50M + Noun Project + GPT3|
|TOOL|Photoshop + Illustrator Tools|
|PANEL|Photoshop + Illustrator Panels|
|FILTER|Photoshop Filters|
|COMMAND|Photoshop + Illustrator Commands|

#### Edges
##### Stats
|Edge|Count|change|diff_count|
|:--|--:|:--|--:|
|ACTION - RELATED_ACTION -> ACTION|11|+0/-0|0|
|ACTION - RELATED_EVENT -> EVENT|1|+0/-0|0|
|ACTION - RELATED_MISC -> MISC|722|+0/-0|0|
|ACTION - RELATED_SCENE_OBJECT -> SCENE_OBJECT|11|+0/-0|0|
|COLOR - CHILD_AX_BROWSE -> COLOR|249|+0/-0|0|
|COLOR - CHILD_OF -> COLOR|249|+0/-0|0|
|DESIGN_TYPE - CHILD_AX_BROWSE -> DESIGN_TYPE|101|+0/-0|0|
|DESIGN_TYPE - CHILD_AX_BROWSE -> INTENT|380|+0/-0|0|
|DESIGN_TYPE - CHILD_OF -> DESIGN_TYPE|93|+0/-0|0|
|DESIGN_TYPE - RELATED_INTENT -> INTENT|1253|+0/-0|0|
|EVENT - RELATED_ACTION -> ACTION|7|+0/-0|0|
|EVENT - RELATED_EVENT -> EVENT|15|+0/-0|0|
|EVENT - RELATED_LOCATION -> LOCATION|3|+0/-0|0|
|EVENT - RELATED_MISC -> MISC|522|+0/-0|0|
|EVENT - RELATED_SCENE_OBJECT -> SCENE_OBJECT|22|+0/-0|0|
|INTENT - CHILD_AX_BROWSE -> ACTION|9|+0/-0|0|
|INTENT - CHILD_AX_BROWSE -> DESIGN_TYPE|40|+0/-0|0|
|INTENT - CHILD_AX_BROWSE -> EVENT|11|+0/-0|0|
|INTENT - CHILD_AX_BROWSE -> INTENT|523|+0/-0|0|
|INTENT - CHILD_AX_BROWSE -> LOCATION|6|+0/-0|0|
|INTENT - CHILD_AX_BROWSE -> MISC|785|+0/-0|0|
|INTENT - CHILD_AX_BROWSE -> SCENE_OBJECT|30|+0/-0|0|
|INTENT - CHILD_OF -> INTENT|1379|+0/-0|0|
|INTENT - RELATED_ACTION -> ACTION|173|+0/-0|0|
|INTENT - RELATED_BACKGROUND -> BACKGROUND|19873|+0/-0|0|
|INTENT - RELATED_COLOR -> COLOR|7453|+0/-0|0|
|INTENT - RELATED_DESIGN_TYPE -> DESIGN_TYPE|8499|+0/-0|0|
|INTENT - RELATED_EVENT -> EVENT|222|+0/-0|0|
|INTENT - RELATED_FONT -> FONT|27762|+0/-0|0|
|INTENT - RELATED_ICON -> ICON|29673|+0/-0|0|
|INTENT - RELATED_LOCATION -> LOCATION|91|+0/-0|0|
|INTENT - RELATED_MISC -> ACTION|147|+0/-0|0|
|INTENT - RELATED_MISC -> EVENT|177|+0/-0|0|
|INTENT - RELATED_MISC -> LOCATION|110|+0/-0|0|
|INTENT - RELATED_MISC -> MISC|12694|+0/-0|0|
|INTENT - RELATED_MISC -> SCENE_OBJECT|330|+0/-0|0|
|INTENT - RELATED_SCENE_OBJECT -> SCENE_OBJECT|689|+0/-0|0|
|LOCATION - RELATED_EVENT -> EVENT|1|+0/-0|0|
|LOCATION - RELATED_LOCATION -> LOCATION|18|+0/-0|0|
|LOCATION - RELATED_MISC -> MISC|658|+0/-0|0|
|LOCATION - RELATED_SCENE_OBJECT -> SCENE_OBJECT|5|+0/-0|0|
|MISC - RELATED_ACTION -> ACTION|25|+0/-0|0|
|MISC - RELATED_EVENT -> EVENT|19|+0/-0|0|
|MISC - RELATED_LOCATION -> LOCATION|7|+0/-0|0|
|MISC - RELATED_MISC -> MISC|2393|+0/-0|0|
|MISC - RELATED_SCENE_OBJECT -> SCENE_OBJECT|30|+0/-0|0|
|PRODUCT - RELATED_COMMAND -> COMMAND|1702|+0/-0|0|
|PRODUCT - RELATED_FILTER -> FILTER|13|+0/-0|0|
|PRODUCT - RELATED_PANEL -> PANEL|78|+0/-0|0|
|PRODUCT - RELATED_TOOL -> TOOL|175|+0/-0|0|
|SCENE_OBJECT - RELATED_ACTION -> ACTION|10|+0/-0|0|
|SCENE_OBJECT - RELATED_EVENT -> EVENT|11|+0/-0|0|
|SCENE_OBJECT - RELATED_LOCATION -> LOCATION|9|+0/-0|0|
|SCENE_OBJECT - RELATED_MISC -> MISC|3092|+0/-0|0|
|SCENE_OBJECT - RELATED_SCENE_OBJECT -> SCENE_OBJECT|83|+0/-0|0|
|VIEW - CHILD_AX_BROWSE -> COLOR|45|+0/-0|0|
|VIEW - CHILD_AX_BROWSE -> DESIGN_TYPE|68|+0/-0|0|
|VIEW - CHILD_AX_BROWSE -> INTENT|207|+0/-0|0|

##### Source

|Edge Type|Computation Method|
|:--|:--|
|Intent -> Font|Triplet Transformer model (Text->intent-Font)|
|Intent -> Foreground (Event, misc, location, action, object)|(Ngram + Phrase Extraction + Co-occurrence Suggestor model ) + Sentence Transformer Ranker|
|Intent -> Design Type|Co-occurrence in 50K AX Data|
|Design Type -> Intent|Co-occurrence in 50K AX Data|
|Intent -> Background|Contrastive Transformer Model of Intent -> Background pairings|
|Intent -> Color|Co-occurrence in 50K AX Data|
|Intent -> Icons (Asset type)|(Ngram + co-occurrence Suggestor Model) + Sentence Transformer Ranker|
|Nodes -> Nodes (Event, misc, location, action, object)|(Ngram + Phrase Extraction + Co-occurrence Suggestor model ) + Sentence Transformer Ranker|
|Child Of (Intent -> Intent)|Graph traversal model|

### Quick Links

- Node Ingestion and Graph generation demo Video: [here](https://adobe-my.sharepoint.com/personal/jaykumar_adobe_com/_layouts/15/stream.aspx?id=%2Fpersonal%2Fjaykumar%5Fadobe%5Fcom%2FDocuments%2FCKG%2Fdemo%5Fvideos%2FCKG%5Fgraph%5Fgeneration%2Emp4&ga=1)
- CKG 3.2 location: s3://adobesearch-ckg/graph/v3_2/
- CKG Node Matcher Wiki: [here](https://wiki.corp.adobe.com/display/adobesearch/Query+Graph+Node+Matcher)
- CKG Graph Visualizer Video: [here](https://adobe-my.sharepoint.com/:v:/p/mpoddar/EUdq5QLOjiBAje09BWeylAMBQhmAFE8gqQqSSlK9lmNcPw?e=4QSkHL)


## Taxonomy.json 
- Edges are in `taxonomy.json` 
	- Approx 56k edges 
		- Design type 
			- 


## Guidelines [Wiki](https://wiki.corp.adobe.com/display/adobesearch/Creative+Knowledge+Graph+Guidelines+and+Principles) 
- Glossary / Terms
	- **Label/Concept:** We will use this term to refer to any concept or label used as target or intermediate entity in use cases. For example, an object detection model's target prediction labels could scene objects such as chair, table and so on. In this example, chair, table are labels. 
	- **Taxonomy**: A taxonomy formalizes the hierarchical relationships among concepts and specifies the term to be used to refer to each; it prescribes structure and terminology. For example, chair and table are furnitures and the taxonomy will capture these hierarchical relationships. 
	- **[[Intent AI Home|Knowledge Graph]]:** A [[Intent AI Home|knowledge graph]] represents a network of real-world entities (i.e. objects, events, situations, or concepts) and illustrates the relationship between them.  
	- **Creative [[Intent AI Home|Knowledge Graph]]:** Creative [[Intent AI Home|Knowledge Graph]] is a Search & Discovery Org wide effort on organizing creative intents, asset-specific concepts, and tools and products specific concepts, help and quick-actions as a graph. Creative [[Intent AI Home|Knowledge Graph]] focuses on user’s intent (main entity) and its associations to the resource entities (foreground and background classes, fonts, colors, icons, shapes etc.) and 
	- **Schema:** A schema defines the types of entities and edges in the graph and also how those entity types are related to each other.
	- **[[global type|Global Types]]:** These are common types which will be used across SDC components. Examples are CKG intent, [[Color]], background and so on.
	- **Node/Entity Type:** Schema will define what types of entity will be present in the graph. This should match with the [[global type]] defined for SDC. Example: INTENT, DESIGN_TYPE, SCENE_OBJECTS are example of entity types.
	- **Node:** Each entity type will have a taxonomy of node instance (ex: a node referring to concept **chair** could be created under entity SCENE_OBJECTS)
	- **Edge/Association:** Two nodes could be connected via an edge to define the relationship between them (according to SCHEMA). Nodes could be from different entities as well as same entities. 
	- **Intent:** We refer to user's creative intent as intent.
	- **Design Type:** We refer to different layout types such as flyers, brochures, cards etc. as Design Type. (also known as tasks in Adobe [[Adobe Express - 8.09.2023 @ 10.59 am - Misc|Express]] Template Meta)
	- **Graph API:** CKG data is exposed via intent understanding (Morpheus) platform. The graph APIs are available for browse and read-only use cases at this time.
	- **Intent Services:** In order to use CKG data, the team has built several intent services which are aimed to do both **Query + User Context** mapping and **Adobe Assets (ex: Templates, Images)** mapping to graph nodes. This could be used in conjunction with Graph API to power different use cases.

### Capabilities 
CKG has several capabilities right now: 
- Taxonomy of user intents
	- Search of assets and creation 
	- [[Adobe Express - 8.09.2023 @ 10.59 am - Misc|CCX]], Stock, A.com 
- Taxonomy of design types (task in [[Adobe Express - 8.09.2023 @ 10.59 am - Misc|CCX]]) creatives make using adobe products 
- Taxonomy of user intents ([[Adobe Express - 8.09.2023 @ 10.59 am - Misc|AX]]) to asset concepts such as Backgrounds, Foreground, Icons, Fonts, Design Types
- Models and services to map user queries and context to CKG [[global type|global types]] 
	- [NodeTypes](https://wiki.corp.adobe.com/display/adobesearch/CKG+NodeTypes)
- Associations of user intents in AX to bg, fg, icons, fonts, design types
- Models and services to make query to [[global type|global types]]
- modesl to map templates and text, shapes, etc to [[global type|GTs]]

Currently the graph focuses on User intent understanding (from context, query, projects, user history) and Adobe asset understanding (templates, stock assets, shapes, etc) and associations (tools, helpX tutorials, etc)


## Capabilities [Wiki](https://wiki.corp.adobe.com/display/adobesearch/Capabilities+and+Use+Cases)
- Diagram: ![[Screen Shot 2022-11-02 at 3.45.50 PM.png]]


---
# Todos
- [x] Go through demo videos ➕ 2023-08-09 ⏳ 2023-08-11
- [x] Go through capabilities wiki ➕ 2023-08-09 ⏳ 2023-08-09 ✅ 2023-08-09
- [x] create CKG vision outline ➕ 2023-08-07 ⏳ 2023-08-10 📅 2023-08-15 ✅ 2023-08-15
	- [x] [[Ritu - 8.7.2023 - 1x1 Meeting]]
	- vision map the biz value assuming no technical constraints 
		- Top line motivation 
			- Use cases / examples 
	- Break out technical questions/dependancies  
	- Get technical understanding 
		- ID deltas between vision and current state
		- take a stab at prioritizing them 
			- buckets with what value is unlocked at each bucket
	- [[CKG Vision Crafting  - 8.11.2023 @ 09.42 am - Misc]]
- [x] Clone the repo locally ➕ 2023-08-08 ✅ 2023-08-08
