---
created: 2025-10-09
tags:
  - claude
  - prompt
pageType: claudeResearch
---

# [[Style Home|Photo Style]] Tagging Analysis Prompt

## Purpose
Analyze photographs using defined [[Style Home|style]] attributes (definitions) and weights to generate top-10 [[Style Home|style]] tags for each image. Produces both weighted and unweighted analysis for comparison.

## Prerequisites
- **Definitions file**: JSON file containing terms, definitions, and examples for [[Style Home|style]] attributes
- **Weights file**: JSON file containing weight multipliers for each term
- **Test images**: Folder containing images to analyze

## Prompt Template

```
We're working on [[Style Home|photo style]] tagging using VLLM models. I need you to analyze images using our current definitions and weights.

**Files needed:**
- Definitions: [path to definitions JSON file]
- Weights: [path to weights JSON file]
- Images: [path to folder with test images]

**Analysis tasks:**

1. **Weighted Analysis**:
   - Read both definitions and weights files
   - For each image, assign scores (0.0-1.0) for how well each tag applies
   - Apply the weight multiplier to each score
   - Report top 10 tags ranked by (score × weight)
   - Include: filename, brief scene description, tag name, weight, raw score

2. **Unweighted Analysis**:
   - Repeat analysis treating all weights as 1.0
   - Report top 10 tags ranked by raw score only
   - Same format as weighted analysis

3. **Comparison Report**:
   - Create markdown report saved alongside test images
   - Include both analyses for each image
   - Create comparison table showing weighted vs unweighted top 3 tags per image
   - Identify key differences and insights about weight impact
   - Note where weighting helped vs. where it buried accurate tags

**Output format:**
- Provide full analysis results in your response
- Save markdown report as: `[test folder]/tagging_analysis_report.md`
```

## Example Usage

```
We're working on [[Style Home|photo style]] tagging using VLLM models. I need you to analyze images using our current definitions and weights.

**Files needed:**
- Definitions: /Users/rmanor/Downloads/Definitions_oct_9.json
- Weights: /Users/rmanor/Downloads/weights_oct_9.json
- Images: /Users/rmanor/Desktop/Style tagging test

**Analysis tasks:**

1. **Weighted Analysis**:
   - Read both definitions and weights files
   - For each image, assign scores (0.0-1.0) for how well each tag applies
   - Apply the weight multiplier to each score
   - Report top 10 tags ranked by (score × weight)
   - Include: filename, brief scene description, tag name, weight, raw score

2. **Unweighted Analysis**:
   - Repeat analysis treating all weights as 1.0
   - Report top 10 tags ranked by raw score only
   - Same format as weighted analysis

3. **Comparison Report**:
   - Create markdown report saved alongside test images
   - Include both analyses for each image
   - Create comparison table showing weighted vs unweighted top 3 tags per image
   - Identify key differences and insights about weight impact
   - Note where weighting helped vs. where it buried accurate tags
```

## Expected Outputs

### 1. Inline Analysis Results
Claude will provide detailed results in the conversation showing:
- Each image's weighted top 10 tags
- Each image's unweighted top 10 tags
- Raw scores and weight-adjusted scores

### 2. Markdown Report File
Saved to test image folder containing:
- Full analysis tables for each image
- Comparison table (weighted vs unweighted top 3)
- Key findings about weight effectiveness
- Specific examples where weights helped or hindered

## Tips for Effective Analysis

1. **Be specific about file paths** - Provide absolute paths to avoid confusion
2. **Request scene descriptions** - Helps identify which image is which in results
3. **Ask for insights** - Request commentary on weight effectiveness and definition quality
4. **Iterate** - Use findings to refine definitions and weights

## Follow-up Questions

After receiving the analysis, consider asking:

- "Are there weaknesses in the definitions that led to poor tagging?"
- "Which weights seem too high or too low based on visual accuracy?"
- "Are there missing attributes that would better describe these images?"
- "Should we consolidate any overlapping or redundant terms?"

## Related Files

- Current definitions: `/Users/rmanor/Downloads/Definitions_oct_9.json`
- Current weights: `/Users/rmanor/Downloads/weights_oct_9.json`
- Previous analysis: Check Desktop/Style tagging test folder for prior reports
