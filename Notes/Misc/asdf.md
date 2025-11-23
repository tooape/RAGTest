---
creation date: 
tags: 
Related Pages: 
aliases:
---



### Multi-year Mission

Our mission represents the goal we intend to drive towards as a team, and where we feel our work is best directed. This creates a guidepost for us to refer back to when making hard decisions, faced with conflicting direction, and answering design questions. Intent Services' mission is:

>To become Adobe's canonical source of understanding the creative process. 

We've specifically included all of Adobe in scope but limited the mission to creative tasks. This keeps us focused on our area of expertise and the areas where we can drive the most impact. For example: if a use case (even one outside Express) requires understanding of some creative workflow or process, we should in theory have that knowledge within intent services and we should be able to server that case. But if that same use case required us to get [[Personalization Home|user understanding]] in a context related to account admin or product info, we would defer them to another team. While our work and our platform will span across Adobe, we will remain focused on creative use cases. 

### Vision

Adobe's vision is to "change the world through digital experiences", and frequently uses the phrase "creativity for all" as a sort of slogan. Adobe's brand has been synonymous with creation, art, and imaging for decades, and these statements speak to that level of impact. Intent services' vision will need to rise to that same scale of opportunity since our mission statement leads us to a position of cutting across Adobe. In our vision statement we take a moment to consider "what will the state of Adobe be once we accomplish our mission"?

> Our vision is to make creation with Adobe products seamless, joyful, and nearly effortless.

If we had a perfect understanding of all three of the types of knowledge laid out above; we would be able to create an ecosystem where the effort and skill required to complete a creative task within Adobe apps is dramatically reduced, if not completely eliminated. This creates a massive value proposition to Adobe. The world will never want or need less art or fewer creative voices tomorrow than it does today. As that demand and breadth of creative need continues to expand, Adobe's offerings will need to become not only more powerful but also much easier to use. Intent services has a critical role to play in maintaining Adobe's position as the foremost platform for creation in the coming years and decades.


## 2024 strategy pillars
---
The two statements above are multi-year goals that will be helpful in guiding our work over time. Narrowing the conversation to focus specifically on 2024 there are a few key strategic decisions and priorities that will shape the functional roadmap that moves us in that direction. 
  
### 1. Powering contextual discovery in Express is our focus  
As stated in our mission, we will have a future outside of Express as a more broad Adobe technology platform. The immediate future however will still be focused on Express contextual discovery, and will not invest substantial effort or energy in seeking out use cases in the core/flagship apps. Express already covers many types of creative flows, and that coverage is growing to include painting, document authoring, and more photo and video cases. In 2024 Express is also looking to continue expanding support for additional geos, and adding more mobile, Enterprise, and K12 functionality. This gives us broad exposure to many types of creation and creative flows, but keeps the complexity down (see graphic below). 


Sticking to Contextual Discovery use cases in Express will help us refine our platform for our long term goals, while quickly delivering value and impact. 




#### Additional Info on Contextual Discovery 
Several types of use cases or user flows fall into this category. Firstly a case where the user is looking for some asset, piece of data, or quick action related to a query or canvas they're working on. A case where we might proactively recommend something. Or even a case meant to inspire or spark new thinking in the user by brining in data outside the immediate topic or creative direction. 

The repository of elements, images, icons, and fonts within Express is colossal (and growing) and users will struggle to find something useful or relevant on their own. This is our opportunity to use our understanding of all three elements of intent mentioned above to offer users a natural path from start to finish in their project. This is especially important in mobile flows (a focus for express in 1H24) where the limited screen real estate can add friction for users trying to exploring all of these options manually. Below is a quick list of features and capabilities we'll look to power in 2024. Specific requirements, timelines, and other details will be linked here as they are defined and finalized. 


### 2. Investing in platform

#### Graph Enrichment 
**2024 Goals** 
> 1. The graph should have sufficient breadth to return intents for every Express template.
> 2. CKG should have no orphaned nodes. 
> 3. Intent Services should have achieved 99% head query coverage on Express. 

Intent understanding will require a very diligent and ongoing investment in our graph. While this comes at the tradeoff of not being able to work on as many production use cases, we view this time spent on our intent understanding models, our graph, and our services as required upkeep. Blocking capacity for this work will also let us be more proactive and incorporate new data sources (like HelpX, or new query logs), and newer modeling and evaluation techniques as the research and technology evolve. 

#### Intent Services Usability
**2024 Goal** 
> All intent services should be easily available behind a single API surface, with the documentation, and supporting material to make for a great DevEx when surface teams want to integrate and tune intent understanding. 

USS & ILUP give us an orchestration layer that surface teams can use for a much easier time integrating intent services into their app. Since USS also contains services like spell checker, named entity recognition, and language detection; the surface team can return a very large amount of intelligence very quickly, and with only one API surface to worry about. 

**Key Deliverables** 
- Giving users in DMe a single API Surface in USS 
- API and data naming strategy aligned with DMe
- Useful parameterization for intent services available through API
- API & Service documentation site with technical docs, service map, and reference code samples
- User guide information for tuning relevance, or explaining how to use intent
- Training/intro video 

### 3. Clarifying the scope of "Understanding Creative Process" 

Intent Services aims to understand the contents of the canvas in comparison to the features or assets within Express, and how users combine these elements. IE. what are the colors, elements, templates, tools, actions, queries, etc that someone uses? We are looking at aggregate behavior and relationships, and Intent services are not a *[[Personalization Home|personalization]]* platform. Understanding of the user themselves, their specific most used colors, assets, tools, etc across projects as an individual is not intent services' domain. Likewise, we are not tracking concerns like user metadata, their specific account entitlements, and their branding restrictions within intent services.  
As the needs of DMe evolve, and cases where individualization become more important we will explore how we might create something within USS to tie in with intent services to handle these cases with some kind of "[[Personalization Home]]". For now, these are outside our focus area, and we'll not spend time or energy on those questions.  

**what are the intent services meant to address?** 
- content understanding 
- query improvements 
- contextualization
- etc. 

**Out of Scope Examples**
- User account info
- Adobe product info like pricing

Intent services are a source of data for surface teams and not the end all be all... For example, surface teams may need to filter down data for display to users (k12, brand guides, etc may restrict what nodes are usable to a given user. We would leverage to our metadata to do this and not try to analyze the specific user). This might fall to a [[Personalization Home]] within ILUP, and work in tandem with Intent Services to build a complete contextual view of the creator or communicator. 