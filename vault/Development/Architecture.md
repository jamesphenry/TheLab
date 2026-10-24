---
title: Harness Architecture
type: architecture
status: active
tags:
  - ai-school
  - architecture
  - python
created: 2026-10-23
updated: 2026-10-23
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

## Module Responsibilities
- `harness/vault/`: Filesystem interface with path sanitization, permission validation, and markdown parsing.
- `harness/models/`: Uniform LLM client abstraction (Ollama, Gemini/OpenAI, local server, or deterministically testable mock).
- `harness/school/`: Teacher prompt loaders, lesson dispatchers, rubric evaluation runners.
- `harness/sandbox/`: Safe execution of C code, tests, or mathematical verification.
- `harness/core/`: Event loop, routine scheduler, and experiment recorder.

## Learner Model Specification (BabyLM ~25M)
Per [[Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001]]:
- **Architecture:** Causal Transformer (Decoder-only), trained from scratch (randomly initialized weights).
- **Parameters:** ~25M ($n_{layers}=8, d_{model}=512, n_{heads}=8, d_{ff}=2048, \text{vocab}=4096, \text{context}=512$).
- **VRAM Footprint:** ~430 MB total for FP32 weights, gradients, and full AdamW optimizer state.
- **Hardware Target:** NVIDIA Tesla P4 (8 GB VRAM, Pascal `sm_61`).
- **Learning Loop:** Interactive real-time forward and backward gradient updates ($< 15\text{ ms}$ per step).

## Security & Isolation Invariants
1. All path operations validate that `os.path.realpath(path)` is within the authorized role directory.
2. Learner role cannot write to `00-System/`, `02-School/`, or `07-Reports/`.
3. Teacher role cannot write to student memory or tamper with other subjects.
