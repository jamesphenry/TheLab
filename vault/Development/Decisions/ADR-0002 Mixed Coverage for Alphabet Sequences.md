---
title: "ADR-0002: Mixed Coverage for Alphabet Sequences"
type: decision
status: accepted
tags:
  - ai-school
  - decision
  - curriculum
  - preschool
created: 2026-10-24
updated: 2026-10-24
---
# ADR-0002: Mixed Coverage for Alphabet Sequences

## Status
Accepted

## Context
Our experiments showed that:
1. Original Lesson 1.1 had coverage gaps causing poor generalization (mean best 25% across seeds)
2. Adding full coverage hurt performance (mean best 18.75%)
3. Adding targeted bridging sequences improved performance significantly (mean best 41.67%)
4. Improvements were consistent across 4 seeds (42, 123, 7, 999)

The model needs to see transitions like r,s,t,u but exhaustive coverage causes overfitting. Targeted additions that bridge gaps work better.

## Decision
Update Lesson 1.1 to use mixed coverage format with targeted bridging sequences: `p q r s t u`, `q r s t u v`, `r s t u v w`, `o p q r s t`

## Consequences
- Better generalization to held-out alphabet sequences
- More stable performance across seeds
- Lesson still follows pattern-completion approach (no rules)
- Checkpoint selection still important
- Sets precedent for evidence-based curriculum changes

## Evidence
- [[2026-10-24 Coverage Fix Experiment]]
- [[2026-10-24 Coverage Fix Multi-Seed Follow-up]]
