---
title: Agent Instructions — AI Learner Laboratory
type: instructions
status: active
tags:
  - ai-school
  - agent-guidelines
created: 2026-10-23
updated: 2026-10-25
---

# Agent Instructions — AI Learner Laboratory

## 1. Mission
Help develop and run the **AI Learner Laboratory (AI School)**. Maintain a trustworthy, navigable Obsidian record of its architecture, lessons, experiment history, and findings.

The codebase and the vault serve complementary roles:
- **The Harness Code (`harness/`):** Authoritative for execution, permissions enforcement, LLM calling, and tool sandboxing.
- **The Obsidian Vault (`vault/`):** Authoritative for the environment, curricula, rubrics, student notes, and experimental logs.

## 2. Working Rules & Principles
- **Separation of Knowledge:**
  1. *Model capability* (initialization and acquired model parameters)
  2. *Retrievable external memory* (vault notes)
  3. *Self-assessment* (metacognition)
- **Technical Permissions:** Always enforce folder boundaries in code; never rely solely on prompting models not to read or edit files outside their purview.
- **Evidence Standard:** In `Development/Experiments/` and `07-Reports/`, distinguish **Hypothesis**, **Method**, **Observed**, **Measured**, **Inferred**, **Conclusion**, and **Proposal**. Retain exact conditions, scoring rules, per-item outputs, failures, and artifact references where available.
- **Non-destructive:** Never delete notes or logs without confirmation.

## 3. Vault Organization
- `00-System/`: Technical rules, permissions, schedules, documentation standards, and vault operating guides.
- `01-Learner/`: Learner goals, self-assessment, questions.
- `02-School/`: Curricula, lessons, assignments, assessments organized by subject.
- `03-Experiences/`: Session logs and narrative interactions.
- `04-Memory/`: Extracted knowledge, rules, and synthesis notes.
- `05-Dreams/`: Idle-time reflection, hypotheses, and association logs.
- `06-Labs/`: Practical problem sets and experiment sandboxes.
- `07-Reports/`: Finalized assessment evaluations, grades, progression reports, and dated research syntheses.
- `Development/`: Technical documentation, decisions, debugging notes, session logs, and experiment records.
- `Development/Experiments/`: Canonical human-readable experiment records and [[Development/Experiments/Experiments Index|their index]]. Runner code and selected JSON outputs are in repository-root `experiments/`.
- `Templates/`: Reusable note templates.

## 4. Experiment Lifecycle

Follow this sequence for every experiment. Use [[Templates/Experiment Template|Experiment Template]] and the detailed [[00-System/Documentation Standard|Documentation Standard]]. Do not treat a completed run as proof that its hypothesis was supported.

### A. Plan before running

1. Search the canonical [[Development/Experiments/Experiments Index|Experiments Index]] and nearby notes to avoid duplicate experiments and to identify prior results.
2. Create a dated experiment note with `status: planned`. State one answerable question and a falsifiable hypothesis before observing outcomes.
3. Specify the intervention, comparison/control conditions, model/configuration, training data, procedure, planned seeds and run count, metrics, decoding, and stopping rule.
4. Define the evaluation split before training. List train, validation, and final test items. Check whether exact strings, targets, relations, or relevant contexts overlap. A new prompt context alone does not make a target or rule held out.
5. Reserve the final test from training, curriculum changes, and checkpoint selection. If a checkpoint is selected on validation performance, use a separate untouched final test.
6. Plan controls that can distinguish the target explanation from alternatives (for example, no-update and matched-data controls). For seed-sensitive claims, predeclare multiple seeds and report each one.

### B. Run and preserve provenance

1. Before execution, record the repository commit/revision and working-tree changes. Record the exact code/configuration paths, environment and package versions, data/exemplar version, seed, and run identifier.
2. Change only the planned variables. If the protocol, data, metric, or test set changes, document the deviation and create a new protocol/version where the change affects interpretation.
3. Save raw outputs and checkpoints when available. Link repository-relative paths; if artifacts cannot be saved or recovered, state that explicitly.
4. Record every run, including failed, negative, unstable, or inconclusive runs. Do not report only the best seed or best checkpoint without the full selection procedure and all relevant outcomes.
5. Do not launch training or modify datasets as part of a documentation task. Run experiments only when the task explicitly authorizes execution.

### C. Analyze and report

1. Separate **Observed** behavior from **Measured** metrics, **Inferred** explanations, and untested **Hypotheses**.
2. Report teacher-forced loss separately from exact generation accuracy and other task metrics. Include per-item results, aggregate statistics, seed-level results, and representative generations.
3. Compare results with the baseline and controls. State what the design can and cannot establish; discuss leakage, alternative explanations, variability, and measurement limits.
4. Complete the conclusion with **Supported**, **Not established**, and the **Next experiment**. A loss reduction, response-format match, or fluent-looking output is not by itself evidence of transfer or underlying reasoning.
5. Set the record status to `completed` when the record is complete, regardless of whether the hypothesis was supported. Add the note once to the canonical experiment index and link related lessons, assessments, scripts, artifacts, and follow-ups.

### D. Preserve the record

- Do not rewrite completed results to fit a later interpretation. Add a new run, dated correction, follow-up experiment, or audit and link it to the earlier record.
- For a substantive revision to a planned experiment or research plan, update `updated` and append a dated `{date, change}` entry to `changelog` frontmatter. Preserve earlier entries so reviewers can see why the protocol changed.
- Keep protocol, execution record, analysis, decision, and cross-study report distinguishable. An accepted ADR or active curriculum does not replace the underlying evidence.
- If new evidence conflicts with a live curriculum, assessment, teacher profile, or self-assessment, document the conflict and seek review before changing the substantive claim or criterion.

## 5. Vault Documentation
- Follow [[00-System/Documentation Standard|Documentation Standard]] for metadata, scientific evidence labels, naming, and links.
- Follow [[00-System/Vault Architecture|Vault Architecture]] for directory roles and source-of-truth guidance.
- Follow [[00-System/Vault Maintenance|Vault Maintenance]] when adding or updating records.
- Use [[00-System/Vault Migration Plan|Vault Migration Plan]] for the latest audit dispositions and unresolved review items.
