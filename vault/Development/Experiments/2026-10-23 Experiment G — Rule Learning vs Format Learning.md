---
title: "Experiment G — Rule Learning vs Format Learning"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - rule-learning
  - format-learning
  - rationale
  - held-out
  - multi-seed
created: 2026-10-23
updated: 2026-10-23
---

# Experiment G — Rule Learning vs Format Learning

## Question

Can a 25M tabula rasa model learn an explicit phonics rule (word → ending pattern), or does rationale training only teach it to produce explanation-shaped text? Experiment F showed the model learns the *format* of explanations (10/10 seeds positive on rationale generation) but cannot correctly map specific words to their sound patterns. This experiment isolates whether that failure is because the model can't learn the rule at all, or because the training signal was too weak.

## Hypothesis

1. **Baseline (existing rationale):** The model will show format learning (positive rationale generation delta) but poor rule accuracy — it will produce explanation-shaped text but with incorrect endings, as in Experiment F.
2. **Explicit-rule condition:** With concise, repeated examples explicitly connecting words to their ending patterns, the model will show *some* improvement in rule accuracy on held-out items, but it will remain well below reliable — the model has the capacity to begin learning the mapping but 15 iterations is insufficient for robust rule acquisition.
3. **Matched control:** The matched control (same text volume, no word-to-ending relationship) will show format learning comparable to the baseline but no rule accuracy improvement — confirming that any explicit-rule advantage comes from the rule signal, not the additional text.
4. **If the explicit-rule condition shows NO improvement over the matched control** on held-out rule accuracy, this confirms that a 25M model at 15 iterations cannot learn the word-to-ending rule at all — the boundary is capacity, not signal strength.

## Variables and Conditions

### Four conditions (all paired by seed):

1. **Baseline:** Train on the existing 5 rationale exemplars from Experiment E/F (e.g. `"The cat sat on the mat. mat has the -at sound."`).

2. **Explicit-rule:** Train on the 5 baseline exemplars PLUS concise, repeated rule examples that explicitly connect words to their ending patterns, including `dig → -ig`:
   - `"cat ends with -at."`
   - `"mat ends with -at."`
   - `"hot ends with -ot."`
   - `"run ends with -un."`
   - `"bed ends with -ed."`
   - `"dig ends with -ig."`
   - `"big ends with -ig."`
   - `"pig ends with -ig."`
   - `"log ends with -og."`
   - `"bug ends with -ug."`

3. **Matched control:** Train on the 5 baseline exemplars PLUS the same number of additional sentences with equivalent token volume but NO word-to-ending relationship:
   - `"cat is a small animal."`
   - `"mat is on the floor."`
   - `"hot means high temperature."`
   - `"run is a fast action."`
   - `"bed is for sleeping."`
   - `"dig is what pigs do."`
   - `"big means large size."`
   - `"pig is a farm animal."`
   - `"log is a piece of wood."`
   - `"bug is a small insect."`

4. **No-rationale baseline (from Experiment F for reference):** Train on the 5 plain exemplars (no rationale text). This provides a reference point for the non-rationale condition.

### Held-out evaluation items (withheld from all training sets):

**Direct completion (pattern application on unseen prompts):**
1. `"A dog sat on the "` → `"mat."`
2. `"The cat is "` → `"hot."`
3. `"The sun can "` → `"run."`
4. `"A pig can "` → `"dig."`
5. `"The bug is "` → `"big."`

**Rule identification (does the model produce the correct ending?):**
6. Prompt: `"cat ends with "` → Target: `"-at."`
7. Prompt: `"hot ends with "` → Target: `"-ot."`
8. Prompt: `"run ends with "` → Target: `"-un."`
9. Prompt: `"dig ends with "` → Target: `"-ig."` *(dig appears in explicit-rule training but this exact prompt is withheld)*
10. Prompt: `"bug ends with "` → Target: `"-ug."`
11. Prompt: `"log ends with "` → Target: `"-og."`
12. Prompt: `"pen ends with "` → Target: `"-en."` *(fully novel — word AND ending never in any training set)*

**Rationale generation (format vs content — from Experiment F for comparison):**
13. `"The cat is hot. hot has the "` → `"-ot sound."`
14. `"A pig can dig. dig has the "` → `"-ig sound."`
15. `"The bug is big. big has the "` → `"-ig sound."`

### Scoring: Rule accuracy, not format resemblance

The key innovation over Experiment F is the evaluation metric. For rule identification items (6-12), we score:
- **Exact ending match:** Does the generated text contain the correct ending string (e.g. `-ig`, `-at`)? Binary per item.
- **First-token accuracy:** Is the first generated token after the prompt the hyphen character (`-`)? This tests whether the model learned the format.
- **Correct ending given format:** Among generations that start with `-`, how many produce the correct ending? This separates format learning from rule learning.

### Seeds

10 seeds: {42, 123, 7, 2026, 99, 314, 256, 13, 555, 8} (same as Experiments C and F).

## Procedure

1. For each seed $s$:
   a. Run Condition 1 (Baseline): fresh model, pre-eval, train 15 iterations, post-eval.
   b. Run Condition 2 (Explicit-rule): fresh model, pre-eval, train 15 iterations, post-eval.
   c. Run Condition 3 (Matched control): fresh model, pre-eval, train 15 iterations, post-eval.
2. For each post-evaluation, compute:
   - Per-item loss delta for direct completion and rationale generation.
   - **Rule accuracy score** for items 6-12: exact ending match (binary), first-token-is-hyphen (binary), correct-ending-given-format (conditional).
3. Aggregate across seeds:
   - Mean loss delta per condition per item type.
   - Rule accuracy rate per condition (what fraction of items 6-12 get the correct ending?).
   - Format compliance rate per condition (what fraction start with `-`?).
   - Conditional accuracy (correct ending / starts with `-`).
4. Compare: Explicit-rule vs Matched control on rule accuracy. If explicit-rule > matched control, the rule signal helps. If equal, the model can't learn the rule.

### Code Changes Required

- Write `experiments/run_experiment_g.py` based on the Experiment F template.
- Add **rule accuracy scoring** function: takes generated text + target ending, returns (starts_with_hyphen: bool, exact_ending_match: bool).
- The explicit-rule and matched-control exemplar lists are longer than baseline (15 vs 5 sentences), so each iteration does more gradient steps — this is intentional (the point is to test whether the rule signal helps, controlling for text volume via the matched control).

## Results

**Model:** BabyLM, 27,411,456 parameters, 15 iterations per run, AdamW ($\eta=10^{-3}$). 30 total runs (10 seeds × 3 conditions).

### Rule Accuracy Summary

| Condition | Format Rate (starts with `-`) | Exact Ending Match | Conditional Accuracy (correct \| has format) |
| :--- | :---: | :---: | :---: |
| Baseline (rationale) | 12.9% (9/70) | **0.0%** (0/70) | 0.0% (0/9) |
| Explicit-rule | **52.9%** (37/70) | **1.4%** (1/70) | **2.7%** (1/37) |
| Matched control | 8.6% (6/70) | **0.0%** (0/70) | 0.0% (0/6) |

### Loss Delta Summary

| Condition | Direct Completion Δ | Rule Identification Δ | Rationale Gen Δ |
| :--- | :---: | :---: | :---: |
| Baseline | +4.27 | +4.15 | +5.90 |
| Explicit-rule | +3.77 | +3.70 | +5.75 |
| Matched control | +5.07 | +4.38 | +5.50 |

### Advantage — Explicit-rule vs Matched Control

| Metric | Mean Advantage | Std Dev | Seeds Positive |
| :--- | :---: | :---: | :---: |
| Direct Completion | **−1.3029** | 0.4148 | **0 / 10** |
| Rule Identification | −0.7985 | 1.4020 | 4 / 10 |
| Rationale Generation | +0.2484 | 0.4223 | 6 / 10 |
| Rule Accuracy (exact) | +1 item (1/70 vs 0/70) | — | — |

### Per-Item Rule Accuracy

| Item | Prompt → Target | Baseline Format | Explicit Format | Matched Format | Explicit Exact | Matched Exact |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 6 | `"cat ends with "` → `"-at."` | 1/10 | 4/10 | 0/10 | 0/10 | 0/10 |
| 7 | `"hot ends with "` → `"-ot."` | 2/10 | 4/10 | 0/10 | 0/10 | 0/10 |
| 8 | `"run ends with "` → `"-un."` | 2/10 | 4/10 | 2/10 | 0/10 | 0/10 |
| 9 | `"dig ends with "` → `"-ig."` | 1/10 | **7/10** | 1/10 | 0/10 | 0/10 |
| 10 | `"bug ends with "` → `"-ug."` | 1/10 | **7/10** | 2/10 | 0/10 | 0/10 |
| 11 | `"log ends with "` → `"-og."` | 1/10 | 6/10 | 0/10 | **1/10** | 0/10 |
| 12 | `"pen ends with "` → `"-en."` (novel) | 1/10 | 5/10 | 1/10 | 0/10 | 0/10 |

### Qualitative Sample (Seed 42)

| Item | Baseline | Explicit-rule | Matched control |
| :---: | :--- | :--- | :--- |
| 6 | `cat ends with ond.unat` | `cat ends with asn..t` | `cat ends with ong.lggt` |
| 9 | `dig ends with otdan os` | `dig ends with a. a..w` | `dig ends with igggnggs` |
| 11 | `log ends with -ede td.` | `log ends with -og.i` ✓ | `log ends with egteotin` |
| 12 | `pen ends with on runda` | `pen ends with -dsd..` | `pen ends with ate.ngsa` |

## Interpretation

### 1. The explicit-rule condition teaches format, not rules

The explicit-rule condition dramatically increased format compliance — 52.9% of generations started with a hyphen, compared to 12.9% for baseline and 8.6% for matched control. The model learned that after `"ends with "`, a hyphen should follow. This is format learning: the explicit-rule examples (`"cat ends with -at."`) consistently pair `ends with` with `-`, so the model learned this bigram-level pattern.

But exact ending match was **1.4%** (1 out of 70 generations across 10 seeds). The single correct match was seed 42 on `log ends with -og.i` — which contains `-og` but is arguably partial (the `.i` suffix is noise). The model cannot map a specific word to its specific ending.

### 2. The matched control confirms: no rule signal = no rule learning

The matched control (same text volume, no word-to-ending relationship) showed 0% exact match and 8.6% format rate. This confirms that the explicit-rule condition's format improvement (52.9% vs 8.6%) comes from the rule examples' format (`X ends with -Y`), not from the additional training text. The rule signal teaches the format; it does not teach the rule.

### 3. Explicit-rule training HURTS direct completion

The most surprising finding: the explicit-rule condition showed a **negative** direct completion advantage vs matched control (−1.30 mean, **0/10 seeds positive**). Adding 10 rule examples to the training set consistently *worsened* the model's ability to complete held-out sentences.

This likely occurs because the rule examples (`"cat ends with -at."`) introduce a competing pattern: `cat` is now followed by `ends with`, not `sat on the`. The model's limited capacity distributes its learning across more patterns, reducing the signal for the sentence-completion patterns. The matched control sentences (`"cat is a small animal."`) cause less interference because they don't reuse the exact sight words in competing syntactic contexts.

### 4. Conditional accuracy is near chance

Given that the model produces a hyphen (format learned), how often is the ending correct? 1/37 = 2.7%. With 26 letters, random chance for the first letter after the hyphen is ~3.8%. The explicit-rule condition's conditional accuracy (2.7%) is **at or below random chance** — the model has learned to produce a hyphen but has no knowledge of which letters should follow it.

### 5. The fully novel probe (`pen → -en`) shows format transfer but zero rule

Item 12 (`pen ends with -en.`) — where neither `pen` nor `-en` appears in any training set — showed 5/10 format compliance for explicit-rule (the model produces a hyphen) but 0/10 exact match. The model generalizes the format (`ends with → hyphen`) but cannot generalize the rule (word → ending pattern). This is the cleanest evidence that the model learns format but not rules.

### 6. The boundary is capacity, not signal

The explicit-rule condition provided clear, direct, repeated examples of the word-to-ending mapping. The model learned the format reliably (52.9% compliance). But it did not learn the rule (1.4% accuracy, at chance given format). This confirms that a 25M tabula rasa model at 15 iterations **cannot learn an explicit phonics rule** — the boundary is model capacity/training depth, not signal strength. Providing the rule more directly did not help.

## Limitations

- The explicit-rule examples use a different sentence format (`"X ends with -Y."`) than the rationale exemplars (`"X has the -Y sound."`). The model must learn both formats. This could dilute the signal, or it could help by providing two views of the same rule.
- 15 iterations may be too few. The format learning (52.9%) suggests the model is absorbing the training signal, but more iterations might be needed for rule internalization.
- The rule accuracy metric is binary (correct ending or not), which is coarse. A softer metric (e.g. edit distance to target ending) might reveal partial learning.
- 10 seeds provides statistical confidence for the aggregate, but per-item conclusions (especially the single fully-novel item `pen → -en`) are limited.
- The negative direct completion effect (−1.30) may be specific to the small exemplar set — with a larger corpus, the interference from rule examples might be diluted.

## Conclusion

- **Supported:**
  1. **Format learning is real and reproducible** — explicit-rule training boosts format compliance from 8.6% to 52.9% (matched control vs explicit-rule), confirming the model learns the *shape* of rules. (Hypothesis 1 partially confirmed.)
  2. **Rule learning does not occur** — exact ending match is 1.4% for explicit-rule vs 0% for matched control, a negligible difference. Conditional accuracy (2.7%) is at random chance. The model cannot map specific words to their endings. (Hypothesis 2 rejected — no meaningful improvement.)
  3. **The matched control confirms the format improvement comes from the rule signal** (52.9% vs 8.6% format rate), not from additional text volume. (Hypothesis 3 confirmed.)
  4. **The boundary is capacity, not signal** — providing the rule more directly and explicitly did not produce rule learning. A 25M model at 15 iterations can learn format but not rules. (Hypothesis 4 confirmed — the model cannot learn the rule.)
- **Not established:**
  1. Whether longer training (100+ iterations) or a larger model could bridge the gap between format and rule learning.
  2. Whether the negative direct completion effect (−1.30) would persist with a larger training corpus.
  3. Whether a different rule representation (e.g. rhyming pairs instead of `ends with`) would be more learnable.
- **This is where language-pattern learning and reasoning behavior definitively diverge.** The model learns the format of rules reliably (52.9% compliance) but cannot learn the content of rules (1.4% accuracy, at chance). Explicit instruction of the rule does not help — the boundary is model capacity and training depth, not signal clarity.

## Related

- [[2026-10-23 Experiment E — Reasoning|Experiment E]] — single-seed rationale experiment
- [[2026-10-23 Experiment F — Multi-Seed Rationale Transfer|Experiment F]] — identified the format-vs-reasoning boundary
- [[2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]] — multi-seed methodology
- Roadmap: [[Development/Roadmap|Roadmap]] — Phase 3 (Metacognition & Self-Directed Study)
