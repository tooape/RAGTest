---
pageTitle: "Intent Understanding: Semantic Topic Extraction model - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/Intent+Understanding%3A+Semantic+Topic+Extraction+model"
dateCaptured: "2025-10-14T21:18:34-07:00"
pageSource: "Adobe Wiki"
author:
  - "Anshul Omar"
tags:
  - "Adobe wikis"
---
# [Intent Understanding: Semantic Topic Extraction model](https://wiki.corp.adobe.com/display/adobesearch/Intent+Understanding%3A+Semantic+Topic+Extraction+model)

[[October 14, 2025]] 

## Summary
This document outlines the \\"[[Intent AI Home|Intent Understanding]]: Semantic Topic Extraction model\\" project, which is currently in progress. The primary objective is to train a model that extracts underlying semantic intent from user queries and organizes it into structured categories such as Topic, Design type, Background, and [[Style Home|Color]].

The current model, a LoRA head fine-tuned on Llama-3.2-1B-Instruct, was trained on a large, synthetically generated dataset (26.2M samples). However, it requires improvements in several key areas: enhancing the Macro F1 score (especially for the \\"topic\\" category), improving performance across short, medium, and long queries, and expanding support for new document-related semantic types.

The document details a comprehensive improvement plan focused on both the dataset and the model. Dataset improvements include creating a high-quality pilot dataset for annotation, analyzing the existing data for balance and redundancy, redesigning the generation strategy to preserve context, and refining human-annotated golden datasets. Model improvements will focus on expanding its ability to extract new document-related intents like document domain, sub-domain, and template type. The document concludes with important links to the Git repository, datasets, and model checkpoints. 

## Highlights
> 

## Details
- **Objective**: To train and improve a model that extracts structured semantic intent (e.g., topic, design type) from user queries.
- **Current Model**: A LoRA head fine-tuned on a Llama-3.2-1B-Instruct model, trained on a synthetically generated 26.2M sample dataset.
- **Problem Areas**: The model needs better F1 scores, improved performance across different query lengths, and support for new document-related semantic types.
- **Planned Improvements**: Focus on enhancing the dataset (quality, balance, context) and expanding the model to recognize new intents like document domain and template type.
- **Project Status**: IN PROGRESS, with contributor Anshul Omar and approvers [[Jayant Kumar]] and [[Kosta Blank|Kosta]] Blank.

