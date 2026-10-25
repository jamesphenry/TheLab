---
title: AI Learner Laboratory - Home
type: hub
status: active
tags:
  - ai-school
  - learner-lab
created: 2026-10-23
updated: 2026-10-25
---

# AI Learner Laboratory — Obsidian Hub

> [!abstract] Project at a Glance
> **Project:** AI Learner Laboratory (AI School)
> **Harness Stack:** Python 3.13
> **Purpose:** Experimental developmental environment for an AI learner model featuring subject-specific teachers, evidence-based assessments, metacognitive self-direction, idle reflection, and human guidance.

## Core Navigation

- [[NOTES|Discussion Notes & Blueprint]]
- [[00-System/Harness-Rules|System Rules & Invariants]]
- [[00-System/Permissions|Permissions Matrix]]
- [[00-System/Schedule|Routines & Schedule]]
- [[01-Learner/Goals|Learner Goals]]
- [[01-Learner/Self-Assessment|Self-Assessment Tracker]]
- [[01-Learner/Current-Questions|Learner Questions]]
- [[02-School/Language/Teacher|Language & Reading School]]
- [[02-School/Mathematics/Teacher|Mathematics School]]
- [[02-School/Programming/Teacher|Programming School]]
- [[Development/README|Development Documentation]]
  - [[Development/Project Overview|Harness Project Overview]]
  - [[Development/Architecture|System Architecture]]
  - [[Development/Roadmap|Development Roadmap]]
  - [[Development/Build and Test|Build & Test Guide]]
  - [[07-Reports/Reports Index|Research & Assessment Reports]]
- [[00-System/Vault Architecture|Vault Architecture and Documentation Guides]]
- [[00-System/Experiment Workflow|Experiment Workflow Guide]]
- [[00-System/Server Experiment Access|Server Experiment Access]]
- [[future|Future Research Directions (Brainstorm)]]

## Current Milestone Focus

- **Objective:** First End-to-End Tabula Rasa Learning Cycle.
- **Model Target:** BabyLM ~25M Parameter Transformer (randomly initialized).
- **Initial Subject:** Early Language & Reading (Stage 0: Phonics & Words -> Stage 1: Basic Associations).
- **Milestone Definition:** *The learner starts at random weights, receives lessons, fails an assessment, adapts via live gradient updates, and demonstrates verifiable transfer on a fresh assessment.*

## Project Principles

- **Separation of Concerns:** The Python harness coordinates, enforces folder permissions, and records events.
- **Technical Access Controls:** Permissions are enforced in harness code, not merely prompt instructions.
- **Evidence-Based Grading:** Mastery requires verified test outcomes evaluated against rubrics.
- **Three Knowledge Layers:** Keep distinct: model capability, external notes, and learner self-assessment.
