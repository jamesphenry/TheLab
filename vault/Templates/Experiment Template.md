---
title: "{{experiment_name}}"
type: experiment
status: planned
scripts: []
tags:
  - ai-school
  - experiment
created: {{date}}
updated: {{date}}
changelog:
  - date: 2026-10-25
    change: "Reorganized as a concise scientific-method record, with explicit procedure, results, and follow-up ideas."
---

# {{experiment_name}}

## Question

What do we want to find out? Keep this to one clear question where possible.

## Background and evidence

What existing observations or records motivate this experiment? Link to them. Separate established observations from open questions.

## Hypothesis

What result do we predict, and what observation would count against that prediction?

## Method

Briefly describe the model/system, data or items, conditions, controls, and how the outcome will be measured. Include only details needed to understand and reproduce this experiment; link to a fuller protocol if one exists.

### Procedure

List the steps actually followed. Before a run, this can be a short proposed procedure; after the run, update it to reflect what actually happened and note deviations.

1. {{step}}

## Results

Record what happened, including negative, failed, unexpected, and inconclusive outcomes. Link to logs and artifacts. Keep measured observations separate from interpretation.

| Condition / run | Observation or metric | Evidence / artifact |
| --- | --- | --- |
| {{condition}} | {{actual_observation}} | {{log_or_output}} |

## Interpretation

What do the results support? What do they not establish? Name plausible alternative explanations and relevant limitations.

## Conclusion

Answer the research question as far as the evidence allows. State whether the hypothesis was supported, contradicted, or unresolved.

## Possible next experiments

List a few useful follow-up questions or small experiments suggested by these results. These are ideas, not approved plans; promote one to a separate plan or protocol before implementation or execution.

- {{possible_follow_up}}

## Provenance and related material

- **Repository revision / commit:**
- **Scripts:** list repository-relative executable scripts in `scripts` frontmatter; use `[]` if none are recorded.
- **Data and split:** identify training, validation, and test items and any overlap relevant to the claim.
- **Seeds / environment / settings:**
- **Checkpoint selection and stopping rule:**
- **Artifacts / logs:**
- **Related notes:**
