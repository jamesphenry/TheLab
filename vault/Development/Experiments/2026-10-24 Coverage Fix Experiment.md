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

- **Mixed coverage performed best in this run.** It achieved 41.67% probe accuracy (5/12), compared with 16.67% (2/12) for the original curriculum and 8.33% (1/12) for full coverage.
- **Exhaustive coverage did not guarantee better performance.** The full-coverage condition performed worst under the tested seed and training budget. The cause is not yet established; possible explanations include optimization behavior, initialization variability, or differences in the effective training distribution.
- **Targeted additions are promising.** Adding overlapping sequences around the `p`–`w` region coincided with improved probe accuracy. This does not yet establish that the additions specifically resolved the `r,s,t,u` coverage issue.
- **Generalization remains unconfirmed.** Some evaluation contexts or transitions overlap with training examples. A separate evaluation set containing genuinely unseen contexts is needed to measure generalization more directly.
- **Checkpoint selection matters.** These results report best-checkpoint accuracy. Final-checkpoint accuracy and performance across multiple random seeds should also be compared.

## Recommendation

Retain Mixed Fixed as the leading candidate for the next experiment, but do not yet replace Lesson 1.1's curriculum.

Repeat all three conditions across multiple seeds with the same training budget, then compare mean and variability in probe accuracy. Include final-checkpoint performance and a separate evaluation set with unseen contexts.

If mixed coverage consistently outperforms both alternatives, adopt it as the preferred curriculum and investigate which targeted additions contribute most to the improvement.

**Current conclusion:** Targeted coverage additions are promising, but the mechanism and reproducibility of the improvement remain open questions.

## Related
- [[2026-10-24 Stability Tracking Across Checkpoints]]
- [[2026-10-24 Comprehensive Diagnostic - Held-Out Expansion]]
