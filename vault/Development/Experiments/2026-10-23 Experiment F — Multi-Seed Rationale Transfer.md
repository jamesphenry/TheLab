---
title: "Experiment F — Multi-Seed Rationale Transfer"
type: experiment
status: completed
scripts:
  - experiments/run_experiment_f.py
tags:
  - ai-school
  - experiment
  - rationale
  - held-out
  - multi-seed
  - transfer
created: 2026-10-23
updated: 2026-10-25
---

# Experiment F — Multi-Seed Rationale Transfer

## Question

Does explicit rationale training produce a **reproducible** improvement on **held-out tasks the model has never seen**, across multiple independent seeds? If the rationale advantage observed in Experiment E survives multi-seed validation on novel items, that is evidence the rationale curriculum contributes something beyond learning to imitate explanation-shaped text.

## Hypothesis

1. **Rationale training will show a positive mean delta advantage on held-out direct completion** across seeds, but the advantage will be smaller and more variable than on training-adjacent items — held-out items test transfer, not memorization.
2. **Rationale training will show a positive mean delta advantage on held-out rationale generation** across seeds, but the advantage will be smaller than on training-adjacent rationale items — the model learned the rationale format, not the phonics reasoning.
3. **The rationale advantage on direct completion will NOT be statistically reliable** (i.e., the across-seed distribution will overlap substantially with the non-rationale condition) — the +0.52 advantage seen in Experiment E was driven by 3 of 4 items on a single seed and may not survive.
4. **If the rationale advantage IS reliable across seeds** on held-out direct completion, this would suggest the rationale curriculum contributes genuine transferable structure, not just format imitation.

## Variables and Conditions

- **Independent variables:**
  - Training format: exemplars-only vs. exemplars-with-rationale (paired by seed).
  - Evaluation items: held-out direct completion + held-out rationale generation (all novel).
  - Random seed: 10 seeds, same for both conditions.
- **Measured outcomes:**
  - Per-seed loss delta on held-out direct completion items (both conditions).
  - Per-seed loss delta on held-out rationale generation items (both conditions).
  - Mean and std of delta advantage (rationale - non-rationale) across seeds.
  - Per-item analysis: which held-out items benefit from rationale, consistently?
  - Generated text for qualitative rationale assessment.
- **Paired design:** Both conditions use the **same seed** — the only difference is the training exemplar set. This isolates the rationale effect from initialization variance.

## Training Exemplars

**Condition 1 (Exemplars only):** Same 5 from Experiments A–E.
**Condition 2 (Exemplars + Rationale):** Same 5 augmented from Experiment E.

## Held-Out Test Items

All items are novel — not present in either training set's exemplar text.

**Held-out direct completion (pattern application on unseen prompts):**
1. `"A dog sat on the "` → `"mat."` *(sentence-context transfer)*
2. `"The cat is "` → `"hot."` *(sentence-context transfer)*
3. `"The sun can "` → `"run."` *(sentence-context transfer)*
4. `"A pig can "` → `"dig."` *(fully novel)*
5. `"The bug is "` → `"big."` *(fully novel)*

**Held-out rationale generation (pattern explanation on unseen words):**
6. `"A dog sat on the mat. mat has the "` → `"-at sound."` *(familiar word, novel sentence context)*
7. `"The cat is hot. hot has the "` → `"-ot sound."` *(familiar word, novel sentence context)*
8. `"A pig can dig. dig has the "` → `"-ig sound."` *(novel word)*
9. `"The bug is big. big has the "` → `"-ig sound."` *(novel word)*

## Seeds

10 seeds: {42, 123, 7, 2026, 99, 314, 256, 13, 555, 8} (same as Experiment C).

## Procedure

1. For each seed s in the seed list:
   a. Instantiate fresh BabyLM with seed s — Condition 1 model.
   b. Pre-evaluate on all 9 held-out items.
   c. Train 15 iterations on exemplars-only.
   d. Post-evaluate on all 9 held-out items. Record deltas.
   e. Instantiate fresh BabyLM with seed s — Condition 2 model.
   f. Pre-evaluate on all 9 held-out items.
   g. Train 15 iterations on exemplars+rationale.
   h. Post-evaluate on all 9 held-out items. Record deltas.
2. Compute per-seed advantage: (Cond2 delta - Cond1 delta) for direct and rationale items.
3. Compute mean, std, min, max of advantage across seeds.
4. Per-item analysis: count how many seeds show rationale advantage per item.
5. Qualitative assessment of generated rationale text.

## Results

**Model:** BabyLM, 27,411,456 parameters, 15 iterations per run, AdamW ($\eta=10^{-3}$). 20 total runs (10 seeds × 2 conditions).

### Summary — Advantage of Rationale Training (Cond 2 − Cond 1)

| Statistic | Direct Completion Advantage | Rationale Generation Advantage |
| :--- | :---: | :---: |
| **Mean** | **−0.1087** | **+3.3057** |
| **Std Dev** | 0.9018 | 0.8976 |
| **Min** | −1.6158 | +1.5103 |
| **Max** | +1.2752 | +4.4457 |
| **Seeds positive (Cond2 > Cond1)** | **4 / 10** | **10 / 10** |

### Per-Seed Results

| Seed | Cond1 Dir Δ | Cond2 Dir Δ | Dir Adv | Cond1 Rat Δ | Cond2 Rat Δ | Rat Adv |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 42 | +4.2675 | +3.3978 | −0.8696 | +2.2537 | +5.6957 | +3.4420 |
| 123 | +4.2914 | +4.2973 | +0.0059 | +1.8041 | +6.2498 | +4.4457 |
| 7 | +3.5530 | +4.5149 | +0.9620 | +3.1319 | +5.8906 | +2.7588 |
| 2026 | +3.8472 | +5.1224 | +1.2752 | +2.4921 | +6.2772 | +3.7850 |
| 99 | +5.2702 | +3.6544 | −1.6158 | +3.1852 | +4.6955 | +1.5103 |
| 314 | +4.4681 | +3.3194 | −1.1487 | +3.1735 | +5.2749 | +2.1014 |
| 256 | +3.2184 | +3.2092 | −0.0092 | +2.4407 | +6.1499 | +3.7092 |
| 13 | +4.6940 | +4.4560 | −0.2380 | +2.9272 | +6.0161 | +3.0889 |
| 555 | +4.9458 | +4.5873 | −0.3585 | +2.3427 | +6.5911 | +4.2484 |
| 8 | +3.7729 | +4.6823 | +0.9094 | +1.8775 | +5.8445 | +3.9670 |

### Per-Item — Held-Out Direct Completion

| Item | Prompt → Target | Cond1 Mean Δ | Cond2 Mean Δ | Advantage | Seeds Positive |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | `"A dog sat on the "` → `"mat."` | +4.6676 | +4.4078 | −0.2598 | 2/10 |
| 2 | `"The cat is "` → `"hot."` | +4.7922 | +4.5305 | −0.2617 | 3/10 |
| 3 | `"The sun can "` → `"run."` | +5.8771 | +6.1611 | +0.2840 | 6/10 |
| 4 | `"A pig can "` → `"dig."` | +2.3024 | +2.1789 | −0.1235 | 5/10 |
| 5 | `"The bug is "` → `"big."` | +3.5250 | +3.3422 | −0.1827 | 4/10 |

### Per-Item — Held-Out Rationale Generation

| Item | Prompt → Target | Cond1 Mean Δ | Cond2 Mean Δ | Advantage | Seeds Positive |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 6 | `"...mat has the "` → `"-at sound."` | +2.7426 | +5.9712 | **+3.2286** | **10/10** |
| 7 | `"...hot has the "` → `"-ot sound."` | +2.8430 | +6.7442 | **+3.9012** | **10/10** |
| 8 | `"...dig has the "` → `"-ig sound."` | +2.0693 | +4.6250 | **+2.5557** | 9/10 |
| 9 | `"...big has the "` → `"-ig sound."` | +2.5966 | +6.1338 | **+3.5372** | **10/10** |

### Qualitative Sample (Seed 42)

| Item | Cond1 Generated | Cond2 Generated |
| :---: | :--- | :--- |
| 6 | `...mat has the t.n..n.n.` | `...mat has the un tounddd mou` |
| 7 | `...hot has the t..n t...` | `...hot has the the soundd.os` |
| 8 | `...dig has the t..n.n..` | `...dig has the harsd sound.-` |
| 9 | `...big has the t..n t...` | `...big has the uhe.daun -auta` |

## Interpretation

### 1. The rationale advantage on direct completion does NOT survive multi-seed validation

The mean direct completion advantage is **−0.1087** — slightly *negative*. Only 4 of 10 seeds showed a rationale advantage. The per-item breakdown is even more telling: no held-out direct completion item showed a consistent rationale advantage (best was Item 3 at 6/10 seeds positive, worst were Items 1 and 2 at 2/10 and 3/10).

This **rejects Hypothesis 4** and confirms Hypothesis 3: the +0.52 advantage seen in Experiment E (single seed, training-adjacent items) was not reproducible. On held-out items across seeds, rationale training does not improve the model's ability to complete novel prompts. The Experiment E result was an artifact of seed selection and training-adjacent evaluation.

### 2. The rationale advantage on rationale generation IS reproducible — but it's format, not reasoning

The mean rationale generation advantage is **+3.3057** — all 10 seeds positive, every per-item advantage positive. This is robust and reproducible. But this advantage reflects the model learning the *statistical format* of rationale text (hyphens, the word `sound`, letter clusters), not genuine phonics reasoning.

The qualitative evidence confirms this: Condition 2 generates text containing `sound`, hyphens, and English-shaped clusters (`un tounddd mou`, `the soundd.os`, `harsd sound.-`), while Condition 1 generates generic phonemic noise (`t.n..n.n.`, `t..n t...`). The model has learned the *shape* of explanations, not the *content* — it cannot map `dig` to `-ig` correctly; it just produces explanation-shaped tokens after `has the`.

### 3. This is where language-pattern learning and reasoning behavior diverge

The experiment cleanly separates two things:
- **Format learning** (reproducible, robust): The model reliably learns the byte-level distribution of explanation text. This transfers to held-out items because the format (`has the [hyphen][letters] sound`) is structurally consistent.
- **Reasoning** (not achieved): The model cannot correctly map a specific word to its specific sound pattern. It cannot generate `-ig` for `dig` or `big` — it generates explanation-shaped noise instead.

This is the boundary the question asked about. The distinction between language-pattern learning and reasoning behavior **begins to matter here**: a 25M tabula rasa model with 15 iterations can learn the format of explanations but cannot perform the reasoning those explanations describe.

### 4. Novel word rationale items show slightly weaker advantage

Items 8–9 (novel words `dig`/`big`) showed a smaller advantage (+2.56, +3.54) than items 6–7 (familiar words `mat`/`hot`, +3.23, +3.90). This suggests the rationale advantage is partly driven by overlap with training rationale text — familiar words appear in the training rationale, so the model has a head start on their explanation format. Novel words still benefit (9/10 and 10/10 seeds positive) but less, consistent with format transfer rather than genuine phonics generalization.

## Limitations

- 10 seeds with paired design is solid but not exhaustive. The direct completion advantage distribution (std=0.90) is wide enough that a small true effect could be masked.
- Only 5 held-out direct items and 4 held-out rationale items — small sample limits per-item conclusions.
- 15 iterations may be too few for the model to leverage rationale semantically. Longer training (50–100+ iterations) might allow deeper integration of the explanation signal.
- The rationale format is highly simplified (`-at sound`). Real pedagogical explanations are more varied and complex, which could either help (richer signal) or hurt (harder to learn).
- Rationale quality is assessed qualitatively, not by automated rubric.

## Conclusion

- **Supported:**
  1. Rationale training produces a **reproducible advantage on rationale generation** (+3.31 mean, 10/10 seeds positive) — but this is format learning, not reasoning. (Hypothesis 2 confirmed.)
  2. Rationale training does **NOT** produce a reproducible advantage on held-out direct completion (−0.11 mean, 4/10 seeds positive). The Experiment E advantage was not robust. (Hypothesis 3 confirmed, Hypothesis 4 rejected.)
  3. The model learns the *shape* of explanations but not the *content* — it generates explanation-shaped text but cannot correctly map words to their phonics patterns. (Hypothesis 2's nuance confirmed.)
- **Not established:**
  1. Whether longer training or a larger model could bridge the gap between format learning and genuine reasoning.
  2. Whether a more varied rationale corpus (different explanation formats) would produce better transfer.
  3. Whether the direct completion disadvantage (−0.11 mean) is a real dilution effect or noise — the std (0.90) is large relative to the mean (−0.11).
- **The distinction between language-pattern learning and reasoning behavior begins to matter here.** A 25M tabula rasa model at 15 iterations can learn the format of explanations but cannot perform the reasoning they describe. This is the boundary.

- [[2026-10-23 Experiment A — Held-Out Test|Experiment A]] — original held-out test (single seed)
- [[2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]] — multi-seed reproducibility
- [[2026-10-23 Experiment E — Reasoning|Experiment E]] — single-seed rationale experiment

## Related
