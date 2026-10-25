---
title: "2026-10-24 Experiment C - Mixed Coverage Curriculum"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - preschool
  - lesson-1.1
  - experiment-c
created: 2026-10-24
updated: 2026-10-24
---
# 2026-10-24 Experiment C - Mixed Coverage Curriculum

## Question
Does targeted addition of bridging sequences improve performance?

## Hypothesis
Strategic coverage of problem areas will help without causing overfitting.

## Variables and Conditions
- **Independent variable(s):** Original + targeted bridging sequences
- **Measured outcome(s):** Best and final checkpoint accuracy on 12 held-out examples
- **Controls:** Same as Experiment A

## Exemplars
```python
["a b c d e f g", "c d e f g h i", "m n o p q r s", "t u v w x y z", "e f g h i j k", 
 "p q r s t u", "q r s t u v", "r s t u v w", "o p q r s t"]
```

## Results
- Mean Best: 41.67%
- Mean Final: 37.50%
- Best improvement over baseline

## Conclusion
Targeted coverage additions significantly improve performance. This is the best approach found.
