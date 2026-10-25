---
title: "AI School — Living Whitepaper"
type: overview
status: active
tags:
  - ai-school
  - whitepaper
  - research
  - project-overview
created: 2026-10-25
updated: 2026-10-25
changelog:
  - date: 2026-10-25
    change: "Established the living project whitepaper with current design, evidence boundaries, repository status, and research priorities."
---

# AI School — Living Whitepaper

> [!abstract] Current summary
> AI School is a human-directed research project exploring whether a small, randomly initialized language model can acquire useful language and reasoning behaviors through structured lessons and feedback. The project values controlled tests and preserved evidence over fluent demonstrations. Current records show reliable short-run loss changes on familiar material and strong sensitivity to response format; they do not establish robust transfer, rule understanding, or preschool-level capability. The current repository also lacks the original `harness/` implementation, so parts of the intended system are not runnable from this checkout.

**Evidence snapshot:** 2026-10-25. This is the maintained project synthesis, not a replacement for source experiment records. Each result below links to its underlying record; update this document when the architecture, evidence, or research direction materially changes.

## 1. Purpose and research question

AI School investigates how a small model behaves when it is initialized without pretrained weights, taught through explicit examples, and evaluated with controlled assessments. The central research question is:

> What can a small learner model acquire from a limited curriculum, and which apparent improvements survive leakage checks, matched controls, multiple seeds, and direct measurement of the intended behavior?

The project distinguishes **parameter learning** from **retrieval of external notes**, **response-format imitation**, and **self-assessment**. A lower teacher-forced loss means the model assigned more probability to a target sequence. It does not by itself show that the model can produce the answer, transfer a rule, understand a concept, or calibrate its own knowledge.

## 2. Project design

### Learner model

The accepted architecture decision describes a roughly 25-million-parameter causal Transformer initialized from random weights, trained through full-parameter updates rather than adapters on a pretrained model. Historical experiments used a byte tokenizer with four special IDs and 256 byte IDs (260 total), while the model's output layer was configured for 4,096 classes. That mismatch became a major measurement confound in the 2026-10-25 CVC study. The design decision and historical parameter counts are in [[Development/Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001]]; per-run settings belong in the experiment records.

### School and environment

The vault organizes curricula, teacher profiles, assessments, learner records, experiments, and reports. The intended learning cycle is lesson, practice, assessment, feedback, and remediation. These materials specify a research environment; their presence does not mean the loop is currently implemented or that a model has met the curriculum's goals. See [[Home]], [[02-School/Preschool/Curriculum|Preschool Curriculum]], and [[02-School/Preschool/Teacher|Preschool Teacher]].

### Research workflow

Experiments are documented before implementation and execution. Protocols fix conditions, data splits, controls, metrics, seeds, and stopping rules. Runs preserve provenance, logs, raw outputs, and failed attempts. Analysis distinguishes measured results from interpretation and records the limits of each claim. See [[00-System/Experiment Workflow|Experiment Workflow]], [[00-System/Documentation Standard|Documentation Standard]], and the [[Development/Experiments/Experiments Index|Experiments Index]].

## 3. What the evidence currently says

| Topic | Recorded evidence | What it does not establish |
| --- | --- | --- |
| Fitting familiar examples | Several short training studies report reproducible reductions in target loss on items adjacent to or overlapping training. | Broad generalization or reliable answer generation. |
| Controls and generic exposure | Unrelated-English training also changes target loss, so some improvements can arise from general byte/statistical exposure. | A phonics-specific causal mechanism without better matched tests. |
| CVC transfer, v2 | In the 10-seed controlled study, the far-item full-head NLL gain contrast (phonics minus shuffled) was −1.229, with a 95% seed-bootstrap interval [−2.514, 0.086]. Letter-conditional NLL worsened in every aggregate condition/stratum; the model shifted probability away from 3,836 impossible output IDs. | Ordered-phonics transfer or a shuffled-training advantage. The interval spans zero, and the eight far words are fixed items, not a sample of a wider word population. See [[Development/Experiments/2026-10-25 Controlled CVC Transfer Replication|canonical experiment record]] and [[Development/Experiments/2026-10-25 Controlled CVC Transfer Replication - Completed Run|detailed run analysis]]. |
| Format and explicit rules | Experiment G reports that explicit-rule training raised hyphen-format compliance to 52.9%, while exact ending matches were 1/70. Most mappings had training exposure and the truly novel probe was very small. | General rule learning, systematic mapping, or reliable reasoning. See [[Development/Experiments/2026-10-23 Experiment G — Rule Learning vs Format Learning]]. |
| Preschool sequence assessment | The independent research audit found that purported held-out alphabet transitions occurred in training and that the best checkpoint was selected on the same items used for reporting. | The curriculum's transfer or graduation claims. The curriculum remains an instructional specification pending valid assessments. See [[07-Reports/2026-10-25 AI School Independent Research Audit - Updated Evidence]]. |

The project-level interpretation is therefore intentionally narrow: the records support short-run optimization effects and response-format sensitivity under tested conditions. They do not currently demonstrate robust transfer, abstract rule learning, coherent rationale, or preschool learning capability. The independent audit and its source links provide the full evidence inventory and caveats.

## 4. Current implementation status

The repository's current tracked tree contains the vault, root `experiments/` scripts, and tests, but no `harness/` directory. This differs from the original system diagrams and some older project notes. The v2 CVC runner imports `harness.learner.config`, `harness.learner.model`, and `harness.learner.tokenizer`, so it cannot run from this checkout as-is. The historical implementation remains inspectable in Git history; it is not current tracked source.

The v3 follow-up protocol proposal is documented in [[Development/Experiments/2026-10-25 Controlled CVC Transfer Replication v3 - Matched Vocabulary]]. It proposes a new 260-token model configuration and a runner-owned minimal model implementation. The protocol is not yet frozen or approved for execution; neither the implementation nor the v3 run exists.

The old [[Development/Project Overview|Project Overview]] and [[Development/Architecture|Architecture]] describe the original design and must be read with this implementation caveat. Update them when the execution architecture is restored or replaced; do not infer implementation from an intended diagram.

## 5. Research priorities

1. Review the v3 protocol, then implement a reproducible runner and minimal model module without silently restoring the removed harness.
2. Verify a data-only preflight and a small server smoke test before considering training approval.
3. Run the 260-token follow-up only after code, data, output schema, and server revision have been reviewed and execution is explicitly approved.
4. Treat v3 as a fixed-item follow-up because its word outcomes were already inspected in v2. Before making broader claims, preregister a larger independently sourced and sealed item set.
5. Reconcile the curriculum, teacher guidance, architecture notes, and experiment records with evidence before using them as capability claims or graduation criteria.

The current experiment lifecycle and server steps are documented in [[00-System/Experiment Workflow|Experiment Workflow]].

## 6. Interpretation commitments

- Report negative, failed, and inconclusive runs alongside successful runs.
- Keep hypotheses, planned methods, measured observations, interpretations, and decisions distinct.
- Do not treat seeds as independent test items or reuse test examples for checkpoint selection.
- Label the exact task: byte-level next-token prediction is not equivalent to reading, word meaning, phonological awareness, or reasoning.
- Keep historical experiment claims intact; add corrections, follow-ups, and new model versions as linked records.
- Treat curricula and teacher profiles as specifications unless a valid assessment demonstrates the claimed behavior.

## 7. Maintaining this whitepaper

This is a living synthesis, not a live data feed. Update it when a validated experiment materially changes the project-level evidence, when architecture or implementation status changes, or when a research priority is adopted or completed. Append a dated changelog entry, link the underlying records, and preserve earlier experiment conclusions. The experiment records and repository remain the sources of truth for detailed methods and measurements.

## Related

- [[Home|AI School home]]
- [[00-System/Computing Environment|Computing Environment]]
- [[Development/Project Overview|Project Overview]]
- [[Development/Architecture|Architecture]]
- [[Development/Roadmap|Roadmap]]
- [[07-Reports/Reports Index|Reports Index]]
- [[Development/Experiments/Experiments Index|Experiments Index]]
