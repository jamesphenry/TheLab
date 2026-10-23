# Agent Instructions — C Project and Obsidian Vault

## 1. Mission

Help develop and understand this C project while maintaining a trustworthy, navigable Obsidian record of its design, experiments, test evidence, decisions, and lessons.

The source repository and this vault have different jobs:

- The **source repository** is authoritative for code and executable behavior.
- The **vault** is authoritative for organized project notes, reasoning, experiment history, and human-readable context.
- Neither is a substitute for the other. Do not invent source behavior from notes or claim notes prove code behavior.

## 2. Start-of-task procedure

Before making meaningful changes:

1. Read `Home.md` and [[Project/Project Overview]].
2. Check [[Project/Build and Test]] for the actual build and test commands.
3. Inspect the relevant source files and current Git status in the code repository.
4. Read relevant architecture, decision, experiment, and debugging notes.
5. Identify the task, constraints, expected behavior, and how success will be verified.
6. If essential information is missing or an action could be destructive, ask before proceeding.

Do not assume paths, commands, dependencies, compiler flags, test counts, or runtime behavior. Verify them from the repository or ask.

## 3. Working rules

- Prefer small, understandable, reviewable changes.
- Do not rewrite unrelated code or documentation.
- Do not add third-party dependencies unless requested or clearly justified and approved.
- Preserve the project's established C standard, naming, formatting, and error-handling conventions.
- Do not claim a command passed unless it was actually run and its result inspected.
- If a test cannot be run, state why and distinguish that from a passing test.
- Inspect diffs before describing a change as complete.
- Never discard user changes, reset branches, force-push, delete files, or run destructive cleanup without explicit authorization.
- Do not put credentials, tokens, private keys, or sensitive personal data in the vault.
- Do not silently convert a hypothesis into a fact.

## 4. Evidence standard

When reporting a result, label the evidence clearly:

- **Observed:** directly seen in command output, source, or reproducible behavior.
- **Measured:** includes the conditions and measurement method.
- **Inferred:** interpretation supported by observations but not directly proven.
- **Hypothesis:** a possible explanation that still needs testing.
- **Unknown:** not yet checked or not established.

Include enough context to reproduce important findings: commit or code version, command, relevant configuration, test conditions, and result. Preserve exact error messages when useful.

## 5. Documentation duties

Update the vault when work changes or clarifies:

- architecture, module responsibilities, interfaces, invariants, or data flow;
- build instructions, dependencies, compiler flags, or supported environments;
- tests, test coverage, validation procedures, or known limitations;
- measured performance, experimental results, or conclusions;
- project decisions, rejected alternatives, or trade-offs;
- bugs, root causes, workarounds, or unresolved questions;
- the roadmap or next actions.

Use the relevant template under `Templates/`. Link the note from its index and link related notes using Obsidian wikilinks.

For a tiny change with no durable learning or operational impact, a session-log entry may be enough. Do not create paperwork just to create paperwork.

### Session log minimum

Record:
- date and task;
- what changed or was investigated;
- commands/tests actually run and their outcomes;
- evidence or commit reference;
- remaining issues;
- next step.

### Experiment minimum

Record:
- question and hypothesis;
- variables and controlled conditions;
- procedure;
- observations/results, including failures;
- interpretation and limitations;
- conclusion and next experiment.

Never fabricate numbers or fill gaps with plausible-looking values.

## 6. C-specific guidance

- Be precise about C standard and implementation-specific behavior.
- Distinguish defined behavior, implementation-defined behavior, unspecified behavior, and undefined behavior when relevant.
- Treat compiler warnings as useful evidence; do not suppress warnings merely to obtain a clean build.
- For pointer, memory, lifetime, integer, and concurrency issues, explain the relevant rules and how they were verified.
- Prefer a minimal reproducer for a suspected language or runtime issue.
- Use the project's existing tests and test framework first.
- Where available and appropriate, use sanitizers and memory-analysis tools; record which checks actually ran.
- Do not introduce a library or framework just to avoid understanding a small concept.
- When teaching, adapt to the user's current understanding. Do not dump a complete solution if the task is intended as a hands-on learning exercise; give a hint or a smaller next step when appropriate.

## 7. Suggested task loop

1. **Orient:** inspect the project, constraints, notes, and working tree.
2. **Plan:** state a short plan and define the verification criteria.
3. **Change:** make the smallest useful change.
4. **Test:** run the most relevant tests, then broader checks when appropriate.
5. **Review:** inspect the diff and look for regressions or undocumented assumptions.
6. **Document:** update the relevant notes and indexes.
7. **Report:** summarize changed files, evidence, limitations, and next steps.

For work requiring multiple roles, use a sequential Planner → Builder → Tester → Reviewer flow. Avoid simultaneous edits to the same files. The reviewer should inspect actual diffs and test evidence, not rely only on the builder's summary.

## 8. Git and synchronization

- Check `git status` before editing and before committing.
- Do not assume the vault and source repository have the same Git root.
- Do not commit automatically unless explicitly requested by the user or the project's established workflow clearly authorizes it.
- Keep generated binaries, build output, temporary files, local IDE state, secrets, and private machine configuration out of Git unless the project explicitly requires them.
- Before sync, rebase, merge, or push operations, inspect the current branch and working tree.
- Never use force-push as a routine conflict-resolution strategy.
- Record meaningful commit hashes in notes when they anchor a result.

## 9. Completion report

At the end of a task, report:

1. What changed.
2. Files and notes updated.
3. Tests/checks run and actual outcomes.
4. Anything not verified.
5. Known risks or open questions.
6. The next sensible step.

Be candid. A partial result with accurate limitations is better than a confident but unsupported success claim.
