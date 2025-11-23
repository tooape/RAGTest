---
pageType: programHome
created: 2025-09-24
tags: claude
aliases:
  - Creative Knowledge Graph 4.0
  - CKG4.0
  - Knowledge Graph 4.0
  - ckg4
Related Pages:
  - "[[Intent AI Home]]"
  - "[[Query Understanding]]"
  - "[[Multi-Language 2025]]"
Wiki Link:
  - https://wiki.corp.adobe.com/display/adobesearch/Node+and+Edge+evaluations+task+tracker
protected: false
---

# [[Intent AI Home|CKG]] 4.0
---

The fourth major version of Adobe's Creative [[Intent AI Home|Knowledge Graph]], a foundational AI system powering intent understanding, [[Recommendations Home|contextual recommendations]], and search capabilities across Adobe's creative products.

## Overview
---

[[Intent AI Home|CKG]] 4.0 represents a significant evolution in Adobe's [[Intent AI Home|knowledge graph]] capabilities, focusing on improved [[Multi-Language 2025|multi-language]] support, enhanced node coverage, better canonicalization, and more sophisticated edge relationships. The system serves as the backbone for [[Intent AI Home|MINT]] services and powers contextual understanding across [[Express]], [[Lr Home|Lightroom]], [[Acrobat|Acrobat]], and other Adobe products.

## Key Initiatives
---

### [[Multi-Language 2025|Multi-Language]] Support
- Expanded language coverage building on [[Multi-Language 2025]] initiatives
- Translation strategy for graph nodes vs query-time text processing
- Coordination with [[Francois Guerin|Francois]] on translation approaches
- Target: 20k topics across 4 languages for initial release

### Node Discovery & Coverage
- Collaboration with [[Arvind]] and [[Mayank Poddar|Mayank]] on automated node discovery
- Coverage analysis for T1 languages and top queries
- Proper noun handling improvements (locations, people, brands)
- Integration with CAT (Creative Asset Taxonomy) concepts

### Edge Quality & Canonicalization
- Enhanced canonicalization of nodes and edges
- Confidence-based association retrieval
- Asset type [[Core Affinity Framework|affinity]] modeling for different contexts
- Behavioral weight adjustments based on surface context

### [[Evaluation]] Framework
- Partnership with [[Tracy King|Tracy]] on comprehensive testing methodologies
- Comparative analysis: 3.5.x vs 4.0 vs legacy systems
- LLM-based quality assessment with manual verification
- Error rate analysis by edge type and node category

## Technical Architecture
---

### Core Components
- **Node Types**: People, multimedia concepts, asset types, tools, actions
- **Edge Types**: "is a", "relates to", [[Core Affinity Framework|affinity]] weights, contextual associations  
- **Integration Points**: [[Intent AI Home|MINT]], [[SLM]], [[NER & SRL]], Bablescape
- **Inference**: Confidence thresholds, dynamic association expansion

### Use Cases
- **[[Recommendations Home|Contextual Recommendations]]**: Asset suggestions in creative workflows
- **Search Enhancement**: Intent understanding and query canonicalization
- **[[Core Affinity Framework|Asset Type Affinity]]**: Content type prediction and routing
- **Cross-Product Discovery**: Unified content understanding across Adobe ecosystem

## Implementation Timeline
---

### Milestone 1 (Current)
- Scope definition and architecture planning
- Node discovery and coverage expansion
- [[Multi-Language 2025|Multi-language]] foundation establishment
- [[Evaluation]] framework setup

### Production Rollout
- [[Express]] [[Recommendations Home|contextual recommendations]] (completed)
- [[Lr Home|Lightroom]] semantic search (in progress)
- [[Acrobat|PDF recommendations]] (September 2025)
- [[Photoshop|Photoshop web]] POC development

## Key Stakeholders
---

### Program Leadership
- **[[Brian Eriksson|Brian]]**: Program oversight and strategic direction
- **[[Ritu Goel|Ritu]]**: Organizational alignment and resource allocation

### Technical Leadership  
- **[[Tracy King|Tracy]]**: [[Evaluation]] methodologies and quality assurance
- **[[Ayush Jaiswal|Ayush]]**: Development coordination and implementation
- **[[Vipul Dalal|Vipul]]** & **Venkat**: Core engineering and graph infrastructure

### Product Integration
- **[[People/Vic Chen|Vic]]**: [[Express]] integration and rollout
- **[[Anuj Agarwal|Anuj]]**: [[Lr Home|Lightroom]] search implementation
- **[[Hao Xu]]**: [[Photoshop|Photoshop web]] POC development

## Challenges & Considerations
---

### Quality vs Coverage
- Balancing comprehensive node coverage with high-precision associations
- Managing over-specificity vs useful granularity
- Content gap identification and remediation

### Canonicalization Complexity
- Multiple entity representations requiring single canonical form
- Cross-language canonical mapping challenges
- Behavioral vs semantic canonicalization strategies

### Production Scaling
- Infrastructure requirements for real-time inference
- Multi-product integration complexity
- Performance optimization across different contexts

## Related Systems
---

- **[[Intent AI Home]]**: Primary consumer of [[Intent AI Home|CKG]] 4.0 capabilities
- **[[Query Understanding]]**: Preprocessing and intent classification
- **[[Recommendations Home]]**: Contextual suggestion engines
- **[[Multi-Language 2025]]**: [[Multi-Language 2025|Internationalization]] framework
- **[[SLM]]**: Small language model integration
- **[[NER & SRL]]**: Named entity and [[NER & SRL|semantic role labeling]]

## Resources
---

### Documentation
- [Node and Edge Evaluations Task Tracker](https://wiki.corp.adobe.com/display/adobesearch/Node+and+Edge+evaluations+task+tracker)
- [[Intent AI Home|CKG Architecture Wikis]]
- [[Query Understanding]] Requirements Documentation

### Development Tools
- Graph Browser and visualization tools
- [[Evaluation]] datasets and testing frameworks
- Integration SDKs and API documentation