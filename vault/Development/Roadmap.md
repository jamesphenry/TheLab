---
title: Roadmap
type: plan
status: active
tags:
  - ai-school
  - roadmap
  - plan
created: 2026-10-23
updated: 2026-10-25
---

# Roadmap — AI Learner Laboratory

## Phase 1: Core Foundation & BabyLM Architecture
- [x] Clean up obsolete repository scaffolding.
- [x] Establish AI School vault hierarchy and permission specifications.
- [x] Implement `VaultController` in Python with role-based permission enforcement and path isolation tests.
- [x] Formalize model sizing decision ([[Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001: 25M Tabula Rasa Architecture]]).
- [x] Implement PyTorch Causal Transformer learner model and byte-level tokenizer ([[Experiments/2026-10-23 BabyLM 25M Baseline Initialization|baseline implementation experiment]]).
- [ ] Implement Teacher Engine interface (for prompting curriculum lessons & grading).

## Phase 2: Early Childhood Curriculum & First Learning Cycle (Milestone 1)
- [ ] Stage 0: Phonics & Character Babbling (entropy collapse, whitespace/word boundaries).
- [ ] Stage 1: Vocabulary & Association (high-frequency nouns, colors, simple pairings).
- [ ] Stage 2: 1st-Grade Syntax & Dialog (Subject-Verb-Object, basic Q&A).
- [ ] Stage 3: Elementary Math & Logic (counting sequences, 1 + 1 = 2).
- [ ] Verify first live developmental improvement: *Unfamiliar word/syntax test -> Failure -> Interactive Teacher Correction -> Instant Weight Update -> Passing Retest*.

## Phase 3: Metacognition & Self-Directed Study
- [ ] Self-Assessment calibration metrics (comparing perceived confidence vs actual grade).
- [ ] Learner question-generation and proactive help-seeking.
- [ ] Experience logging and memory consolidation.

## Phase 4: Reflection & Long-Term Adaptation
- [ ] Idle period / "dream" reflection loop.
- [ ] A/B experimental comparisons across learner instances.
