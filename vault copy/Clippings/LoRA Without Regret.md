---
pageTitle: "LoRA Without Regret"
pageSource: "https://thinkingmachines.ai/blog/lora/"
dateCaptured: "2025-09-29T13:55:07-07:00"
read: true
---
# [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/)

[[September 29, 2025]] 

The article \\"LoRA Without Regret\\" investigates the conditions under which Low-Rank Adaptation (LoRA) can match the performance and efficiency of full fine-tuning (FullFT). The authors find that LoRA can indeed achieve comparable results to FullFT when specific details are addressed, particularly in typical post-training scenarios. This opens the door for widespread adoption of efficient fine-tuning.

Key findings include:
- LoRA performs as well as FullFT when applied to all layers of the network, especially MLP and MoE layers.
- LoRA and FullFT achieve similar performance for reinforcement learning, even with very low LoRA ranks.
- The optimal learning rate for LoRA is consistently about 10x higher than for FullFT.


**Highlights**
> Today’s leading language models contain upwards of a trillion parameters, pretrained on tens of trillions of tokens. Base model performance keeps improving with scale, as these trillions are necessary for learning and representing all the patterns in written-down human knowledge.
> 
> n contrast, post-training involves smaller datasets and generally focuses on narrower domains of knowledge and ranges of behavior. It seems wasteful to use a terabit of weights to represent updates from a gigabit or megabit of training data.
> 
> The leading PEFT method is low-rank adaptation, or LoRA
> 
> LoRA replaces each weight matrix W from the original model with a modified version $W’ = W + \gamma BA$, where B and A are matrices that together have far fewer parameters than W, and $\gamma$ is a constant scaling factor. In effect, LoRA creates a low-dimensional representation of the updates imparted by fine-tuning.
> 
> For supervised fine-tuning on small-to-medium-sized instruction-tuning and reasoning datasets, LoRA performs the same as full fine-tuning.
> 
> We calculate that LoRA takes slightly more than ⅔ of the FLOPs that full fine-tuning does per pass. As a result, it will often outperform FullFT on compute efficiency overall.

