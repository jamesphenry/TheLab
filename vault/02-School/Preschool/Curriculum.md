---
title: Preschool Curriculum
type: curriculum
status: active
tags:
  - ai-school
  - curriculum
  - preschool
created: 2026-10-24
updated: 2026-10-24
---

# Preschool Curriculum

## Overview

A four-module curriculum designed for a 25M parameter tabula rasa Transformer. Each module builds on the model's demonstrated ability to learn byte-level patterns and generalize to held-out items. The curriculum avoids rule-based instruction (which experiments show the model cannot learn) and focuses on pattern completion, sequence continuation, and template filling.

## Module 1: Pattern Sequences

**Goal:** The model can complete simple ordered sequences — alphabet, counting, and step-by-step patterns — including sequences it has never seen before.

- **Lesson 1.1:** Alphabet Sequences (`a b c ` → `d`)
- **Lesson 1.2:** Counting Sequences (`1 2 3 ` → `4`)
- **Lesson 1.3:** Alternating Patterns (`a b a b a ` → `b`)
- **Assessment:** Complete novel sequences (held-out letters, numbers, and patterns)

## Module 2: Word Associations

**Goal:** The model can complete common word-pair associations — sight words, animal sounds, colors — in sentence contexts it has not seen before.

- **Lesson 2.1:** Sight Word Completion (`The cat is ` → `big.`)
- **Lesson 2.2:** Animal Sounds (`The cow says ` → `moo.`)
- **Lesson 2.3:** Color Associations (`The apple is ` → `red.`)
- **Assessment:** Complete associations with novel subject words

## Module 3: Sentence Templates

**Goal:** The model can fill in blanks in simple SVO sentence templates using familiar vocabulary in rearranged contexts.

- **Lesson 3.1:** Subject-Verb Completion (`The dog can ` → `run.`)
- **Lesson 3.2:** Object Completion (`The cat sat on the ` → `mat.`)
- **Lesson 3.3:** Adjective Completion (`The sun is ` → `hot.`)
- **Assessment:** Complete templates with novel word combinations

## Module 4: Simple Chain-of-Thought

**Goal:** The model can complete step-by-step sequences where each step follows from the previous one, treating reasoning as sequential pattern completion rather than rule application.

- **Lesson 4.1:** Action Chains (`The cat sat. The cat ran. The cat ` → `sat.`)
- **Lesson 4.2:** Counting Chains (`1 2 3 4 5 ` → `6`)
- **Lesson 4.3:** Description Chains (`The cat is big. The cat is red. The cat is ` → `hot.`)
- **Assessment:** Complete novel multi-step sequences

## Graduation Requirements

To graduate from Preschool, the model must pass all four module assessments:

- **Pass threshold:** Post-training loss delta > +2.0 on held-out items (based on Experiment C mean of +4.63 with std 0.71, this is well within the model's demonstrated range).
- **Format compliance:** Generated text must produce valid English letters, spaces, and punctuation (not random bytes) on at least 50% of items.
- **Held-out requirement:** At least 2 items per assessment must be fully novel (not in training exemplars).
- **Retention test:** After all four modules, a comprehensive final exam tests items from all modules simultaneously. The model must maintain loss delta > +2.0 on this combined test.

## Retention Policy

If the model fails any module assessment:
1. The model is **held back** in that module.
2. Additional training iterations (remediation) are applied using the same exemplars.
3. The assessment is re-administered with different held-out items.
4. After 3 failed attempts, the module is flagged for human review.

If the model fails the comprehensive final:
1. The model repeats the full preschool cycle with all four modules.
2. The second cycle uses different exemplars and different held-out items.
3. After 2 failed comprehensive attempts, the model is held back and the curriculum is reviewed.

## What This Curriculum Does Not Attempt

Based on Experiments E, F, and G:
- **No rule instruction** — the model cannot learn `"dig ends with -ig"` as a rule.
- **No rationale generation** — the model cannot explain why a completion is correct.
- **No metacognitive self-assessment** — the model cannot evaluate its own confidence.
- **No transfer of rationale training** — adding explanations to training does not improve task performance.

These are deferred to future curriculum stages (Kindergarten+) where the model may have greater capacity through more training, larger architecture, or accumulated weights from prior modules.
