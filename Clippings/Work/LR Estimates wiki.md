---
pageTitle: "LR Estimates - Adobe Sensei - Adobe Wiki"
pageLink: "https://wiki.corp.adobe.com/display/Sensei/LR+Estimates#LREstimates-AdobeOneV2ModelinMassiveBatchOptimization**"
dateCaptured: "2025-10-24T09:38:55-07:00"
pageSource: "Adobe Wiki"
author:
  - "Harish Suvarna"
tags:
  - "adobeWikis"
---
# [LR Estimates](https://wiki.corp.adobe.com/display/Sensei/LR+Estimates#LREstimates-AdobeOneV2ModelinMassiveBatchOptimization**)

[[October 24, 2025]] 

## Summary
This document outlines load testing and cost estimates for various Adobe Search services, primarily focusing on machine learning models and infrastructure components. It covers:

*   **CAT Model on CPF Async:** Details performance (320 RPM, 31.25 mins for 10K images) and cost (\$0.40 per 10K images with 20% CPF overhead) for the CAT model using one A10G GPU. It also lists enhancement requests for performance gains.
*   **CAT Model on Massive Batch:** Presents optimized batch processing costs for the CAT model (\$0.22 per 10K images with 30% batch overhead) by processing images from S3 on GPUs in bulk.
*   **AdobeOne V1 Model:** Shows performance (270 RPM, 37.07 mins for 10K requests) and cost (\$0.91 per 10K images with 20% CPF overhead) for the AdobeOne V1 model, noting that both CAT and AdobeOne V1 models resize 1000px input images to 224x224 pixels automatically.
*   **MINT Service:** Provides cost estimates for the MINT service (\$0.28 per 10K requests with 20% CPF overhead), running on T4 GPUs.
*   **Elastic Search:** Analyzes current ES costs, calculating an average hosting cost of \$0.53 per GB. It estimates the cost for 10K documents with MINT and AdobeOne embeddings to be \$0.24 (0.45 GB).
*   **AdobeOne V2 Model:** Presents updated performance and cost figures for the AdobeOne V2 model on CPF. Images cost \$0.19 per 10K, English Text \$0.015 per 10K, and MultiLingual Text \$0.045 per 10K, all using a G5 GPU with 20% CPF overhead.
*   **AdobeOne V2 Model in Massive Batch Optimization:** Highlights significant cost reduction for image processing to \$0.0064 per 10K images using massive batch processing with a G5 GPU and 30% batch overhead. 

## Highlights
> 

## Details
-   CAT Model (CPF Async): \$0.40 / 10K images (A10G GPU, 20% CPF overhead)
-   CAT Model (Massive Batch): \$0.22 / 10K images (A10G GPU, 30% Batch overhead)
-   AdobeOne V1 (CPF Async): \$0.91 / 10K images (A10G GPU, 20% CPF overhead)
-   AdobeOne V2 (CPF Async): \$0.19 / 10K images (Images, G5 GPU, 20% CPF overhead)
-   AdobeOne V2 (Massive Batch): \$0.0064 / 10K images (Images, G5 GPU, 30% Batch overhead)

