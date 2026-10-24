---
title: "Lesson 4.3 — Description Chains"
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
# Lesson 4.3 — Description Chains

## Objective
Teach the model to continue description sequences where attributes build up or follow a pattern.

## Teaching Material & Exemplars
1. **Building descriptions:**
   - `The cat is big. The cat is red. The cat is ` -> `soft.`
   - `The dog is small. The dog is black. The dog is ` -> `fast.`
   - `The bird is tiny. The bird is blue. The bird is ` -> `fast.`
   - `The frog is green. The frog is small. The frog is ` -> `wet.`
   - `The pig is pink. The pig is fat. The pig is ` -> `slow.`

2. **Consistent pattern:**
   - `The ball is round. The ball is red. The ball is ` -> `big.`
   - `The box is square. The box is blue. The box is ` -> `hard.`
   - `The cup is small. The cup is white. The cup is ` -> `full.`
   - `The hat is black. The hat is big. The hat is ` -> `new.`
   - `The bag is brown. The bag is old. The bag is ` -> `full.`

3. **Varied attributes:**
   - `The sun is hot. The sun is bright. The sun is ` -> `big.`
   - `The moon is white. The moon is round. The moon is ` -> `far.`
   - `The apple is red. The apple is round. The apple is ` -> `sweet.`
   - `The cake is big. The cake is sweet. The cake is ` -> `new.`
   - `The ice is cold. The ice is hard. The ice is ` -> `wet.`

## Practice Exercises
- Complete: `The fox is red. The fox is big. The fox is ` -> `fast.`
- Complete: `The rock is hard. The rock is gray. The rock is ` -> `cold.`
- Complete: `The kite is blue. The kite is big. The kite is ` -> `new.`

## Notes
This tests sequential pattern completion where the model must infer the next attribute. The attributes are plausible but not strictly logical - the key is learning the pattern of continuing the description chain. As the curriculum notes say, this is pattern completion, not reasoning.
