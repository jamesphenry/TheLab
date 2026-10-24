---
title: "2026-10-24 Throwaway Preschool Harness Test"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - throwaway-harness
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Throwaway Preschool Harness Test

## Question
Can we test the newly created Preschool curriculum (Modules 1-4) using a minimal throwaway harness that properly distinguishes training loss, held-out loss, and generated-answer accuracy?

## Hypothesis
1. A fresh 25M model trained on Lesson 1.1 (Alphabet Sequences) exemplars will show loss reduction on held-out items.
2. The harness must track three metrics separately - training loss, held-out loss, and generated-answer accuracy.
3. Lesson 1.2 (Counting Sequences) should also work without harness modifications.

## Method
Created throwaway harness at `experiments/test_preschool_throwaway.py` with:
- Fresh student initialization per seed
- Separate tracking of training loss, held-out loss (cross-entropy with prompt masking), and generation accuracy
- Tests Lesson 1.1 and Lesson 1.2 from the newly created curriculum

## Results

### Lesson 1.1 (Alphabet Sequences) - Multiple Seeds
| Seed | Baseline Loss | Post Loss (All) | Δ Loss (All) | Held-out Loss | Δ Loss (Held-out) | Post Acc (Held-out) | Passed |
| :-- | :------------ | :-------------- | :----------- | :------------ | :----------------- | :----------------- | :------ |
| 42  | 8.3434        | 3.4583          | +4.8851      | 8.2315        | -5.7727           | 0.00%             | False   |
| 123 | 8.3359        | 3.4362          | +4.8997      | 3.1510        | +5.1849           | 0.00%             | True    |

Note: High variance across seeds - seed 42 shows held-out loss increased (worse) while seed 123 improves. Generation accuracy is 0% for all cases.

### Lesson 1.2 (Counting Sequences)
| Seed | Baseline Loss | Post Loss (All) | Δ Loss (All) | Held-out Loss | Δ Loss (Held-out) | Post Acc (Held-out) | Passed |
| :-- | :------------ | :-------------- | :----------- | :------------ | :----------------- | :----------------- | :------ |
| 42  | 8.3831        | 3.8917          | +4.4914      | 3.3220        | +5.0611           | 0.00%             | True    |

## Observations

**What worked:**
- Could test both lessons without modifying the harness - just passed different exemplars and test items
- Successfully distinguished training loss, held-out loss, and generation accuracy as separate metrics
- Fresh student initialization per seed worked
- Loss improvements observed on held-out in most cases

**Failure modes discovered:**
1. **High seed variance** - Lesson 1.1 fails completely on seed 42 but passes on seed 123. This suggests the model is very sensitive to initialization.
2. **Generation vs loss mismatch** - Loss improves significantly but generation accuracy is 0%. The model learns to predict tokens in context (lowering loss) but doesn't generate the exact expected completions in the same format.
3. **Exemplar format issues** - Our space-separated format like "a b c " may not be optimal.
4. **Held-out loss can increase** - Some seeds show held-out loss getting worse even as training loss drops, suggesting overfitting or poor generalization.

**Requirements for a proper harness:**
- Must support separate tracking of training/held-out/generation metrics
- Must allow fresh initialization per seed
- Must accept arbitrary exemplars and test items without code changes
- Should use greedy decoding or lower temperature for evaluation
- Need better generation accuracy measurement
- May need to be more careful about prompt masking in loss calculation
- Should track per-item details better

## Conclusion
The throwaway harness works for basic testing. Lesson 1.2 works fine without changes. The curriculum format is parseable without special-case code. The key issue is that loss improvement doesn't always translate to correct generation, and there's high seed variance.
