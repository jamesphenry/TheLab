---
title: "Assessment 3 — Sentence Templates"
type: assessment
status: active
tags:
  - ai-school
  - assessment
  - preschool
  - sentences
created: 2026-10-24
updated: 2026-10-24
---
# Assessment 3 — Sentence Templates

## Purpose
Evaluate whether the model can fill in blanks in simple sentence templates using familiar vocabulary in rearranged contexts.

## Pass Criteria
- Post-training loss delta > +2.0 on held-out items
- Generated text contains valid English words and punctuation on at least 50% of items

## Rubric
- **Level 0 (Babble):** Output is random bytes or non-letter characters.
- **Level 1 (Format):** Output produces valid words in appropriate form.
- **Level 2 (Template):** Output fills the template slot correctly with a plausible word.
- **Level 3 (Transfer):** Output fills the template correctly with appropriate word in novel combination (held-out).

## Test Items

### Subject-Verb (held-out combinations)
1. Prompt: `The fox can ` -> Target: `run.`
2. Prompt: `A bat can ` -> Target: `fly.`
3. Prompt: `The lizard can ` -> Target: `crawl.` (held-out)

### Object Completion (held-out combinations)
4. Prompt: `The mouse hid in the ` -> Target: `hole.`
5. Prompt: `The bird sat on a ` -> Target: `branch.`
6. Prompt: `The frog sat on the ` -> Target: `log.` (held-out)

### Adjective Completion (held-out combinations)
7. Prompt: `The rock is ` -> Target: `hard.` (held-out)
8. Prompt: `The pillow is ` -> Target: `soft.` (held-out)

## Scoring
- Items 1-2, 4-5: Training-adjacent (same pattern type, different content)
- Items 3, 6, 7, 8: Held-out (novel combinations)
- Pass requires: avg loss delta > +2.0 AND at least 2 held-out items show positive delta
