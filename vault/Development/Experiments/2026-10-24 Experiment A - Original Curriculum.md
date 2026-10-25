---
title: "2026-10-24 Experiment A - Original Curriculum"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - lesson-1.1
  - experiment-a
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Experiment A - Original Curriculum

## Question
What is the baseline performance of the original Lesson 1.1 curriculum?

## Hypothesis
The original curriculum will show some learning but may have coverage gaps.

## Variables and Conditions
- **Independent variable(s):** Original exemplar set
- **Measured outcome(s):** Best and final checkpoint accuracy on 12 held-out examples
- **Controls:** Seeds (42, 123, 7, 999), 30 iterations, lr=1e-3, model 27M

## Exemplars
```python
["a b c d e f g", "c d e f g h i", "m n o p q r s", "t u v w x y z", "e f g h i j k"]
```

## Results
- Mean Best: 25.00%
- Mean Final: 20.83%
- Per seed: 42(25%/25%), 123(16.67%/16.67%), 7(25%/16.67%), 999(33.33%/25%)

## Conclusion
Baseline performance established. Coverage gaps visible (especially r,s,t,u transitions).
