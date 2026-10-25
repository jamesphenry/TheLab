---
title: AI School Vault Maintenance Guide
type: procedure
status: active
tags:
  - ai-school
  - vault
  - maintenance
created: 2026-10-25
updated: 2026-10-25
---

# AI School Vault Maintenance Guide

Use this routine when adding experiments, sessions, decisions, or reports.

## Before creating a note

1. Read [[Documentation Standard]] and the closest existing example/template.
2. Search by title, date, topic, and experiment identifier to avoid duplicate notes or indexes.
3. Decide whether the note is a protocol, an actual run record, an interpretation, a decision, a session log, or a synthesis. Keep these roles distinct.

## Recording an experiment

1. Start with [[Templates/Experiment Template|Experiment Template]]. Record the question and hypothesis before running when possible.
2. Add repository-relative runner paths to the `scripts` frontmatter property. Use an empty list when no dedicated runner is known; do not infer that a supporting test reproduces a historical run.
3. When substantively revising a planned protocol, update `updated` and append a dated `{date, change}` entry to its `changelog` frontmatter list. Preserve earlier entries.
4. Record the exact conditions, data/examples, train/validation/test split, model configuration, seed, code revision, environment, decoding, and checkpoint-selection rule.
5. Preserve raw output and artifacts with repository-relative references. If artifacts are unavailable, say so.
6. Report measured loss and generated-answer accuracy separately. Include per-item results and failures; do not call items held out if their targets or relations were trained.
7. Separate observations, interpretation, limitations, and conclusions. Add follow-up runs as new records.
8. Link the note to the lesson/assessment, supporting code/artifacts, and relevant earlier or follow-up experiments. Add it once to [[Development/Experiments/Experiments Index|Experiments Index]].

## Recording a decision or report

- Use the ADR template for an adopted or proposed choice. Link the evidence and define what would prompt review.
- Use [[Templates/Research Audit Template|Research Audit Template]] for a synthesis across records. State its date and scope, identify missing sources, and preserve earlier reports.
- Add a completed report to [[07-Reports/Reports Index|Reports Index]] once. Link navigation from [[Home|Home]] through that index.

## Reviewing and maintaining the vault

- Check wiki links and update affected indexes when a note is added or renamed.
- Prefer targeted edits to stable navigation and live guidance. Preserve completed results and meaningful historical wording.
- Do not use an index as a second copy of experiment results. Fix a stale index entry by linking to the canonical record.
- When newer evidence conflicts with an active lesson, assessment, self-assessment, or teacher profile, log the conflict and request/review the substantive change rather than silently rewriting the scientific claim.
- Before finishing, verify frontmatter, destination, links, exactly-once index entry, and that unrelated files remain untouched.
