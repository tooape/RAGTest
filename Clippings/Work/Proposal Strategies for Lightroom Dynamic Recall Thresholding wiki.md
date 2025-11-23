---
pageTitle: "Proposal : Strategies for Dynamic Thresholding - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/adobesearch/Proposal+%3A+Strategies+for+Dynamic+Thresholding"
dateCaptured: "2025-09-29T09:05:16-07:00"
pageSource: "Adobe Wiki"
author:
  - "Aman Goyal"
tags:
  - "Adobe wikis"
---
[[September 29, 2025]] 

**Summary**
This proposal outlines strategies for dynamic thresholding in the recall phase of [[Query Understanding|semantic search]], aiming to improve result filtering by adapting similarity score cutoffs per [[Lr Home|Lightroom]] query. It addresses the limitations of static thresholds, which are suboptimal for varying query characteristics, and proposes a conditional approach based on the standard deviation of similarity scores to determine the best thresholding method (e.g., Z-score, elbow method, percentage drop from top score). 

**Highlights**
> ## 5\. Suggested / Recommended Approach
> 
> 1. **When standard deviation is low** (i.e., **< 0.1**): Use a simple cutoff formula ( cutoff\_factor has default value as 1 , and is configurable ):
> 	- `cutoff = mean - (cutoff_factor × std_dev)`
> 2. **When standard deviation is high** (i.e., **\> 0.1 , <8**):
> 	- Use the **elbow method** to identify a sharp drop in the score distribution as the cutoff point.
> 	- Alternatively , measure score differences **relative to the top score** rather than just consecutive elements — treating the top score as a baseline.
> 3. When standard deviation is very high ( ie , > 8 ): Use **Percentage drop from Top Score** to identify the cutoff

**Details**
-   **Problem:** Fixed similarity thresholds are brittle, leading to suboptimal results due to varying score distributions across queries.
-   **Goal:** Adapt cutoff points dynamically based on how sharply similarity scores drop to improve precision without significant [[Evaluation|recall]] loss.
-   **Similarity Scores:** Original cosine similarity values (-1 to 1) are adjusted to range from 0-2.
-   **Proposed Strategies:** Z-Score, Knee/Elbow Detection, Percentile-Based Filtering, Entropy/Variance-Based, and Percentage drop from Top Score.
-   **Recommended Approach:**
    -   **Low Std Dev (< 0.1):** `cutoff = mean - (cutoff_factor × std_dev)`
    -   **High Std Dev (0.1 to < 8):** Elbow method or score differences relative to top score.
    -   **Very High Std Dev (> 8):** Percentage drop from Top Score.

