---
title: "2026-10-24 Generation Diagnosis - Steps 1 and 2"
type: experiment
status: completed
scripts:
  - experiments/diagnose_step1.py
  - experiments/diagnose_step2.py
tags:
  - ai-school
  - experiment
  - preschool
  - generation
  - diagnosis
created: 2026-10-24
updated: 2026-10-25
---
# 2026-10-24 Generation Diagnosis - Steps 1 and 2

## Step 1: Inspect Next-Token Probabilities

For prefix "a b c " expecting "d":
- Tokenized: [101, 36, 102, 36, 103, 36] -> ['a', ' ', 'b', ' ', 'c', ' ']
- Expected "d" tokenized: [104] -> ['d']
- **Expected token probability: 0.0973** (rank 3)

Top predictions:
1. 'c' (id=103): 0.2426
2. 'f' (id=106): 0.1485
3. 'd' (id=104): 0.0973 ← EXPECTED
4. 'w' (id=123): 0.0947
5. 'e' (id=105): 0.0917

**Finding:** The model does assign some probability to the expected token 'd', but it's not the highest. The most probable token is 'c' (repeating the last token). This suggests the model learned something different from what we intended.

## Step 2: Greedy Decoding

With greedy decoding (always pick highest prob):
- Greedy generated: 'a b c c f' → completion is 'c f' (wrong)
- Multinomial (temp=0.8): sometimes picks 'd' by chance

**Finding:** Greedy decoding confirms the model does not choose 'd' - it chooses 'c' first. The loss improvement we saw is real (teacher-forced evaluation), but the model hasn't learned the intended sequential pattern well enough to generate it correctly. It's learned some other pattern from the training data.

## Implications
- The failure is in **learning**, not evaluation/generation mechanism. The model needs better training data format or more training to learn the alphabet sequence pattern.
- Teacher-forced loss can improve even if the model doesn't learn the exact intended pattern.
- We need to look at how the exemplars are structured - maybe training on full sequences "a b c d" as continuous text helps more than fragments.
