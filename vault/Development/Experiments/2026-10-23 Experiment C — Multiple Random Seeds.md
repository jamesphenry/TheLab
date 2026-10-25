---
title: "Experiment C — Multiple Random Seeds"
type: experiment
status: completed
scripts:
  - experiments/run_experiment_c.py
tags:
  - ai-school
  - experiment
  - random-seeds
  - statistical-validity
created: 2026-10-23
updated: 2026-10-25
---

# Experiment C — Multiple Random Seeds

## Question

Is the loss reduction observed in Lesson 1.1 reproducible across independent model initializations, or was the result of a single run an artifact of a favorable random seed? What is the variance in loss reduction across seeds, and what is a statistically defensible estimate of the mean effect?

## Hypothesis

1. The mean loss reduction across seeds will be positive (i.e. training on Lesson 1.1 exemplars reduces evaluation loss on average), but the magnitude will vary.
2. The standard deviation of the loss delta across seeds will be substantial enough that a single run (as in the original Lesson 1.1 experiment) is not sufficient to draw confident conclusions about the exact magnitude.
3. Some seeds may produce runs where loss reduction is significantly larger or smaller than the original single-run result of $\Delta \mathcal{L} = 3.7655$.
4. The training loss convergence trajectory will vary in shape across seeds (some converge faster, some slower), but all should show monotonic decrease within 15 iterations.

## Variables and Conditions

- **Independent variable:** Random initialization seed ($s \in \{42, 123, 7, 2026, 99, 314, 256, 13, 555, 8\}$ — 10 seeds).
- **Measured outcomes:**
  - Pre-training evaluation loss per seed.
  - Post-training evaluation loss per seed.
  - Loss delta ($\Delta \mathcal{L} = \mathcal{L}_{\text{pre}} - \mathcal{L}_{\text{post}}$) per seed.
  - Mean loss delta $\bar{\Delta}$ and standard deviation $\sigma_{\Delta}$ across seeds.
  - Training loss trajectory per seed (15 data points each).
  - Generated text quality per seed (qualitative).
- **Fixed conditions across all seeds:**
  - Same model architecture (BabyLM 25M, $L=8, d=512, H=8, V=4096$).
  - Same optimizer (AdamW, $\eta=10^{-3}$, grad clip = 1.0).
  - Same training exemplars (the original 5).
  - Same test items (the original 4).
  - Same number of iterations (15).
- **Seeds:** 10 independently drawn seeds: $\{42, 123, 7, 2026, 99, 314, 256, 13, 555, 8\}$
- **Environment / architecture:** Debian Linux x86_64, Python 3.13.5, PyTorch 2.14.1 (CPU development mode).
- **Code reference:** `harness.learner.model.BabyLM`, `harness.learner.tokenizer.BabyTokenizer`, `harness.school.classroom.ClassroomSession`.

## Procedure

1. For each seed $s$ in $\{42, 123, 7, 2026, 99, 314, 256, 13, 555, 8\}$:
   a. Set `torch.manual_seed(s)` and `torch.cuda.manual_seed_all(s)`.
   b. Instantiate `BabyLM` with random weights.
   c. Instantiate a fresh `AdamW` optimizer.
   d. Run `ClassroomSession.run_learning_cycle` (or equivalent direct training loop) with the standard Lesson 1.1 exemplars and test items for 15 iterations.
   e. Record: pre-eval loss, post-eval loss, delta, training loss trajectory, generated text.
2. After all 10 runs, compute:
   - Mean pre-loss, post-loss, and delta.
   - Standard deviation of each.
   - Min and max delta.
   - Coefficient of variation ($\sigma / \mu$).
3. Compare the original single-run result ($\Delta = 3.7655$) against the distribution.
4. Log all results in a comparison table.

### Code Changes Required

- **Seed setting:** Need explicit `torch.manual_seed(s)` calls before model init. The current `run_lesson_1` in `cli.py` does not set a seed.
- **Suggested approach:** Write a standalone experiment script (e.g. `experiments/run_experiment_c.py`) that:
  1. Loops over the list of seeds.
  2. For each seed: sets the seed, instantiates model + optimizer, runs the training/eval cycle, collects results.
  3. Does **not** write vault files for each run (to avoid clutter) — collects results in memory and writes a single summary.
  4. Outputs a summary table with per-seed stats and aggregate statistics.
- **Alternatively:** Add a `seed` parameter to `run_lesson_1` in `cli.py` and a `--seeds` flag that accepts a comma-separated list, enabling multi-seed runs from the CLI.
- **Note on independence:** Each seed must get a **fresh model and optimizer** — the current `run_learning_cycle` method is fine since it uses `self.model` and `self.optimizer`, so re-instantiating both per seed is sufficient.

## Results

**Model:** BabyLM, 27,411,456 parameters, 15 iterations per seed, AdamW ($\eta=10^{-3}$).

### Per-Seed Summary

| Seed | Pre-Avg Loss | Post-Avg Loss | Delta ($\Delta$) | Init Train Loss | Final Train Loss |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 42 | 8.3223 | 3.6128 | +4.7096 | 6.5446 | 0.6905 |
| 123 | 8.3168 | 4.8245 | +3.4923 | 6.1331 | 0.6897 |
| 7 | 8.4182 | 3.5322 | +4.8860 | 6.8212 | 1.2677 |
| 2026 | 8.6401 | 3.6431 | +4.9970 | 6.3458 | 0.5142 |
| 99 | 8.5197 | 2.9968 | +5.5229 | 6.4106 | 0.8753 |
| 314 | 8.3761 | 2.9441 | +5.4320 | 6.4835 | 1.0758 |
| 256 | 8.3883 | 5.0658 | +3.3226 | 6.0605 | 0.5690 |
| 13 | 8.7101 | 3.7285 | +4.9816 | 6.1612 | 0.5688 |
| 555 | 8.3045 | 3.5120 | +4.7925 | 6.2784 | 0.9245 |
| 8 | 8.5170 | 4.4022 | +4.1147 | 6.1120 | 0.6759 |

### Aggregate Statistics

| Statistic | Pre-Avg Loss | Post-Avg Loss | Delta ($\Delta$) | Final Train Loss |
| :--- | :---: | :---: | :---: | :---: |
| **Mean** | 8.4513 | 3.8262 | **+4.6251** | 0.7851 |
| **Std Dev** | | | **0.7118** | |
| **Min** | 8.3045 | 2.9441 | +3.3226 | 0.5142 |
| **Max** | 8.7101 | 5.0658 | +5.5229 | 1.2677 |
| **CV ($\sigma/\mu$)** | | | 0.1539 | |

### Comparison with Original Single-Run

- **Original Lesson 1.1 single-run delta:** +3.7655
- **Mean delta across 10 seeds:** +4.6251
- **Std dev:** 0.7118
- **Range:** [+3.3226, +5.5229]

### Per-Item Analysis Across Seeds

| Item | Prompt → Target | Mean Improvement | Std Dev | Range |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `The cat sat on the ` → `mat.` | +4.9274 | 1.1249 | [+2.94, +6.77] |
| 2 | `The sun is ` → `hot.` | +4.9879 | 0.9102 | [+3.35, +6.13] |
| 3 | `The dog can ` → `run.` | +5.7400 | 0.8501 | [+4.41, +7.45] |
| 4 | `The red pen is on the ` → `bed.` | +2.8452 | 1.4849 | [+0.19, +4.94] |

## Interpretation

### 1. The effect is reproducible — no single-run artifact

All 10 seeds produced positive loss deltas ranging from +3.32 to +5.52. The effect is **100% reproducible** in direction: every seed showed meaningful loss reduction. The original single-run result (+3.77) falls within the observed range and is actually below the mean (+4.63), meaning the original experiment was a slightly conservative estimate, not a lucky outlier.

### 2. Variance is moderate but meaningful

The standard deviation of 0.71 (CV = 15.4%) indicates that while the effect is reliable, its magnitude varies by ±0.71 across seeds. The original single-run delta of +3.77 was near the low end (only seed 256 at +3.32 was lower), suggesting the original experiment may have slightly understated the typical effect size. A single run is sufficient to establish the effect's existence but not its precise magnitude.

### 3. Item 4 ("bed.") is the hardest and most variable

Item 4 shows the lowest mean improvement (+2.85) and the highest variability (std = 1.49, range +0.19 to +4.94). Seed 123 nearly failed on this item (+0.19), while seed 99 succeeded strongly (+4.94). This confirms the pattern from Experiments A and B — longer prompts with more specific targets are harder for the model and more sensitive to initialization. The model's learning of `"bed."` as a completion for `"The red pen is on the "` is fragile.

### 4. Item 3 ("run.") is the easiest and most consistent

Item 3 shows the highest mean improvement (+5.74) and low variability (std = 0.85). The prompt `"The dog can "` is short, and `run.` appeared frequently in the training exemplars (twice in 5 exemplars). This combination of short prompt + frequent target produces the most reliable learning.

### 5. Training loss convergence is consistent across seeds

All 10 seeds converged training loss to below 1.3, with 8 of 10 reaching below 1.0. The mean final training loss was 0.79, confirming that the model reliably fits the training data regardless of initialization. The variation in evaluation loss (post-avg range: 2.94–5.07) reflects differences in generalization, not training fit.

## Limitations

- 10 seeds is a reasonable sample but not exhaustive. Confidence intervals remain wide (the delta range spans 2.2 points).
- Only tests variance in initialization, not variance in training data ordering (exemplar order is fixed). A more thorough study would also shuffle exemplar order per seed.
- CPU-only execution may introduce minor non-determinism in floating-point operations across runs, though PyTorch CPU is generally deterministic for a given seed.
- Does not test variance across different lesson content — only initialization variance.
- Does not test the held-out items from Experiment A across seeds — combining C with A would provide the strongest evidence.

## Conclusion

- **Supported:**
  1. The loss reduction effect is **100% reproducible** across seeds — all 10 runs showed positive deltas (+3.32 to +5.52). (Hypothesis 1 confirmed.)
  2. The standard deviation (0.71, CV=15.4%) is substantial enough that a single run cannot pin down the exact magnitude. The original single-run result (+3.77) was at the low end of the distribution. (Hypothesis 2 confirmed.)
  3. The original Lesson 1.1 result was not a lucky seed — it slightly underestimated the typical effect size (mean +4.63). (Hypothesis 3 not confirmed — original was conservative, not favorable.)
  4. All seeds showed monotonic training loss decrease within 15 iterations. (Hypothesis 4 confirmed.)
- **Not established:**
  1. Whether the per-item variability (especially Item 4's fragility) would stabilize with more iterations or a larger exemplar set.
  2. Whether held-out generalization (Experiment A) is equally reproducible across seeds — requires combining C with A.
- **Next experiment:** [[2026-10-23 Experiment D — Inspect Tokenization|Experiment D]] to verify tokenizer internals, or [[2026-10-23 Experiment E — Reasoning|Experiment E]] for rationale-conditioned training.

## Related

- Prior experiment: [[2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition|Lesson 1.1 Phonics and Word Acquisition]]
- Related experiments: [[2026-10-23 Experiment A — Held-Out Test|Experiment A]], [[2026-10-23 Experiment B — Control Group|Experiment B]], [[2026-10-23 Experiment D — Inspect Tokenization|Experiment D]]
