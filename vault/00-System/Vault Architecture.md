---
title: AI School Vault Architecture
type: architecture
status: active
tags:
  - ai-school
  - vault
  - information-architecture
created: 2026-10-25
updated: 2026-10-25
---

# AI School Vault Architecture

This guide describes the existing vault organization and the intended role of each area. It is deliberately conservative: existing paths have working links, and the current structure is adequate without a broad migration.

## Navigation and standards

- [[Home]] is the primary navigation hub.
- The repository-root `vault/README.md` summarizes the vault for people opening it outside Home.
- [[Documentation Standard]] defines metadata, status, scientific-record, naming, and linking conventions.
- [[Vault Maintenance]] describes the routine for adding and reviewing records.
- [[Vault Migration Plan]] records the current audit disposition and unresolved review items.

## Directory map

| Location | Purpose and contents | Keep out |
| --- | --- | --- |
| `00-System/` | Harness and vault policies, permissions, schedules, documentation standards, and information-architecture guidance | Raw run results and subject lesson content |
| `01-Learner/` | Learner goals, learner-generated questions, and self-assessment snapshots | Research hypotheses or unverified capability claims presented as measured facts |
| `02-School/<Subject>/` | Teacher profiles, curricula, lessons, and assessment definitions. Preschool, Language, Mathematics, Programming, and an empty Science directory are present | Run results and post hoc analysis; link to those in Development/Experiments or Reports |
| `03-Experiences/` | Dated classroom/session narratives | Sole repository for quantitative experiment evidence |
| `04-Memory/` | Learner's retrievable external memory | Raw experiment records or system policy |
| `05-Dreams/` | Reflection and speculative associations; keep hypotheses labeled | Established conclusions without evidence |
| `06-Labs/` | Practical learner workspaces and sandbox exercises | Canonical experiment analysis or immutable assessment results |
| `07-Reports/` | Assessment reports and cross-record research audits; [[07-Reports/Reports Index|Reports Index]] is the collection index | Rewriting historical experiment records |
| `Development/` | Human-maintained technical architecture, roadmap, decisions, debugging, operational notes, and experiment records | Learner memory or unrecorded changes to research results |
| `Templates/` | Reusable note templates and their instructions | Completed source records |
| `.obsidian/` | Obsidian application configuration | Research content |

`04-Memory/`, `05-Dreams/`, `06-Labs/`, and `02-School/Science/` currently have no Markdown records. They are retained as planned spaces; do not create placeholder notes unless a real workflow needs them.

Research runner code and the two tracked machine-readable result bundles currently live in repository-root `experiments/`, outside the Obsidian vault. `Development/Experiments/` contains the human-readable records and canonical index. Keep code/artifact references repository-relative in those records. The observed `harness/experiments/` directory is untracked workspace content, not the tracked experiment source of record.

## Authority when notes overlap

- **Runtime behavior and permissions:** current harness source code is authoritative; [[Development/Architecture|Harness Architecture]] describes it and must distinguish implemented from planned components.
- **Current school content:** the active subject curriculum, lesson, and assessment define what is taught and tested. However, a curriculum is not evidence that a capability was achieved.
- **What happened in an experiment:** its dated experiment record is the result record. Later audits synthesize and critique records but do not supersede their observations.
- **Adopted technical/curriculum choice:** the latest accepted ADR is authoritative for that decision until superseded. The ADR links to evidence; it does not replace that evidence.
- **Research synthesis:** dated reports in `07-Reports/` summarize evidence within an explicit scope. They are time-bounded and should not be silently overwritten by later audits.
- **Initial proposals:** [[NOTES|Discussion Notes]] and [[future|Future Research Directions]] preserve early concepts. Accepted ADRs and active specifications govern where proposals conflict.
- **Indexes:** use [[Development/Experiments/Experiments Index|Experiments Index]] for experiment records, [[Development/Decisions/Decision Index|Decision Index]] for ADRs, and [[07-Reports/Reports Index|Reports Index]] for reports.

## Naming and adding documents

Follow [[Documentation Standard]]. In brief: use ISO-dated filenames for records, role-based names for stable notes, unique experiment records, and vault-root wiki links. Add a new experiment to the canonical experiment index and a new report to the reports index. Do not create parallel indexes. Preserve old paths if they may be externally linked; deprecate with a pointer rather than deleting.

## Historical and superseded notes

Keep completed experiments, session logs, and dated audits in place. Mark replaced guidance or duplicate navigation `superseded`, explain the replacement, and link to it. Preserve observations and provenance. Do not merge records with distinct seeds, conditions, interpretations, or historical purpose.
