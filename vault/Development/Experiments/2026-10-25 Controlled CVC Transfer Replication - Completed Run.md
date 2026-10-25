---
title: Controlled CVC Transfer Replication — Completed Run
type: experiment
status: completed
scripts:
  - experiments/run_cvc_transfer_v2.py
tags:
  - ai-school
  - experiment
  - cvc
  - transfer
  - completed-run
created: 2026-10-25
updated: 2026-10-25
changelog:
  - date: 2026-10-25
    change: Linked this detailed result analysis to the canonical experiment record, which now includes the procedure, summary results, and conclusion.
reviewed: complete
---

# Controlled CVC Transfer Replication — Completed Run

## Question

Does training on the original Lesson 1.1 sentences improve next-letter probabilities for unseen CVC words whose final two-letter sequences are absent from phonics training, beyond character-frequency and generic-English exposure effects?

This is a narrow byte-level spelling-completion probe. It does not test word meaning, pronunciation, phoneme awareness, or reliable free-form word generation. The canonical scientific-method record, including the frozen protocol and experiment conclusion, is [[2026-10-25 Controlled CVC Transfer Replication]].

## Hypothesis

The planned hypothesis was that phonics training would reduce full-head target-letter NLL on the eight far items more than the byte-multiset-matched shuffled control, with the five near items serving as a positive-control stratum. The hypothesis was **not supported** by the completed run: the average far-item contrast favored shuffled training, and its seed-bootstrap interval included zero.

## Variables and Conditions

- **Independent variable:** training corpus condition: phonics, fixed shuffled strings, or unrelated English.
- **Stratification:** near items have a final two-letter sequence occurring in the phonics examples; far items do not.
- **Measured outcomes:** full 4096-class target NLL (primary), target NLL renormalized over 26 lowercase letters (diagnostic), unrestricted and letter-restricted greedy next-letter accuracy, target rank, and probability mass assigned to impossible output IDs.
- **Model:** BabyLM with a 4096-token output head, maximum sequence length 256, embedding dimension 512, 8 layers, 8 heads, MLP ratio 4, and dropout 0.0. The tokenizer emits 260 IDs (four special tokens plus byte IDs).
- **Optimizer:** AdamW, learning rate `1e-3`, betas `(0.9, 0.999)`, epsilon `1e-8`, weight decay `0.01`, no AMSGrad, gradient clipping norm `1.0`.
- **Control details:** shuffled strings preserve each phonics sentence's byte multiset and length while disrupting order. Unrelated English is not byte-count matched. Exposure counts and exact strings are in the plan and raw bundle; “far” is defined relative to phonics, not every control.
- **Data overlap:** the preflight passed whole-word overlap, character coverage, split disjointness, suffix-classification, and frozen exposure checks. None of the 13 complete final-test words appears in the training strings. Development and final-test words/prompts are disjoint. The full split and item list are in the linked plan and `experiments/data/cvc_transfer_v2.json`.

## Run Provenance

- **Run ID:** `cvc-transfer-20261025-retry03`.
- **Status:** completed; 10 seeds, 30 trained condition arms, and 2,250/2,250 optimizer updates.
- **Run time:** 2026-10-25 09:52:29–10:03:40 UTC.
- **Repository:** branch `codex/cvc-transfer-v2-runner`; runner/data revision `a6191dfa4b9e3937daf147baddb1c1e031d7012f`. The run-artifact commit is `0c1a6f83528fd309401288f5b645545c0af2c9ad`.
- **Runner / data:** `experiments/run_cvc_transfer_v2.py`, SHA-256 `4279cc7ff60cb2626b5cc501ee2025e6f5cf767ea610ba6b636c39a334844357`; `experiments/data/cvc_transfer_v2.json`, SHA-256 `2c51b7d109972d19c47efcbd93e3d03bb79d02bcf2f1bd3029ddf47529e93590`.
- **Actual execution command on Jane:** `.venv/bin/python experiments/run_cvc_transfer_v2.py --run-id cvc-transfer-20261025-retry03 --device cpu` (launched with `nohup` so the run survived the SSH session).
- **Environment:** Jane (`jane`), Python 3.11.2, PyTorch `2.14.1+cpu`, CPU device. CUDA was unavailable to this venv despite a Tesla P4 being present on the host. No checkpoint was selected; each arm used the final weights after exactly 15 passes.
- **Paired initialization:** one initial state per seed was cloned to each arm. All tensor-by-tensor equality checks and raw-payload SHA-256 comparisons passed. The ten initial-state digests and condition checks are in the bundle.
- **Artifacts:** `experiments/results/cvc_transfer_v2/cvc-transfer-20261025-retry03.json` and `experiments/results/cvc_transfer_v2/cvc-transfer-20261025-retry03.log`. Both are committed to `origin` in the run-artifact commit above.
- **Provenance caveats:** the bundle's `command` field says `python3`, while the actual invocation used `.venv/bin/python`; the actual command is recorded above. Its Git status also reports the run's own log as untracked because the status was captured after that log was created. The checkout was verified clean at launch at `a6191df`; this is not evidence of unrelated pre-run modifications. The runner was subsequently fixed to capture provenance before creating outputs and to record the actual interpreter in future runs.

## Procedure

1. Run the frozen, standard-library-only preflight before any model construction. It passed for this protocol.
2. For each of ten predeclared seeds (`42, 123, 7, 2026, 99, 314, 256, 13, 555, 8`), evaluate the untrained baseline, clone its initial state, and verify identical tensors for all three conditions.
3. Train each arm for 15 passes over five strings (75 optimizer updates per arm), using a fresh AdamW optimizer for each condition. This yielded 2,250 updates total. No early stopping or checkpoint selection was used.
4. Evaluate four development items and all 13 final items after training. The final items were five near (`bat`, `bun`, `pot`, `hen`, `bog`) and eight far (`dig`, `sip`, `bit`, `tag`, `cup`, `mud`, `hid`, `rib`). The complete prompts, targets, and fixed training strings are in the plan and frozen data file.
5. Score deterministic one-byte completion with unrestricted 4096-class and lowercase-letter-restricted greedy decoders. Retain all seed-by-item baseline and final outputs in the result bundle.

The complete condition strings were:

- **Phonics:** `The cat sat on the mat.`; `The dog can run in the sun.`; `The sun is hot.`; `The red pen is on the bed.`; `A cat can run.`
- **Shuffled:** `Tsh toc hae tn tta eam.`; `Trd oia hgn tsu cn eun hne.`; `Tio sth ue hsn.`; `Ten bie eoh hd re psd etn.`; `A car nut can.`
- **Unrelated English:** `The system processes data files.`; `Network latency affects throughput.`; `Database queries return results.`; `The compiler optimizes register allocation.`; `Memory allocation requires careful management.`

## Results

### Run attempts

| Run ID | Outcome | Evidence |
| --- | --- | --- |
| `preflight-20261025-2837ee0` | Preflight passed; no model or training. | `experiments/results/cvc_transfer_v2/preflight-20261025-2837ee0.json` and `.log` |
| `cvc-transfer-20261025-main` | Failed before model construction: default `/usr/bin/python3` had no PyTorch. | `experiments/results/cvc_transfer_v2/cvc-transfer-20261025-main.json` and `.log` |
| `cvc-transfer-20261025-retry01` | Interrupted before the first saved seed. Python-level storage-byte conversion was prohibitively slow; zero optimizer updates. | `experiments/results/cvc_transfer_v2/cvc-transfer-20261025-retry01.json` and `.log` |
| `cvc-transfer-20261025-retry02` | Failed at paired-state digest verification before any condition arm. Later diagnostics confirmed tensor equality and equal raw payloads; serialized archive metadata caused the mismatch. Zero optimizer updates. | `experiments/results/cvc_transfer_v2/cvc-transfer-20261025-retry02.json` and `.log` |
| `cvc-transfer-20261025-retry03` | Completed; validated against the frozen protocol. | Bundle and log linked above. |

The three failed/interrupted full-run attempts are retained and are not included in the completed run's measurements.

### Measured aggregate results

“Full-head gain” is baseline mean full-head NLL minus final mean full-head NLL; positive means the target's NLL decreased. “26-letter gain” is the same difference after renormalizing over lowercase letters; negative means target NLL increased within that set.

| Condition | Stratum | Full-head gain | 26-letter NLL gain | Letter-restricted exact | Full-head exact | Final impossible-ID mass |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Phonics | Near (5 items) | +1.829 | −1.253 | 5/50 (10%) | 3/50 (6%) | 0.80% |
| Phonics | Far (8 items) | +1.130 | −2.762 | 3/80 (3.75%) | 0/80 | 0.55% |
| Shuffled | Near (5 items) | +2.821 | −1.005 | 4/50 (8%) | 3/50 (6%) | 0.38% |
| Shuffled | Far (8 items) | +2.359 | −1.238 | 4/80 (5%) | 1/80 (1.25%) | 0.53% |
| Unrelated English | Near (5 items) | +2.938 | −1.924 | 0/50 | 0/50 | 0.81% |
| Unrelated English | Far (8 items) | +1.732 | −3.092 | 0/80 | 0/80 | 1.13% |

The preregistered primary contrast was the per-seed far-item phonics gain minus shuffled gain:

- **Mean:** −1.229 NLL units; **median:** −1.319; **sample SD:** 2.254.
- **95% percentile bootstrap interval over the ten seeds:** [−2.514, 0.086], 10,000 resamples, bootstrap seed `20261025`.
- The seed-level contrast was negative for seven seeds and positive for three. The inferential resampling unit is seeds; the final set remains eight fixed far words, not 80 independent words.

### Output-space diagnostic and item-level failures

At baseline, mean probability mass on the 26 lowercase letters was approximately 0.65% for both strata, while mean mass on impossible output IDs (IDs 260–4095) was about 93.6%. After training, the impossible-ID mass fell to 0.38–1.13% across conditions/strata, and lowercase-letter-set mass rose to 40–85%. Despite that shift, target NLL **within the 26 letters worsened in every aggregate condition/stratum**. The full-head NLL reductions therefore do not demonstrate that probability was selectively assigned to the correct target letter; much of the change reflects learning to avoid impossible outputs and to emit letters generally.

Far-item summary (mean full-head gain across seeds; letter-restricted correct predictions out of ten):

| Item | Phonics | Shuffled | Unrelated English |
| --- | ---: | ---: | ---: |
| `dig` | +0.465; 0/10 | +2.601; 0/10 | +1.038; 0/10 |
| `sip` | +1.077; 0/10 | +1.810; 0/10 | +2.690; 0/10 |
| `bit` | +0.116; 0/10 | +1.709; 0/10 | +3.619; 0/10 |
| `tag` | +2.200; 0/10 | +1.826; 0/10 | +1.924; 0/10 |
| `cup` | +0.246; 0/10 | +0.423; 0/10 | +2.067; 0/10 |
| `mud` | +1.019; 1/10 | +4.170; 1/10 | −0.184; 0/10 |
| `hid` | +2.945; 2/10 | +4.265; 3/10 | −0.031; 0/10 |
| `rib` | +0.973; 0/10 | +2.070; 0/10 | +2.737; 0/10 |

Across all far predictions, the phonics letter-restricted decoder chose `h` 37/80 times and `n` 15/80 times; the unrelated-English decoder chose `e` 43/80 times. Exact failures and every raw prediction are in the bundle. Full-head greedy accuracy was zero for phonics and unrelated English on far items, and one correct output for shuffled.

## Interpretation

**Observed:** all three conditions substantially reduced full-head target NLL on average, but the shuffled condition's far-item gain exceeded phonics, and the unrelated-English arm also improved full-head NLL. Exact target-letter selection remained rare. The large reduction in impossible-ID mass coincided with a rise in overall lowercase-letter mass; target likelihood normalized within lowercase letters declined in every condition.

**Inferred, bounded:** this run does not establish ordered phonics transfer to unseen CVC completions. The strong full-head NLL changes are compatible with output-space calibration—moving probability from impossible IDs toward valid letters—rather than learning the correct continuation. The shuffled result is consistent with generic byte-frequency or other non-phonics effects, but the controls do not isolate every alternative: shuffled strings destroy natural order/syntax, and unrelated English differs in length and byte exposure. The negative primary contrast and its interval do not support the planned phonics-over-shuffle advantage on these fixed items.

## Limitations

- The output head has 4096 classes while the tokenizer emits only 260 IDs. This confound dominates interpretation of full-head NLL and remains unresolved in this run.
- Only eight fixed far items and five near items were tested. Seeds measure initialization sensitivity, not item-population uncertainty; no broad word-generalization claim follows.
- Exact letter selection was low, and the prefix does not uniquely determine a CVC word. The task probes byte-level spelling distributions, not reading or phonological concepts.
- The unrelated-English arm is not byte-count matched. The shuffled arm preserves byte multisets but destroys ordered n-grams and natural syntax. Some suffix exposure occurs in controls; see the frozen exposure audit in the plan and bundle.
- Results use a CPU-only PyTorch build on Jane; the host GPU was unavailable to that environment. The run completed, but no GPU comparison was made.
- The run bundle records its own log as untracked and has a `command` field naming `python3`; the actual `.venv/bin/python` invocation and clean pre-run checkout were independently verified and are recorded above. The runner was corrected after this run; the original result bundle remains unmodified.
- No checkpoints were retained; the protocol used the fixed final checkpoint, and per-item outputs plus code/data hashes are preserved.

## Conclusion

- **Supported:** the three training regimes shifted probability away from impossible output IDs and reduced full-head target NLL on average for these fixed evaluation items. This describes measured behavior, not successful completion.
- **Not established:** an ordered-phonics advantage over the shuffled control; generalization to a wider population of CVC words; meaningful word completion; phoneme awareness; or preschool learning capability.
- **Next experiment:** preregister a separate protocol with an output head matched to the 260-token tokenizer (or a clearly justified target-letter objective), retaining a leakage-checked held-out word set and matched controls. Treat it as a new model/protocol version; do not revise this run's data or historical claims.

## Related

- Canonical experiment record and frozen protocol: [[2026-10-25 Controlled CVC Transfer Replication]]
- Workflow and observed execution gotchas: [[00-System/Experiment Workflow|Experiment Workflow]]
- Earlier evidence: [[2026-10-23 Experiment A — Held-Out Test]], [[2026-10-23 Experiment B — Control Group]], [[2026-10-23 Experiment C — Multiple Random Seeds]]
- Run bundle: `experiments/results/cvc_transfer_v2/cvc-transfer-20261025-retry03.json`
- Run log: `experiments/results/cvc_transfer_v2/cvc-transfer-20261025-retry03.log`
- Artifact commit: `0c1a6f83528fd309401288f5b645545c0af2c9ad`
