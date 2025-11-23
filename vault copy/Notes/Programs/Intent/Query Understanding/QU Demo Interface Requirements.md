---
created: "2025-11-11"
pageType: misc
tags:
  - claude
Related Pages:
  - "[[Query Understanding]]"
  - "[[Intent AI Home]]"
---
# [[Query Understanding]] Demo Interface Requirements
---
- [Wiki link ](https://wiki.corp.adobe.com/display/adobesearch/QU+Demo
## Overview
---

**Purpose**: [[APS]] season is here and we'll need to be able to demo our [[Query Understanding|QU]] capabilities to other teams. We need an demoHub page where team members can enter queries and view the full range of [[Query Understanding]] intelligence outputs.

## Functional Requirements
---

### Input
- **Text field**: Accepts any length of text
- **Media upload**: Images or PDFs
- **Submit button**: Triggers analysis

### Output
Display all [[Query Understanding]] intelligence for the entered query:

1. **Named Entity Recognition ([[Query Understanding|NER]])**: Entities extracted with types and confidence scores
2. **[[NER & SRL|Semantic Role Labeling]] ([[NER & SRL|SRL]])**: Predicates and argument structure
3. **[[Query Understanding|Core Affinity]] Framework ([[Core Affinity Framework|CAF]])**: Intent classification with confidence scores
4. **[[Multimodal intent|Multi-Modal]] Outputs** (when image/PDF provided): Vision features and cross-modal alignment
5. **[[Intent AI Home|Knowledge Graph]] Integration**: Matched [[CKG 4.0]] nodes and relationships
6. **Metadata & Diagnostics**: 
   - Query UUID
   - Timestamp
   - Processing time / latency
   - Model versions used

