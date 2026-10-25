---
title: Research Artifact Inventory Correction — 2026-10-25
type: report
status: completed
tags:
  - ai-school
  - research-integrity
  - artifact-inventory
created: 2026-10-25
updated: 2026-10-25
---

# Research Artifact Inventory Correction — 2026-10-25

This addendum corrects the artifact inventory in [[2026-10-25 AI School Independent Research Audit - Updated Evidence|the updated-evidence audit]] without replacing or rewriting that dated report.

## Correction

The audit stated that the checkout lacked corresponding complete run scripts and machine-readable result bundles for most of the documented studies. A subsequent repository-root inventory found that statement was too broad.

At commit `c426b71366abc150c6850eb55d1c1d672d7770f0`, the repository tracks:

- `experiments/run_experiment_a.py` through `experiments/run_experiment_g.py`.
- Preschool and alphabet comparison/diagnostic scripts, including coverage tests, lesson tests, generation diagnostics, checkpoint/rank tracking, and a larger-model test under `experiments/`.
- Two JSON result bundles: `experiments/lesson11_updated_results.json` and `experiments/preschool_test/results_20261024_180535.json`.

The reviewed workspace did not contain saved model checkpoints (`.pt`, `.pth`, or `.ckpt`), `.log` files, or `.csv` results. The experiment drivers and JSON files improve traceability, but their presence alone does not verify that a run can be reproduced with the same environment or that each summary table exactly matches its script output. The separate `harness/experiments/` directory in the working tree is untracked and should not be confused with the tracked repository-root experiment suite.

## Scope of correction

This corrects the earlier audit's claim that the scripts and machine-readable bundles were absent. It does not alter that audit's substantive cautions about training/evaluation overlap, best-checkpoint selection, loss versus generation accuracy, or the need to verify each run's configuration and outputs.

## Related

- [[2026-10-25 AI School Independent Research Audit - Updated Evidence|Updated-evidence audit]]
- [[Development/Experiments/Experiments Index|Experiment records index]]
- [[00-System/Vault Architecture|Vault Architecture]]
- [[00-System/Vault Migration Plan|Vault Migration Plan]]
