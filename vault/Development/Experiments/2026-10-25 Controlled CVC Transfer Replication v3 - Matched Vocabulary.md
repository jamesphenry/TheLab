---
title: "Controlled CVC Transfer Replication v3 — Matched Vocabulary"
type: experiment
status: planned
scripts: []
tags:
  - ai-school
  - experiment
  - cvc
  - transfer
  - preregistration
created: 2026-10-25
updated: 2026-10-25
changelog:
  - date: 2026-10-25
    change: "Initial preregistration for a new 260-token-vocabulary replication; no implementation or execution has occurred."
---

# Controlled CVC Transfer Replication v3 — Matched Vocabulary

> [!warning] Preregistration status
> This is a proposed protocol, not an executed experiment. Implementation and execution require separate review and approval. Do not alter v2 data, results, or historical conclusions.

## Question

With the model output vocabulary matched to the tokenizer's 260 IDs, does phonics training improve prediction of the correct final letter on held-out CVC items more than a byte-multiset-matched shuffled control?

This is a new model and protocol version motivated by the v2 output-space confound. It tests a narrow next-letter distribution, not word meaning, pronunciation, phoneme awareness, or preschool learning.

## Background and evidence

In v2, the model had 4,096 output classes while the byte tokenizer emitted 260 IDs. Baseline probability mass on impossible output IDs was about 93.6%; after training it fell to 0.38–1.13%. Full-head NLL fell, but 26-letter-normalized target NLL worsened in all aggregate conditions and the preregistered phonics-minus-shuffled far-item full-head NLL gain was −1.229 (95% bootstrap interval over seeds [−2.514, 0.086]). This leaves the claimed ordered-spelling transfer unsupported and makes the full-head metric difficult to interpret.

The completed v2 record and detailed result analysis are [[2026-10-25 Controlled CVC Transfer Replication]] and [[2026-10-25 Controlled CVC Transfer Replication - Completed Run]]. This follow-up changes the model vocabulary only; its outcomes must not be used to rewrite v2.

## Hypothesis

On the eight fixed far items, phonics training will improve the mean negative log likelihood of the target letter **conditional on the 26 lowercase letters** more than the fixed shuffled control. The primary contrast is phonics gain minus shuffled gain, where gain is baseline 26-letter-normalized NLL minus final NLL; a positive value favors the hypothesis.

The hypothesis is not supported if the paired-seed contrast is nonpositive or its preregistered 95% interval includes zero. A result in which full 260-class NLL improves but the primary letter-conditional metric does not will count as general output calibration, not evidence of correct-letter transfer.

## Competing explanations

1. **Ordered spelling transfer:** phonics order helps select target letters on far items beyond shuffled exposure.
2. **Generic byte exposure:** phonics and shuffled training have similar effects because byte frequency, rather than order, drives performance.
3. **General language exposure:** unrelated English produces similar changes, without phonics-specific transfer.
4. **Output-space correction:** eliminating the 3,836 impossible classes resolves much of the v2 loss movement, but does not produce correct-letter discrimination.
5. **Initialization sensitivity:** seed-to-seed variation is large relative to the treatment contrast.
6. **Control mismatch:** shuffling disrupts natural letter order and syntax, so any phonics/shuffle difference may reflect broad sequence quality rather than a phonics-specific mechanism.

## Method

### Model and protocol version

- Reuse the BabyLM causal Transformer architecture/configuration from the historical tracked implementation at commit `2372f9155ec901a6fc804a9970e2c8898ccac3c8`, with `vocab_size=260` (four reserved IDs plus 256 byte IDs). Keep maximum sequence length 256, width 512, 8 layers, 8 attention heads, MLP ratio 4, dropout 0.0, tied token embedding/output weights, and all other architecture/training settings fixed unless the implementation review documents a necessary deviation.
- This is a new initialization and parameterization. Do not load v2 checkpoints or describe v2-to-v3 differences as a randomized causal comparison. The tied embedding/output table shrinks by 3,836 × 512 = 1,964,032 parameters; estimated total model size is about 25.45M parameters, versus about 27.41M for the 4,096-class version.
- The training objective remains next-byte prediction over the 260-token tokenizer. The primary evaluation metric conditions logits on the 26 lowercase-letter classes, matching the one-letter completion question. Also report total probability on the three non-predictive special IDs (`pad`, `bos`, `unk`) and on non-letter byte IDs; do not call valid byte IDs impossible.

### Conditions and controls

Use the exact v2 condition strings, copied into a new frozen v3 data file rather than editing `experiments/data/cvc_transfer_v2.json`:

1. **Phonics:** the five original Lesson 1.1 exemplars.
2. **Matched shuffled control:** the five fixed strings that preserve each phonics sentence's byte multiset and length while disrupting order. Verify exact byte-multiset equality before any model construction.
3. **Unrelated-English control:** the same five fixed sentences from v2. This is an auxiliary generic-English comparison and is not byte-count matched.

For every seed, evaluate an untrained baseline, then train one arm per condition from identical cloned initial weights and a fresh optimizer. Verify tensor-by-tensor equality and record a canonical initial-state digest before the first update. The no-update baseline controls for initialization; shuffled is the primary matched comparison; unrelated English is auxiliary.

### Training, validation, and final test

- **Training:** only the five fixed condition strings for the corresponding arm; 15 passes, 75 optimizer updates per arm.
- **Development:** retain v2's four items (`cap`, `cot`, `met`, `ram`) for descriptive pipeline output only. Their earlier outcomes are known; they cannot be used to tune code, hyperparameters, or selection decisions.
- **Final common-item set:** retain v2's five near items (`bat`, `bun`, `pot`, `hen`, `bog`) and eight far items (`dig`, `sip`, `bit`, `tag`, `cup`, `mud`, `hid`, `rib`) for direct fixed-item comparison. Whole-word overlap checks must pass against every training condition. The held-out designation means absent from training, not blind to researchers: these outcomes were previously inspected in v2. Treat v3 as a targeted follow-up on this fixed set, not an independent item-sampled replication or broad generalization test.
- **Checkpoint:** use final weights after exactly 15 passes. No checkpoint selection, early stopping, or development/test-driven tuning.
- **Leakage and integrity preflight:** compute whole words and suffix bigrams from the exact frozen strings; require all 13 final words absent as whole words from all conditions; verify near/far labels against phonics suffix exposure; verify targets are lowercase ASCII and reachable tokenizer IDs; report each final suffix's exposure in all three arms; verify development and final item lists are disjoint; verify the phonics/shuffled byte multiset and length match. Save the complete audit to the run bundle before training. Any failure stops the run pending protocol revision.

### Variables and baselines

- **Independent variable:** training corpus condition (phonics, shuffled, unrelated English).
- **Primary stratum:** far items, defined by suffix bigrams absent from phonics training.
- **Secondary stratum:** near items, whose suffix bigrams occur in phonics training.
- **Primary baseline:** same-seed untrained model, evaluated before any updates.
- **Fixed factors:** architecture except the planned vocabulary correction, tokenizer, optimizer, schedule, data strings, seeds, scoring, and final checkpoint rule.

### Metrics and analysis

- **Primary outcome:** mean target-letter NLL conditional on lowercase `a`–`z`, averaged over the eight far items per seed.
- **Primary contrast:** for each seed, `(phonics baseline NLL − phonics final NLL) − (shuffled baseline NLL − shuffled final NLL)` on the far items; summarize the ten paired values by mean, median, and sample SD, with a 95% percentile bootstrap interval over paired seeds (10,000 resamples, seed `20261025`).
- **Secondary outcomes:** corresponding primary metric on near items; full 260-class target NLL; unrestricted 260-class and 26-letter-restricted exact accuracy; target rank; lowercase-letter probability mass; probability mass on `pad`/`bos`/`unk`; mass on non-letter byte IDs; and every item-by-seed prediction and NLL.
- Report all seed-level results. The bootstrap unit is initialization seed. The eight far words remain eight fixed items; do not use 80 seed-item rows as independent item replications. No post hoc item-level significance test is planned.

### Seeds, sample size, and stopping rule

- Use the same ten predeclared seeds as v2: `42, 123, 7, 2026, 99, 314, 256, 13, 555, 8`.
- Total planned: 30 trained arms, 75 updates per arm, 2,250 optimizer updates; plus ten same-seed baselines.
- Stop an arm early only on runtime/code failure or non-finite loss. Record seed, condition, last completed update, and error. Preserve every failed or interrupted run under a unique run ID; a rerun is a new attempt and must not overwrite artifacts.
- Do not extend training because results appear weak. No model checkpoint is selected.

## Procedure

Proposed steps, pending implementation and execution approvals:

1. Create and freeze `experiments/data/cvc_transfer_v3.json`, copying v2 inputs into a distinct protocol version and adding the exact 260-vocabulary configuration, analysis settings, and leakage audit expectations.
2. Implement a focused `experiments/run_cvc_transfer_v3.py` and a runner-owned model module under `experiments/cvc_transfer/`. Do not restore the deleted `harness/` tree. Preserve the historical architecture and implement only the v3 vocabulary change.
3. Run a data-only preflight and inexpensive server smoke test after the code and frozen data are reviewed. Do not run training during planning or implementation review.
4. Review code revision, data hash, output schema, seed list, exact train/dev/test items, expected artifacts, and run command. Obtain explicit execution approval.
5. On Jane, verify the approved revision and clean working tree, then run the documented command using the server's `.venv`. Preserve run-ID-specific JSON bundle and log; record provenance before outputs are created.
6. Validate completeness, schema, checksums, preflight, initial-weight equality, 2,250/2,250 update count, and item-level results. Analyze only after validation; preserve failed attempts and report deviations.

## Required scripts, data, and artifacts

These paths are **planned outputs**, not existing functionality:

- `experiments/run_cvc_transfer_v3.py` — preflight-first runner, with unique run ID and resumable failure preservation.
- `experiments/cvc_transfer/model.py` — minimal runner-owned implementation of the historical Transformer; it must not import the removed `harness.learner` package. Record the source revision and verify the 260 output dimension and weight tying.
- `experiments/data/cvc_transfer_v3.json` — immutable v3 copy of condition strings, items, vocabulary configuration, seeds, metric definitions, and bootstrap parameters.
- `experiments/results/cvc_transfer_v3/<run-id>.json` and `<run-id>.log` — result bundle and progress/provenance log.
- `experiments/results/cvc_transfer_v3/<run-id>-preflight.json` and `.log` — preflight evidence, if kept separate from the main bundle.
- Raw per-item and per-seed baseline/final metrics, full 260-way and letter-conditional scores, invalid special-token mass, training trajectory, actual interpreter/environment, code/data hashes, and exact condition text.
- Completed scientific-method record in this vault, with failed attempts, deviations, measured results, limitations, and links to all artifacts.

## Implementation dependency and compute

The current `experiments/run_cvc_transfer_v2.py` imports model/config/tokenizer modules from `harness.learner`, but the `harness/` directory was removed from the current repository. Therefore the current runner cannot be reused as-is from this checkout. Implementation must provide the small runner-owned model module listed above, based on the historical source revision, and validate its architecture before any full training.

The planned model has about 25.45M parameters and the same 2,250 updates as the completed v2 run. The v2 CPU run took about 11 minutes on Jane; v3 is expected to be similar or somewhat faster, but that is an estimate, not a measured runtime. The v2 record has no peak-memory measurement, so memory requirements remain unmeasured. Use Jane's `.venv`/CPU for the eventual run; the Chromebook is not the recommended training host. Measure memory in the approved smoke test before full execution.

## Results

Not run. This protocol contains no v3 measurements. Record results only after an approved run and artifact validation. Keep the v2 run and its conclusions unchanged.

## Interpretation and conclusion

Pending results. A positive primary contrast with an interval above zero would support a phonics advantage on these fixed far items under the corrected output vocabulary, not broad word generalization. Similar gains across conditions, or full-vocabulary improvements without a letter-conditional gain, would favor generic exposure/output calibration explanations. An interval spanning zero is inconclusive about small effects; it is not evidence of equivalence. Any claim is limited by the eight fixed far items and by prior exposure of researchers to their v2 outcomes.

## Possible next experiments

- If the letter-conditional outcome remains inconclusive, preregister a larger independently sourced and sealed CVC item set before any further fitting.
- If the corrected vocabulary yields a clear treatment effect, test whether it replicates on that independent item set before making broad transfer claims.

## Related

- Prior experiment and analysis: [[2026-10-25 Controlled CVC Transfer Replication]] and [[2026-10-25 Controlled CVC Transfer Replication - Completed Run]]
- [[00-System/Experiment Workflow|Experiment Workflow Guide]]
- [[00-System/Documentation Standard|Documentation Standard]]
- Frozen v2 source data for protocol comparison: `experiments/data/cvc_transfer_v2.json` (copy to v3; do not edit in place)
- Historical model implementation source: commit `2372f9155ec901a6fc804a9970e2c8898ccac3c8`
