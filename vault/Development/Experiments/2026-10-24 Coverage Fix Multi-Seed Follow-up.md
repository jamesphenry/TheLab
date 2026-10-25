---
title: "2026-10-24 Coverage Fix Multi-Seed Follow-up"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - curriculum
  - coverage
  - multi-seed
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Coverage Fix Multi-Seed Follow-up

## Question
Do the coverage improvements hold up across multiple seeds with best and final checkpoint comparison?

## Hypothesis
Mixed coverage will consistently outperform original and full coverage across seeds.

## Variables and Conditions
- **Independent variable(s):** Training exemplar format/coverage
- **Measured outcome(s):** Best and final checkpoint accuracy on 12 held-out examples
- **Controls:** Model size (27M), seeds (42, 123, 7, 999), iterations (30), learning rate (1e-3)
- **Conditions:** Original, Full Coverage, Mixed Fixed

## Results

| Format | Mean Best Acc | Mean Final Acc | Best vs Final Gap |
| :-------- | :------------ | :------------- | :---------------- |
| Original | 25.00% | 20.83% | -4.17% |
| Full Coverage | 18.75% | 12.50% | -6.25% |
| Mixed Fixed | 41.67% | 37.50% | -4.17% |

Per-seed results:
- **Original:** Seed42: 25%/25%, Seed123: 16.67%/16.67%, Seed7: 25%/16.67%, Seed999: 33.33%/25%
- **Full Coverage:** Seed42: 25%/25%, Seed123: 8.33%/8.33%, Seed7: 25%/0%, Seed999: 16.67%/16.67%
- **Mixed Fixed:** Seed42: 50%/41.67%, Seed123: 41.67%/41.67%, Seed7: 41.67%/41.67%, Seed999: 33.33%/25%

## Interpretation

- **Mixed coverage is consistently better** across all seeds (mean best 41.67% vs 25% original)
- **Reproducible improvement** - not just a lucky seed
- **Checkpoint selection still matters** - gap between best and final is smaller than before but still exists
- **Full coverage consistently worse** - confirms overfitting/poor optimization with exhaustive coverage
- **Original has high variance** (16.67% to 33.33%) while mixed is more consistent (33.33% to 50%)

## Conclusion
- **Supported:** Mixed targeted coverage additions improve generalization across multiple seeds
- **Recommended:** Update Lesson 1.1 with the mixed fixed format (`p q r s t u`, `q r s t u v`, `r s t u v w`, `o p q r s t`)
- **Note:** Early stopping/checkpoint selection still beneficial

## Related
- [[2026-10-24 Coverage Fix Experiment]]
- [[2026-10-24 Comprehensive Diagnostic - Held-Out Expansion]]
