---
title: "2026-10-24 Model Size Comparison - Larger Model Test"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - model-size
  - scaling
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Model Size Comparison - Larger Model Test

## Question
Does doubling model size (from 27M to ~109M params) improve acquisition, generalization, and reliability on the alphabet sequence task?

## Hypothesis
Larger model capacity will lead to more stable learning and better generalization to held-out patterns.

## Variables and Conditions
- **Independent variable(s):** Model size (27M vs ~206M params)
- **Measured outcome(s):** Best held-out greedy accuracy, training stability, checkpoint gap
- **Controls:** Same training data, same evaluation set (12 examples), same seed (123), same training budget (30 iterations)
- **Environment / architecture:** BabyLM with dim 512/n_layers 8 vs dim 1024/n_layers 16
- **Elapsed time:** Small 58.6s, Large 335.1s (CPU)

## Procedure
1. Train small model (27M) with seed 123 for 30 iterations
2. Train large model (~206M) with same seed 123 for 30 iterations
3. Track best checkpoint accuracy on expanded held-out set
4. Record elapsed time for both

## Results

| Model | Parameters | Best Acc | Best Iter | Final Acc | Gap (best-final) | Time |
| :------ | :----------- | :--------- | :--------- | :--------- | :---------------- | :----- |
| Small | 27,411,456 | 25.00% (3/12) | 30 | 25.00% (3/12) | 0.00% | 58.6s |
| Large | 205,850,624 | 8.33% (1/12) | 5 | 8.33% (1/12) | 0.00% | 335.1s |

**Improvement in best accuracy: -16.67%** (worse)

## Interpretation

- **Larger model performed worse** under same training budget and learning rate
- **Both models showed stable checkpoints** (gap 0) in this run - different from previous run where small model had gap
- **More capacity didn't help** - suggests the issue isn't model capacity
- **Training budget may matter** - larger model needs more iterations or different learning rate to be effective
- **Supports prediction**: "the larger model may fit the training sequences more easily, but I'm not convinced it will solve the held-out generation problem by itself"

## Limitations
- Only tested one seed
- Same training budget (30 iterations) may not be equivalent for different model sizes
- Same learning rate for both models
- CPU-bound training

## Conclusion
- **Supported:** Larger model did not improve held-out generalization under same conditions
- **Not established:** Whether larger model would help with more training or different hyperparameters
- **Next experiment:** Try different learning rates for larger model, or more iterations. But the key point stands - increasing model size alone won't fix this issue.

## Related
- Previous: [[2026-10-24 Comprehensive Diagnostic - Held-Out Expansion]]
