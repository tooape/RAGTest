---
created: "2025-11-10"
pageType: misc
tags:
  - claude
Related Pages:
  - "[[Query Understanding]]"
  - "[[November 10, 2025]]"
---
# Query Understanding MM Model Evaluation Plan
---

## Overview

Two evaluation workstreams identified from QU checkin on November 10, 2025 for assessing the multimodal (MM) model performance.

## Evaluation Ask 1: Swimlane 3 MM Model for PDF2Pres

**Objective**: Define evaluation methodology for the swimlane 3 multimodal model in the [[pdf2pres]] use case.

**Action**: Collaborate with [[Andrei Stefan|Andrei]] and [[Brian Eriksson|Brian]] to establish appropriate evaluation framework and success criteria for this model in the presentation generation context.

**Key Questions**:
- What metrics are most relevant for PDF-to-presentation conversion quality?
- How should we measure multimodal understanding in this specific use case?
- What baseline should we compare against?

## Evaluation Ask 2: Express Templates Evaluation

**Objective**: Compare MM model performance against MINTv1 baseline using [[Express]] templates.

**Two-Phase Approach**:

### Phase 1: Offline Evaluation (LLM-as-a-Judge)
- **Scale**: 500 templates (stratified sample)
- **Method**: LLM-based quality assessment
- **Comparison**: MM model vs. MINTv1
- **Purpose**: Broad coverage quality comparison across template types

### Phase 2: Online Evaluation
- **Scale**: Top 100 head templates
- **Method**: Side-by-side rendition comparison
- **Comparison**: MM model vs. MINTv1
- **Purpose**: Real-world performance validation on high-traffic templates

## Timeline & Dependencies

Both evaluation workstreams support the Adobe ecosystem node ingestion unification exercise led by [[Anshul Omar|Anshul]].

**Next Steps**:
1. Schedule evaluation planning meeting with Andrei and Brian
2. Coordinate with Express team to obtain template dataset
3. Define stratification strategy for 500-template offline eval
4. Identify criteria for "head templates" selection (top 100)
