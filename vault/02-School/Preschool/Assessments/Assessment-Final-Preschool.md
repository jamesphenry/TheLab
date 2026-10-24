---
title: "Assessment — Final Preschool Comprehensive Exam"
type: assessment
status: active
tags:
  - ai-school
  - assessment
  - preschool
  - final
created: 2026-10-24
updated: 2026-10-24
---
# Assessment — Final Preschool Comprehensive Exam

## Purpose
Comprehensive test covering all four modules simultaneously. Tests retention across the full curriculum.

## Pass Criteria
- Post-training loss delta > +2.0 on held-out items (all modules combined)
- Generated text contains valid English letters, spaces, and punctuation on at least 50% of items
- Must pass all four module areas

## Rubric
- **Level 0 (Babble):** Output is random bytes or non-letter characters.
- **Level 1 (Format):** Output produces valid characters in expected form.
- **Level 2 (Competent):** Correct completion for most module types.
- **Level 3 (Mastery):** Correct completion across all module types on novel items.

## Test Items

### Module 1: Pattern Sequences
1. Prompt: `h i j k ` -> Target: `l` (held-out alphabet)
2. Prompt: `13 14 15 ` -> Target: `16` (held-out counting)
3. Prompt: `m n m n m ` -> Target: `n` (held-out alternating)

### Module 2: Word Associations
4. Prompt: `The deer is ` -> Target: `fast.` (held-out sight word)
5. Prompt: `The donkey says ` -> Target: `hee.`
6. Prompt: `The pear is ` -> Target: `green.` (held-out color)

### Module 3: Sentence Templates
7. Prompt: `The goat can ` -> Target: `run.` (held-out S-V)
8. Prompt: `The chick hid in the ` -> Target: `nest.` (held-out object)
9. Prompt: `The sand is ` -> Target: `hot.` (held-out adjective)

### Module 4: Chain Completion
10. Prompt: `The horse ran. The horse ate. The horse ` -> Target: `ran.` (held-out action chain)
11. Prompt: `6 7 8 9 10 ` -> Target: `11` (held-out counting chain)
12. Prompt: `The duck is white. The duck is small. The duck is ` -> Target: `wet.` (held-out description chain)

## Scoring
- All 12 items are held-out or novel combinations not seen in training
- Pass requires: avg loss delta > +2.0 across all items AND at least 6 of 12 items show positive delta
- Must demonstrate competence in all four modules
- Failure means repeat full preschool cycle with different exemplars
