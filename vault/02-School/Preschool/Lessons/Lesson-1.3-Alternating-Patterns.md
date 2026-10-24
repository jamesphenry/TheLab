---
title: "Lesson 1.3 — Alternating Patterns"
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

# Lesson 1.3 — Alternating Patterns

## Objective
Teach the model to complete repeating patterns — the simplest non-linear sequence type.

## Teaching Material & Exemplars
1. **Two-item alternation:**
   - `a b a b a b ` -> `a`
   - `x y x y x ` -> `y`
   - `1 2 1 2 1 ` -> `2`
   - `a 1 a 1 a ` -> `1`
2. **Three-item cycles:**
   - `a b c a b c a ` -> `b`
   - `1 2 3 1 2 3 ` -> `1`
   - `r s t r s ` -> `t`
3. **Growth patterns:**
   - `a aa aaa ` -> `aaaa`
   - `x xx ` -> `xxx`

## Practice Exercises
- Complete: `b c b c b ` -> `c`
- Complete: `5 6 5 6 5 ` -> `6`
- Complete: `a a a a ` -> `a`

## Notes
Alternating patterns test whether the model can learn periodicity, not just monotonic order. This is harder than forward sequences because the model must detect the cycle length. If the model struggles, fall back to two-item alternation only. Three-item cycles may be beyond the model's current capacity at 15 iterations.
