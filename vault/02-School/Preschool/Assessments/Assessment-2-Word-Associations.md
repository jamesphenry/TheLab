---
title: "Assessment 2 — Word Associations"
type: assessment
status: active
tags:
  - ai-school
  - assessment
  - preschool
  - words
created: 2026-10-24
updated: 2026-10-24
---
# Assessment 2 — Word Associations

## Purpose
Evaluate whether the model can complete common word-pair associations in sentence contexts it has not seen before.

## Pass Criteria
- Post-training loss delta > +2.0 on held-out items
- Generated text contains valid English letters and punctuation on at least 50% of items

## Rubric
- **Level 0 (Babble):** Output is random bytes or non-letter characters.
- **Level 1 (Format):** Output produces valid words in the correct character class.
- **Level 2 (Association):** Output produces a reasonable word for the association.
- **Level 3 (Transfer):** Output produces the correct association word in a novel context (held-out).

## Test Items

### Sight Words (held-out subjects)
1. Prompt: `The bear is ` -> Target: `big.`
2. Prompt: `A frog is ` -> Target: `tiny.`
3. Prompt: `The wolf is ` -> Target: `fast.` (held-out)

### Animal Sounds (held-out animals)
4. Prompt: `The mouse says ` -> Target: `squeak.`
5. Prompt: `The bee says ` -> Target: `buzz.`
6. Prompt: `The cat says ` -> Target: `meow.` (held-out)

### Colors (held-out objects)
7. Prompt: `The tomato is ` -> Target: `red.` (held-out pattern)
8. Prompt: `The plum is ` -> Target: `purple.` (held-out pattern)

## Scoring
- Items 1-2, 4-5: Training-adjacent (same pattern type, different content)
- Items 3, 6, 7, 8: Held-out (novel content or novel pattern)
- Pass requires: avg loss delta > +2.0 AND at least 2 held-out items show positive delta
