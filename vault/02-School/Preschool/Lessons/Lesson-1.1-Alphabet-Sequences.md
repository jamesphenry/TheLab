---
title: "Lesson 1.1 — Alphabet Sequences"
type: lesson
status: active
tags:
  - ai-school
  - lesson
  - preschool
  - patterns
created: 2026-10-24
updated: 2026-10-24
---

# Lesson 1.1 — Alphabet Sequences

## Objective
Teach the model to complete ordered alphabet sequences by presenting the pattern in multiple starting positions.

## Teaching Material & Exemplars
1. **Forward sequences (varied starts):**
   - `a b c d e f g`
   - `c d e f g h i`
   - `m n o p q r s`
   - `t u v w x y z`
   - `e f g h i j k`
   - `p q r s t u`
   - `q r s t u v`
   - `r s t u v w`
   - `o p q r s t`
2. **Single-step completion:**
   - `a b c ` -> `d`
   - `f g h ` -> `i`
   - `p q r ` -> `s`
   - `v w x ` -> `y`
3. **Backward sequences:**
   - `z y x w v u`
   - `z y x ` -> `w`
   - `m l k ` -> `j`

## Practice Exercises
- Complete: `h i j ` -> `k`
- Complete: `r s t ` -> `u`
- Complete: `d e f ` -> `g`

## Notes
The model learns byte-level order. The key is variety in starting position so the model learns the *pattern* (each letter is followed by the next) rather than memorizing a single starting point. Experiment A showed strong transfer to novel items when component patterns were seen in varied contexts.
