---
title: "Side Experiment - Is Seed 42 Actually Special?"
type: experiment
status: planned
tags:
  - ai-school
  - learn-000
  - random-seeds
  - reproducibility
  - cross-project
  - future-experiment
created: 2026-10-24
updated: 2026-10-24
---

# Side Experiment - Is Seed 42 Actually Special?

## Status

**Parked for later. Not part of the current experiment sequence.**

This is a cross-project investigation prompted by a recurring observation: seed 42 appears to perform unusually well in multiple experiments, including AI School language-model training and the separate `learn_000` game-AI project. Language models also frequently favor the number 42 when asked to choose a number or suggest a random seed.

These observations may have different explanations and must be investigated separately.

## Question

Does seed 42 have a reproducible performance advantage across different experiments, or does the apparent pattern result from chance, shared implementation details, selection bias, or the cultural prominence of the number 42?

## Hypotheses

- **H1 — Chance:** Seed 42 is an ordinary seed, and its apparent advantage is random variation.
- **H2 — Shared implementation effect:** Seed 42 produces favorable random sequences in particular RNG implementations or initialization procedures.
- **H3 — Cross-task effect:** Seed 42 performs unusually well across multiple tasks or configurations, beyond what would be expected from the tested seed population.
- **H4 — Selection bias:** Seed 42 appears exceptional partly because memorable successes are more likely to be noticed, recorded, or retested.
- **H5 — Language-model number preference:** Models favor 42 because of patterns learned from human-generated text, independently of whether it is a good experimental seed.

These hypotheses are not mutually exclusive.

## Investigation Plan

### 1. Establish the observation

Review existing experiment records from both projects.

- Identify every documented comparison involving seed 42.
- Record the other seeds, configurations, evaluation metrics, and outcomes.
- Distinguish results recorded systematically from results noticed retrospectively.
- Identify shared RNG implementations, initialization procedures, and other common components.
- Record unsuccessful experiments as well as successful ones.

Do not treat the strongest remembered results as a representative sample.

### 2. Compare seed 42 against other seeds

Run a controlled seed comparison in each project.

- Hold the model architecture, training procedure, data, and evaluation protocol fixed within each experiment.
- Select comparison seeds without examining their outcomes.
- Include seed 42 as a predefined candidate, not as a seed chosen after observing results.
- Record all seeds, failures, metrics, and checkpoints.
- Compare distributions, not just the winner and average.

For AI School, retain the current accepted Mixed Fixed curriculum as the baseline if the experiment begins while that curriculum remains appropriate. Freeze the configuration before running the comparison.

For `learn_000`, choose and document a specific game, model configuration, training budget, and evaluation protocol before starting.

### 3. Test implementation dependence

Where practical, compare seed behavior across different RNG implementations or initialization procedures.

Document the distinction between the numeric seed and the random sequence it produces. The same integer seed does not necessarily produce equivalent sequences across different RNGs, libraries, or implementations.

If seed 42 performs well only with one implementation, investigate that implementation before suggesting a general seed effect.

### 4. Test across tasks and configurations

Check whether any observed advantage persists across multiple tasks or materially different configurations.

- Keep comparisons controlled within each task.
- Report results separately by project and task.
- Distinguish repeated runs of one setup from genuinely different experimental conditions.
- Avoid treating correlated experiments as independent evidence.

### 5. Use an independent seed gauntlet

Once the initial protocol is established, run a larger batch of seeds selected without inspecting their performance.

- Define the seed population and evaluation metrics in advance.
- Choose the batch size before examining results.
- Evaluate every seed under the same conditions.
- Record all outcomes, not only the top performers.
- Compare seed 42 against the complete distribution and report its rank and uncertainty.

A large batch is useful only if the evaluation is consistent and the analysis accounts for the number of seeds tested.

### 6. Control selection bias with a fresh evaluation

Reserve an untouched final evaluation set or test protocol.

- Use the initial results to identify candidate seeds.
- Define the finalist-selection procedure before evaluating finalists on the untouched test.
- Do not use final-test results to tune configurations or repeatedly select new winners.
- If a seed is selected for further tuning, evaluate the resulting configuration on new independent data or tasks.

For AI School, ensure that final evaluation contexts are genuinely excluded from training and seed selection. For game AI, use an evaluation protocol that does not reuse the same outcomes that determined which seeds were finalists.

### 7. Investigate the language-model preference separately

Test whether language models disproportionately choose 42 when asked to select a number or random seed.

- Use several models and repeated trials.
- Keep prompt wording and allowed number ranges controlled.
- Compare number frequencies against an appropriate baseline.
- Record whether models explain their choice or simply output a number.
- Do not interpret a preference for saying "42" as evidence that seed 42 improves training.

## Measurements

| Measurement | Purpose |
|---|---|
| Per-seed performance | Preserve the full result distribution |
| Mean, median, spread, and rank | Measure typical performance and variability |
| Seed 42 percentile | Quantify how unusual its result is |
| Best versus final checkpoint | Detect checkpoint-selection effects |
| Performance on untouched evaluation | Test whether apparent advantages persist |
| Results by project, task, and RNG | Identify implementation-specific patterns |
| Number-choice frequency by model | Measure the separate language-generation bias |

Select task-specific performance metrics before running the experiment.

## Interpretation Rules

- A strong result in one small batch is preliminary evidence, not proof of a special seed.
- An advantage in both projects is more interesting, but does not establish independence if the projects share relevant implementation details.
- An advantage that disappears with another RNG suggests implementation dependence rather than a universal property of the integer 42.
- A seed that wins a large search may still be overfit to the selection metric. The untouched evaluation is essential.
- A model's preference for the number 42 and a seed's measured performance are separate phenomena unless evidence connects them.

## Success Criteria

The investigation succeeds if it establishes a reproducible, appropriately qualified answer to whether seed 42 performs unusually well under defined conditions.

A "perfect seed" should be defined operationally for each task. It should not mean merely winning a search or achieving 100% on a test repeatedly used for selection.

Even if seed 42 proves ordinary, the investigation remains useful: it establishes a baseline for seed variance and improves the project's experimental discipline.

## Expected Deliverables

- A consolidated record of existing seed-42 observations across both projects.
- A frozen, reproducible comparison protocol.
- Results for every tested seed.
- An analysis of implementation dependence and cross-task consistency.
- An independent final evaluation.
- A conclusion distinguishing observed evidence from unresolved explanations.

## Related Work

- [[ADR-0002: Mixed Coverage for Alphabet Sequences]]
- [[2026-10-24 Lesson 1.1 Updated Test]]
- `learn_000` seed comparisons and game-AI experiment records

## Final Reminder

**The goal is not to prove that 42 is special. The goal is to give it a fair test.**

The answer may be that 42 is ordinary, that it benefits from a particular implementation, or that it performs unusually well under a defined set of conditions. Any of those outcomes is scientifically useful.
