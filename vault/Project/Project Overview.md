---
title: Project Overview
type: project
status: active
tags:
  - project
  - python
  - ai-school
created: 2026-10-23
updated: 2026-10-23
---

# Project Overview — AI School Harness

## Identity
- **Project Name:** AI Learner Laboratory Harness
- **Purpose:** A modular Python coordinator that mediates interactions between an AI learner model, subject-specific teachers, an evidence-based assessment engine, and an Obsidian vault environment.
- **Language/Stack:** Python 3.13+ (standard library + minimal dependencies)
- **Primary Environment:** Linux (Debian 14.2/Python 3.13)

## Goals

### In Scope
1. **Sandboxed Vault Manager:** Strict permission enforcement for reading and writing files based on caller role (`Learner`, `Teacher`, `Assessment`, `Human`).
2. **Subject Teaching Engine:** Loading teacher profiles and curricula from `02-School/<Subject>/` and orchestrating lesson interactions.
3. **Assessment & Rubrics Engine:** Evaluating student test answers against rubrics with evidence tracking.
4. **Student Lifecycle Loop:** Driving the cycle of: Lesson -> Practice -> Exam -> Grading -> Self-Reflection -> Remediation / Advancement.

### Out of Scope (Initial Phase)
- Autonomous weight fine-tuning or backpropagation pipelines.
- Elaborate GUI dashboards (Obsidian serves as the UI).
- Unrestricted internet access or arbitrary shell tool execution.

## Related Notes
- [[Architecture]]
- [[Build and Test]]
- [[Roadmap]]
- [[00-System/Permissions|Permissions Matrix]]
- [[00-System/Harness-Rules|Harness Rules]]
