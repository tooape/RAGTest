---
pageType: claudeResearch
created: "2025-09-25"
tags: ["claude", "mcp", "agents", "product-analysis"]
---

# MCP Agents Use Cases - September 2025
---

*Extracted from: [[20250919_Agents__use cases in LLMs_v1.pdf]]*
## Three Criteria to Prioritize Use Cases

1. **User value**: Do we have the right tools to support the highest-value use cases that customers who start their workflows in a chat interface will take?

2. **Feasibility**: Can we expose these tools without significant technical blockers? Can we create a positive user experience, given the constraints of accessing MCP servers from a chat interface today?

3. **Differentiation**: Do we offer capabilities that differentiates us relative to what other companies have offered or what LLMs provide natively?

---

## Photoshop

### Scope Definition
**Focus**: High-impact tools that are a step up from existing MCP connectors today

**Tool Categories**:

| **Base enablement** | **Global edits** | **Generative edits** | **Fine-tuning edits** | **Advanced actions** |
|---|---|---|---|---|
| • Basic file operations<br>• Asset retrieval/export<br>• Basic format support and conversion | • Resize & rotate<br>• Apply filters (grain, blur)<br>• Apply effects (overlay, sketch)<br>• Retouching<br>• Other global adjustments (brightness, contrast, hue, etc.) | • Generative expand<br>• Generative fill<br>• Generate background<br>• Generative remove<br>• Generative upscale<br>• Harmonize | • Basic add text<br>• Selection & masks<br>• Add shadow to (blur + multiply)<br>• Advanced text effects & operations<br>• Shapes operations | • Transforms<br>• Compositing<br>• Complex layer operations<br>• Advanced automation |

**Scope Status**:
- ✅ **In scope but not differentiated**: Base enablement
- ✅ **Differentiated**: Global edits, Generative edits  
- ❌ **Out of scope for initial MCP release**: Fine-tuning edits, Advanced actions

### Customer Segments & Use Cases

| **Segment** | **Size** | **Sub Segment** | **Example Prompts** | **API Workflow** |
|---|---|---|---|---|
| **Creators** | 610M | Monetizing Social Creators | Make a YouTube thumbnail from this selfie… include a bold 3-word title…make it more cinematic | Retrieve asset→ resize→ blur background → resize→ add text → apply effects |
| | | Enthusiastic Creative Hobbyists | Remove the background and set me in a fantasy forest… add a glowing lantern in my hand | Retrieve asset→ remove background→ gen background→ gen fill |
| **Students** | 2.1B | - | Make me a movie poster for class…add a gorilla coming into the street of my image…harmonize with background | Retrieve asset→ add object→ add shadow→ harmonize |
| **Photo Hobbyists** | 1.3B | - | Clean up this old family photo by removing dust…add a vintage camera on the table | Retrieve asset→ gen upscale → gen fill |
| **Creative Pros** | 49M | - | Upscale this image to 4K…make the background look more metallic…and drop in the product name with a soft shadow | Gen upscale → apply effect → apply text → apply shadow |

---

## [[Express]]

### Scope Definition
**Focus**: High-impact tools that support differentiated handoff to the Express Assistant

**Tool Categories**:

| **Search & retrieval** | **Create assets & designs** | **Asset-level edits*** | **Design-level edits** |
|---|---|---|---|
| • Search public templates<br>• Get rendition<br>• Search documents<br>• Get document data<br>• Summarize document<br>• Search custom templates | • Generate image (Firefly API)<br>• Fill template [text]<br>• Fill template [image, style]<br>• Generate presentation<br>• Generate video<br>• Generate QR code<br>• Fill tagged template<br>• Publish template | • Remove background (Ps API)<br>• Replace background (Ps API)<br>• Crop (Ps API)<br>• Generative Expand (Firefly API)<br>• Caption Video (DVA API)<br>• Merge video (DVA API)<br>• Enhance speech (DVA API) | • Apply brand<br>• Edit document<br>• Translate document<br>• Submit for review<br>• Review document |

**Scope Status**:
- ✅ **Differentiated**: Search & retrieval, Create assets & designs
- ✅ **Stretch with dependency on Photoshop MCP**: Asset-level edits  
- ❌ **Out of scope for initial MCP release**: Design-level edits

*\* Stretch with dependency on Photoshop MCP*

### Customer Segments & Use Cases

| **Segment** | **Size** | **Example Prompts** | **API Workflow** |
|---|---|---|---|
| **Marketing teams** | XXM | Create a design for a flyer to promote Bella's Boutique summer sale, with up to 50% off select items | Search templates → Fill templates |
| | | Generate close-up of a pediatrician gently listening to a young child's heartbeat with a stethoscope, both smiling, warm and professional…crop it to remove empty space at the top | Generate image → Crop |
| | | Create images resized for Meta and LinkedIn ads…replace background with something cleaner…add space on the right side for clinic name and tagline | Generate image → Crop → Replace background → Gen Expand* |
| **Knowledge workers** | XXM | Create a design for a LinkedIn post to announce a promotion to Project Manager at BlueSky Solutions. | Search templates → Fill templates |
| | | Create a business card for Alex Rivera, freelance designer…include phone number, email, and website | Search templates → Fill templates |

---

## Acrobat

### Scope Definition
**Focus**: APIs go beyond traditional asset storage and retrieval available today

**Tool Categories**:

| **Create or retrieve** | **Transform file** | **Basic edit / modify actions** | **Specialized edits** |
|---|---|---|---|
| • Create file<br>• Storage search<br>• Export file<br>• Extract | • Compress file<br>• Convert file type<br>• Combine PDFs<br>• Split PDFs | • Organize pages<br>• Rotate pages<br>• Delete pages<br>• Convert to image<br>• OCR<br>• Edit text<br>• Replace text<br>• Flatten | • Accessibility features<br>• Redact<br>• Sign<br>• Convert to form |

**Scope Status**:
- ✅ **In scope but not differentiated**: Create or retrieve
- ✅ **Differentiated**: Transform file, Basic edit/modify actions
- ❌ **Out of scope for launch**: Specialized edits (some actions planned for phase 2, others infeasible given current UX)

### Customer Segments & Use Cases

| **Segment** | **Size** | **Example Prompts** | **API Workflow** |
|---|---|---|---|
| **Business professionals** | XXM | Split the big scanner dump into separate files every 25 pages and name them with a part number | Split PDFs |
| | | From the Invoices/2025/Q1 folder, combine all PDFs into a single file called Invoices Q1 2025 and then compress it below 10 MB | Search → Combine → Create → Compress |
| | | Turn the policy PDF into a Word document that keeps headers, footers, and tables editable | Search → Convert file type |
| | | Find all files named Canva newsletters in Acrobat…rotate the first page of each newsletter to landscape…combine into a single file | Search → Rotate pages → Combine |
| | | Find all files that are invoices uploaded in 2024 in Acrobat and merge them to a single file | Search → Combine |

---

## Technical Constraints

- **Tool Limit**: MCP servers can reliably handle ~20 tools today
- **Performance**: May need to trim tool lists if performance is degraded during testing
- **Differentiation**: Focus on capabilities that differentiate from MCP servers today, which primarily focus on asset retrieval and storage

---

## Competitive Context

- **Current MCP Landscape**: Existing servers (e.g., Canva) focus primarily on asset retrieval and require kick-out to application for essentially all other actions
- **Adobe's Advantage**: End-to-end workflows within chat interface without application handoff