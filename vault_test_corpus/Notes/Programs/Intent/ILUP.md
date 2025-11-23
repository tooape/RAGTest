---
aliases:
  - Morpheus
protected: true
pageType: programHome
---
# Intent and Language Understanding Platform Home
---
ILUP serves as an orchestration layer and query processor for language understanding features across USS. Originally developed as Query processor Service "QPS" for Stock, it now provides broader processing capabilities with recent advancements in systems like [[Multimodal intent|Multi-Modal]] intent understanding. ILUP provides quick and easy access to many intelligence services:

1. Block list - Filtering of blocked terms which may be offensive, crude, or harmful.
2. Dictionary - Maintains vocabulary and term definitions used across search systems.
3. Tokenization - Breaks down queries and text into individual meaningful units for processing.
4. Lemmatization - Reduces words to their base or dictionary form to improve matching.
5. Natural language processing - Spacy library integration for linguistic analysis.
6. Babelscape - A large dictionary and [[Intent AI Home|knowledge graph]] trained on Wikipedia, available in several languages.
7. Language Detection - Specialized in detecting English content in queries and text.
8. Spellchecker - Legacy spelling correction system for query processing.
9. Named Entity Recognition ([[Query Understanding|NER]]) -
	1. Identifies semantic matches using regex patterns
	2. Performs span detection in text
	3. Rule-based entity identification
	4. Can leverage [[Intent AI Home|MINT]] for entity detection
10. Adobe One Integration
	1. Orchestrates requests to Adobe One services
	2. Normalizes responses for SDC stack compatibility Orchestrator Allows request federation to non ILUP services, and normalizes responses for interoperability with USS systems

**Wikis:**
- https://wiki.corp.adobe.com/display/adobesearch/2025+Intent+%28ILUP%29+Services+Projects+Planning
- https://wiki.corp.adobe.com/display/adobesearch/FY25+Consolidated+ILUP+and+MINT+APIs+-+Unified+Usecase

