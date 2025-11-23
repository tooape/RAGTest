---
pageTitle: "SDC Search and Discovery mcp server integration requirements guidelines - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/SDC+Search+and+Discovery+mcp+server+integration+requirements+guidelines"
dateCaptured: "2025-09-24T21:20:20-07:00"
pageSource: "Adobe Wiki"
---
[[September 24, 2025]] 

The page outlines Adobe's goal to integrate search capabilities from its products (e.g., [[Acrobat|Acrobat]], [[Lr Home|Lightroom]], [[Express]]) with AI applications like ChatGPT and Claude using the Model Context Protocol (MCP). MCP, an open-source standard, allows AI agents to access external systems, enabling them to perform complex, multi-step tasks by invoking Adobe's search tools. The document also details various requirements and considerations for this integration.

- MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems (data, tools, workflows).
- AI agents use MCP to leverage external tools, such as Adobe's search capabilities, to complete complex tasks iteratively.
- The goal is to expose Adobe product search via MCP servers, allowing AI apps to query user-specific content (e.g., PDFs, photos).
- Key integration requirements cover supporting use cases, prompt handling, access management, search API specifications, non-functional requirements (NFRs), and logging.
- Critical considerations include legal safety for querying personal, enterprise, and educational assets, and how search results from media assets (like video) will be handled.