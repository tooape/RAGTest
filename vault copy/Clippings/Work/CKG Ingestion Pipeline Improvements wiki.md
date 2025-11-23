---
pageTitle: "CKG Ingestion Pipeline Improvements - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/CKG+Ingestion+Pipeline+Improvements"
dateCaptured: "2025-10-01T13:48:43-07:00"
pageSource: "Adobe Wiki"
author:
  - "Anshul Omar"
tags:
  - "Adobe wikis"
---
# [CKG Ingestion Pipeline Improvements](https://wiki.corp.adobe.com/display/adobesearch/CKG+Ingestion+Pipeline+Improvements)

[[October 01, 2025]] 

**Summary**
This document outlines proposed improvements to the CKG ingestion pipeline to address its current limitations, such as manual intervention, sequential processing, and slow performance. The goal is to achieve an end-to-end automated pipeline that reduces ingestion times from days to hours and supports a much higher graph scale. The proposed architecture leverages modern tools like Prefect for orchestration, Polars for data manipulation, and DuckDB/RDict for graph operations, with a roadmap spanning immediate automation to long-term MapReduce scaling with Apache Spark. 

**Highlights**
> 

**Details**
- The current CKG ingestion pipeline is manual, sequential, slow, and lacks performance metrics.
- The goal is to create an end-to-end automated pipeline, reducing ingestion times from days to hours and increasing graph scale.
- Key proposed technologies include Prefect for orchestration, Polars for data manipulation, DuckDB (for graph ops) and RDict (for caching) to replace Networkx, and Parquet as the storage format.
- Design principles emphasize streaming/chunked processing, asynchronous/parallel execution, and an optimized LLM API client.
- The implementation roadmap progresses from immediate automation, to short-term performance enhancements (e.g., Polars, DuckDB, Parquet), medium-term parallel execution (Prefect), and long-term MapReduce scaling (Apache Spark).

