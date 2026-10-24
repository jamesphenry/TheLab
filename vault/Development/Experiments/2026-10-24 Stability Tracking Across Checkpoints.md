---
title: "2026-10-24 Stability Tracking Across Checkpoints"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - stability
  - checkpoints
created: 2026-10-24
updated: 2026-10-24
---

# 2026-10-24 Stability Tracking Across Checkpoints

## Question
Does the instability persist when evaluating the same fixed probe set after every training checkpoint?

## Hypothesis
The model can learn the pattern (acquisition) but fails to retain it reliably (retention) across training iterations, leading to unstable performance.

## Variables and Conditions
- **Independent variable(s):** Training iteration count
- **Measured outcome(s):** Target token rank and probability on fixed probes, held-out greedy accuracy, training loss
- **Controls:** Same probe prefixes, same tokenizer/evaluation, same training config, fixed seed per run
- **Environment / architecture:** BabyLM 25M, 8 layers, 512 dim
- **Code:** experiments/track_stability.py

## Procedure
1. Initialize fresh model with fixed seed
2. Train on exemplars that never include probe prefixes
3. At each checkpoint (every iteration), evaluate fixed probe set for target token rank/prob
4. Evaluate held-out probes with greedy decoding
5. Track training loss
6. Repeat for multiple seeds

## Results

### Seed 42
| Iter | Train Loss | Held-out Acc | a b c->d (r, p) | f g h->i (r, p) | h i j->k (r, p) | r s t->u (r, p) |
| :-- | :---------- | :----------- | :-------------- | :-------------- | :-------------- | :-------------- |
| 0   | 7.8044      | 0.00%        | r180 (0.000)    | r3446 (0.000)   | r1567 (0.000)   | r805 (0.000)    |
| 5   | 1.2203      | 0.00%        | r7 (0.070)      | r3 (0.105)      | r9 (0.031)      | r1517 (0.000)   |
| 10  | 0.9080      | 0.00%        | r4 (0.147)      | r1 (0.243)      | r6 (0.064)      | r1476 (0.000)   |
| 13  | 0.9231      | 0.00%        | r1 (0.288)      | r3 (0.134)      | r6 (0.055)      | r1426 (0.000)   |
| 15  | 0.8269      | 0.00%        | r1 (0.391)      | r1 (0.230)      | r5 (0.073)      | r1549 (0.000)   |
| 17  | 0.7092      | 25.00%       | r2 (0.311)      | r1 (0.295)      | r4 (0.148)      | r1843 (0.000)   |
| 20  | 0.8330      | 0.00%        | r1 (0.475)      | r1 (0.487)      | r6 (0.052)      | r1345 (0.000)   |
| 21  | 1.0965      | 25.00%       | r3 (0.234)      | r1 (0.300)      | r1 (0.264)      | r1280 (0.000)   |
| 23  | 0.6391      | 0.00%        | r1 (0.489)      | r4 (0.138)      | r1 (0.328)      | r543 (0.000)    |
| 25  | 0.5256      | 25.00%       | r1 (0.621)      | r1 (0.367)      | r1 (0.484)      | r1323 (0.000)   |

### Seed 123
| Iter | Train Loss | Held-out Acc | a b c->d (r, p) | f g h->i (r, p) | h i j->k (r, p) | r s t->u (r, p) |
| :-- | :---------- | :----------- | :-------------- | :-------------- | :-------------- | :-------------- |
| 0   | 8.3353      | 0.00%        | r2602 (0.000)   | r3934 (0.000)   | r3475 (0.000)   | r1504 (0.000)   |
| 11  | 0.7955      | 0.00%        | r1 (0.347)      | r4 (0.119)      | r13 (0.024)     | r3135 (0.000)   |
| 13  | 0.8682      | 0.00%        | r2 (0.236)      | r3 (0.194)      | r10 (0.058)     | r2432 (0.000)   |
| 18  | 0.8292      | 25.00%       | r2 (0.305)      | r1 (0.543)      | r10 (0.012)     | r2974 (0.000)   |
| 23  | 0.6113      | 25.00%       | r1 (0.536)      | r1 (0.515)      | r8 (0.066)      | r2498 (0.000)   |
| 25  | 0.4577      | 0.00%        | r1 (0.581)      | r2 (0.226)      | r5 (0.007)      | r2318 (0.000)   |

## Interpretation
- **Acquisition:** Yes - targets do reach rank 1 with high probability on many probes
- **Retention:** No, not reliably - rank/probability fluctuate wildly across iterations. Sometimes rank 1, sometimes rank 2-10
- **Generalization:** Partial - held-out greedy accuracy is sporadic (0% or 25%). Sometimes works, often doesn't
- **Instability is real** across multiple seeds

The pattern "r s t -> u" never learns (stays at very high rank) - suggesting some patterns are harder or the model doesn't generalize the rule.

## Limitations
- Small probe set
- Only tested one training format
- Greedy decoding may be harsh

## Conclusion
- **Supported:** The model can acquire the capability temporarily
- **Not established:** Stable retention or reliable generalization
- **Next experiment:** Try different optimizers/learning rates, more stable training (lower LR, more iterations with patience), or test if early stopping at peak performance helps. Also test if mixed training format is more stable.

## Related
- Experiments: track_rank.py, test_lesson11_proper.py
