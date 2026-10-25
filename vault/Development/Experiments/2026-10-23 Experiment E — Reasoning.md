---
title: "Experiment E — Reasoning"
type: experiment
status: completed
scripts:
  - experiments/run_experiment_e.py
tags:
  - ai-school
  - experiment
  - reasoning
  - rationale
  - metacognition
created: 2026-10-23
updated: 2026-10-25
---

# Experiment E — Reasoning

## Question

Can the model apply and explain learned patterns? Specifically:
1. **Answer accuracy:** Does the model produce correct completions on pattern-based tasks (phonics rules, sight word usage, sentence templates)?
2. **Rationale quality:** Can the model generate a plausible explanation for *why* a completion is correct (e.g. "cat ends with -at because it follows the consonant-vowel-consonant pattern")?
3. **Rationale effect:** Does training with explicit rationale (pattern explanations alongside exemplars) improve answer accuracy compared to training on exemplars alone?

## Hypothesis

1. **Answer accuracy will be measurable** but limited — at 15–30 iterations on a small exemplar set, the model will show lower cross-entropy on pattern-based completions than an untrained model, but generated text will still be phonemically rough (consistent with Experiments A and B).
2. **Rationale quality will be poor to nonexistent** — a 25M parameter model trained tabula rasa on 5–15 exemplars does not have the capacity or training depth to generate coherent meta-linguistic explanations like "this word follows the CVC pattern." Any rationale-like output will likely be surface-level pattern repetition, not true explanation.
3. **Training with rationale will not meaningfully outperform training without rationale** at this model scale and training duration. The rationale text adds tokens to the training sequence, but the model lacks the representational capacity to leverage the meta-linguistic signal in only 15–30 iterations. If anything, the rationale tokens may dilute the signal from the exemplar tokens.
4. **Alternative hypothesis:** If rationale training *does* improve accuracy, this would suggest that structured teacher explanations provide useful conditioning context even for small models, pointing toward a curriculum design that includes explanations.

## Variables and Conditions

- **Independent variables:**
  - Training format: exemplars-only vs. exemplars-with-rationale.
  - Evaluation type: direct completion (pattern application) vs. rationale generation (pattern explanation).
- **Measured outcomes:**
  - Cross-entropy loss on direct completion test items (same metric as Experiments A–C).
  - Cross-entropy loss on rationale-generation test items (prompt: explain why the answer is correct).
  - Generated text quality on both completion and rationale prompts.
  - Comparison of loss deltas: rationale-trained vs. exemplar-only-trained model.
- **Training conditions:**
  - **Condition 1 (Exemplars only):** Train on the original 5 Lesson 1.1 exemplars (same as Experiments A–C).
  - **Condition 2 (Exemplars + Rationale):** Train on augmented exemplars that include a brief pattern explanation after each sentence, e.g. `"The cat sat on the mat. mat has the -at sound."` The rationale text uses simple phonics vocabulary the model has been exposed to (letters, patterns, rhyming words).
- **Rationale exemplar format (proposed):**
  1. `"The cat sat on the mat. mat has the -at sound."`
  2. `"The dog can run in the sun. run has the -un sound."`
  3. `"The sun is hot. hot has the -ot sound."`
  4. `"The red pen is on the bed. bed has the -ed sound."`
  5. `"A cat can run. cat has the -at sound."`
- **Test items:**

  *Direct completion (pattern application):*
  1. Prompt: `"The cat sat on the "` -> Target: `"mat."`
  2. Prompt: `"The sun is "` -> Target: `"hot."`
  3. Prompt: `"The dog can "` -> Target: `"run."`
  4. Prompt: `"The red pen is on the "` -> Target: `"bed."`

  *Rationale generation (pattern explanation):*
  5. Prompt: `"The cat sat on the mat. mat has the "` -> Target: `"-at sound."`
  6. Prompt: `"The sun is hot. hot has the "` -> Target: `"-ot sound."`
  7. Prompt: `"The dog can run. run has the "` -> Target: `"-un sound."`
  8. Prompt: `"The red pen is on the bed. bed has the "` -> Target: `"-ed sound."`

- **Controls:**
  - Same model architecture (BabyLM 25M, $L=8, d=512, H=8, V=4096$).
  - Same optimizer (AdamW, $\eta=10^{-3}$, grad clip = 1.0).
  - Same number of iterations (15, or 30 if rationale tokens require more steps).
  - Same seed (seed=42) for direct comparison with Experiments A–C.
  - Both conditions use the same total training budget (same number of gradient steps; rationale exemplars are longer but same count).
- **Environment / architecture:** Debian Linux x86_64, Python 3.13.5, PyTorch 2.14.1 (CPU development mode).
- **Code reference:** `harness.learner.model.BabyLM`, `harness.learner.tokenizer.BabyTokenizer`.

## Procedure

1. Instantiate `BabyLM` with random weights (seed=42) — Condition 1 model.
2. **Condition 1 (Exemplars only):** Train 15 iterations on the original 5 exemplars. Evaluate on all 8 test items (4 direct completion + 4 rationale generation). Record per-item loss and generated text.
3. Instantiate a fresh `BabyLM` with the same seed (seed=42) — Condition 2 model.
4. **Condition 2 (Exemplars + Rationale):** Train 15 iterations on the 5 augmented rationale exemplars. Evaluate on the same 8 test items. Record per-item loss and generated text.
5. Compare loss deltas across conditions for both direct completion and rationale generation items.
6. Qualitatively assess rationale-generated text: does it produce coherent phonics explanations, or just pattern-adjacent noise?
7. Log results.

### Code Changes Required

- **No new harness methods required** — can reuse the same `evaluate_items` and `train_on_exemplars` patterns from Experiments A and B.
- **Suggested approach:** Write a standalone experiment script (`experiments/run_experiment_e.py`) that:
  1. Defines both exemplar sets (with and without rationale) and both test item categories.
  2. Runs Condition 1 (exemplars-only) with pre/post evaluation on all 8 items.
  3. Runs Condition 2 (exemplars+rationale) with pre/post evaluation on all 8 items.
  4. Outputs comparison tables separated by evaluation type (direct vs. rationale).
  5. Includes a qualitative assessment section printing generated rationale text for manual inspection.
- **Considerations:**
  - The rationale exemplars are longer (more tokens) than plain exemplars, so each gradient step updates on more tokens. This is a feature, not a bug — it reflects the real tradeoff of adding explanation text to curriculum.
  - If the model cannot generate coherent rationale (likely at this scale), that is itself a meaningful finding about the limits of meta-linguistic reasoning in small tabula rasa models.

## Results

**Model:** BabyLM, 27,411,456 parameters, seed=42, 15 iterations, AdamW ($\eta=10^{-3}$).

### Loss Delta Summary

| Condition | Direct Completion Δ (items 1-4) | Rationale Generation Δ (items 5-8) |
| :--- | :---: | :---: |
| Condition 1 (Exemplars only) | +4.7096 | +3.1548 |
| Condition 2 (Exemplars + Rationale) | **+5.2326** | **+6.1684** |

### Pre/Post Loss Comparison

| Condition | Direct Pre | Direct Post | Rationale Pre | Rationale Post |
| :--- | :---: | :---: | :---: | :---: |
| Condition 1 (Exemplars only) | 8.3223 | 3.6128 | 8.4594 | 5.3046 |
| Condition 2 (Exemplars + Rationale) | 8.3223 | **3.0897** | 8.4594 | **2.2910** |

### Training Loss

| Condition | Initial Train Loss | Final Train Loss |
| :--- | :---: | :---: |
| Condition 1 (Exemplars only) | 6.5446 | 0.6905 |
| Condition 2 (Exemplars + Rationale) | 5.9501 | 1.1925 |

### Per-Item — Direct Completion (Pattern Application)

| Item | Prompt → Target | Cond 1 Δ | Cond 2 Δ | Winner |
| :---: | :--- | :---: | :---: | :---: |
| 1 | `"The cat sat on the "` → `"mat."` | +4.5135 | **+5.1371** | Cond 2 |
| 2 | `"The sun is "` → `"hot."` | **+4.8526** | +3.4246 | Cond 1 |
| 3 | `"The dog can "` → `"run."` | +4.5911 | **+6.3284** | Cond 2 |
| 4 | `"The red pen is on the "` → `"bed."` | +4.8811 | **+6.0404** | Cond 2 |

### Per-Item — Rationale Generation (Pattern Explanation)

| Item | Prompt → Target | Cond 1 Δ | Cond 2 Δ | Winner |
| :---: | :--- | :---: | :---: | :---: |
| 5 | `"...mat has the "` → `"-at sound."` | +3.7519 | **+5.9154** | Cond 2 |
| 6 | `"...hot has the "` → `"-ot sound."` | +3.4008 | **+6.3824** | Cond 2 |
| 7 | `"...run has the "` → `"-un sound."` | +3.7234 | **+6.6567** | Cond 2 |
| 8 | `"...bed has the "` → `"-ed sound."` | +1.7431 | **+5.7190** | Cond 2 |

### Sample Generated Text (Post-Training)

**Direct Completion:**

| Item | Cond 1 Generated | Cond 2 Generated |
| :---: | :--- | :--- |
| 1 | `The cat sat on the n..ed.` | `The cat sat on the un.auta` |
| 2 | `The sun is cun t..` | `The sun is atun au` |
| 3 | `The dog can ut t..` | `The dog can heothhe ` |
| 4 | `The red pen is on the t.un..` | `The red pen is on the ostasa` |

**Rationale Generation:**

| Item | Cond 1 Generated | Cond 2 Generated |
| :---: | :--- | :--- |
| 5 | `...mat has the t.....n.` | `...mat has the -oun unddha-ha` |
| 6 | `...hot has the t....n ru` | `...hot has the shas the unhrm` |
| 7 | `...run has the t....n..` | `...run has the oot.uoundaun.s` |
| 8 | `...bed has the t.n t.n t.n` | `...bed has the ounrsiusounou` |

## Interpretation

### 1. Rationale training improves both direct completion AND rationale generation

Condition 2 (exemplars + rationale) outperformed Condition 1 (exemplars only) on both evaluation types:
- **Direct completion:** +5.23 vs +4.71 (Cond 2 wins by +0.52)
- **Rationale generation:** +6.17 vs +3.15 (Cond 2 wins by +3.01)

The rationale generation gap is massive — Condition 2 nearly doubles Condition 1's delta (+6.17 vs +3.15). This is unsurprising since Condition 2 was trained on rationale text. But the direct completion improvement (+0.52) is the more interesting finding: **adding rationale to the training exemplars improved the model's ability to do the core task, not just the explanation task.** This contradicts Hypothesis 3 (that rationale tokens would dilute the exemplar signal).

### 2. Direct completion improvement is uneven but mostly positive

Condition 2 won on 3 of 4 direct completion items (items 1, 3, 4), with item 3 (`run.`) showing a dramatic advantage (+6.33 vs +4.59). Item 2 (`hot.`) was the exception — Condition 1 won by +1.43 (+4.85 vs +3.42). This variability suggests the rationale benefit is item-specific: it helps most when the target word appears in the rationale explanation (e.g. `run has the -un sound` reinforces `run` as a completion for `"The dog can "`).

### 3. The model cannot generate coherent rationale

Neither condition produces clean phonics explanations. Condition 2's output is recognizable as English-shaped (`-oun unddha-ha`, `oot.uoundaun.s`, `ounrsiusounou`) but not coherent — it produces the right *kind* of tokens (letters, hyphens, periods, spaces) but not the correct sequence. The loss reduction on rationale items (Cond 2: post-avg 2.29) shows the model has learned the statistical distribution of the rationale text, but generation quality remains at early phonemic stage.

### 4. Condition 2's training loss converges higher but evaluates better

Condition 2's final training loss (1.19) is higher than Condition 1's (0.69) because the rationale exemplars are longer and more varied — harder to fit completely. But Condition 2 evaluates better on both direct and rationale items. This suggests the richer training signal (longer sequences with explanatory context) provides better generalization even when the training fit isn't as tight.

### 5. The rationale format is being learned at the byte level

Condition 2's rationale generations show the model has learned the *shape* of the rationale format — hyphens (`-`), the word `ound` (approximating `sound`), and short clustered tokens. But it hasn't learned the correct mapping from a specific word to its specific sound pattern (e.g. `mat` → `-at`). The model is learning "after `has the `, there's a hyphen and some letters ending in `ound`" as a byte-level pattern, not as a phonics rule.

## Limitations

- The rationale text is English meta-linguistic vocabulary (`-at sound`, `pattern`) that the model has never seen before the rationale exemplars. The model must learn both the phonics patterns *and* the explanation vocabulary simultaneously, which may be too much for 15 iterations.
- A 25M parameter model is likely too small to generate coherent multi-sentence explanations. This experiment primarily demonstrates a *limitation* in rationale generation, but a *capability* in leveraging rationale for improved task performance.
- Rationale quality is assessed qualitatively (human inspection of generated text), not by an automated rubric. This introduces subjectivity.
- The rationale format (`"-at sound"`) is a simplification of real phonics instruction. Real pedagogical rationale would be more complex and varied.
- Single seed; pair with Experiment C methodology for multi-seed validation if results are promising.

## Conclusion

- **Supported:**
  1. Answer accuracy is measurable — both conditions show significant loss reduction on direct completion (+4.71 and +5.23). (Hypothesis 1 confirmed.)
  2. Rationale quality is poor — neither condition generates coherent phonics explanations, though Condition 2 produces English-shaped approximations. (Hypothesis 2 confirmed.)
  3. **Hypothesis 3 REJECTED** — rationale training *does* improve direct completion (+5.23 vs +4.71), contrary to the expectation that rationale tokens would dilute the exemplar signal. The richer training context helps, not hurts. (Alternative hypothesis supported.)
  4. Rationale training dramatically improves rationale generation loss (+6.17 vs +3.15), showing the model learns the statistical structure of explanations even if it can't generate them coherently.
- **Not established:**
  1. Whether the direct completion improvement (+0.52) holds across multiple seeds — the advantage is driven by 3 of 4 items and may be seed-specific.
  2. Whether longer training (50+ iterations) would allow the model to generate coherent rationale text.
  3. Whether the rationale benefit scales with more complex explanations or larger rationale corpora.
- **Next experiment:** Multi-seed validation of the rationale effect (combine with Experiment C methodology), or test with longer training (50+ iterations) to see if rationale generation quality improves.

## Related

- Prior experiments: [[2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition|Lesson 1.1]], [[2026-10-23 Experiment A — Held-Out Test|Experiment A]], [[2026-10-23 Experiment B — Control Group|Experiment B]]
- Curriculum: [[02-School/Language/Curriculum|Language Curriculum]]
- Related experiments: [[2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]], [[2026-10-23 Experiment D — Inspect Tokenization|Experiment D]]
- Roadmap: [[Development/Roadmap|Roadmap]] — Phase 3 (Metacognition & Self-Directed Study)
