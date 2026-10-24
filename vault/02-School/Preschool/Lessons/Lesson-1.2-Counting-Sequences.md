---
title: "Lesson 1.2 — Counting Sequences"
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

# Lesson 1.2 — Counting Sequences

## Objective
Teach the model to complete numeric sequences using the same pattern-completion approach as alphabet sequences.

## Teaching Material & Exemplars
1. **Forward counting (varied starts):**
   - `1 2 3 4 5 6`
   - `3 4 5 6 7 8`
   - `7 8 9 10 11 12`
   - `10 11 12 13 14 15`
   - `5 6 7 8 9 10`
2. **Single-step completion:**
   - `1 2 3 ` -> `4`
   - `4 5 6 ` -> `7`
   - `8 9 10 ` -> `11`
   - `12 13 14 ` -> `15`
3. **Skip counting:**
   - `2 4 6 8 ` -> `10`
   - `5 10 15 ` -> `20`
   - `10 20 30 ` -> `40`

## Practice Exercises
- Complete: `6 7 8 ` -> `9`
- Complete: `14 15 16 ` -> `17`
- Complete: `3 6 9 ` -> `12`

## Notes
Multi-digit numbers (10+) are multiple bytes each. The model must learn byte-level patterns within numbers (e.g. `1` then `0` for `10`). Start with single digits and gradually introduce two-digit numbers. Skip counting introduces a secondary pattern (the step size) that may be harder — use as stretch material.
