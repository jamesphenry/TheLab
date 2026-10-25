---
title: "2026-10-24 Experiment B - Full Coverage Curriculum"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - lesson-1.1
  - experiment-b
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Experiment B - Full Coverage Curriculum

## Question
Does exhaustive coverage of all consecutive alphabet sequences improve performance?

## Hypothesis
More complete coverage will help the model learn all transitions.

## Variables and Conditions
- **Independent variable(s):** All consecutive sequences from a-z
- **Measured outcome(s):** Best and final checkpoint accuracy on 12 held-out examples
- **Controls:** Same as Experiment A

## Exemplars
20 consecutive sequences covering all positions.

## Results
- Mean Best: 18.75%
- Mean Final: 12.50%
- Worse than original

## Conclusion
Exhaustive coverage hurts performance - likely due to overfitting or optimization issues. More data isn't always better.
