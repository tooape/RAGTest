# Test Cases for Rag App 
Here we ID the testing methodology for the [[Smart Connections Enhancement - Custom RAG]]. 

# Hand Written queries 
1. Q: "who's the PsW PM?" | A: [[Hao Xu|Hao]]
	1. Q: "When was the last time I met with them?" | A: [[November 17, 2025]]
2. Q: "What did I discusYs with Ritu in our last 1x1" | A: "Hiring the intern for next summer, I pitched her moving me to a manager, we discussed the Lr ranker, but mostly the Q1 must nails." 
3. Q: "what are the Q1 '26 must nails" | A: "[[November 18, 2025#Q1 2026 Must Nails]]"
4. Q: "photoshop" | A: "[[Photoshop]]

# Synthetic queries

## Person & Meeting Queries

1. Q: "Who is the Group PM manager for Lightroom?" | A: [[Peter Baust]]
2. Q: "When did I last meet with Kosta?" | A: [[November 20, 2025]]
3. Q: "What did Brian and I discuss in our most recent 1x1?" | A: Should reference latest [[Brian Eriksson]] 1x1 meeting notes ([[November 19, 2025]]) with Q1 2026 Must Nails discussion
4. Q: "Who works on Intent AI?" | A: Should mention [[Ayush Jaiswal]] (Intent Strategy), [[Kosta Blank]] (Engineering Manager), and program structure from [[Intent AI Home]]
5. Q: "What's Ritu's role?" | A: Sr Director of Product in SDC, direct manager, reports to [[Vipul Dalal]]
6. Q: "Find all my meetings with Rhut" | A: Should list meetings mentioning Rhut Vasavada
7. Q: "Who is leading the Firefly semantic search project?" | A: [[Rhut Vasavada]]
8. Q: "When was my last staff meeting with Ritu?" | A: Should find most recent Ritu staff meeting
9. Q: "Who do I talk to about Query Understanding?" | A: [[Subhajit]] and [[Jayant Kumar]]
10. Q: "What does Michael Lewis do?" | A: PsM PM

## Project Status & Planning Queries

11. Q: "What's the status of Photo Styles?" | A: Should reference recent Photo Styles work from November 20 notes
12. Q: "What are my Q1 2026 priorities?" | A: Should find [[November 18, 2025#Q1 2026 Must Nails]]
13. Q: "What's the current plan for Photoshop Web recommendations?" | A: Should reference [[Photoshop Web]] page and recent discussions
14. Q: "Is there an eval strategy for DC Recs?" | A: Should reference [[November 20, 2025]] DC Recs sync meeting
15. Q: "What's the Intent AI 2026 strategy?" | A: Should reference Intent Strategy whitepaper meeting from November 20, and include sharepoint link.
16. Q: "What's the scope of Universal Asset Browser?" | A: Should reference Firefly semantic search meeting details
17. Q: "Where is the link to the CPro strategy deep dive video?" | A: Should find IATV link from Ritu staff meeting
18. Q: "What files are included in UAB search?" | A: Should list PSD, AI, Firefly generations, Express, InDesign, PDFs from November 20 meeting
19. Q: "What's the peak load for contextual recs?" | A: Should find "120 RPS" from Kosta meeting November 20
20. Q: "Is Lightroom included in Universal Asset Browser?" | A: Should find "not currently part of this" from November 20 notes

## Technical & Architecture Queries

21. Q: "How does temporal retrieval work in the RAG plugin?" | A: Exponential decay with 30-day half-life, two-stage filtering
22. Q: "What embedding model did we choose?" | A: EmbeddingGemma with 256d Matryoshka optimization
23. Q: "What's the difference between graph and temporal signals?" | A: Graph boosts query-relevant only, temporal has 120-day recency bypass
24. Q: "How are chunks created in the indexer?" | A: H2-based chunking via DocumentChunker, 50-char minimum

## Product & Platform Queries

31. Q: "What's the difference between Express and Firefly?" | A: Should explain products and their relationship
32. Q: "Is there a mobile version of Ps recommendations?" | A: Should reference "nice to have" vs Ps Web priority from [[November 19, 2025]] and [[November 20, 2025]]
33. Q: "What products use the Intent AI system?" | A: Should list products from Intent AI hub page
34. Q: "Where is the photo styles eval deployed?" | A: Discovery Hub (discovery-hub.corp.adobe.com:8080/photo-styles-search)
35. Q: "What Adobe products currently have contextual recommendations integrated?" | A: Express, DC. Mention planned PsW recommendations. 

## Browse & Relationship Queries

41. Q: "Show me everything related to Query Understanding" | A: Should find hub page and connected notes via graph
42. Q: "What notes mention both Brian and Lightroom?" | A: Should find intersection of [[Brian Eriksson]] meetings and Lr discussions
43. Q: "Show me recent notes about recommendations" | A: Should combine temporal + semantic for Recommendations content
44. Q: "What have I worked on with Kosta recently?" | A: Should find recent Kosta 1x1 meetings and referenced projects
45. Q: "Find all notes about NER and SRL" | A: Should find Query Understanding related content
46. Q: "What meetings discussed embeddings?" | A: Should find technical meetings mentioning embedding models
47. Q: "Show me all work related to Adobe Express" | A: Should find [[Express]] hub and connected notes

## Multi-Hop Reasoning Queries

51. Q: "Who should I talk to about improving the AdobeOne ranking for Lr?" | A: Feng bin from November 20th 1x1 with ritu
52. Q: "How does the photo styles ranking system compare to semantic search?" | A: Should explain both systems and their differences
53. Q: "What's the timeline for Ps Web recs and what's blocking it?" | A: Should find Q1 priority + any blockers from meetings
54. Q: "What's the relationship between the APS deck and CPro strategy?" | A: Should reference Ritu staff meeting alignment task

# Result summary

| System          | Ranking of correct result | Context token count | Query latency |
| --------------- | ------------------------- | ------------------- | ------------- |
| 11/22 baseline  |                           |                     |               |
| MXBAI Re ranker |                           |                     |               |
| Pure BM25       |                           |                     |               |
