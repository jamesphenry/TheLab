---
title: Component Permissions Matrix
type: specification
status: active
tags:
  - ai-school
  - system
  - permissions
created: 2026-10-23
updated: 2026-10-23
---

# Component Permissions Matrix

The harness enforces granular filesystem and tool permissions based on role:

| Component | Read Access | Write Access | Tool Permissions |
| :--- | :--- | :--- | :--- |
| **Learner** | `01-Learner/`, `02-School/*/Lessons/`, `03-Experiences/`, `04-Memory/`, `05-Dreams/` | `01-Learner/`, `03-Experiences/`, `04-Memory/`, `05-Dreams/` | Approved sandboxed tools (e.g. calculator, sandbox runner) |
| **Teacher** | `00-System/`, `02-School/<Subject>/`, `01-Learner/Self-Assessment.md` | `02-School/<Subject>/` (Lessons, Assignments, Assessments) | None (instruction/grading only) |
| **Assessment Engine**| Submitted learner answers, `02-School/<Subject>/Assessments/` | `07-Reports/`, Protected assessment records | Verifier runtimes (compiler, linter, unit test runner) |
| **Human Guide** | Unrestricted (`vault/`, harness configs, logs) | Unrestricted | All |

## Restrictions
- **Learner cannot modify:** `00-System/`, `02-School/` (curricula, rubrics, tests), or `07-Reports/` (grades).
- **Teacher cannot modify:** `00-System/`, other subjects' folders, learner memory, or previously finalized assessment reports.
- **Path Traversal:** All file paths resolved relative to `vault/` must strictly validate within the designated subfolder.
