---
title: "2026-10-24 Generation Debug - Why Zero Accuracy"
type: experiment
status: completed
scripts:
  - experiments/debug_generation.py
  - experiments/debug_generation2.py
  - experiments/debug_generation3.py
  - experiments/debug_generation4.py
  - experiments/debug_generation5.py
  - experiments/debug_generation6.py
  - experiments/debug_generation7.py
  - experiments/debug_generation8.py
tags:
  - ai-school
  - experiment
  - preschool
  - generation
  - debugging
created: 2026-10-24
updated: 2026-10-25
---
# 2026-10-24 Generation Debug - Why Zero Accuracy

## Question
Why does the model show loss improvement but 0% generation accuracy?

## Findings

### Issue 1: Teacher-forced loss vs free generation are different
- Teacher-forced cross-entropy: model predicts next token given correct previous tokens
- Free generation: model predicts next token given its own previous predictions (autoregressive)
- These can diverge - model might know probabilities but not be stable in generation

### Issue 2: Training format matters
Testing different formats:
1. Training on full sequences like "a b c d e f g" (no special tokens) - model learns the pattern
2. When prompted with "g h i " and asked to generate 1 token, it predicts 'h' (following the cycle pattern it saw)
3. When we include the completion pattern in training differently, results vary

### Issue 3: The exemplar format in our test doesn't teach completion
Looking at how we structured exemplars:
```python
exemplars = [
    "a b c d e f g",      # full sequence
    "c d e f g h i",
    ...
    "a b c ",             # prefix only
    "f g h ",
    ...
]
```
The model sees prefixes but doesn't see explicit completions like "a b c d" as training examples in the form we tested. Or maybe it needs different structure.

Also in the actual lesson 1.1, it says:
```
2. Single-step completion:
   - `a b c ` -> `d`
   - `f g h ` -> `i`
```
But in our test we tried to adapt this. Maybe the format "a b c  d" (with spaces) or the arrow format needs to be used differently.

### Issue 4: Generation with special tokens
When using BOS/EOS (add_special_tokens=True like classroom does), generation is even worse/weirder.

## Recommendations

1. **Use greedy decoding for evaluation** - temperature 0.8 with multinomial sampling adds randomness. Try temperature near 0 or greedy.
2. **Match training and evaluation format exactly** - the way we prompt for generation must match how the model saw patterns during training.
3. **Check if the model is actually learning the right thing** - teacher-forced loss on the exact test format is what matters for the "loss delta" metric.
4. **For Lesson 1.1 style alphabet sequences, maybe train on full sequences and test differently** - or train on the completion pattern explicitly.

## Next Steps
- Fix the test harness to use better generation (greedy/low temperature)
- Verify loss calculation is correct
- Try training format that matches test format better
- Test with the exact exemplars from the lesson as written
