---
title: "Assessment 1 — Pattern Sequences"
type: assessment
status: active
tags:
  - ai-school
  - assessment
  - preschool
  - patterns
created: 2026-10-24
updated: 2026-10-24
---

# Assessment 1 — Pattern Sequences

## Purpose
Evaluate whether the model can complete ordered sequences on items it has never seen before.

## Pass Criteria
- Post-training loss delta > +2.0 on held-out items
- Generated text contains valid letters/digits (not random bytes) on at least 50% of items

## Rubric
- **Level 0 (Babble):** Output is random bytes or non-letter characters.
- **Level 1 (Format):** Output produces valid letters or digits in the correct character class.
- **Level 2 (Sequence):** Output produces the correct next element in a seen-pattern context.
- **Level 3 (Transfer):** Output produces the correct next element in a novel-pattern context (held-out).

## Test Items

### Alphabet (held-out starting positions)
1. Prompt: `g h i ` -> Target: `j`
2. Prompt: `n o p ` -> Target: `q`
3. Prompt: `s t u ` -> Target: `v` (held-out)

### Counting (held-out starting positions)
4. Prompt: `2 3 4 ` -> Target: `5`
5. Prompt: `9 10 11 ` -> Target: `12`
6. Prompt: `15 16 17 ` -> Target: `18` (held-out)

### Alternating (held-out patterns)
7. Prompt: `c d c d c ` -> Target: `d` (held-out pattern)
8. Prompt: `4 5 4 5 4 ` -> Target: `5` (held-out pattern)

## Scoring
- Items 1-2, 4-5: Training-adjacent (same pattern type, different content)
- Items 3, 6, 7, 8: Held-out (novel content or novel pattern)
- Pass requires: avg loss delta > +2.0 AND at least 2 held-out items show positive delta
