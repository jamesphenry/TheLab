---
title: "2026-10-24 Curriculum Promotion - Mixed Coverage"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - curriculum-promotion
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Curriculum Promotion - Mixed Coverage

## Decision
Promoted Mixed Fixed coverage format to be the standard for Lesson 1.1.

## Evidence Summary
- **Single seed test:** Mixed Fixed achieved 41.67% vs Original 16.67%
- **Multi-seed validation (4 seeds):** Mixed Fixed mean best = 41.67%, Original mean best = 25.00%
- **Consistency:** Mixed Fixed showed better consistency across seeds (33-50%) vs Original (17-33%)
- **Full coverage worse:** 18.75% mean best, confirms overfitting issue

## Changes Made
1. Updated Lesson 1.1 with targeted bridging sequences
2. Created ADR-0002 documenting the decision
3. Updated Curriculum.md to include best-checkpoint evaluation protocol
4. All evidence documented in experiments

## Next Research Questions

Based on results, new questions emerge:
1. **Can we apply similar targeted coverage principles to other lessons?** (Counting, Alternating patterns)
2. **Does checkpoint selection strategy need refinement?** We need better held-out sets for checkpoint selection
3. **Why does full coverage hurt?** Understanding the optimization dynamics better
4. **Can we improve the mixed format further?** Which specific bridging sequences contribute most?
5. **How to make training more stable?** The gap between best/final suggests instability remains

## Next Experiment
Test the updated Lesson 1.1 (with mixed coverage) in the full preschool harness to see if it passes the actual assessment criteria.
