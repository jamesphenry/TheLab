---
title: Assessment 1.1 — Phonics and Sight Words Evaluation
type: assessment
status: active
tags:
  - ai-school
  - assessment
  - language
created: 2026-10-23
updated: 2026-10-23
---

# Assessment 1.1 — Phonics & Sight Words

## Purpose
Evaluate whether the student model has begun learning character sequences, whitespace boundaries, and CVC word patterns.

## Rubric
- **Level 0 (Entropy/Babble):** Output is random characters or non-letter bytes.
- **Level 1 (Phonemic Awareness):** Output produces valid English letters and spaces with lower loss on target words.
- **Level 2 (Word Formation):** Successfully outputs target letters/words in context (e.g. `cat`, `run`, `sun`).
- **Level 3 (Transfer):** Demonstrates lower cross-entropy on unfamiliar CVC words not directly in the prompt.

## Test Items
1. Prompt: `The cat can ` -> Target: `run`
2. Prompt: `The sun is ` -> Target: `hot`
3. Prompt: `a b c ` -> Target: `d`
4. Prompt: `A cat sat on a ` -> Target: `mat`
