---
pageTitle: "Intent Understanding: SRL model - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/Intent+Understanding%3A+SRL+model"
dateCaptured: "2025-09-24T09:24:26-07:00"
pageSource: "Adobe Wiki"
---
[[September 24, 2025]] 

This page details the development of an [[Intent AI Home|Intent Understanding]] [[NER & SRL|semantic role labeling]] model for extracting [[NER & SRL|NER]] and their semantic roles from user queries to improve search filtering. It covers the model architecture, data generation process, post-processing steps, and [[Evaluation|evaluation]] methodology.

-   **Objective:** Extract [[NER & SRL|NER]] and semantic role mappings from user queries for precise search result filtering.
-   **Model:** `meta-llama/LLama-3.2-1B-Instruct` fine-tuned with a LORA head.
-   **Data Generation:** Synthetic dataset created using `meta-llama/Llama-4-Scout-17B-16E-Instruct` by generating attribute-value combinations and user prompts.
-   **[[Evaluation]]:** Assessed using absolute match, granular match, precision, recall, and F1 score, both overall and field-wise.
-   **Future Work:** Significant planned improvements focus on dataset quality and diversity, pre/post-processing enhancements, and training optimizations.

The [[Evaluation|evaluation]] methods planned are as follows:

-   **Metrics:**
    -   **Absolute match:** Checks if all entities and their values exactly match between ground truth and model output.
    -   **Granular match:** Assigns +1 for key name match and another +1 if the corresponding value also matches. The total score for all attributes is divided by the number of attributes in the ground truth entities.
    -   **Precision:** `tp / (tp + fp)`
    -   **Recall:** `tp / (tp + fn)`
    -   **F1 Score:** `(precision * recall) / (precision + recall)` (overall and field-wise)
    -   **True/False Positive/Negative logic:**
        -   `tp`: Model output matches ground truth exactly (e.g., `{\\"created_by\\": \\"John\

**Related:** [[NER & SRL]] - Canonical overview of [[Query Understanding|NER]] and [[NER & SRL|SRL]] concepts and applications
