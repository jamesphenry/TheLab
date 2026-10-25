---
title: "2026-10-24 Comprehensive Diagnostic - Held-Out Expansion"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - held-out
  - generalization
  - checkpoints
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Comprehensive Diagnostic - Held-Out Expansion

## Question
With expanded held-out set and checkpoint tracking, can we better understand generalization and reliability?

## Method
- Expanded held-out set from 4 to 12 examples
- Tracked performance every iteration for 30 iterations
- Saved best checkpoint, compared with final checkpoint
- Evaluated all tokens (not just first) for greedy accuracy
- Seed 123

## Results

| Checkpoint | Held-out Loss | Greedy Acc | Notes |
| :----------- | :------------ | :---------- | :------ |
| Iter 0 | 8.5721 | 0.00% (0/12) | Random |
| Iter 29 (best) | 4.9930 | 41.67% (5/12) | Peak performance |
| Iter 30 (final) | 4.9549 | 25.00% (3/12) | Degraded from best |

## Detailed Results at Best Checkpoint (iter 29)
✓ 'g h i ' -> 'j' (correct)
✓ 'n o p ' -> 'q' (correct)  
✗ 's t u ' -> 'v' got 'q'
✗ 'p q r ' -> 's' got 'r'
✓ 'e f g ' -> 'h' (correct)
✗ 'i j k ' -> 'l' got 'i'
✗ 'j k l ' -> 'm' got 'i'
✓ 'o p q ' -> 'r' (correct)
✓ 'd e f ' -> 'g' (correct)
✗ 'k l m ' -> 'n' got 'i'
✗ 'h i j ' -> 'k' got 'i'
✗ 't u v ' -> 'w' got 'r'

## Key Findings

1. **Expanded held-out reveals real picture** - With 4 examples we saw 25% increments (misleading). With 12 examples we see 41% is the best, not amazing.
2. **Early stopping helps** - Best checkpoint (iter 29) gets 41.67%, final checkpoint only 25%. This confirms saving best checkpoint is important.
3. **Loss doesn't predict accuracy** - Held-out loss improved overall but accuracy fluctuates. Loss can go down while generation gets worse.
4. **Pattern emerges** - The model does better on some sequences (g h i, n o p, e f g, o p q, d e f) but fails on others. It often predicts 'i' or 'r' or 'q' - seems stuck in certain patterns.
5. **The 'r s t -> u' issue extends** - 's t u' fails (and also 't u v'). The model struggles with transitions near the end of alphabet ranges seen in training.
6. **Training examples matter** - "t u v w x y z" is in training, but "r s t -> u" and "s t u -> v" fail. "m n o p q r s" ends at 's', so seeing "s t u" as a prefix wasn't well-represented.

## Implications for AI School

This confirms the three-stage evaluation:
- **Acquisition:** Model can learn on some probes (reaches 41% with best checkpoint)
- **Generalization:** Limited - only works on ~5/12 unseen examples
- **Reliability:** Poor - needs checkpoint selection, performance varies wildly

## Recommendations
1. **Use early stopping** based on held-out performance
2. **Expand evaluation sets** - 4 examples is too coarse
3. **Don't just look at loss** - need generation accuracy
4. **Before changing curriculum**, we need to understand if different training formats give more stable generalization
5. **The "r s t -> u" failure is due to coverage** in training exemplars - curriculum might need adjustment, but this needs more investigation
