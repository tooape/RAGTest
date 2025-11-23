---
created: "2025-10-20"
pageType: claudeResearch
tags:
  - claude
  - machine-learning
  - photo-styles
  - gemma
  - annotations
---

# Photo Style Annotations - Gemma 27B Refinement - October 2025
---

## Context

We're building a photography style embedding space for [[Lr Home|Lightroom]] and Photoshop using Gemma 3 27B to annotate training images across 64+ style dimensions. The model analyzes images and outputs confidence scores (0.0-1.0) for each dimension, which are then used to create style embeddings for similarity matching.

**Model**: Gemma 3 27B (multimodal)
**Task**: Image annotation across photography style dimensions
**Output**: JSON array of `{"term": "<dimension>", "score": <0.0-1.0>}` for 64 dimensions
**Weighting Algorithm**: Soft-IDF base weights with manual multipliers (see Maya's explanation in Slack)

## Problems Identified

### 1. **Opposite Dimensions Showing Weak Correlation**

**Issue**: Correlation analysis revealed that opposite dimension pairs weren't showing the expected strong negative correlations:
- high contrast vs low contrast: r=-0.534 (expected closer to -0.9)
- high saturation vs low saturation: r=-0.637 (should be stronger)
- high key vs low key: r=-0.440 (weak negative correlation)
- overexposure vs underexposure: r=0.215 (positive! should be negative)

**Root cause**: The system prompt didn't explicitly instruct Gemma to treat opposite pairs as inversely related. The model could score both "high contrast" and "low contrast" moderately without understanding they're mutually exclusive.

### 2. **Overlapping/Redundant Dimensions**

**Issue**: Multiple dimensions describing very similar or overlapping concepts:

**Grain categories (5 → 2)**:
- coarse grain, rough grain, smooth grain, high grain, low grain
- Problem: "coarse grain" and "rough grain" had nearly identical definitions
- Solution: Consolidated to just "high grain" and "low grain"

**Color intensity (3 → 1)**:
- bright colors, bold colors, vibrant colors
- Problem: Too similar - all describe saturated/impactful colors
- Solution: Merged bright into bold colors, kept vibrant as distinct (focuses on purity)

**Cool tints (3 → 2)**:
- aqua tint, cyan tint, blue tint
- Problem: Aqua and cyan both described "teal" tones
- Solution: Merged aqua into cyan tint (now covers cyan-to-teal range)

**Red-purple family (2 → 1)**:
- magenta tint, purple tint
- Problem: Both described as "between red and blue"
- Solution: Merged into magenta tint (now covers purplish-pink to violet range)

### 3. **Technical "How It's Made" Language**

**Issue**: Definitions included camera settings, post-processing techniques, and technical details that Gemma can't observe:
- "Achieved by lowering the blacks slider..."
- "Created using wide apertures (f/1.4, f/1.8, f/2.8)..."
- "Results from shooting at high ISO (1600+)..."

**Root cause**: Definitions were written for photographers, not for ML visual analysis.

**Solution**: Rewrote all 64+ definitions to focus purely on observable visual characteristics:
- Before: "Achieved through the highlights slider in the Basic panel..."
- After: "Bright areas appear less glaring while retaining texture and detail..."

### 4. **Ambiguous "Neutral" Terms**

**Issue**: Dimensions like "neutral exposure," "neutral saturation," "neutral white balance" created conceptual confusion:
- What does it mean to score 1.0 on "neutral exposure"?
- Is that "strongly neutral" (paradoxical) or "perfectly balanced"?
- How does "neutral white balance" relate to "warm white balance"?

**Root cause**: The prompt didn't clarify that "neutral" means "baseline/unmodified" not "somewhat present."

### 5. **Missing Popular Aesthetics**

**Issue**: The dimension set didn't include "matte faded look" - one of the most popular modern photography aesthetics (Instagram/lifestyle/wedding photography).

**Characteristics**: Lifted blacks (milky gray shadows), compressed tonal range, flat/hazy appearance, vintage feel.

**Why it matters**: While technically a composite of "raised shadows" + "low contrast," it's such a recognizable and requested style that the model benefits from learning it as a distinct pattern.

## Solutions Implemented

### 1. **Updated System Prompt for Opposite Dimensions**

Added explicit instruction in the prompt:

```markdown
3. **Opposite dimensions**: Some style pairs are opposites:
   - high contrast / low contrast
   - high saturation / low saturation
   - high grain / low grain
   - overexposure / underexposure
   - high key / low key
   - raised vs lowered (highlights, shadows, whites, blacks)

   For these pairs, if one scores high (0.7+), the other should score low.
```

Also added concrete example showing inverse scoring in practice.

### 2. **Consolidated to 64 Dimensions**

**Final dimension count: 64** (down from 70)

**Removed**:
- aqua tint → merged into cyan tint
- purple tint → merged into magenta tint
- bright colors → merged into bold colors
- coarse grain, rough grain, smooth grain → consolidated to high/low grain
- desaturated blues → removed (too specific)

**Added**:
- matte faded look → new dimension for popular aesthetic

**Enhanced**:
- monochrome → emphasized sepia tone more prominently in definition

### 3. **Rewrote All Definitions - Visual Only**

Every definition now describes only what's observable in the image:
- Removed all camera settings references (ISO, aperture, shutter speed)
- Removed all post-processing technique descriptions (sliders, curves, panels)
- Removed causation language ("results from," "achieved by," "created using")
- Focused on visual appearance, mood, and perceptual qualities

**Example - shallow depth of field**:

Before:
> Achieved through wide apertures (f/1.4, f/1.8, f/2, f/2.8), longer focal lengths, closer focusing distances, or larger sensor formats...

After:
> A narrow zone of acceptable sharpness where only a small portion of the image (typically the subject) is in focus while foreground and/or background elements are significantly blurred. The out-of-focus areas show progressive blur that increases with distance from the focal plane.

### 4. **Clarified "Neutral" Terms in Prompt**

Added explicit guidance:

```markdown
4. **Neutral terms**: For dimensions like "neutral exposure," "neutral saturation,"
   "neutral white balance," etc.:
   - **1.0** = perfectly balanced, unmodified baseline
   - **0.0** = strongly adjusted away from neutral (either direction)

   An image with strong yellow cast or warm white balance should score low on
   "neutral white balance" and high on "warm white balance".
```

### 5. **Improved Scoring Scale Granularity**

**Before**: Only defined 0.0, 0.5, 1.0 (three anchor points)

**After**: Five-tier scale with clear ranges:
- 0.9-1.0: Dominant, defining characteristic
- 0.6-0.8: Clearly present and noticeable
- 0.3-0.5: Subtly present or moderately exhibited
- 0.1-0.2: Barely detectable
- 0.0: Not present

**Rationale**: Gemma 27B benefits from explicit guidance on intermediate values.

### 6. **Updated Weights File**

Created new weights file (`style_dimension_weights_v2.json`) matching the 64 dimensions.

**Key weight decisions** (based on Maya's soft-IDF algorithm):
- **1.25**: black & white (boosted - rare and highly distinctive)
- **1.0**: Most dimensions (54) - no manual boost, let soft-IDF decide
- **0.75**: All 7 tints + monochrome (downweighted - vary with lighting)
- **0.5**: desaturated (moderate downweight - overlaps with low saturation)

**Important**: These are multipliers on top of automatic soft-IDF base weights. Rare features automatically get higher base weights, then these multipliers apply.

## Prompt Structure Optimizations for 27B Model

### Use Clear Hierarchy
- Markdown headers organize information
- Numbered lists for sequential rules
- Bullet points for related items

### Provide Concrete Examples
- Abstract rules alone aren't enough for smaller models
- Show realistic scoring scenario (sunset portrait example)
- Demonstrate inverse scoring for opposite dimensions

### Repeat Key Concepts
- "Focus on overall aesthetic" appears in multiple forms
- Reinforces the most important instruction

### Structured Sections
1. Scoring Guidelines (with 5-tier scale)
2. Important Rules (5 numbered rules)
3. Output Format (JSON specification)
4. Example (concrete demonstration)

## Files Created

1. **`top_styles_definitions_v2_visual_only.json`** (64 dimensions)
   - Visual-only descriptions
   - 2-4 sentences each
   - Three scored examples per dimension
   - No technical/camera terminology

2. **`image_style_annotator_prompt_v2.md`**
   - Optimized for Gemma 27B
   - Explicit opposite dimension handling
   - Clarified neutral terms
   - 5-tier scoring scale
   - Concrete examples

3. **`style_dimension_weights_v2.json`** (64 dimensions)
   - Aligned with consolidated dimensions
   - Comments explain weighting strategy
   - Organized by Lightroom panel sections

## Lessons for Future ML Annotation Work

### 1. **Test Opposite Dimension Correlations Early**
Run correlation analysis on opposite pairs immediately. This catches conceptual misunderstandings in the prompt before extensive annotation work.

### 2. **Write Definitions for ML Models, Not Humans**
If the model can't observe it (camera settings, post-processing steps, intent), don't include it. Focus exclusively on visual characteristics.

### 3. **Consolidate Overlapping Dimensions Before Training**
Similar dimensions dilute each other's signal. Better to have fewer, clearer dimensions than many ambiguous ones.

### 4. **Explicit > Implicit for Smaller Models**
27B models need clear rules about:
- Mutually exclusive categories
- Scoring scales with specific ranges
- What "neutral" means
- How multiple dimensions can coexist

### 5. **"Neutral" is Conceptually Tricky**
Terms like "neutral exposure" require special handling. The prompt must explicitly state that high scores = perfectly balanced, low scores = adjusted away from baseline.

### 6. **Popular Aesthetics Matter**
Even if a look is technically a composite (matte = raised shadows + low contrast), if it's a commonly recognized style, include it as a distinct dimension.

### 7. **Trust the Soft-IDF Algorithm**
Don't over-weight manually. Most dimensions should be 1.0 and let the automatic inverse document frequency calculation determine importance based on rarity in the dataset.

### 8. **Structure Prompts for the Model Size**
27B models benefit from:
- Clear hierarchical organization
- Concrete examples showing expected behavior
- Repetition of key concepts in different forms
- Explicit rules about edge cases

## Next Steps for Photo Styles V2

When we revisit this work:

1. **Run correlation analysis** on the new 64-dimension annotations
2. **Validate opposite pairs** show strong negative correlations (r < -0.7)
3. **Check neutral terms** - images with strong adjustments should score low on neutral dimensions
4. **Evaluate matte faded look** - verify it's being detected as distinct from just low contrast
5. **Review tint consistency** - with 0.75 downweighting, verify they're not over-triggered
6. **Consider composition dimensions** - spatial relationships, rule of thirds, leading lines, symmetry, etc.

## Related Work

- [[Evaluation]] - General evaluation frameworks
- [[Lr Home]] - Lightroom integration context
- [[Style Home]] - Photography style understanding overview

## References

- Gemma 3 27B model card: [Link if available]
- Soft-IDF weighting algorithm: Maya's Slack explanation (October 2025)
- Correlation analysis charts: See attached images in Slack thread
