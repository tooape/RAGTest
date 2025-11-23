---
pageTitle: "Nodes for CKG 4.0 - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/Nodes+for+CKG+4.0"
dateCaptured: "2025-10-07T11:25:30-07:00"
pageSource: "Adobe Wiki"
author:
  - "Ayush Jaiswal"
  - "Mayank Poddar"
  - "Josep Valls"
tags:
  - "Adobe wikis"
---
# [Nodes for CKG 4.0](https://wiki.corp.adobe.com/display/adobesearch/Nodes+for+CKG+4.0)

[[October 07, 2025]] 

## Summary
CKG 4.0 is a significant update aiming to enhance the Creative Knowledge Graph's concept coverage, quality, and precision by evolving its general world knowledge. This document outlines the requirements, sources, methods, and evaluation plan for CKG nodes.

Key requirements include representing canonical concepts (singular meaning, language-agnostic) rather than terms, which improves scalability by mapping term variations internally. The graph will exclude overly specific or highly complex concepts. Coverage targets 100% of relevant CKG 3.5.9 and AssetKG concepts, broad world knowledge, Adobe product-specific taxonomies (e.g., Express, Stock, Lightroom), and named entities (excluding copyrighted ones from client exposure). Concepts will be polymorphically tagged with types such as Event, Scene Object, Person, Location, Human Attributes, Material, Topic, and various Adobe Ecosystem subtypes. Nodes will also feature annotations like 'offensive' or 'trademarked'.

Concept sources include existing CKG 3.5.9, AssetKG, Babelscape (a licensed knowledge graph used for canonicalization and hierarchy), and specialized external data sources like GeoNames for location data. Methods involve processing existing concepts (deduplication, decompounding, type verification, clustering) and grounding them in Babelscape, or directly filtering and expanding concepts from Babelscape and external sources. All concepts will leverage Babelscape's hierarchy for expansion and refinement.

Evaluation will track metrics for canonicalization (Term Semantic Similarity, Concept Uniqueness), specificity (Hypernym-Hyponym Distinction, Sibling Similarity to avoid redundancy), and coverage (Concept Count, CKG 3.5.9, AssetKG, and Search Coverage). Concept-type labeling accuracy will be assessed through human and LLM-based evaluations. 

## Highlights
> 

## Details
- CKG 4.0 nodes will be canonical concepts, not terms, with internal mappings to term variations to improve scalability and reduce ambiguity.
- Concepts will be tagged with multiple types (e.g., Event, Scene Object, Person, Location, Adobe Ecosystem subtypes) and can be polymorphic.
- Primary concept sources include CKG 3.5.9, AssetKG, Babelscape (for canonicalization and hierarchy), and external sources like GeoNames for specific data types.
- Methods involve processing existing concepts (deduplication, clustering) and grounding them in Babelscape, or directly identifying and filtering concepts from Babelscape and external sources.
- Evaluation focuses on canonicalization, specificity (avoiding overly general or specific concepts), and coverage against previous CKG versions and search queries.

