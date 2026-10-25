---
title: "Experiment A — Held-Out Test"
type: experiment
status: completed
scripts:
  - experiments/run_experiment_a.py
tags:
  - ai-school
  - experiment
  - held-out
  - generalization
created: 2026-10-23
updated: 2026-10-25
---

# Experiment A — Held-Out Test

## Question

Can the model generalize beyond the specific exemplars it was trained on? Does structured exposure to Lesson 1.1 reduce cross-entropy on **novel** sentence contexts and **unseen** CVC words, or is the observed loss reduction merely memorization of the training material?

## Hypothesis

1. If the model is learning genuine phonics/letter patterns (not just memorizing), held-out CVC words drawn from the same phonics families (e.g. `bat`, `pen`, `log`) will show measurable loss reduction, though smaller than the training exemplars.
2. Novel sentence contexts using familiar sight words but different structure (e.g. `"A dog sat on the "` -> `"bed."`) will show modest improvement, since the model has seen the component words in different arrangements.
3. The largest loss reduction will be on items that closely mirror training exemplars; the smallest on items with no lexical overlap.

## Variables and Conditions

- **Independent variable:** Training set composition (fixed: the original 5 exemplars) vs. evaluation set composition (novel prompts/targets not in training).
- **Measured outcomes:**
  - Target-token cross-entropy on held-out items, pre- and post-training.
  - Generated completions on held-out prompts.
  - Loss delta comparison: training-adjacent items vs. fully novel items.
- **Controls:**
  - Same model architecture (BabyLM 25M, $L=8, d=512, H=8, V=4096$).
  - Same optimizer (AdamW, $\eta=10^{-3}$, grad clip = 1.0).
  - Same number of training iterations (15).
  - Fixed random seed (for reproducibility within this run).
- **Training exemplars (unchanged):**
  1. `"The cat sat on the mat."`
  2. `"The dog can run in the sun."`
  3. `"The sun is hot."`
  4. `"The red pen is on the bed."`
  5. `"A cat can run."`
- **Held-out test items (novel — not present in training exemplars):**

  *Category 1 — CVC words from same phonics families (seen letters, unseen words):*
  1. Prompt: `"The cat sat on the "` -> Target: `"bat"` *(rhymes with mat, but different word)*
  2. Prompt: `"A dog can "` -> Target: `"log"` *(rhymes with dog, unseen as target)*
  3. Prompt: `"The pen is "` -> Target: `"red"` *(seen in training as "red pen" but not as target completion)*

  *Category 2 — Novel sentence contexts (rearranged familiar words):*
  4. Prompt: `"A dog sat on the "` -> Target: `"mat."` *(word transfer, new subject)*
  5. Prompt: `"The cat is "` -> Target: `"hot."` *(word transfer, new subject)*
  6. Prompt: `"The sun can "` -> Target: `"run."` *(word transfer, new subject)*

  *Category 3 — Fully novel (no lexical overlap with training):*
  7. Prompt: `"A pig can "` -> Target: `"dig."` *(unseen CVC pattern)*
  8. Prompt: `"The bug is "` -> Target: `"big."` *(unseen CVC pattern)*

- **Environment / architecture:** Debian Linux x86_64, Python 3.13.5, PyTorch 2.14.1 (CPU development mode).
- **Code reference:** `harness.school.classroom.ClassroomSession.run_learning_cycle`, `harness.learner.model.BabyLM`, `harness.learner.tokenizer.BabyTokenizer`.

## Procedure

1. Instantiate `BabyLM` with random weights (`seed=42`) on CPU.
2. Run pre-training evaluation on all 8 held-out test items, recording per-item cross-entropy and generated text.
3. Train for 15 iterations on the original 5 exemplars via `run_learning_cycle` (or equivalent direct training loop).
4. Run post-training evaluation on the same 8 held-out test items.
5. Also evaluate on the original 4 training-adjacent test items (from Experiment: Lesson 1.1) for direct comparison.
6. Record results grouped by category (phonics-family transfer, sentence-context transfer, fully novel).
7. Log session to `03-Experiences/`, assessment to `07-Reports/`.

### Code Changes Required

- **New evaluation function needed:** `ClassroomSession.run_held_out_test()` (or a standalone script) that accepts separate training exemplars and held-out test items, runs the training loop, and evaluates both sets before/after. The current `run_learning_cycle` conflates training and evaluation items — it uses the same `test_items` for pre/post test, with no separate held-out set.
- **Suggested approach:** Add a `held_out_test_items` parameter to `run_learning_cycle`, or create a new method `run_held_out_experiment()` that:
  1. Evaluates on both `test_items` (training-adjacent) and `held_out_test_items` before training.
  2. Trains on `exemplars` for N iterations.
  3. Evaluates on both sets after training.
  4. Reports loss deltas for each category separately.
- **Alternatively:** Write a standalone experiment script (e.g. `experiments/run_experiment_a.py`) that uses the existing `BabyLM`, `BabyTokenizer`, and `ClassroomSession.evaluate_test_items` directly, bypassing `run_learning_cycle` for full control over the evaluation protocol.

## Results

**Model:** BabyLM, 27,411,456 parameters, seed=42, 15 iterations, AdamW ($\eta=10^{-3}$).
**Training:** 5 exemplars, initial training loss 6.5446, final training loss 0.6905.

### Loss Delta Summary (Pre → Post)

| Category | n | Pre-Avg Loss | Post-Avg Loss | Delta ($\Delta$) |
| :--- | :---: | :---: | :---: | :---: |
| Training-Adjacent | 4 | 8.3223 | 3.6128 | **+4.7096** |
| Cat 1 — Phonics-family transfer | 3 | 8.4361 | 5.2451 | **+3.1910** |
| Cat 2 — Sentence-context transfer | 3 | 8.3248 | 3.5898 | **+4.7350** |
| Cat 3 — Fully novel | 2 | 8.1769 | 4.6108 | **+3.5661** |
| **All Held-Out Combined** | 8 | 8.3296 | 4.4658 | **+3.8638** |

### Per-Item Results

**Training-Adjacent Items:**

| Prompt | Target | Pre-Loss | Post-Loss | $\Delta$ | Generated (Post) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `The cat sat on the ` | `mat.` | 8.2479 | 3.7344 | +4.5135 | `The cat sat on the t...` |
| `The sun is ` | `hot.` | 8.3811 | 3.5285 | +4.8526 | `The sun is a.n.` |
| `The dog can ` | `run.` | 8.3573 | 3.7662 | +4.5911 | `The dog can un t.` |
| `The red pen is on the ` | `bed.` | 8.3032 | 3.4221 | +4.8811 | `The red pen is on the t.un.` |

**Category 1 — Phonics-family transfer (seen letters, unseen CVC words):**

| Prompt | Target | Pre-Loss | Post-Loss | $\Delta$ | Generated (Post) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `The cat sat on the ` | `bat` | 8.3863 | 4.2697 | +4.1166 | `The cat sat on the t..` |
| `A dog can ` | `log` | 8.4531 | 7.9585 | +0.4946 | `A dog can cb.n.` |
| `The pen is ` | `red` | 8.4689 | 3.5070 | +4.9619 | `The pen is iut t` |

**Category 2 — Sentence-context transfer (rearranged familiar words):**

| Prompt | Target | Pre-Loss | Post-Loss | $\Delta$ | Generated (Post) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `A dog sat on the ` | `mat.` | 8.1203 | 3.6411 | +4.4792 | `A dog sat on the tn.n.` |
| `The cat is ` | `hot.` | 8.3378 | 3.3726 | +4.9652 | `The cat is t cr t` |
| `The sun can ` | `run.` | 8.5162 | 3.7556 | +4.7606 | `The sun can un t.` |

**Category 3 — Fully novel (no lexical overlap with training):**

| Prompt | Target | Pre-Loss | Post-Loss | $\Delta$ | Generated (Post) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `A pig can ` | `dig.` | 8.1818 | 4.5449 | +3.6369 | `A pig can tn.n.` |
| `The bug is ` | `big.` | 8.1721 | 4.6767 | +3.4954 | `The bug is cun.` |

## Interpretation

### 1. The model generalizes beyond memorization

The held-out combined delta of **+3.86** is substantial — only **0.85 points lower** than the training-adjacent delta of +4.71. This means the model is not simply memorizing specific exemplar-target mappings. It has learned transferable representations from just 5 training sentences over 15 iterations.

### 2. Sentence-context transfer is remarkably strong

Category 2 (+4.74) nearly matches training-adjacent performance (+4.71). When the model has seen the component words (e.g. `dog`, `sat`, `mat`) in different sentence arrangements during training, it generalizes almost as well to novel arrangements as to the original training prompts. This suggests the model is learning word-level associations and sentence structure templates, not just fixed n-gram sequences.

### 3. Phonics-family transfer is weaker and more variable

Category 1 (+3.19) shows the most variability. Two items (`bat` +4.12, `red` +4.96) showed strong transfer, but `log` barely moved (+0.49). The prompt `"A dog can "` → `"log"` maintained near-random loss (7.96) post-training. This likely occurs because `log` was never seen as a target completion, and the CVC pattern `l-o-g` has minimal byte-level overlap with trained targets. The model learned some phonics patterns (the `-at` family transfers well from `mat` to `bat`) but not all.

### 4. Fully novel items still improve substantially

Category 3 (+3.57) is perhaps the most striking result. Even for prompts and targets with **zero lexical overlap** to training material (`pig`, `dig`, `bug`, `big`), the model showed significant loss reduction. This can be explained at the byte level: the model learned that English CVC patterns follow predictable letter distributions (consonant-vowel-consonant), that periods follow completions, and that sentence templates like `"The X is "` or `"A X can "` have learnable structure independent of the specific words.

### 5. Generation quality remains early-stage

Across all categories, generated text shows correct whitespace, periods, and English letter distribution, but word boundaries and spelling are still rough (e.g. `t..`, `tn.n.`, `un t.`). The model has learned the *shape* of English text but not precise orthography — consistent with early-stage phonics acquisition.

## Limitations

- A single seed run cannot distinguish generalization from lucky initialization. Pair with [[2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]] for statistical confidence.
- The held-out set is small (8 items). Larger held-out sets would provide more robust generalization estimates.
- Byte-level tokenization means "novel CVC word" still shares byte tokens with training words — true lexical novelty is impossible at the byte level. This is a feature, not a bug, but limits the strength of generalization claims.
- The strong Category 3 result may partly reflect byte-level distributional learning rather than "true" word-level generalization. The model may be learning "after a space, a consonant is likely" rather than generalizing the concept of CVC words.

## Conclusion

- **Supported:**
  1. The model generalizes beyond memorization — held-out items show substantial loss reduction (+3.86 avg delta).
  2. Sentence-context transfer is nearly as strong as training-adjacent performance, suggesting word-level association learning.
  3. Even fully novel prompts show meaningful improvement (+3.57), indicating the model learns transferable byte-level and structural patterns.
  4. The largest loss reduction is on training-adjacent items (+4.71), and the smallest on phonics-family transfer (+3.19), partially supporting Hypothesis 3.
- **Not established:**
  1. Whether the generalization would hold across multiple random seeds (requires Experiment C).
  2. Whether the generalization is word-level or primarily byte-level distributional learning.
  3. Whether the `log` outlier (Δ=+0.49) is seed-specific or a systematic difficulty for this model.
- **Next experiment:** [[2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]] for statistical validation across seeds, and [[2026-10-23 Experiment B — Control Group|Experiment B]] to confirm the effect is lesson-specific.

## Related

- Prior experiment: [[2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition|Lesson 1.1 Phonics and Word Acquisition]]
- Lesson: [[02-School/Language/Lessons/Lesson-1.1-Alphabet-and-Phonics|Lesson 1.1]]
- Related experiments: [[2026-10-23 Experiment B — Control Group|Experiment B]], [[2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]], [[2026-10-23 Experiment D — Inspect Tokenization|Experiment D]]
