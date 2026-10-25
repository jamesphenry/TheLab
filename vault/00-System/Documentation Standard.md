---
title: AI School Vault Documentation Standard
type: specification
status: active
tags:
  - ai-school
  - documentation
  - research-integrity
created: 2026-10-25
updated: 2026-10-25
---

# AI School Vault Documentation Standard

This note defines the default conventions for new and materially updated vault documents. Preserve older notes as historical records; do not retrofit them wholesale just to match this standard.

## Frontmatter

Use YAML frontmatter for authored notes:

```yaml
---
title: Descriptive title
type: experiment
status: planned
tags:
  - ai-school
created: YYYY-MM-DD
updated: YYYY-MM-DD
changelog: []
---
```

- `title`, `type`, `status`, and `tags` are expected for new notes.
- `created` records the known creation date. Do not infer it from a file's current location or Git commit. If it is unknown for an older note, leave it unknown rather than inventing a date.
- `updated` changes when the note is substantively edited; do not update it for a read-only check.
- For a substantive revision to a planned protocol or research plan, use the optional `changelog` YAML list with `date` and `change` fields. Append the newest entry first and preserve prior entries. A new plan may start with `changelog: []`; add the first entry when it is revised.
- Quote titles containing YAML-sensitive punctuation when needed. Use a YAML list for tags and lowercase hyphenated tag values.
- Keep the established `type` values where they fit: `experiment`, `decision`, `assessment`, `lesson`, `curriculum`, `report`, `experience`, `log`, `plan`, `project`, `architecture`, `specification`, `procedure`, `debugging`, `index`, `hub`, `overview`, `blueprint`, `instructions`, `learner-log`, `learner-profile`, `self-assessment`, and `teacher-profile`. A new type should identify a genuinely different document role, not a subject label.

## Status vocabulary

Use a status that describes the document's lifecycle:

- `planned`: proposed work or an experiment not yet run.
- `proposed`: a decision awaiting adoption.
- `active`: current guidance, curriculum, index, or specification.
- `in-progress`: work or investigation underway.
- `completed`: a finished session, experiment record, or report. This does not mean its hypothesis was supported.
- `accepted`: an adopted decision.
- `superseded`: retained for history but replaced as the current reference.
- `archived`: retained for provenance and no longer maintained.

Avoid `done`; distinguish the status of a document from whether an experiment's prediction was supported.

## Scientific records

### Experiment protocol and record

Use [[Templates/Experiment Template|Experiment Template]] for a planned or completed experiment. Keep the record self-contained enough to identify what was done:

- **Runner paths:** list repository-relative executable experiment/test scripts in the `scripts` frontmatter property. Use `scripts: []` if no dedicated runner is recorded. This field identifies associated code; it does not claim that the script exactly reproduces the reported run.
- **Question** and falsifiable **Hypothesis** (before results are known).
- **Method / Procedure**, including the actual dataset and split, training examples, held-out examples, controls, model/configuration, decoding/evaluation procedure, and stopping or checkpoint-selection rule.
- **Run provenance:** repository-relative code paths, commit or revision, environment, seed per run, and links to raw outputs/checkpoints where available.
- **Results / Observations:** report actual values and representative outputs; label measured values as **Measured** and directly inspected behavior as **Observed**. Preserve failed, negative, and inconclusive runs.
- **Interpretation**, **Limitations**, qualified **Conclusion**, and **Next experiment**.
- **Related** links to protocol, assessments, supporting code/artifacts, and follow-up records.

State explicitly whether evaluation items, target strings, or relations overlap training. Reserve “held out” for examples kept out of training; distinguish a new prompt context from a withheld target or rule. If a checkpoint is selected using a validation set, keep final test results on a separate untouched set.

### Research audits and syntheses

Use [[Templates/Research Audit Template|Research Audit Template]] for cross-record reviews. Separate recorded evidence from interpretation and proposal; cite source notes and report missing provenance. An audit may identify issues in historical records but must not silently rewrite those records.

### Other document roles

- **Assessment:** fixed items, scoring rule, rubric, and train/validation/test relationship. Version the assessment if items or scoring change.
- **Decision (ADR):** context, options, decision, consequences, evidence, review trigger, and links to relevant experiments. Do not use an ADR to replace experiment records.
- **Session experience/log:** dated account of what occurred; link outcomes to formal assessment or experiment notes rather than making the log the only result record.
- **Architecture/procedure/operational guide:** identify implementation status and source of truth; label planned components as planned.
- **Index/hub:** navigation only. Keep one canonical index per collection and link to source notes rather than duplicating results.
- **Blueprint/brainstorm:** preserve tentative ideas as such; link adopted decisions where the design has since changed.

## Naming and links

- Use ISO dates in dated filenames: `YYYY-MM-DD Descriptive Title.md`. Keep stable reference documents named by role.
- Use `ADR-NNNN Descriptive Title.md` for decisions.
- Preserve existing filenames when renaming would break links or obscure history. Add an alias or redirect note for deprecated navigation paths.
- Use Obsidian links without `.md`, relative to the vault root when including a folder: `[[Development/Experiments/Example|Experiment name]]`.
- For code, data, and outputs outside the vault, use repository-relative paths in inline code (for example, `harness/learner/model.py`) and record the commit/revision. Do not put machine-specific absolute paths in durable notes.
- Add reciprocal links where useful: experiments to assessments/lessons and reports, reports to source experiments, decisions to evidence, and all new records to the canonical index.

## History and corrections

Do not overwrite a completed experiment with later findings. Add a new run, correction, follow-up experiment, or dated audit and link it to the earlier note. Keep the original observations intact. If a live curriculum, assessment, or guide conflicts with newer evidence, record the conflict and review it before changing instructional or scientific claims.
