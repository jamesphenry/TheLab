---
title: "2026-10-24 Training Format Comparison - Rank Tracking"
type: experiment
status: completed
scripts:
  - experiments/track_rank.py
tags:
  - ai-school
  - experiment
  - preschool
  - training-formats
  - diagnosis
created: 2026-10-24
updated: 2026-10-25
---
# 2026-10-24 Training Format Comparison - Rank Tracking

## Question
Does the expected token (d) improve in rank/probability over training, or does training loss fall while this plateaus?

## Results (seed 123, tracking "a b c " -> "d")

### Full Sequences Format
Training on: `["a b c d e f g", "b c d e f g h", "c d e f g h i", "d e f g h i j", "e f g h i j k"]`

| Iter | exp_prob | rank | top_token |
| :-- | :-------- | :--- | :--------- |
| 0   | 0.000187 | 2602 | (random)   |
| 5   | 0.327121 | 1    | 'd' ✓      |
| 10  | 0.066972 | 3    | 'f'        |
| 15  | 0.017482 | 3    | 'e'        |
| 20  | 0.177904 | 2    | 'e'        |

### Prefix-Only Format
Training on: `["a b c ", "b c d ", "c d e ", "f g h ", "m n o "]`

| Iter | exp_prob | rank | top_token |
| :-- | :-------- | :--- | :--------- |
| 0   | 0.000187 | 2602 | (random)   |
| 5   | 0.098727 | 7    | 'c'        |
| 10  | 0.208790 | 2    | 'c'        |
| 15  | 0.270231 | 1    | 'd' ✓      |
| 20  | 0.061363 | 4    | 'c'        |

### Mixed Format
Training on: `["a b c d e f g", "c d e f g h i", "a b c ", "f g h "]`

| Iter | exp_prob | rank | top_token |
| :-- | :-------- | :--- | :--------- |
| 0   | 0.000187 | 2602 | (random)   |
| 5   | 0.132137 | 3    | 'h'        |
| 10  | 0.605586 | 1    | 'd' ✓      |
| 15  | 0.065227 | 2    | 'g'        |
| 20  | 0.063037 | 2    | 'g'        |

## Findings

1. **All formats can learn the pattern** - they all reach rank 1 at some point during training
2. **Unstable training** - Once learned, the model doesn't retain it stably. Rankings fluctuate (go back up). This explains high seed variance.
3. **Full sequences learn fastest** but are also most unstable
4. **Mixed format is relatively stable** - stays at rank 1 or 2
5. **Prefix-only is slower to learn** but eventually gets there

## Implications for AI School
- The student CAN acquire the capability, but it's not stable yet
- Loss decreasing overall might not mean this specific capability is retained
- We need to look at evaluation at the end (post-training) not just during training
- Seed variance is real - need multiple seeds
- For promotion, we need stable held-out performance, not just training loss reduction
- The curriculum as designed might need adjustment - full sequences might be better than just prefixes

## Recommendation
Before changing the curriculum, test with more stable training or longer training. Or use mixed format. The key is understanding that capability acquisition is real but unstable with current setup.
