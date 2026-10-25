---
title: "2026-10-24 Coverage Fix Experiment"
type: experiment
status: completed
scripts:
  - experiments/test_coverage_fix.py
tags:
  - ai-school
  - experiment
  - preschool
  - curriculum
  - coverage
created: 2026-10-24
updated: 2026-10-25
---
# 2026-10-24 Coverage Fix Experiment

## Question
Does adding coverage for missing transitions (like r,s,t,u) fix the generalization issues?

## Hypothesis
Adding exemplars that bridge coverage gaps will improve performance on held-out transitions.

## Variables and Conditions
- **Independent variable(s):** Training exemplar format/coverage
- **Measured outcome(s):** Best held-out greedy accuracy on 12 examples
- **Controls:** Same model size (27M), seed (123), iterations (30), learning rate
- **Conditions tested:**
  1. Original format from lesson
  2. Full coverage (all consecutive sequences)
  3. Mixed - original + targeted coverage additions

## Results

| Format | Best Acc | Notes |
| :-------- | :--------- | :------ |
| Original | 16.67% (2/12) | Baseline |
| Coverage Fixed (full) | 8.33% (1/12) | Worse - overfit to seeing everything? |
| Mixed Fixed | 41.67% (5/12) | Better - adding just key bridging sequences helps |

**Mixed Fixed failures:** 'g h i'->'j' got 't', 's t u'->'v' got 'u', 'i j k'->'l' got 's', etc.

## Interpretation

- **Just adding targeted coverage helps** - the mixed approach with a few bridging sequences improved from 16.67% to 41.67%
- **Too much coverage hurts** - full coverage of all sequences made it worse (8.33%). This suggests overfitting or the model gets confused
- **The r,s,t,u issue is partially addressed** - "p q r s t u", "q r s t u v" helped
- **Quality over quantity** - strategic additions to the curriculum are better than exhaustive coverage

## Recommendation
Update Lesson 1.1 to include a few bridging sequences like "p q r s t u", "q r s t u v", "r s t u v w" to fill coverage gaps without overwhelming the lesson. This is a data coverage fix, not a model size issue.

## Related
- [[2026-10-24 Stability Tracking Across Checkpoints]]
- [[2026-10-24 Comprehensive Diagnostic - Held-Out Expansion]]
