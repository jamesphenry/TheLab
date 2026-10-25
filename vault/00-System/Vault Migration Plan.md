---
title: AI School Vault Audit — Migration and Disposition Plan
type: plan
status: completed
tags:
  - ai-school
  - vault
  - audit
  - migration
created: 2026-10-25
updated: 2026-10-25
---

# AI School Vault Audit — Migration and Disposition Plan

## Scope and decision

Inventory covered the 91 Markdown files and directory structure present before this plan was created, including templates, indexes, reports, experiments, operational notes, school materials, and root notes. Supporting experiment code and two JSON result bundles are tracked in repository-root `experiments/`, outside the vault; no saved checkpoints, `.log`, or `.csv` run outputs were found in the repository scan. Code references are repository-relative inline paths.

**No bulk relocation is recommended.** Current files generally occupy sensible existing locations and internal links resolve when interpreted relative to their source note. Moving them would add link risk without improving research integrity. The changes below are targeted navigation, metadata, and standards corrections. Historical experiment records are not to be merged, rewritten, or deleted.

## Disposition

| Classification | Files / area | Action |
| --- | --- | --- |
| No change required | `00-System/Harness-Rules.md`, `Permissions.md`, `Schedule.md`; `01-Learner/`; Language/Mathematics/Programming subject notes; Preschool materials other than the three review annotations below; `03-Experiences/`; experiment records; ADRs; debugging notes; reports; Obsidian configuration | Retain in place. Preserve existing dates, results, and provenance. |
| No change required | `04-Memory/`, `05-Dreams/`, `06-Labs/`, `02-School/Science/` | These directories are empty. Retain as intended capacity; do not add placeholder notes. |
| Formatting / metadata correction | Root `future.md` | Add descriptive title/type/status/tags and an `updated` date for this edit. Its original creation date is unknown, so do not add `created`. Link it from Home as a speculative blueprint. |
| Evidence-status annotation | `02-School/Preschool/Teacher.md`, `Curriculum.md`, and `Assessments/Assessment-1-Pattern-Sequences.md` | Add a dated audit link and caution that transfer claims need review. Leave original teaching claims, assessment items, and scoring criteria unchanged pending a leakage-free rerun and owner review. |
| Navigation correction | `Development/Experiments/Experiments Index.md` | Treat this plural index as canonical because README links to it. Add all existing dated experiments omitted from its current list. |
| Duplicate / superseded navigation | `Development/Experiments/Experiment Index.md` | Retain the filename for existing bookmarks, mark it `superseded`, and point to the canonical plural index. The duplicated entries are reproduced in the canonical index; do not delete the file. |
| Template correction | `Templates/Decision Template.md`, `Templates/Session Log Template.md`, `Templates/Experiment Template.md` | Change misleading default statuses (`accepted` for an undecided ADR and `done` for a blank log); add run-provenance and split-validity fields to future experiment notes. Add a research-audit template because this document type is now in use. |
| New documentation | `00-System/Documentation Standard.md`, `Vault Architecture.md`, `Vault Maintenance.md` | Establish metadata/evidence conventions, explain current locations and authority, and provide an operational checklist. |
| New documentation | This migration plan | Record the audit disposition and unresolved issues without changing historical research. |
| Navigation maintenance | `Development/Decisions/Decision Index.md`, `Development/Roadmap.md`, `Development/Logs/Logs Index.md`, `Development/README.md`, and root navigation | Add the accepted ADR, mark the implemented learner model/tokenizer complete with its evidence link, clarify the log naming convention, and link vault guides. Preserve all other roadmap state. |
| Artifact-reference correction | [[07-Reports/2026-10-25 Research Artifact Inventory Correction|Research Artifact Inventory Correction]] and `Development/Experiments/README.md` | Correct the earlier audit's overly broad claim that scripts/results were absent, and map tracked runner/artifact locations to vault records. Keep the earlier audit as history. |
| No merge | `NOTES.md`, `future.md`, ADRs, experiments, reports | Their overlap is useful historical context. Add provenance/current-authority pointers; do not consolidate distinct proposals, decisions, and results. |
| Human decision required | Active preschool teacher/curriculum claims of held-out transfer, assessment splits, and graduation rules | Research records show apparent train/test overlap, weak greedy accuracy, and same-set checkpoint selection. Review and revise live curriculum claims only after a leakage-free rerun; do not alter these instructional decisions in this structural audit. |
| Human decision required | `01-Learner/Current-Questions.md`, `Self-Assessment.md`, and `Development/Roadmap.md` | Their dated state may not reflect newer records or implementation progress. Preserve learner-authored/dated content; ask the project owner or learner process to update it. |
| Human decision required | `Development/Project Overview.md` and `Development/Roadmap.md` | Reconcile remaining scope language and unchecked work with the current learner model/classroom implementation and experiments. The roadmap's model/tokenizer item was marked complete with its baseline record; other engine/milestone items remain unchanged. |

## Applied changes

- Added documentation standard, vault architecture guide, maintenance procedure, and research-audit template; expanded the experiment template's run-provenance requirements.
- Added frontmatter to `future.md` without inventing its creation date.
- Added evidence-status links to the affected active preschool guidance and assessment without changing their original claims, test items, or scoring rules.
- Added a separate artifact-inventory correction after finding tracked experiment scripts and JSON result bundles; did not rewrite the earlier audit.
- Completed the canonical experiment index and marked its duplicate path as a retained superseded pointer.
- Added a code-to-record map for repository-root experiment runners and JSON outputs.
- Updated Home, root README, Development README, decision index, and reports navigation.
- Updated the roadmap's implemented model/tokenizer item and the session log naming guidance.
- Clarified implementation status in engineering architecture documentation.
- Preserved all experiment records and both earlier dated research audits.

## Deferred work

- No directory moves, merges of research notes, or deletion of duplicate-path files.
- No change to experiment interpretations, active assessment criteria, or curriculum promotion decisions.
- No attempt to reconstruct missing raw logs, checkpoints, datasets, or historical creation dates; the tracked scripts and JSON bundles remain at repository-root `experiments/`.
