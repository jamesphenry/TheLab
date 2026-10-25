---
title: "2026-10-24 Investigate r s t -> u Failure"
type: experiment
status: completed
scripts:
  - experiments/test_coverage_fix.py
  - experiments/track_stability.py
tags:
  - ai-school
  - experiment
  - preschool
  - diagnosis
  - failure-analysis
created: 2026-10-24
updated: 2026-10-25
---
# 2026-10-24 Investigate r s t -> u Failure

## Question
Why does "r s t -> u" fail persistently while other alphabet transitions learn?

## Findings
With full lesson exemplars ["a b c d e f g", "c d e f g h i", "m n o p q r s", "t u v w x y z", "e f g h i j k"]:
- Training coverage: 'r','s','t','u' appear in "m n o p q r s" and "t u v w x y z" 
- But when prompted with "r s t " expecting "u", the model predicts 'h','p','f' etc with rank ~20
- The model hasn't learned this specific transition

The issue is that in the training data, 'r','s' appear together in sequence but we don't see 'r','s','t','u' as a contiguous block in the exemplars. The exemplars go up to 's' in "m n o p q r s" and start at 't' in "t u v w x y z" - so the model sees "r s" followed by end of sequence, and sees "t u" at start of another sequence, but never sees the transition "r s t -> u" in context.

## Conclusion
This is a coverage issue - the training examples don't provide sufficient coverage of this specific transition. The curriculum needs to include exemplars that cover all the test patterns, or we need to understand that not all transitions will be learned equally.

But changing the curriculum now would be premature - we need to understand the full picture first.
