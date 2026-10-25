---
title: AI School Experiment Workflow
type: procedure
status: active
tags:
  - ai-school
  - experiments
  - workflow
created: 2026-10-25
updated: 2026-10-25
---

# AI School Experiment Workflow

Operational checklist for planning, running, and reporting experiments. This describes the current checkout as inspected on 2026-10-25. The vault has a documented research lifecycle, but it does **not** yet contain a standardized runner, result-bundle schema, run-ID generator, artifact validator, or automated `complete` command. The CVC replication remains a plan; its runner and frozen item file have not been implemented. Do not treat the legacy commands below as execution commands for that plan.

## 1. Plan — Codex and researcher

- Search the [[Development/Experiments/Experiments Index|canonical Experiments Index]], related lesson/assessment notes, and dated audits before proposing a duplicate.
- Codex drafts a dated note from [[Templates/Experiment Template|Experiment Template]], with `status: planned`, `scripts`, a falsifiable hypothesis, controls, frozen split/items, metrics, seeds, checkpoint rule, stopping rule, and provenance/artifact plan. Record uncertainty and competing explanations.
- Researcher reviews the protocol. **Planning approval is not approval to implement or run.** Substantive revisions to a planned protocol update `updated` and append a dated `changelog` entry; preserve previous entries.

See [[Documentation Standard]], [[Vault Maintenance]], and [[AGENTS]] for evidence and approval boundaries.

## 2. Prepare — Codex in the repository

After the plan is approved for implementation, Codex creates or modifies only the listed runner and frozen inputs, then documents the exact command, expected outputs, paths, schema, and preflight checks in the plan. It checks that final-test items are disjoint from training and validation and that checkpoint selection does not inspect the final test. Code and data changes are reviewed before execution approval.

**Current implementation gap:** the CVC plan at [[Development/Experiments/2026-10-25 Plan - Controlled CVC Transfer Replication]] names `experiments/run_cvc_transfer_v2.py` and `experiments/cvc_transfer_v2.json` as work to create; neither is a runnable, approved protocol artifact yet. Its planned log and bundle paths are not current outputs. There is no generic runner standard or example-runner document in this vault. The existing [[Development/Experiments/README|artifact map]] links legacy scripts; it warns that name correspondence does not prove reproduction.

## 3. Review — researcher approval

Before execution, inspect the diff and approved commit; runner and data paths; exact training and evaluation items; leakage/preflight report; controls; paired initialization checks; output paths; expected schema; seeds; stopping/checkpoint rules; and compute estimate. Approve implementation and execution as separate decisions. No run starts from a plan alone.

## 4. Push approved implementation to `origin` — Codex

After implementation review and explicit approval to publish the runner, Codex commits only the approved implementation/protocol/input files and pushes that approved branch to `origin`. This first push publishes code and frozen inputs; it contains no run results and does not authorize execution. Record the exact pushed commit hash for Jane to verify. Do not push unrelated workspace changes.

## 5. SSH and pull to Jane — researcher on the server

Use [[00-System/Server Experiment Access|Server Experiment Access]] to verify SSH identity, host key, repository path, remote, and Git state. The documented repository path is `~/projects/The-Lab/`. On Jane, first confirm `git status --short` is clean; stop if it is dirty. Then pull the approved branch with fast-forward-only behavior, using the branch name recorded in the review:

```sh
git pull --ff-only origin <approved-branch>
git status --short
git rev-parse HEAD
```

The status must be clean and `HEAD` must equal the implementation commit Codex pushed and the researcher approved. If not, stop. Do not pull with a merge, rebase, reset, or discard local changes to force the expected state.

## 6. Test — researcher on Jane, only after execution approval

Use only the exact command recorded in the approved experiment note. Existing scripts are historical, script-specific examples, not a standardized runner:

- `python3 experiments/test_lesson11_updated.py` writes `experiments/lesson11_updated_results.json` and overwrites that fixed path. Do not rerun it as an example workflow or without an explicit preservation plan.
- `python3 experiments/test_preschool_throwaway.py` writes a timestamped JSON under `experiments/preschool_test/` and prints progress to the terminal. It is a legacy harness test, not the planned CVC runner.
- `python3 experiments/run_experiment_b.py` prints results to the terminal; it does not write a result bundle.

These invocations are visible from each script's `__main__` block. Dependencies/environment setup must be confirmed on Jane; this guide does not claim these commands were run or verified there. For a future approved runner, its record must specify durable log capture, bundle path, and safe-resume behavior. A terminal interruption is not evidence of completion. Preserve partial output and document failure; do not silently restart or change the protocol.

## 7. Validate — researcher, then Codex evidence review

Before publishing, compare the run's revision/configuration with approval; inspect exit status and log for completion/errors; check every required artifact exists, is non-empty, parses against the documented schema, and contains every planned seed/condition/item. Recheck preflight/leakage and compare raw output with summaries. No shared validator currently performs these checks; validation of legacy scripts is manual and limited to their outputs. A script's printed “Complete” or a JSON `passed` field is not provenance or artifact-validation status.

## 8. Commit and push run evidence — researcher on Jane

After validation, inspect `git status --short`; stage only this run's artifacts and approved evidence updates; review `git diff --cached` before committing. Do not use `git add .` or overwrite a prior result file; use a new run-specific output path for new runs. Commit and push the run evidence to `origin`, then share the resulting commit hash with Codex. This is the second push in the lifecycle. There is no artifact-commit automation. If output is too large or excluded by policy, preserve it in the approved durable location and record its exact path/checksum; do not claim it was published to Git.

## 9. Request completion — researcher to Codex

When you say **“complete”** for an approved run, Codex treats it as a request to inspect and finish the evidence record: verify the supplied revision, repository state, log, bundle, schema, required seeds/conditions/items, and failure/partial status; compare artifacts with the preregistered protocol; then create a new dated experiment record, summarize measured results and item-level failures, discuss limitations, link artifacts and plan, and add the record once to [[Development/Experiments/Experiments Index|Experiments Index]].

`complete` does not authorize rerunning training, changing data or protocol, choosing a different checkpoint, or declaring a hypothesis supported without evidence. If evidence is missing or inconsistent, Codex records the gap and leaves the run incomplete or failed; a follow-up needs separate approval.

## 10. Review analysis — researcher

Find the new dated record in the [[Development/Experiments/Experiments Index|Experiments Index]]. Check the raw bundle and log, all seed and per-item results, control comparisons, split integrity, and the distinction between measured outcome and interpretation. Decide whether the evidence supports the bounded hypothesis, leaves it unestablished, or motivates a separately planned follow-up. Update curriculum/teacher/assessment claims only through their review process; do not rewrite historical findings.

## 11. Troubleshooting

| Problem | Action |
| --- | --- |
| Run fails or is interrupted | Preserve logs and partial outputs under a unique path; record revision, seed, condition, last completed step, and error. Mark failed/incomplete. Review before a repaired rerun; keep the failed attempt. |
| Missing artifacts or invalid schema | Do not mark complete or summarize as a valid run. Preserve what exists, identify missing fields/files, and request a repair plan. No schema validator is currently provided. |
| Dirty working tree on Jane | Stop before pull/run. Preserve unrelated work; do not discard it to make the tree clean. |
| Commit differs from approved revision | Stop before execution, or quarantine output if already run. Report both hashes and obtain review for the revised run. |
| Output path already exists | Do not overwrite. Select a new run-specific path only through the approved protocol or a documented amendment. |
| Control exposure or split check fails | Stop before training. Preserve the preflight report and revise the protocol with a changelog entry and renewed approval. |

## Example: reading an existing result bundle

The legacy `experiments/lesson11_updated_results.json` records four seeds. Seed 42 has `delta_loss: 6.398976...` and `acc_held: 0.6667` (`2/3`); seed 123 has positive loss improvement (`6.128312...`) but `acc_held: 0`. The JSON `timestamp` identifies when the file was written; each result object holds seed-level metrics. Its `passed` field is that script's criterion, not independently validated completion status. This is historical evidence only: the evaluation was contaminated by checkpoint selection on those same “held-out” items, as documented in the updated research plan. The example shows why raw values, test design, and limitations must be read together.

## What the record fields mean

- **Result bundle:** machine-readable per-run/per-item evidence. There is no common bundle contract; existing JSON layouts differ.
- **Log:** chronological progress and errors. Legacy scripts generally print to the terminal; durable log capture is not standardized.
- **Provenance:** revision, working-tree state, runner/data versions, environment, seed, and run details identifying what produced the output. The vault standard requires recording these, but legacy artifacts often omit them.
- **Run ID:** unique label keeping attempts and outputs distinct. No generator or required format is implemented; require a unique label/path in an approved protocol before execution.
- **Completion status:** whether the planned run finished and artifacts passed validation. No shared status field/tool exists. Keep this separate from `hypothesis_supported` and legacy `passed` metrics.

## References

- [[00-System/Documentation Standard|Documentation Standard]]
- [[00-System/Vault Maintenance|Vault Maintenance]]
- [[00-System/Server Experiment Access|Server Experiment Access]]
- [[AGENTS|Vault Agent Instructions]]
- [[Development/Experiments/Experiments Index|Experiments Index]] and [[Development/Experiments/README|Experiment Artifact Map]]
- [[Templates/Experiment Template|Experiment Template]] and [[Templates/Plan Template|Plan Template]]
- [[Development/Build and Test|Build and Test Guide]] (harness commands, not a research-runner standard)
- Existing script examples: `experiments/test_lesson11_updated.py`, `experiments/test_preschool_throwaway.py`, `experiments/run_experiment_b.py`
- [[Development/Experiments/2026-10-25 Plan - Controlled CVC Transfer Replication|Planned CVC replication]]
