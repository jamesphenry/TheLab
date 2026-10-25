---
title: AI School — Independent Research Audit (Updated Evidence)
type: report
status: completed
tags:
  - ai-school
  - research-audit
  - report
  - updated-evidence
created: 2026-10-25
updated: 2026-10-25
---

# AI School — Independent Research Audit (Updated Evidence)

**Audit date:** 2026-10-25

**Purpose:** Reassess the documented findings using the expanded experiment records committed on 2026-10-24. This report supplements [[2026-10-25 AI School Independent Research Audit|the earlier audit]] and does not replace it.

## Executive Summary

The newer records materially broaden the evidence. They include a single-seed held-out CVC evaluation, control conditions, a ten-seed replication on the original four completion items, tokenizer inspection, rationale-format comparisons, rule-identification probes, and a series of alphabet-sequence curriculum diagnostics. The overall pattern is now clearer: the model can reduce teacher-forced byte-level loss, and those changes are often reproducible; this does not reliably produce correct free generation or demonstrate abstract rule learning.

The best-supported positive finding is narrow: under the recorded setup, training on the original phonics examples changes completion-token probabilities, and ten seeds all show reduced average loss on the same four training-adjacent items. A no-update control remains unchanged, while random-byte training worsens those items. Yet unrelated English training also produces a large loss improvement, so generic byte/statistical learning accounts for a substantial share of the treatment effect. The ten-seed study repeats the same overlapping evaluation items; it does not replicate the genuinely novel cases from Experiment A.

The new preschool studies reveal a major validity issue. The three “held-out” alphabet items in the updated lesson assessment (`g h i `→`j`, `n o p `→`q`, `s t u `→`v`) occur as contiguous transitions in the updated training exemplars. The notes therefore do not establish held-out transfer for that assessment. In addition, best-checkpoint accuracy is selected using the same evaluation set on which it is reported, which makes best-checkpoint scores optimistic. The final-checkpoint results are less affected by that selection step but still face training/evaluation overlap.

Rationale experiments directly address the risk of mistaking a learned response format for reasoning. Across ten paired seeds, rationale training improves rationale-target loss consistently but does not improve held-out direct completion on average; generated “explanations” remain noisy. In the explicit-rule comparison, the model more often starts rule answers with a hyphen, while exact ending accuracy is only 1/70 in that condition. However, most rule mappings were included in explicit-rule training, and the one fully novel word probe is too small to support a broad capacity conclusion.

**Overall:** the project has a useful experimental trajectory and has corrected some earlier overclaims, especially by separating loss from generation accuracy. Current evidence supports small-scale sequence fitting and format sensitivity. It does not yet support reliable transfer, robust rule learning, or the claim that targeted coverage causes generalizable capability. Stronger conclusions require leakage-free test design, fixed test sets not used for checkpoint selection, saved run artifacts, and replicated outcomes on genuinely novel relations.

## Scope and Provenance

### Checkout verification

- **Branch:** `main`
- **HEAD:** `c426b71366abc150c6850eb55d1c1d672d7770f0`
- **HEAD date and subject:** 2026-10-24, `Document Experiments A-D separately`
- **Working tree:** not clean. It contains the earlier audit/navigation edits and an untracked `harness/experiments/` directory. The expanded 2026-10-23 and 2026-10-24 vault research records and preschool materials are tracked in this commit. The prior audit file was preserved and not overwritten.

### Material inspected

I inspected vault instructions and navigation, the experiment template and experiment indexes, the dated 2026-10-23 Experiment A–G notes, the original baseline and Lesson 1.1 notes, the 2026-10-24 preschool experiment records, ADR-0002, the updated Lesson 1.1 and Assessment 1, and the preschool curriculum. The 2026-10-24 material includes coverage comparisons and follow-up, a four-seed updated test, held-out expansion, generation diagnostics, rank/checkpoint tracking, a model-size comparison, and a throwaway harness evaluation.

The experiment notes contain reported tables and qualitative outputs, but the checkout has no corresponding complete run scripts, raw logs, saved checkpoints, or machine-readable result bundles for most of these studies. `harness/experiments/experiment_a.py` is present, but it is not the full set of drivers for the reported A–G and preschool studies. Thus, the report can audit the records and compare their internal claims, but cannot independently reproduce their numeric results from saved artifacts.

### Evidence labels

- **Recorded:** directly stated in an inspected experiment or design note.
- **Source-checked:** verified against inspected source/configuration or compared across records.
- **Interpretation:** an explanation consistent with the record, but not uniquely established by it.
- **Proposal:** a suggested future experiment, not an observed finding.

## Research Questions and Framework

The project’s original questions remain relevant: can a randomly initialized model improve through instruction; does improvement generalize to unfamiliar inputs; how do training weights differ from external notes; and can self-assessment track measured ability? The 2026-10-23 experiments operationalize these questions using byte-level next-token loss, generated completions, controls, and multiple random seeds. The 2026-10-24 work shifts toward alphabet pattern completion and compares training-example coverage and format.

The key distinction for this audit is among:

1. **Teacher-forced loss:** how well the model predicts target bytes when given the correct preceding bytes.
2. **Free-generation accuracy:** whether its own next-token choices produce the exact required answer.
3. **Transfer or rule use:** whether it succeeds on a relation or pattern withheld from training.

These outcomes are not interchangeable. The records provide repeated examples of loss decreasing while greedy generation remains wrong or unstable. They also show rationale-format compliance improving without demonstrated rule accuracy.

## Chronological Research Narrative

### 2026-10-23: initial phonics and held-out CVC work

The original Lesson 1.1 run reported mean target loss improving from 8.4218 to 4.6563 after 15 iterations on five exemplars. As described in the earlier audit, its four targets all occur in training, so it is training-adjacent rather than held out.

Experiment A extends the evaluation to eight nominally held-out CVC/context items for seed 42. It reports mean held-out loss falling from 8.3296 to 4.4658 (delta +3.8638). Categories include familiar words in rearranged contexts, unseen CVC words built from seen letters, and two items with no lexical overlap (`pig`→`dig`, `bug`→`big`). Greedy or sampled generations remain malformed. This is a promising single-seed loss result, but its interpretation as lexical or word-level generalization is not established: all strings share byte tokens, and generic byte statistics are a plausible alternative.

Experiment B compares phonics training with no update, random bytes, and unrelated English. The phonics condition improves by +4.7096 on the original four items; no-update is 0; random bytes worsen by −0.6910; unrelated English improves by +3.2824. This makes a pure evaluation-artifact explanation less likely and shows data distribution matters. It also indicates a large gain from generic English byte regularities. Treatment exceeds unrelated English by +1.43 in this one seed, but the control text shares language and some common words, so it is not a clean isolation of phonics-specific learning.

Experiment C repeats only the original four training-adjacent items across ten seeds. All ten reported deltas are positive, mean +4.6251 and standard deviation 0.7118. This supports reproducibility of loss reduction on those items, not of the held-out transfer in Experiment A. The item `run` is easiest and `bed` most variable, consistent with target frequency and prompt differences.

Experiment D verifies that `BabyTokenizer` is byte-level: 260 IDs total (4 specials + 256 byte values), while the model uses a 4096-class output/embedding configuration. The note estimates 3,836 never-indexed rows and approximately 1.96 million unused embedding parameters. This resolves the earlier audit’s concern about vocabulary mismatch. It remains a configuration inefficiency and an interpretive caveat for losses computed across a 4096-way output head.

### 2026-10-23: rationale and rule-format studies

Experiment E is a single-seed comparison. Rationale-augmented training improves both direct-completion and rationale-target losses relative to the plain exemplars in this run. Its direct-completion advantage is not reproduced in Experiment F’s ten-seed paired comparison: mean direct-completion advantage is −0.1087, with rationale training better on 4/10 seeds. By contrast, rationale-target loss improves by an average +3.3057 in the rationale condition, with a positive difference in all ten seeds. The reported generated text includes words such as “sound” and hyphen-like forms but does not provide coherent, reliably correct explanations. **Interpretation:** this is evidence of acquiring the statistical form of rationale responses; it is not evidence of learning the phonics rule.

Experiment G compares baseline rationale training, explicit word-ending examples, and a matched text-volume control over ten seeds. Explicit-rule training raises hyphen-start format rate to 52.9% versus 8.6% in matched control. Exact ending match is 1/70 versus 0/70. This is a strong caution against treating answer shape as rule competence. The design has an important limitation: most evaluated word-ending relations (`cat`→`-at`, `hot`→`-ot`, `dig`→`-ig`, etc.) were themselves included in explicit-rule training. Only `pen`→`-en` is described as wholly novel, and it has 0/10 exact matches. Therefore the records show poor generation even on mostly trained mappings and no success on one novel probe; they do not establish a general inability to learn rules across training budgets or representations.

### 2026-10-24: alphabet sequence diagnostics and curriculum changes

The throwaway preschool harness record separates training loss, held-out loss, and greedy accuracy. It reports large train-loss reductions but 0% generation accuracy on the small alphabet tests in the reported cases, and seed-dependent held-out loss. This is an important correction to the earlier loss-only success framing.

The expanded diagnostic evaluates 12 alphabet prompts through 30 iterations for seed 123, reporting 5/12 correct at the selected best checkpoint (iteration 29) and 3/12 at the final checkpoint. Related checkpoint and rank-tracking notes report transient rank-1 predictions and unstable outcomes. They support the observation that probability/rank, loss, and greedy accuracy can move differently over training.

Coverage comparisons report mean best accuracy of 25.00% for original examples, 18.75% for full coverage, and 41.67% for mixed targeted coverage across four seeds; corresponding mean final accuracies are 20.83%, 12.50%, and 37.50%. ADR-0002 promotes mixed coverage, and the lesson was updated with bridging sequences. These figures are suggestive but do not securely establish transfer: the later assessment’s three alphabet “held-out” items are each present as contiguous transitions in the updated training sequences. In addition, the reported best checkpoint is selected on the same 12-item evaluation set used to report its best score. The updated test record then reports mean held-out accuracy of 16.67% across four seeds (one seed 66.67%, three seeds 0%), despite loss deltas above +5 for every seed. This undercuts the claim that the mixed-coverage lesson robustly passes its stated outcome.

The larger-model comparison reports a single-seed 205.9M-parameter model performing worse than the 27.4M model under the same 30-iteration budget (8.33% vs. 25.00% best accuracy). This establishes only that scaling alone did not help in that specific setup; it does not compare adequately tuned or compute-matched models.

## Experiment Inventory and Evidence Assessment

| Study | Main record | What is recorded | Audit assessment |
| --- | --- | --- | --- |
| Initial Lesson 1.1 | [[Development/Experiments/2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition|Initial phonics run]] | +3.7655 mean target-loss reduction; target words occur in training | Evidence of fitting/optimization on overlapping items; no held-out transfer |
| CVC held-out test | [[Development/Experiments/2026-10-23 Experiment A — Held-Out Test|Experiment A]] | Seed 42; +3.8638 mean loss delta over eight labeled held-out items | More informative than initial run; single seed, small test, loss not exact generation, byte-overlap caveat |
| Controls | [[Development/Experiments/2026-10-23 Experiment B — Control Group|Experiment B]] | No-update 0; random bytes −0.691; unrelated English +3.282; phonics +4.710 | Evidence data distribution matters; phonics-specific increment is single-seed and control is not byte/lexically matched |
| Repeated original items | [[Development/Experiments/2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]] | 10/10 positive on the original four, mean +4.625, SD 0.712 | Good direction replication for the same items; not held-out replication |
| Tokenizer | [[Development/Experiments/2026-10-23 Experiment D — Inspect Tokenization|Experiment D]] | 260-token tokenizer against 4096 output classes; UTF-8 byte mappings verified | Source inspection supports findings; unused rows inflate parameter count and output space |
| Rationale | [[Development/Experiments/2026-10-23 Experiment E — Reasoning|Experiment E]] | Single-seed loss gains from rationale augmentation | Initial exploratory result; direct-completion result did not replicate robustly |
| Multi-seed rationale | [[Development/Experiments/2026-10-23 Experiment F — Multi-Seed Rationale Transfer|Experiment F]] | 10 paired seeds; rationale-target advantage +3.306 (10/10); direct completion −0.109 mean (4/10 positive) | Strong evidence for format-target loss change; generated rationale remains incoherent and direct-transfer benefit absent |
| Explicit rules | [[Development/Experiments/2026-10-23 Experiment G — Rule Learning vs Format Learning|Experiment G]] | Format rate 52.9%; exact mapping 1/70; novel `pen` probe 0/10 | Strong format/correctness separation; most rule mappings were trained, novel sample count is one item |
| Alphabet baseline/full/mixed | [[Development/Experiments/2026-10-24 Coverage Fix Multi-Seed Follow-up|Coverage follow-up]] | Four seeds, mixed reported at 41.67% mean best vs 25% original and 18.75% full | Suggestive curriculum comparison; test leakage and same-set checkpoint selection undermine generalization estimate |
| Updated assessment | [[Development/Experiments/2026-10-24 Lesson 1.1 Updated Test|Updated Lesson 1.1 test]] | Four seeds; mean loss delta +6.23, mean held accuracy 16.67%; one pass | Direct counterevidence to stable generation mastery; assessment items overlap updated lesson sequences |
| Generalization diagnostics | [[Development/Experiments/2026-10-24 Comprehensive Diagnostic - Held-Out Expansion|Expanded diagnostic]] and [[Development/Experiments/2026-10-24 Stability Tracking Across Checkpoints|Checkpoint tracking]] | Best/final accuracy diverges; next-token ranks fluctuate | Supports instability and metric separation; reported test/training overlap and best-checkpoint selection limit transfer claims |
| Model size | [[Development/Experiments/2026-10-24 Model Size Comparison - Larger Model Test|Larger model test]] | One seed; larger model worse under same iteration/LR budget | Not a fair capacity conclusion; one seed and unequal compute/update cost |

## Contradictions, Alternative Explanations, and Limitations

1. **“Held-out” does not consistently mean withheld relation.** Some 2026-10-23 CVC test items have unseen prompt contexts but use target words present in training. For the updated alphabet lesson, the actual prompt-target transitions are embedded in training exemplars. The report labels do not ensure independence; split by relation/example before training and verify mechanically.
2. **Best-checkpoint selection contaminates the reported test score.** Selecting the maximum across 30 iterations using held-out accuracy makes that set a validation set. A separate untouched final test is needed for an unbiased estimate.
3. **Loss and generated correctness diverge.** Teacher-forced loss fell substantially in several studies while greedy completion remained 0% or low. A lower loss is an optimization outcome, not a mastery criterion by itself.
4. **Generic byte learning is a major alternative.** Unrelated English reduces target loss by +3.28, versus +4.71 for the phonics treatment in the one-seed comparison. Byte-level tokenization and short repetitive strings make generic character/space statistics plausible contributors.
5. **Rationale format is not reasoning evidence.** Multi-seed gains on rationale-target loss are reliable, but direct completion does not benefit on average and generated explanations are malformed. Format rate and rule accuracy must remain separate outcomes.
6. **The explicit-rule test is mostly trained on its mapping.** This weakens a claim specifically about novel rule acquisition. The single truly novel `pen` probe is useful but statistically very limited.
7. **Experimental provenance is incomplete.** Most run-driving scripts, raw outputs, checkpoint selection logic, exact code revision, and environment details are absent. Many conclusions are based on compact summary records rather than independently auditable artifacts.
8. **Curriculum comparison caveats.** Only four seeds are reported; the full-coverage condition changes training text volume/content; the updated set of assessment items is seen verbatim in the mixed exemplars; and selection over checkpoints favors the selected condition/run. The causal claim “targeted coverage improves generalization” remains a promising hypothesis, not established fact.
9. **Capacity claims exceed the tested range.** One larger-model run under a fixed 30-iteration schedule cannot establish a capacity boundary. The results may reflect optimization budget, learning-rate mismatch, initialization, or compute differences.

## Highest-Priority Unanswered Questions

1. Does training improve exact completion on genuinely withheld transitions or mappings, with every evaluated relation absent from all training strings?
2. Does mixed coverage retain an advantage when the training examples are matched in token count and difficulty, and when evaluated on a pre-registered test never used for checkpoint selection?
3. What is the distribution of final and best-but-validation-selected accuracy over more seeds, and how much is due to initialization versus exemplar order?
4. Can the model generate correct completions reliably under deterministic decoding, not merely increase teacher-forced target probability?
5. Does explicit rule instruction help on unseen word-ending mappings if training and test use matched formats and the withheld mapping is truly novel?
6. Can a saved, minimal experiment runner reproduce the reported results from a clean checkout and expose all seed, data, checkpoint, and decoding settings?

## Proposed Next Experiments, Ranked by Expected Information Value

1. **Leakage-free alphabet transfer test (highest information value).** Freeze training sequences and a separate validation set for checkpoint selection. Construct a test set of transitions/relations absent as contiguous substrings from every training string; include varied positions and difficulty. Select a checkpoint only on validation data, then report final and selected-checkpoint performance on the untouched test. Publish exact strings, a leakage check, raw per-seed outputs, loss, greedy exact accuracy, and byte-level accuracy. This directly tests the promoted mixed-coverage claim.
2. **Matched, multi-seed curriculum ablation.** Compare original, mixed, and full-coverage curricula with equal token/update budgets, randomized example order, at least the existing four seeds plus additional predeclared seeds, and identical evaluation. Keep best-checkpoint selection on validation only. Report paired seed-level differences and uncertainty, including final checkpoint results.
3. **Held-out rule/content vs. response-format experiment.** Train explicit mappings for one set of words, keep distinct mappings and words entirely out of training, and include matched-format control examples. Score exact mapping, first-token/format compliance, and conditional correctness separately under greedy decoding. Use enough distinct held-out relations and paired seeds; archive outputs and code. This will test whether any rule content transfers beyond explanation-shaped text.

Before making additional curriculum promotions, also preserve an executable runner and raw result artifact for each study. Existing notebooks/notes remain useful as records, but they are not sufficient for independent reproduction.

## Overall Assessment

Research maturity has improved: the record now includes controls, multi-seed studies, explicit failure analyses, generated samples, and an effort to distinguish loss, generation, and rule accuracy. The research narrative also contains meaningful negative findings. The main weakness has shifted from lack of experiments to validity and provenance: the newer alphabet evaluations reuse training transitions, checkpoint selection reuses the evaluation set, and most numerical results cannot be rerun from artifacts present in this checkout.

**Established by records:** short-run optimizer-driven loss changes; repeatability of loss reduction on the original overlapping CVC items across ten seeds; sensitivity to training-data distribution; a large rationale-format loss effect; and low exact rule-answer generation under the tested conditions.

**Not established:** robust held-out transfer of alphabet rules, causal superiority of mixed coverage, stable mastery across seeds, general inability to learn rules, or a model-size/capacity boundary. The results support a carefully bounded claim: this setup readily fits repeated byte patterns and can acquire response-format statistics, while reliable free-generation of novel sequence completions remains weak and inconsistent.

## Related Sources

- [[2026-10-25 AI School Independent Research Audit|Earlier independent audit]]
- [[Development/Experiments/Experiments Index|Experiments index]]
- [[Development/Experiments/2026-10-23 Experiment A — Held-Out Test|Experiment A — Held-Out Test]]
- [[Development/Experiments/2026-10-23 Experiment B — Control Group|Experiment B — Control Group]]
- [[Development/Experiments/2026-10-23 Experiment C — Multiple Random Seeds|Experiment C — Multiple Random Seeds]]
- [[Development/Experiments/2026-10-23 Experiment D — Inspect Tokenization|Experiment D — Inspect Tokenization]]
- [[Development/Experiments/2026-10-23 Experiment E — Reasoning|Experiment E — Reasoning]]
- [[Development/Experiments/2026-10-23 Experiment F — Multi-Seed Rationale Transfer|Experiment F — Multi-Seed Rationale Transfer]]
- [[Development/Experiments/2026-10-23 Experiment G — Rule Learning vs Format Learning|Experiment G — Rule Learning vs Format Learning]]
- [[Development/Experiments/2026-10-24 Coverage Fix Multi-Seed Follow-up|Coverage fix multi-seed follow-up]]
- [[Development/Experiments/2026-10-24 Lesson 1.1 Updated Test|Updated Lesson 1.1 test]]
- [[Development/Experiments/2026-10-24 Comprehensive Diagnostic - Held-Out Expansion|Expanded held-out diagnostic]]
- [[Development/Experiments/2026-10-24 Model Size Comparison - Larger Model Test|Model size comparison]]
- [[Development/Decisions/ADR-0002 Mixed Coverage for Alphabet Sequences|ADR-0002 mixed-coverage decision]]
- [[02-School/Preschool/Lessons/Lesson-1.1-Alphabet-Sequences|Preschool Lesson 1.1]]
- [[02-School/Preschool/Assessments/Assessment-1-Pattern-Sequences|Assessment 1]]
- [[02-School/Preschool/Curriculum|Preschool curriculum]]
