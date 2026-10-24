---
title: "ADR-0001 25M Tabula Rasa Architecture"
type: decision
status: accepted
tags:
  - ai-school
  - decision
  - architecture
  - model-spec
created: 2026-10-23
updated: 2026-10-23
---

# ADR-0001 — 25M Tabula Rasa Architecture for the Learner

## Status
Accepted

## Context
The goal of the AI Learner Laboratory is an interactive, ongoing learning environment rather than a static in-context chatbot with frozen weights. We must select an initial model size and learning paradigm that matches the target hardware: an NVIDIA Tesla P4 (Pascal GP104, `sm_61`, 8 GB VRAM, no Tensor Cores, native FP32/INT8).

Additionally, using an existing pretrained model (such as a 1.5B LLM) introduces massive pretrained biases, making it difficult to distinguish genuine newly acquired capabilities from latent training distributions.

## Decision Drivers
- **Verifiable Developmental Learning:** Eliminating pretrained artifacts by starting from zero knowledge (tabula rasa / random weights).
- **Interactive Real-Time Speed:** Backward and forward passes must execute within single-digit milliseconds so learning occurs live during interactions.
- **Hardware Budget:** Entire training state (FP32 weights, gradients, AdamW momentum & variance) must fit comfortably within the Tesla P4's 8 GB VRAM.
- **Capacity for Kindergarten/1st Grade Logic:** The model must have sufficient expressive capacity to learn spelling, grammar, simple narrative comprehension, and basic arithmetic.

## Options Considered

### Option A — 1.5B Pretrained Model + PEFT/LoRA Adapter
- *Benefits:* High out-of-the-box language fluency and coding ability.
- *Costs / risks:* High VRAM footprint; learning is confined to adapter layers; difficult to falsify whether the model "learned" a concept or simply recalled a pretrained pattern.

### Option B — 1M–5M Micro Model from Scratch
- *Benefits:* Ultra-fast training and minimal memory.
- *Costs / risks:* Very low capacity; may struggle to retain vocabulary alongside multi-step reasoning and syntax.

### Option C — ~25M Parameter Transformer from Scratch (Selected)
- *Architecture:* 8 layers, 512 hidden dimension, 8 attention heads, 4,096 vocab size, 512 context length.
- *Total Memory:* ~108 MB weights, ~108 MB gradients, ~216 MB AdamW states -> Total training state ~432 MB. Leaves >7 GB VRAM headroom.
- *Benefits:* 100% full-parameter backpropagation in single-digit milliseconds on the Tesla P4; plenty of parameter capacity to master 1st-grade language and math; zero pretrained contamination.

## Decision
We select **Option C: A ~25M parameter causal Transformer initialized from scratch (random weights)**. The learner model will be educated from the ground up starting with early-childhood curricula (phonics, vocabulary, simple syntax, and basic counting).

## Consequences
- **Positive:**
  - True empirical learning: every learned token, word, and rule is directly traceable to the school's lessons and feedback.
  - Interactive live plasticity: updates run synchronously in milliseconds without blocking conversation.
  - Fits easily in < 1 GB of the Tesla P4's 8 GB memory.
- **Negative:**
  - Initial outputs will be random entropy (babbling) until the first phase of phonics and vocabulary training converges.
  - Requires early childhood curricula in `vault/02-School/` before advancing to complex subjects like C programming.
- **Follow-up Work:**
  - Implement PyTorch causal Transformer module with ~25M parameters.
  - Implement basic tokenizer (e.g. byte-level BPE with 4k vocab).
  - Add early-childhood curriculum stages (Phonics, Vocabulary, Simple Sentences, Counting) in `02-School/`.

## Related
- [[NOTES|AI Learner Laboratory Discussion Notes]]
- [[Architecture|Harness Architecture]]
