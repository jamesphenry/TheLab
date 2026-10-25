---
title: "Plan — Controlled CVC Transfer Replication"
type: experiment
status: planned
scripts:
  - experiments/run_cvc_transfer_v2.py
tags:
  - ai-school
  - experiment
  - research-plan
  - cvc
  - transfer
created: 2026-10-25
updated: 2026-10-25
changelog:
  - date: 2026-10-25
    change: "Implementation draft: freeze the inputs/bootstrap recipe and add a preflight-first paired-seed runner with unique run IDs and partial-run preservation; no preflight command or experiment was executed."
  - date: 2026-10-25
    change: "Review revision: verify paired initial weights, expose control n-gram counts and sequences, and limit inference to seeds and items tested."
  - date: 2026-10-25
    change: "Aligned the primary-metric statement with the runner: full-head NLL is primary; letter-renormalized NLL is secondary."
  - date: 2026-10-25
    change: "Removed the runner's unnecessary NumPy requirement from canonical tensor hashing after the first server attempt found NumPy unavailable; the failed attempt remains preserved."
  - date: 2026-10-25
    change: "Replaced slow Python iteration over tensor storage with raw payload extraction from Torch serialization after the CPU retry made no saved progress; its interrupted attempt is preserved separately."
  - date: 2026-10-25
    change: "Recorded a second hash failure: paired tensors were equal, but serialized archive metadata differed; the digest now hashes only the raw tensor payload, excluding archive metadata."
---

# Plan — Controlled CVC Transfer Replication

> [!warning] Execution attempts preserved; no training results yet
> The frozen protocol passed data-only preflight. The first full-run attempt failed because the default server Python lacked PyTorch. A CPU-only retry was interrupted before its first seed record because the initial-state hash path was prohibitively slow. A second retry reached the paired-state check and failed despite equal tensors because the serialized archive metadata differed; diagnostics confirmed the raw payloads matched. All attempts are preserved under their run IDs; no optimizer update or scientific result has been produced. Fix and review the runner, then use a new run ID for any retry.

## Research question

Does training on the original Lesson 1.1 sentences increase a 27M BabyLM's probability of completing the final letter of CVC spellings that never occur as words in training, beyond changes caused by character frequency or generic English-byte exposure? Does any effect depend on whether the target's final two-letter sequence appeared in training?

This operationalizes a narrow byte-level spelling-completion claim. It does not test word meaning, phoneme awareness, or reliable free-form word generation.

## Motivation and current evidence

- The initial Lesson 1.1 record reports a mean target-loss decrease of 3.7655, but its four target words (`mat`, `hot`, `run`, `bed`) appear in the five training sentences. The result supports fitting those strings, not transfer.
- Experiment A reports a 3.8638 mean loss decrease over eight nominally held-out items in one seed. Its test set mixes new contexts for trained words, words with familiar spelling fragments, and only two fully novel CVC words (`dig`, `big`). Its generations are not reliably correct.
- Experiment B reports target-loss decreases of 4.7096 for phonics examples and 3.2824 for unrelated English, with one seed and the four overlapping Lesson 1.1 targets. Generic English-byte learning is therefore a live alternative explanation.
- Experiment C reports ten positive deltas on the same four training-adjacent targets. It does not replicate Experiment A's unseen-word cases.
- The current preschool alphabet assessment is not valid evidence of transfer: the updated curriculum includes the three alphabet transitions labeled held out in Assessment 1. The updated lesson runner also selects a checkpoint using those same three items and reports performance on them. Its JSON bundle reports mean held-out accuracy of 16.67% across four seeds, alongside a mean loss delta of about 6.23; these metrics separate sharply, but the test is contaminated.
- `harness/experiments/experiment_a.py` contains a useful CVC evaluation implementation, but it is untracked, uses one seed, samples generation at temperature 0.7, and has no saved result bundle. The tracked `experiments/run_experiment_a.py` has related held-out CVC code, but also samples generation and mixes truly unseen words with familiar targets. Neither is a controlled, multi-seed result for the protocol below.
- The current model has 4096 output classes while `BabyTokenizer` emits 260 IDs (four special tokens plus byte values). This plan keeps the training configuration unchanged for comparability, reports probability over both the full output space and the 26 lowercase letters, and records mass assigned to invalid output IDs.

Sources: [[2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition]], [[2026-10-23 Experiment A — Held-Out Test]], [[2026-10-23 Experiment B — Control Group]], [[2026-10-23 Experiment C — Multiple Random Seeds]], [[2026-10-24 Lesson 1.1 Updated Test]], [[2026-10-24 Coverage Fix Multi-Seed Follow-up]], [[02-School/Preschool/Curriculum|Preschool Curriculum]], [[02-School/Preschool/Teacher|Preschool Teacher]], [[02-School/Preschool/Assessments/Assessment-1-Pattern-Sequences|Assessment 1]], and the 2026-10-25 [[07-Reports/2026-10-25 AI School Independent Research Audit - Updated Evidence|updated audit]] plus its [[07-Reports/2026-10-25 Research Artifact Inventory Correction|artifact-inventory correction]].

## Competing explanations

1. **Ordered spelling exposure transfers:** training raises probability for novel CVC continuations because the model uses ordered letter patterns learned from words such as `cat`, `mat`, `run`, and `pen`.
2. **Whole-word memorization:** gains occur only for words or complete target strings present in the training corpus. The final test forbids this overlap.
3. **Character-frequency shift:** gains come from seeing the same letters more often, regardless of their order. A shuffled control preserves each training sentence's byte inventory and length while disrupting letter order.
4. **Generic English statistics:** unrelated English improves letter predictions similarly to the phonics material. An English-text control reuses Experiment B's corpus; its unequal byte lengths will be reported as a limitation.
5. **Initialization variance:** apparent transfer is driven by a small number of favorable random seeds. Each condition is paired by seed and repeated across ten predeclared seeds.

## Control-exposure audit

The suffix counts below are literal, case-insensitive occurrences in each complete training corpus before its 15 passes. They make clear that “far” means absent from the **phonics treatment**, not necessarily absent from every control. The unrelated-English corpus exposes `at`, `en`, and `ag`; in particular, the `tag` item is not suffix-novel relative to that arm. The shuffled corpus is fixed rather than regenerated per model seed, so the exact sequences and their exposures are auditable.

| Test suffix | Phonics treatment | Unrelated English | Fixed shuffled control |
| --- | ---: | ---: | ---: |
| Near `at` | 4 | 5 | 0 |
| Near `un` | 4 | 0 | 1 |
| Near `ot` | 1 | 0 | 0 |
| Near `en` | 1 | 2 | 1 |
| Near `og` | 1 | 0 | 0 |
| Far `ig` | 0 | 0 | 0 |
| Far `ip` | 0 | 0 | 0 |
| Far `it` | 0 | 0 | 0 |
| Far `ag` | 0 | 1 | 0 |
| Far `up` | 0 | 0 | 0 |
| Far `ud` | 0 | 0 | 0 |
| Far `id` | 0 | 0 | 0 |
| Far `ib` | 0 | 0 | 0 |

The fixed shuffled strings use `random.Random(20261025)` to permute alphabetic slots within each treatment sentence while preserving initial capitalization, punctuation/space positions, and each sentence's exact byte multiset:

```text
Tsh toc hae tn tta eam.
Trd oia hgn tsu cn eun hne.
Tio sth ue hsn.
Ten bie eoh hd re psd etn.
A car nut can.
```

The suffix counts include the two near suffixes `un` and `en` that occur incidentally in these shuffled strings. No full final-test word occurs as a whole word in the unrelated-English or fixed shuffled corpus. The runner must reproduce this table from the frozen `cvc_transfer_v2.json`; if counts or strings differ, stop before training and revise the protocol with a new changelog entry.

Each corpus is replayed for 15 passes, so raw counts multiply by 15 in the training exposure ledger. For example, `ag` appears once in the unrelated-English corpus and is presented 15 times over the planned run; `at` appears five times there and is presented 75 times.

The unrelated-English corpus used for these counts is:

- `The system processes data files.`
- `Network latency affects throughput.`
- `Database queries return results.`
- `The compiler optimizes register allocation.`
- `Memory allocation requires careful management.`

## Falsifiable hypothesis

Relative to both the no-update baseline and the character-shuffled control, phonics training will produce a larger reduction in target-letter negative log likelihood on the **far** test cohort, whose target suffix bigrams are absent from the phonics exemplars. The near cohort, whose suffix bigrams are already present in other words, is a positive-control stratum and is expected to improve more than the far cohort.

The hypothesis is not supported if the phonics condition's far-cohort improvement is no greater than the shuffled or unrelated-English condition, or if any apparent advantage is limited to the near cohort. A likelihood gain without exact letter prediction will be reported as a probability shift, not as successful completion.

## Experimental design and controls

### Conditions

1. **Phonics treatment:** the five fixed original Lesson 1.1 exemplars, copied exactly from `experiments/run_experiment_b.py`:
   - `The cat sat on the mat.`
   - `The dog can run in the sun.`
   - `The sun is hot.`
   - `The red pen is on the bed.`
   - `A cat can run.`
2. **Matched order control:** the five fixed strings in the control-exposure audit above. The exact strings are shared across all seeds; do not regenerate them per run. A preflight check rejects any mismatch in their byte inventories or an accidental final-test word / far suffix.
3. **Unrelated-English control:** the five fixed `CONTROL_ENGLISH` sentences in `experiments/run_experiment_b.py`. This condition receives the same number of passes and optimizer steps. Its longer and different byte exposure is measured and reported; it is an auxiliary generic-English comparison, not a perfectly token-matched control.

For each arm, store and report the exact realized training strings and per-item suffix counts before training. The counts above show why far/near is defined relative to treatment: the unrelated-English arm includes `ag`, while the fixed shuffled arm incidentally includes `un` and `en`.

For each seed, instantiate one reference initialization and clone its `state_dict`. Load those exact tensors into each condition's fresh model and use `torch.equal` on every named tensor before the first update; record a canonical SHA-256 digest of the initial state. Create a fresh optimizer per condition. A seed reset alone is not sufficient evidence that paired runs start from identical weights. Record the untrained model's evaluation before any updates. Keep the 4096-class model, byte tokenizer, CPU/GPU selection, AdamW learning rate `1e-3`, gradient clipping `1.0`, and 15 passes over five training strings. This is 75 optimizer updates per condition. No model or training behavior is changed in this planning task.

### Fixed evaluation items

The task is one-byte completion: present the first two letters of a CVC word and score the expected third letter. This removes sentence-semantic variation from the primary measurement. It remains a spelling-distribution probe: a two-letter prefix can have multiple valid completions, so exact top-1 accuracy on the selected words is descriptive and is not a general word-mastery criterion.

| Stratum | Word | Prompt | Target | Basis |
| --- | --- | --- | --- | --- |
| Near | `bat` | `ba` | `t` | `at` occurs in `cat`, `sat`, and `mat` |
| Near | `bun` | `bu` | `n` | `un` occurs in `run` and `sun` |
| Near | `pot` | `po` | `t` | `ot` occurs in `hot` |
| Near | `hen` | `he` | `n` | `en` occurs in `pen`; `he` also occurs in `the` |
| Near | `bog` | `bo` | `g` | `og` occurs in `dog` |
| Far | `dig` | `di` | `g` | `ig` is absent from the phonics exemplars |
| Far | `sip` | `si` | `p` | `ip` is absent |
| Far | `bit` | `bi` | `t` | `it` is absent |
| Far | `tag` | `ta` | `g` | `ag` is absent |
| Far | `cup` | `cu` | `p` | `up` is absent |
| Far | `mud` | `mu` | `d` | `ud` is absent |
| Far | `hid` | `hi` | `d` | `id` is absent |
| Far | `rib` | `ri` | `b` | `ib` is absent |

All listed letters occur in the phonics training corpus. The words are absent as complete words. The final test's suffix class is computed from the exact training bytes by code, not trusted from this table. The fixed development/validation items are `cap`, `cot`, `met`, and `ram`; they are not used for gradient updates or checkpoint selection, and do not appear in the final test list.

### Leakage and split controls

- Before training, mechanically verify for every condition that no validation or test word appears as a whole word in its training strings; every prompt and target is ASCII lowercase; every target letter occurs in the training vocabulary; and the near/far suffix classification matches the treatment corpus.
- Record every evaluation target's byte n-grams and whether they occur in each training condition. A far item is far only relative to the phonics training corpus; if its suffix appears in a control, mark that exposure explicitly rather than silently relabeling it.
- The development set and final test have disjoint words and prompts. Use development items only to verify the frozen evaluation code. Do not tune epochs, learning rate, seeds, examples, or decoding based on development results. If a protocol change is needed after inspecting development outcomes, increment the protocol version and replace the final test before any final-test access.
- Freeze the final item JSON, code revision, and split-check output before fitting models. Do not use final-test values for checkpoint selection or curriculum changes. Since the stopping schedule is fixed, no checkpoint selection is planned.

## Training, validation, and final test separation

- **Training:** only the five exemplars for the phonics arm; the matched shuffled strings for its control; and the specified unrelated-English strings for the auxiliary control.
- **Validation/development:** four separate CVC items (`cap`, `cot`, `met`, `ram`) for pipeline checks and descriptive reporting only. They are not included in training and do not select checkpoints.
- **Final test:** the 13 words in the table above, evaluated only after all conditions, seeds, item definitions, and scoring code are frozen. No final item is used for training, early stopping, or parameter selection.
- **Leakage audit:** exact whole-word lookup, character-coverage check, suffix-bigram membership check, test/validation disjointness check, and a printed per-condition overlap matrix are required before the first training update. Save the audit output with the results.

## Independent variables and baselines

- **Primary independent variable:** training corpus condition (phonics, byte-multiset-matched shuffled, unrelated English).
- **Stratification variable:** whether the target's final two letters occur as a contiguous bigram in the phonics exemplars (near vs. far).
- **Baseline:** same-seed untrained model evaluated before training. The no-update comparison is therefore paired with every condition.
- **Initialization control:** for each seed, load the same cloned initial tensors into each condition. Verify equality tensor by tensor before updating and record the per-seed canonical SHA-256 digest in the result bundle.
- **Digest definition:** sort `state_dict` entries by key and hash each key, dtype, and shape separated by NUL bytes, followed by the raw `data/0` storage payload extracted from a Torch-saved contiguous CPU tensor and a NUL delimiter. Exclude serialization/archive metadata. Record the PyTorch version with provenance. Log the digest before training each arm and verify that all three arms for a seed have the same digest.
- **Fixed conditions:** model architecture and 4096-way output head; tokenizer; optimizer; learning rate; gradient clipping; update count; decoding; item set; and software environment within each seed.

## Metrics and item-level failure analysis

### Primary metric

Mean target-letter negative log likelihood under the unchanged full 4096-class output head is the primary metric on the eight far items, measured before and after training. Report per-seed changes and the paired difference between phonics and shuffled-control improvement. Lowercase-letter-renormalized NLL is a secondary diagnostic. Also report the near-cohort value separately; never combine the two strata into one transfer claim.

Because the model predicts 4096 classes but the tokenizer can emit only 260 IDs, report both (1) target NLL under the unchanged full 4096-way training distribution and (2) target probability renormalized over the 26 lowercase letters. Record probability mass assigned to impossible output IDs. Do not change the training loss or model vocabulary in this experiment.

### Secondary metrics

- Greedy next-letter accuracy under two declared decoders: unrestricted 4096-way argmax and argmax restricted to the 26 lowercase letters. Report invalid-token output rate. The letter-restricted metric reflects the task contract; it does not replace the unconstrained result.
- Correct-letter rank among all 4096 classes and among the 26 lowercase letters.
- Near- and far-stratum mean NLL, per-item NLL change, per-seed outcome, and dispersion.
- Development-item results, training-loss trajectory, exact generated byte, and item-level failures for every condition and seed.

No single “pass” threshold is defined. With 13 related probes, describe the evidence and uncertainty; do not treat items as independent replications of the model-training intervention.

## Seeds, sample sizes, and checkpoint selection

- Ten paired seeds from the existing multi-seed set: `42, 123, 7, 2026, 99, 314, 256, 13, 555, 8`.
- Three fresh training runs per seed (30 total), plus each same-seed pre-training baseline.
- Thirteen final items: five near and eight far; four development items. Report all seed-by-item outcomes, not only means or best seeds.
- Use the final checkpoint after exactly 15 passes. Do not select a best checkpoint. The schedule is fixed to match the original 15-pass CVC/phonics studies; no early stopping.
- Report paired per-seed condition differences, mean/median, sample standard deviation, and a 95% percentile bootstrap interval over seeds (10,000 resamples; bootstrap seed `20261025`) as a descriptive uncertainty summary. Preserve all failed runs and record any rerun as a separate attempt.
- Interpret the bootstrap interval over seeds as initialization uncertainty for these fixed items. Ten seeds do not turn the eight far words into 80 independent test items; report the item count as eight and limit generalization claims accordingly.

## Stopping rule

Run exactly 15 passes over the five training strings in each condition. Stop a run early only for a code/runtime failure or a non-finite loss; record the seed, condition, last completed update, and error. Do not extend training because results look weak. A repaired rerun must use the same frozen protocol and be recorded alongside the failed attempt.

## Required scripts, data, and artifacts

- **New runner:** `experiments/run_cvc_transfer_v2.py`. It supports a data-only `--preflight-only` mode and a separate training mode. Reuse `BabyLM`, `BabyLMConfig`, and `BabyTokenizer`; implement deterministic one-byte scoring and the two declared decoders. Do not modify the historical experiment scripts.
- **Frozen item/control file:** `experiments/data/cvc_transfer_v2.json`, containing exact train, development, and final-test strings, the control shuffle seed and strings, near/far labels, expected suffix counts, and bootstrap settings. The runner computes the leakage/exposure audit from these frozen inputs and records it before constructing a model or optimizer. Review and commit both code and data before execution.
- **Result bundle:** `experiments/results/cvc_transfer_v2/<run-id>.json`, containing commit and dirty-tree state, Python/PyTorch/device information, model/config and optimizer settings, seeds, each per-seed initial-state SHA-256 digest, training-byte/update counts, per-item baseline/final metrics, per-seed summaries, decoding outputs, exact control strings/exposure counts, leakage-audit output, and completion/failure status. A run ID is mandatory; existing bundle or log paths are never overwritten.
- **Run log:** `experiments/results/cvc_transfer_v2/<run-id>.log`, including progress, failures, interruptions, and completion status. The runner writes partial bundle updates after each completed pass and preserves partial records on handled errors/interruption. Abrupt power loss may leave status `running`; treat it as incomplete.
- **Commands after separate review/approval:** data-only audit: `python3 experiments/run_cvc_transfer_v2.py --run-id <unique-preflight-id> --preflight-only`; full experiment: `python3 experiments/run_cvc_transfer_v2.py --run-id <unique-run-id>`. A preflight-only ID creates its own bundle/log and cannot be reused for training.
- **Follow-up record:** create a new dated completed experiment note after execution and link it here. Preserve this plan and all earlier experiment records.
- **No checkpoint archive is required for the primary result** because the fixed seeds and code/data revision reconstruct the run; if checkpoints are retained, record their paths and storage cost.

## Expected outcomes and interpretation

| Outcome | Interpretation update |
| --- | --- |
| Phonics beats shuffled control on near and far items across seeds | Preliminary evidence on these fixed items that ordering in the phonics examples changes probabilities beyond exact word memorization and unigram frequencies. Far-item evidence is still byte-level transfer, not proof of phoneme concepts or broad CVC generalization. |
| Phonics beats shuffle only on near items | Supports reuse of familiar rime bigrams; does not support broader novel-bigram completion. |
| Phonics and shuffled control improve similarly | Character exposure or optimization is sufficient to explain the measured change; ordered phonics structure is not established as the cause. |
| Unrelated English matches phonics | Generic English-byte statistics remain a sufficient explanation for the observed likelihood shift. |
| Likelihood improves but letter accuracy does not | The model assigns more probability to targets without making the expected next letter its top choice; do not call this successful completion. |
| Effects vary strongly by seed or item | The average is not a reliable learner-level claim; report the instability and preserve per-item outcomes. |
| No condition improves over baseline | The earlier single-seed transfer result does not replicate under this probe; investigate code/data provenance before proposing a larger curriculum change. |

Even if the predicted pattern appears across all ten seeds, the conclusion remains limited to these 13 selected words (eight far items); the seeds quantify initialization sensitivity and are not additional word-level replications.

## Limitations and unresolved questions

- A one-letter target after a two-letter prefix is a deliberately narrow byte-level probe. It does not establish meaningful word completion, reading, pronunciation, or phonological awareness.
- The target word is not uniquely determined by its first two letters. Top-1 exact-word-style scoring is therefore descriptive; likelihood comparisons are the primary outcome.
- Thirteen items are a small, hand-selected set. Item-level uncertainty and limited CVC families constrain generalization claims.
- The shuffled control matches byte inventories and length but destroys English bigrams and natural syntax. It distinguishes unigram exposure from ordered exposure; it does not isolate every form of generic English-statistical learning.
- The eight far items are a small, fixed item set. Even a consistent effect over all ten seeds supports only a preliminary result on these words; it does not demonstrate broad CVC generalization.
- The unrelated-English condition has longer sentences and a different character distribution. Equal optimizer updates do not imply equal token exposure or compute.
- The 4096-versus-260 output mismatch remains. Reporting both full-head and letter-normalized probabilities makes it visible but does not resolve its effect on learning.
- Results do not repair the current Preschool Assessment 1 split or validate the promoted mixed-coverage curriculum. A separate leakage-free alphabet curriculum evaluation remains necessary before using preschool graduation criteria.

## Implementation status and exact execution sequence

1. **Protocol/data frozen; execution attempts preserved:** `experiments/data/cvc_transfer_v2.json` freezes the protocol strings/items, suffix-exposure expectation, optimizer settings, seeds, and bootstrap recipe. Data-only preflight passed as `preflight-20261025-2837ee0`. Full attempt `cvc-transfer-20261025-main` failed before model creation because `/usr/bin/python3` lacked Torch. Attempt `cvc-transfer-20261025-retry01` used the existing CPU-only `.venv` and was interrupted before its first saved seed because Python-level storage-byte conversion was too slow. Attempt `cvc-transfer-20261025-retry02` failed at the paired-state digest check before any condition arm; diagnosis confirmed equal tensors and equal raw payloads but differing serialized archive metadata. All attempt bundles/logs are preserved; no optimizer update completed.
2. Before execution, review the exact code/data diff and a clean committed revision against this plan. Use a fresh `--run-id`; output collisions are rejected rather than overwritten.
3. Run the separate `--preflight-only` command first if desired. It computes leakage, byte-ID, shuffle-inventory, near/far, and suffix-exposure checks and writes a preflight-only bundle/log without importing Torch or constructing a model. Use a different run ID for the later full experiment.
4. After preflight and separate execution approval, run the full command once. The runner repeats and saves the audit before constructing any model/optimizer; it then evaluates the same-seed baseline, clones and hashes the initial weights, verifies each condition tensor-by-tensor, trains the fixed 15 × 5 updates, and evaluates the final checkpoint without checkpoint selection or stochastic decoding.
5. The runner saves per-item baseline/final metrics, both declared decoders, impossible-token mass, raw strings/exposures, environment/provenance, summaries, and a durable progress log. It retains failed/interrupted attempts in their run-ID paths. After execution, create a new dated result record and index it; do not rewrite this protocol or prior findings.

**Execution boundary and current next step:** the data-only preflight ran and passed; the three full-run attempts above are failed/interrupted, with zero completed training updates. Do not reuse any run ID or treat those bundles as experiment results. The current fix hashes only raw tensor payload bytes extracted from Torch serialization; after reviewing and publishing that exact revision, use a new run ID for another attempt.

## Estimated compute and memory requirements

The current model has about 27.4M parameters. In float32, weights, gradients, and two AdamW moment buffers require roughly 0.41 GiB before activations, temporary tensors, and framework overhead. Plan for **1–2 GiB resident memory for one training process**; this is an estimate from parameter count, not a measured peak. Runs are sequential, so memory does not multiply by the 30 runs.

The protocol performs 30 trained fits × 75 optimizer updates = **2,250 updates total**, plus small evaluation passes. The source scripts do not provide a verified runtime for this exact protocol, so wall-clock time is unknown; benchmark one approved run before scheduling all seeds.

Given the reported low-memory Chromebook, use the server for the multi-seed run. A single fit may fit on a Chromebook with adequate free RAM, but the full paired study risks memory pressure and slow CPU execution; no hardware-specific guarantee is available from this checkout. No run is authorized by this planning note.

## Alternatives considered

| Candidate | Scientific value and discrimination | Feasibility and cost | Decision |
| --- | --- | --- | --- |
| Leakage-free re-evaluation of mixed alphabet coverage | Directly addresses preschool claims and the contaminated Assessment 1 / same-set checkpoint selection. Highest curricular relevance, but the current 12 items cannot be reused; it needs a newly partitioned transition set and careful validation of the modified training examples. | Medium design cost; 27M model; likely similar or greater run count if replicated. | Next after this CVC probe, before using current alphabet assessment for graduation. |
| Controlled CVC transfer replication (this plan) | Tests a foundational byte-level spelling claim with genuinely unseen target words, near/far n-gram strata, ten seeds, and order/frequency controls. It distinguishes several live explanations in one small study. | Existing model/training infrastructure and a relevant source script; one focused runner and a small frozen JSON file; 2,250 optimizer updates. | **Recommended primary experiment.** |
| Held-out explicit-rule/content versus response-format test | High conceptual value for AI School's reasoning claims. Existing Experiment G mostly trains the evaluated mappings and has only one fully novel mapping, so a clean design needs a new mapping inventory and matched formats. | Higher protocol/data-design cost; not required to answer the immediate CVC transfer question. | Defer until the spelling/sequence measures have cleaner baselines. |

## Related

- [[2026-10-23 Experiment A — Held-Out Test]]
- [[2026-10-23 Experiment B — Control Group]]
- [[2026-10-23 Experiment C — Multiple Random Seeds]]
- [[2026-10-24 Lesson 1.1 Updated Test]]
- [[2026-10-24 Coverage Fix Multi-Seed Follow-up]]
- [[07-Reports/2026-10-25 AI School Independent Research Audit - Updated Evidence|Updated research audit]]
- [[07-Reports/2026-10-25 Research Artifact Inventory Correction|Artifact-inventory correction]]
