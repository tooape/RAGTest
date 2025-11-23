---
pageTitle: "Query Understanding - Intent Action and Subprompt Extraction Using SLMs - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/Query+Understanding+-+Intent+Action+and+Subprompt+Extraction+Using+SLMs"
dateCaptured: "2025-10-14T21:19:34-07:00"
pageSource: "Adobe Wiki"
author:
  - "Suhas Suresha"
tags:
  - "Adobe wikis"
---
# [Query Understanding - Intent Action and Subprompt Extraction Using SLMs](https://wiki.corp.adobe.com/display/adobesearch/Query+Understanding+-+Intent+Action+and+Subprompt+Extraction+Using+SLMs)

[[October 14, 2025]] 

## Summary
This document outlines a [[Query Understanding]] system designed to power discovery across Adobe platforms. The system has two main components built on a Small Language Model ([[SLM]]), specifically `Llama-3.2-1B-Instruct` fine-tuned with LoRA.

1.  **Intent Action Prediction**: This component classifies a user's natural language query into one of 26 predefined tool actions, such as `COMBINE_FILES` or `REMOVE_BACKGROUND`. In its current phase, it focuses on identifying a single primary intent per query.

2.  **Subprompt Extraction**: This component refines user queries for better search performance. It removes non-essential information that can be handled by API parameters—such as action verbs, dates, people's names, and file formats—leaving only the core content-identifying keywords. The system is designed to correctly preserve filenames while removing other metadata.

The document details the technical architecture, data generation strategy (using a legally compliant Llama Scout model), specific tool categories, and the rules for subprompt extraction. [[Evaluation]] methodologies are also described: standard classification metrics (Accuracy, F1 Score) for intent prediction, and a combination of Embedding Similarity and GPT-4o-as-judge for assessing the quality of subprompt extraction. 

## Highlights
> 

## Details
- **Core Project**: Implements a [[Query Understanding]] pipeline using SLMs for two tasks: Intent Action Prediction and Subprompt Extraction.
- **Base Model**: Both components use `meta-llama/Llama-3.2-1B-Instruct` fine-tuned with Low-Rank Adaptation (LoRA).
- **Intent Prediction**: Classifies queries into 26 distinct tool actions across PDF, Document, and Adobe [[Express]] tools.
- **Subprompt Extraction**: Cleans queries by removing metadata (e.g., dates, file types, action verbs) to isolate core search terms, improving search recall.
- **[[Evaluation]]**: Intent prediction is measured with classification metrics (Accuracy, F1), while subprompt extraction uses Embedding Similarity and a GPT-4o-as-judge approach.

