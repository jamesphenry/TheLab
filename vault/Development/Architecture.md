---
title: Harness Architecture
type: architecture
status: active
tags:
  - ai-school
  - architecture
  - python
created: 2026-10-23
updated: 2026-10-25
---

# Architecture — AI School Harness

## System Summary
The harness coordinates an AI learner model, teacher agents, and deterministic assessment checkers while using the Obsidian vault as a shared, human-inspectable state representation.

```
+-----------------------------------------------------------+
|                      Python Harness                       |
|                                                           |
|  +-------------------+  +------------------------------+  |
|  |  VaultController  |  |       ExecutionSandbox       |  |
|  | (Permissions / IO)|  |     (Code/Check Runnings)    |  |
|  +-------------------+  +------------------------------+  |
|                                                           |
|  +-----------------------------------------------------+  |
|  |                  Lifecycle Engine                   |  |
|  | (Lesson -> Practice -> Exam -> Grade -> Remediate)  |  |
|  +-----------------------------------------------------+  |
|                                                           |
|  +-----------------------------------------------------+  |
|  |                    Model Client                     |  |
|  |      (Local Ollama / API Client / Mock Runner)      |  |
|  +-----------------------------------------------------+  |
+-----------------------------------------------------------+
                            |
                            v
               +-------------------------+
               |     Obsidian Vault      |
               | (Markdown File System)  |
               +-------------------------+
```

For the note organization and authority model, see [[00-System/Vault Architecture|Vault Architecture]].

> [!note] Implementation status
> The diagram represents the intended system boundary. Current code does not include all shown components; see the implementation-status section below before treating a box as implemented.

## Module Responsibilities
- `harness/vault/`: Filesystem interface with path sanitization, permission validation, and markdown parsing.
- `harness/learner/`: Current BabyLM model, tokenizer, and configuration.
- `harness/school/`: Current classroom learning-cycle orchestration.
- Repository-root `experiments/`: Tracked research and diagnostic scripts with selected JSON result bundles. The vault's `Development/Experiments/` holds the narrative records.

### Implementation status (checked 2026-10-25)

The current tracked repository has no `harness/` directory. This differs from the original architecture design documented above. The v2 CVC runner imports `harness.learner.config`, `harness.learner.model`, and `harness.learner.tokenizer`, so it is not runnable from the current checkout without restoring or replacing those modules. The historical implementation is available in Git history, not current source. See [[AI School Whitepaper|AI School — Living Whitepaper]] for current project status and the planned runner-owned model approach.

## Learner Model Specification (BabyLM ~25M)
Per [[Development/Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001]]:
- **Architecture:** Causal Transformer (Decoder-only), trained from scratch (randomly initialized weights).
- **Recorded model size:** Experiment records report 27,411,456 parameters for the lesson model. `vocab_size=4096` is the model head configuration; [[Development/Experiments/2026-10-23 Experiment D — Inspect Tokenization|tokenizer inspection]] reports only 260 encodable IDs.
- **Design target:** The ADR estimates about 430 MB training state and targets an NVIDIA Tesla P4 (8 GB VRAM, Pascal `sm_61`). The inspected experiment records use CPU development mode; the P4 memory and latency targets are not benchmarks established by those records.
- **Context:** The default config and experiment configurations differ; record the exact context length for each run rather than assuming 512.

## Security & Isolation Invariants
1. All path operations validate that `os.path.realpath(path)` is within the authorized role directory.
2. Learner role cannot write to `00-System/`, `02-School/`, or `07-Reports/`.
3. Teacher role cannot write to student memory or tamper with other subjects.
