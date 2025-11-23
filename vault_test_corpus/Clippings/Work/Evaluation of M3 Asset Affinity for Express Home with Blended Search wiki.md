---
pageTitle: "Evaluation of M3 Asset Affinity for Express Home with Blended Search - Adobe Search - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Evaluation+of+M3+Asset+Affinity+for+Express+Home+with+Blended+Search"
dateCaptured: "2025-10-23T15:39:41-07:00"
pageSource: "Adobe Wiki"
author:
  - "Priya Shanmugasundaram"
tags:
  - "adobeWikis"
---
# [Evaluation of M3 Asset Affinity for Express Home with Blended Search](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=adobesearch&title=Evaluation+of+M3+Asset+Affinity+for+Express+Home+with+Blended+Search)

[[October 23, 2025]] 

## Summary
This document outlines the evaluation of two asset affinity models (Treatment 1 and Treatment 2, the latter from the M3 Asset Affinity Model) for blended search in Express Home. The evaluation utilizes behavioral data from user search queries and asset interactions (templates, photos, design assets, backgrounds, videos) over 365 days, enriched with GPT-based query type and content type scores.

Offline analysis compares the performance of these treatments based on 'Asset Mix' metrics (Coverage Ratio, Dominant Asset) and 'Ranking' metrics (Top-1 Asset, Overlap Ratio). Queries are flagged for human review if there's a significant difference (>20%) in coverage ratio for any asset type or low overlap (<40%) in top-10 results. While high template coverage was observed uniformly, the third flagging criterion (single asset type dominating >80% of results) was relaxed.

The results indicate strong overall agreement between the two treatments, with 87.9% of queries yielding the same top-1 asset type. In cases of disagreement (12.1%), the primary conflicts were between templates and photos. Treatment 2 showed a stronger bias towards video content, while Treatment 1 more frequently surfaced design assets and backgrounds as top-1 results. Both treatments demonstrated high consistency in their Top-10 (median overlap of 10) and Top-50 results (mean overlap of ~59%). 

## Highlights
> 

## Details
- **Evaluation Purpose:** Compare Treatment 1 (T1) and M3 Asset Affinity Model (Treatment 2 or T2) for blended search in Express Home.
- **Dataset:** 365 days of user search queries and asset interaction data (templates, photo, design_asset, background, video), with GPT-based query intent and content type scores.
- **Metrics:** Coverage Ratio, Dominant Asset (Asset Mix) and Top-1 Asset, Overlap Ratio (Ranking).
- **Flagging Criteria:** Queries are flagged for human review if coverage ratio difference > 20% or top-10 overlap < 40%.
- **Key Insight:** 87.9% agreement in top-1 asset type; T2 favors video, T1 favors design assets/backgrounds when they differ.

