---
title: "Assessment 4 — Chain Completion"
type: assessment
status: active
tags:
  - ai-school
  - assessment
  - preschool
  - chains
created: 2026-10-24
updated: 2026-10-24
---
# Assessment 4 — Chain Completion

## Purpose
Evaluate whether the model can complete step-by-step sequences where each step follows from the previous one.

## Pass Criteria
- Post-training loss delta > +2.0 on held-out items
- Generated text contains valid English letters, spaces, and punctuation on at least 50% of items

## Rubric
- **Level 0 (Babble):** Output is random bytes or non-letter characters.
- **Level 1 (Format):** Output produces valid characters in sequence form.
- **Level 2 (Chain):** Output continues the chain with a plausible next element.
- **Level 3 (Transfer):** Output continues a novel chain correctly (held-out).

## Test Items

### Action Chains (held-out sequences)
1. Prompt: `The rat ran. The rat ate. The rat ` -> Target: `ran.`
2. Prompt: `The bat flew. The bat ate. The bat ` -> Target: `flew.`
3. Prompt: `The lizard crawled. The lizard ate. The lizard ` -> Target: `crawled.` (held-out)

### Counting Chains (held-out)
4. Prompt: `4 5 6 7 ` -> Target: `8`
5. Prompt: `I see 4. I see 5. I see ` -> Target: `6.`
6. Prompt: `11 12 13 14 ` -> Target: `15` (held-out)

### Description Chains (held-out)
7. Prompt: `The bear is big. The bear is brown. The bear is ` -> Target: `slow.` (held-out)
8. Prompt: `The wolf is gray. The wolf is big. The wolf is ` -> Target: `fast.` (held-out)

## Scoring
- Items 1-2, 4-5: Training-adjacent (same pattern type, different content)
- Items 3, 6, 7, 8: Held-out (novel content)
- Pass requires: avg loss delta > +2.0 AND at least 2 held-out items show positive delta
