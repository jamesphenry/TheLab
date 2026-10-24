---
title: "Lesson 4.1 — Action Chains"
type: lesson
status: active
tags:
  - ai-school
  - lesson
  - preschool
  - chains
created: 2026-10-24
updated: 2026-10-24
---
# Lesson 4.1 — Action Chains

## Objective
Teach the model to complete sequential action patterns where each step follows from the previous one.

## Teaching Material & Exemplars
1. **Simple sequential actions:**
   - `The cat sat. The cat ran. The cat ` -> `sat.`
   - `The dog ate. The dog slept. The dog ` -> `ate.`
   - `The bird flew. The bird ate. The bird ` -> `flew.`
   - `The frog hopped. The frog ate. The frog ` -> `hopped.`
   - `The pig ate. The pig slept. The pig ` -> `ate.`

2. **Different action sequences:**
   - `The boy ran. The boy fell. The boy ` -> `ran.`
   - `The girl played. The girl sang. The girl ` -> `played.`
   - `The pup ate. The pup slept. The pup ` -> `ate.`
   - `The cat ate. The cat played. The cat ` -> `ate.`
   - `The dog played. The dog slept. The dog ` -> `played.`

3. **Longer chains:**
   - `The cat sat. The cat ran. The cat jumped. The cat ` -> `sat.`
   - `The dog ate. The dog ran. The dog slept. The dog ` -> `ate.`
   - `The bird flew. The bird ate. The bird slept. The bird ` -> `flew.`

## Practice Exercises
- Complete: `The fox ran. The fox ate. The fox ` -> `ran.`
- Complete: `The ant crawled. The ant ate. The ant ` -> `crawled.`
- Complete: `The bee flew. The bee ate. The bee ` -> `flew.`

## Notes
This is pattern completion, not reasoning - the model learns to predict the next in a cyclic/recurring pattern. The key is repetition of actions across the chain. Keep the sequence length manageable (3-4 sentences).
