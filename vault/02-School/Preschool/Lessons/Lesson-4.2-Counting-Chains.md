---
title: "Lesson 4.2 — Counting Chains"
type: lesson
status: active
tags:
  - ai-school
  - lesson
  - preschool
  - chains
created: 2026-10-24
updated: 2026-10-24
---
# Lesson 4.2 — Counting Chains

## Objective
Teach the model to continue counting sequences across multi-step contexts.

## Teaching Material & Exemplars
1. **Sequential counting:**
   - `1 2 3 4 5 ` -> `6`
   - `2 3 4 5 6 ` -> `7`
   - `10 11 12 13 ` -> `14`
   - `5 6 7 8 9 ` -> `10`
   - `20 21 22 ` -> `23`

2. **Counting in context:**
   - `I have 1. I have 2. I have ` -> `3.`
   - `Count: 1 2 3 ` -> `4`
   - `Step 1. Step 2. Step ` -> `3.`
   - `One two three ` -> `four`
   - `First second third ` -> `fourth`

3. **Chain progression:**
   - `1 2 3 4 5 6 ` -> `7`
   - `A B C D ` -> `E`
   - `1 2 1 2 ` -> `1`
   - `10 20 30 ` -> `40`
   - `5 10 15 20 ` -> `25`

## Practice Exercises
- Complete: `3 4 5 6 ` -> `7`
- Complete: `I see 1. I see 2. I see ` -> `3.`
- Complete: `7 8 9 10 ` -> `11`

## Notes
Counting chains build on Lesson 1.2. The multi-step context helps reinforce the pattern. Both numeric and contextual forms are presented. Keep numbers in manageable ranges.
