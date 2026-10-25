---
title: AI School — Independent Research Audit
type: report
status: completed
tags:
  - ai-school
  - research-audit
  - report
created: 2026-10-25
updated: 2026-10-25
---

# AI School — Independent Research Audit

**Audit date:** 2026-10-25

**Scope:** Research evidence documented in the vault and supporting implementation/source records available in this repository.

## Executive Summary

The project has a coherent early research direction: determine whether a randomly initialized learner can acquire measurable capabilities through instruction and update its weights, while distinguishing model capability from external memory and self-assessment. The current evidence establishes a limited engineering result and a preliminary optimization result. It does not yet establish durable language learning, phonemic understanding, generalization, or transfer.

The baseline note documents a 27,330,560-parameter model that initializes, computes loss, takes optimizer steps, and generates correctly shaped output. The Lesson 1.1 record documents training loss falling from 6.1193 to 0.6251 and mean target loss falling from 8.4218 to 4.6563 across four items. However, those evaluation target words (`mat`, `hot`, `run`, `bed`) and their relevant patterns occur in the five training exemplars. The result is therefore compatible with memorization or local sequence fitting; the record does not establish a held-out test. Generated samples remain imperfect, and the exact assessment defined in the curriculum is not the assessment reported in the lesson experiment.

The most important next step is to run and archive the already-authored independent evaluation in `harness/experiments/experiment_a.py`, which defines new sentence contexts and CVC targets absent from its listed training set. That script has no result record in the inspected materials, so this audit makes no claim about its outcome. Replicate across multiple initialization seeds and add controls before interpreting any improvement as a general learning capability.

**Evidence labels used here:** *Observed* means directly stated in an inspected record or code; *Inferred* means an interpretation consistent with those observations; *Hypothesis* means an untested explanation or proposed design.

## Scope and Sources Inspected

### Vault conventions

- `Templates/Experiment Template.md`: YAML fields `title`, `type`, `status`, `tags`, `created`, `updated`, then question, hypothesis, conditions, procedure, results, interpretation, limitations, conclusion, and related sources.
- `Home.md`: main navigation hub with wiki links grouped under Core Navigation.
- Existing report: `07-Reports/2026-10-23-Language-Assessment-Report.md`; it uses `type: report`, `status: completed`, date fields, and tags.
- `07-Reports/` had no report index. Existing indexes elsewhere in the vault use `type: index`, a short purpose statement, and bullet wiki links. This audit adds a reports index following that convention.
- Experiment notes are stored under `Development/Experiments/`; the two documented records are dated `2026-10-23 ...`. Reports use `YYYY-MM-DD` in filenames.

### Research and project sources

- [[Development/Experiments/2026-10-23 BabyLM 25M Baseline Initialization|Baseline initialization and gradient-step experiment]]
- [[Development/Experiments/2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition|Lesson 1.1 phonics experiment]]
- [[07-Reports/2026-10-23-Language-Assessment-Report|Language assessment report]]
- [[03-Experiences/2026-10-23-Language-Lesson-1|Language lesson session log]]
- [[02-School/Language/Lessons/Lesson-1.1-Alphabet-and-Phonics|Lesson 1.1 teaching material]]
- [[02-School/Language/Assessments/Assessment-1.1|Assessment 1.1 rubric and items]]
- [[Development/Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001 model decision]]
- [[NOTES|Discussion notes and research principles]]
- [[01-Learner/Self-Assessment|Learner self-assessment]] and [[01-Learner/Current-Questions|current questions]]
- [[Development/Architecture|Harness architecture]], [[Development/Project Overview|project overview]], [[Development/Roadmap|roadmap]], and [[02-School/Language/Curriculum|language curriculum]]
- Supporting source inspected: `harness/experiments/experiment_a.py`, `harness/school/classroom.py`, `harness/learner/config.py`, `harness/learner/model.py`, and `harness/learner/tokenizer.py`.

The available corpus is small: two experiment notes, one assessment report, one session log, one architecture decision, and design/curriculum notes. No run artifact for `experiment_a.py`, raw training trace for the baseline or Lesson 1.1, machine-readable dataset manifest, or multi-seed result table was found. This audit did not launch experiments or training runs.

## Research Questions and Theoretical Framework

### Main questions documented

The discussion notes propose investigating whether a learner can improve through structured instruction, whether improvement generalizes to unfamiliar problems, whether persistent notes and model weights contribute differently, and whether self-assessment tracks measured capability. The roadmap narrows the first milestone to a full learning cycle with a fresh assessment after instruction.

The first concrete model question is narrower: can a randomly initialized causal Transformer execute training updates and reduce loss on lesson material, then improve on an assessment? The intended stronger claim is that it learns reusable language patterns, rather than only replaying examples or producing text that looks more structured.

### Theoretical commitments and status

- **Separation of model capability, retrievable notes, and self-assessment** — *Documented design principle* in [[NOTES|Discussion Notes]]. The inspected Lesson 1.1 experiment concerns direct parameter updates, but no controlled memory-versus-weight comparison is recorded.
- **A from-scratch model reduces pretrained-knowledge confounds** — *Documented rationale* in [[Development/Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001]]. Random initialization addresses pretrained language knowledge; it does not, by itself, show what was acquired during a short training run or exclude memorization of the supplied examples.
- **Unfamiliar tests are required to support transfer** — *Documented principle* in [[NOTES|Discussion Notes]] and [[02-School/Language/Assessments/Assessment-1.1|Assessment 1.1]]. The actual recorded Lesson 1.1 measurements do not meet this test's stronger criterion because targets overlap the exemplars.
- **Human-like behaviors should be operationalized and not inferred from fluent text** — *Documented principle* in [[NOTES|Discussion Notes]]. The present records do not test agency, metacognition, consciousness, or durable behavioral change.

## Chronological Research Narrative

### 2026-10-23 — Initial system design

The discussion note frames AI School as a long-running environment with lessons, assessments, external memory, reflection, and human guidance. It explicitly warns against treating self-reports or human-like behavior as evidence of capability. These are design hypotheses and methodological cautions, not empirical findings.

### 2026-10-23 — Model choice and baseline feasibility

ADR-0001 selects a randomly initialized causal Transformer instead of a pretrained model, targeting roughly 25 million parameters and interactive full-parameter updates. The baseline experiment configures 8 layers, width 512, 8 heads, vocabulary dimension 4096, and context length 128; it reports 27,330,560 parameters and initial loss about 8.32, close to `ln(4096)`. The note reports successful tests for forward loss, training-step loss decrease, generation shape, and tokenizer roundtrip.

This is evidence of basic implementation/test viability. The run record does not provide an exact seed value, raw outputs, hardware memory measurements, or a repeated-seed distribution. The ADR's P4 speed and memory figures are design estimates in the decision record; the baseline experiment itself says CPU development mode and does not establish P4 performance.

### 2026-10-23 — Lesson 1.1

The lesson record reports five text exemplars, 15 iterations, and improved loss on four prompt-target pairs. The training and evaluation facts are summarized below. A follow-up experiment script was found in the working tree; it defines novel contexts and unseen words (`bat`, `hen`, `pot`, `bus`) but has no captured results in the available records.

## Experiment Inventory and Findings

| Record / artifact | Question and method | Reported outcome | What it supports | Key limitation |
| --- | --- | --- | --- | --- |
| [[Development/Experiments/2026-10-23 BabyLM 25M Baseline Initialization|Baseline initialization and gradient step]] | Randomly initialized model; forward loss, five AdamW steps on a fixed synthetic sequence, generation shape, tokenizer roundtrip | 27,330,560 parameters; initial loss ≈8.32; tests report loss reduction and shape/roundtrip success | The implementation can initialize and execute a basic optimization path | No exact seed, raw log, repeated runs, natural-language learning, or target-hardware benchmark is documented |
| [[Development/Experiments/2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition|Lesson 1.1 phonics experiment]] / [[03-Experiences/2026-10-23-Language-Lesson-1|session log]] / [[07-Reports/2026-10-23-Language-Assessment-Report|assessment report]] | Five exemplars, 15 iterations, four prompt-target losses before and after | Training loss 6.1193→0.6251; target-average loss 8.4218→4.6563; individual losses improve 0.2583–6.2161; samples are not consistently correct | Training on the five strings changed model probabilities on the measured completions | Evaluation targets are in the exemplars; only one documented condition/run; generation is sampled and inaccurate; no independent transfer result |
| `harness/experiments/experiment_a.py` | Code defines 5 exemplars, 15 iterations, seed 42, novel contexts with known words and a second set of four CVC targets absent from the exemplar strings | No output or result note found | A potentially discriminating follow-up is specified in code | Results, actual execution, and reproducibility are unverified; the script's existence is not evidence of an outcome |

### Lesson 1.1 target overlap

The five training exemplars include “The cat sat on the mat.”, “The dog can run in the sun.”, “The sun is hot.”, “The red pen is on the bed.”, and “A cat can run.” The reported test targets are `mat.`, `hot.`, `run.`, and `bed.`. Every target word and spelling therefore appears in training; several contexts also substantially reproduce training sentences. Lower target loss is a real recorded metric change, but the evaluation is not held out by target vocabulary and offers weak evidence for transfer.

The separate Assessment 1.1 note specifies four different items (`The cat can `→`run`, `The sun is `→`hot`, `a b c `→`d`, and `A cat sat on a `→`mat`). The lesson experiment reports a different item set. The records do not explain whether the assessment was revised, whether the rubric items were administered, or how rubric levels were assigned. In particular, the experiment report's phrase “unseen evaluation prompts” must not be read as proof of unseen target patterns.

## Evidence Strength and Replication Status

### Strongest evidence

**Observed:** The baseline test record reports successful model initialization, loss computation, gradient updates, and generation tensor shape. The lesson session/report preserve numeric pre/post loss values and generated examples. These are useful first-run engineering and training observations.

### Moderate-to-weak evidence

**Observed:** The Lesson 1.1 mean target loss decreased by 3.7655 in its documented run. **Inferred:** The updates made the model assign greater probability to the supplied target sequences under those prompts. This is consistent with learning the training examples in the broad optimization sense, but it is not separable from memorizing those examples.

### Not established

- Transfer to new words or contexts; the recorded targets overlap training.
- Robustness across seeds, example order, data selection, or evaluation items.
- Durable retention after a delay or intervening training.
- Correct, reliable generation: none of the four shown completions exactly produces its target, and samples are stochastic.
- Phoneme awareness or word-boundary acquisition as a mechanism. The tokenizer maps UTF-8 bytes, so improvements in byte sequences do not independently demonstrate phonological representations.
- A “maximum entropy” distribution over all 4096 logits in the baseline: the tokenizer emits only 260 token IDs (four special tokens plus 256 byte values), while the model config uses 4096 output classes. The reported initial loss near `ln(4096)` is consistent with near-uniform output across the full configured head, but most output classes are not produced by this tokenizer. This mismatch should be resolved or explicitly justified before interpreting entropy or training efficiency.
- Planned Tesla P4 speed or memory performance. The recorded baseline used CPU development mode.
- Effectiveness of the defined Assessment 1.1 rubric: no rubric scoring record was found.

No experiment in the inspected notes has a documented replication across independent random seeds. The baseline records tests, but not repeated independent experiment runs. The Lesson 1.1 report calls the observed loss reduction “deterministic”; `ClassroomSession.run_learning_cycle` does not itself set a random seed, so that description is not sufficient evidence of deterministic results across executions.

## Relationships Between Theories and Experiments

| Theory or design claim | Relevant evidence | Audit judgment |
| --- | --- | --- |
| From-scratch initialization avoids pretrained language capabilities | ADR-0001 and baseline initialization note | Supported as a configuration choice by the records; not equivalent to proof of zero non-linguistic priors or general learning |
| Direct gradient updates can alter behavior | Baseline and Lesson 1.1 loss trajectories | Supported for measured loss/optimizer operations; scope limited to synthetic/few-string training |
| Lesson instruction teaches language patterns | Lesson 1.1 example fit and generated completions | Preliminary: target loss improves, but overlap and poor exact generation prevent a transfer claim |
| Fresh tests can distinguish learning from imitation | Assessment rubric and discussion notes | Methodologically sound goal, not achieved by the reported Lesson 1.1 measurements |
| Capability, external notes, and self-assessment are distinct | Discussion notes and self-assessment note | Clear conceptual separation, but no comparative experiment; self-assessment currently restates the same loss delta rather than independently calibrating mastery |

## Contradictions, Alternatives, and Limitations

1. **“Held-out” wording vs. target overlap.** The experiment asks about unseen evaluation prompts and the report claims lower loss on held-out targets, but the reported targets appear in training exemplars. The objective is correctly computed over target bytes after masking prompt positions; this does not make the target unseen.
2. **Rubric vs. administered test.** The specified Assessment 1.1 items differ from the items in the session and report. It is unclear which assessment was actually administered, and there is no rubric grade.
3. **Loss reduction vs. capability.** Training on text sequences is expected to lower loss on those sequences. This alone cannot distinguish useful abstraction from memorization, nor does loss reduction guarantee correct sampling.
4. **Generated appearance vs. reasoning/phonics.** Output that contains ASCII letters, spaces, or familiar words is not evidence of phonemic reasoning. The model is trained on UTF-8 byte tokens and the output samples are still malformed or target-inaccurate.
5. **Vocabulary mismatch.** Model output has 4096 classes but the tokenizer only encodes 260 IDs. Loss includes the full output head. This makes the initialization-entropy interpretation and output-space design important to revisit.
6. **Single-run confounding.** A single initialization and small, repeated exemplar set leave seed variance and data-order sensitivity unknown. The session runner shown in code does not seed Torch.
7. **Alternative explanations.** Improvements may arise from memorization, repeated exposure to exact byte substrings, context overlap, token-distribution adjustment, or stochastic sampling differences. These are not mutually exclusive with learning; the current design does not quantify their contributions.

## Highest-Priority Unanswered Questions

1. Does improvement persist on targets and contexts absent from training, relative to the same randomly initialized model before instruction?
2. How much does measured gain vary across seeds, and does it exceed an untrained baseline's variability?
3. Does the model generate correct completions, or only assign lower average loss to known byte strings?
4. Is any gain attributable to reusable CVC/character regularities, or mainly repeated sentence/template overlap?
5. How should the 4096-way model vocabulary be reconciled with the 260-ID byte tokenizer?
6. Does performance persist after a delay and unrelated updates, and does model weight retention differ from external-note retrieval?
7. Can the assessment procedure be fixed in advance and scored independently from instruction so that claimed rubric outcomes are auditable?

## Proposed Next Experiments, Ranked by Expected Information Value

1. **Run and archive the coded held-out evaluation.** Execute `harness/experiments/experiment_a.py` only as a future experiment, preserving raw output and environment details. Its two evaluation sets are useful: novel contexts with known words and CVC words absent from the five exemplars. Report per-item loss and exact generation accuracy, and verify no test strings or target words leak into training. This most directly tests whether the current effect extends beyond repeated targets. The current audit did not execute it.
2. **Replicate with multiple independent seeds and matched controls.** Fix the data and procedure; evaluate each seed before and after training; include an untrained control and a control with shuffled or irrelevant exemplar-to-target associations. Report distributions and item-level results, not only a best run. This estimates variability and tests whether exposure structure matters.
3. **Separate memorization, compositional generalization, and retention.** Pre-register disjoint train/dev/test words and contexts, test novel combinations plus delayed evaluation after intervening material, and include exact generation/character metrics alongside cross-entropy. Keep model weights fixed during assessment and avoid using evaluation examples in remediation. This tests generalization and durability.

Before interpreting these experiments, document/resolve the tokenizer-output vocabulary mismatch and make the assessment item set identical to the stated rubric or explicitly version the assessment.

## Overall Assessment of Current Research State

AI School is at an early prototype and pilot stage. The research principles are stronger than the present evidential design: the notes explicitly value falsifiability, unfamiliar tests, alternative explanations, and separating actual capability from self-assessment. The baseline provides initial engineering validation, and the Lesson 1.1 run provides a measurable optimization observation. Evidence for learning beyond the exact instructional material remains insufficient, and the intended milestone of failure followed by improvement on a genuinely fresh assessment is not yet documented as achieved.

**Established by the inspected records:** a particular randomly initialized model configuration can run forward/backward operations; one documented short training session reduced loss on its chosen completion items.

**Not established:** transfer, robust acquisition, calibrated mastery, durable capability, or the planned target-hardware performance. The independent held-out script may provide relevant evidence once results are recorded and replicated.

## Source Links

- [[Development/Experiments/2026-10-23 BabyLM 25M Baseline Initialization|Baseline experiment]]
- [[Development/Experiments/2026-10-23 BabyLM Lesson 1.1 Phonics and Word Acquisition|Lesson 1.1 experiment]]
- [[07-Reports/2026-10-23-Language-Assessment-Report|Assessment report]]
- [[03-Experiences/2026-10-23-Language-Lesson-1|Session log]]
- [[02-School/Language/Lessons/Lesson-1.1-Alphabet-and-Phonics|Lesson 1.1]]
- [[02-School/Language/Assessments/Assessment-1.1|Assessment 1.1]]
- [[Development/Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001]]
- [[NOTES|Discussion notes]]
- [[01-Learner/Self-Assessment|Self-assessment]]
- [[01-Learner/Current-Questions|Current questions]]
- Supporting code: `harness/experiments/experiment_a.py`, `harness/school/classroom.py`, `harness/learner/config.py`, `harness/learner/model.py`, `harness/learner/tokenizer.py`.
