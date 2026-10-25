---
title: Future Research Directions
type: blueprint
status: active
tags:
  - ai-school
  - research
  - future-directions
updated: 2026-10-25
---

# Future Research Directions

> This note captures an undated early brainstorm. Its creation date is unknown; ideas below are proposals, not findings or adopted decisions.

The whitepaper I'd want to read
I'd structure it around five questions:
1. What can a small, randomly initialized, byte-level Transformer learn from minimal training?
2. How reproducible are its apparent improvements across random seeds?
3. Does performance on familiar or training-adjacent examples transfer to genuinely held-out tasks?
4. Can rationale supervision improve task performance, or does it primarily teach the model to imitate explanatory text?
5. What do the failures tell us about the relationship between statistical pattern learning and demonstrated reasoning?

---

# high priority here
What if scientific thinking becomes part of the curriculum?
Imagine introducing a very simple experimental process during preschool:
1. Observe: Something happened.
2. Wonder: Why did it happen?
3. Predict: What do I think will happen next?
4. Test: Try something that can answer the question.
5. Compare: Did the result match the prediction?
6. Learn: What should I try next?

---

Early school — Learn patterns

Sequences, associations, language structure, and basic generalization. Your preschool curriculum is testing this foundation.




Later school — Learn to solve problems

Apply learned patterns to unfamiliar situations, follow multi-step processes, recognize mistakes, and improve through feedback.




Advanced school — Learn how to learn

Figure out what information is missing, test hypotheses, compare evidence, and transfer knowledge between tasks.




Research — Learn beyond the classroom

Use search tools and reference material, evaluate sources, retrieve relevant facts, and use new information to solve problems.

---


I'd model a school year as a learning cycle

1. Teach

Introduce a capability through several lessons, examples, and formats. Vary the examples so the student isn't just memorizing a single pattern.




2. Practice and revisit

Reintroduce earlier concepts across later lessons. Mix familiar examples with new ones, and revisit concepts the student struggles with.




3. Assess

Test on held-out examples, novel combinations, and retained earlier skills. Don't let the same examples used for teaching determine whether the student passes.




4. Advance or remediate

If the student struggles, provide additional instruction and retest. If it passes, move forward while continuing to monitor previously acquired capabilities.



The school calendar
Your half-year idea gives us a useful starting point. We can treat one school year as a defined training budget rather than a wall-clock year.

For example, a simulated school year might have:
- Instruction: multiple lessons per subject, with variation between lessons.
- Practice: repeated exposure and cumulative exercises.
- Exams: fixed benchmark sets plus fresh, held-out challenges.
- Remediation: extra lessons for weak areas.
- Finals: comprehensive assessment of both current and previously learned material.
- Summer break: an optional experiment to test retention after a period without practice.
That last one could be particularly revealing. Does the student retain its skills without continued reinforcement? Since its knowledge is largely encoded in its weights, you can investigate retention directly.
One architectural decision will matter later
I'd separate the school from the student.
AI School

Curriculum · Lessons · Schedule · Exams · Promotion rules

The Student

Model parameters · Learned capabilities · Current performance

Independent Evaluation

Learning progress · Retention · Generalization · Failure analysis


That separation means you can improve the curriculum without rewriting the model, change assessment policies without changing lessons, and eventually add subjects and grades without rebuilding the school.

One important experimental safeguard: keep a fixed benchmark that the teacher and curriculum never train against, alongside rotating assessments. Otherwise, as the school becomes more sophisticated, you risk measuring how well it teaches to its own exams.

And there's a deeper question worth preserving for later: does the student advance only when it reaches a mastery threshold, or does it follow the school calendar regardless and receive extra support where needed? Either can work as a policy, and comparing them could itself become an experiment.

For now, I wouldn't build the entire school infrastructure. I'd first make preschool support multiple varied lessons, repeated practice, remediation, and a cumulative final exam. That would give you the first functioning piece of the institution you're imagining.


---

Can a small model learn the basics cheaply, then pass what it learned to a larger model that develops more sophisticated capabilities?
Three ways we could experiment with this









1. Widen the existing model

Train a model with a smaller hidden dimension, then expand its layers from, say, 512 to 1024 dimensions. Copy the learned weights into the corresponding parts of the larger model and initialize the new parameters.

Question: Does the larger model benefit from the smaller model's learned representations?












2. Deepen the existing model

Start with, for example, 4 Transformer layers. After the model learns the alphabet patterns, insert more layers, initialize them appropriately, and continue training.

Question: Can a model acquire useful behavior before it has its final depth?












3. Grow through stages

Train a small model, expand it, train again, and potentially expand it a second time. Evaluate after each stage.

Question: Does staged growth outperform training the final-size model from scratch?



The important distinction
Growing a model isn't simply increasing its parameter count. We need to preserve as much of its learned behavior as possible.

For example, suppose the small model learns:
- a b c → d
- d e f → g
- g h i → j
After expansion, we would test whether the larger model retains those abilities before further training. Then we'd measure how much it learns afterward.

That gives us three separate measurements:
1. Transfer: What did the grown model retain immediately after expansion?
2. Learning: How much did additional training improve it?
3. Efficiency: Did growing it reach a given performance level with less total compute than training the large model from scratch?
The third comparison is especially important. Otherwise, growth might look successful simply because the grown model received more total training.
How I'd structure the future experiment
Group	Training procedure
A — Baseline	Train the small model; evaluate it
B — Scratch	Train the large model from random initialization
C — Grow	Train the small model, expand it, then continue training
D — Control	Expand the small model but evaluate before further training

Keep the data, tokenizer, evaluation probes, and final evaluation criteria consistent. Ideally, compare both equal training steps and equal total compute.

One technical wrinkle: some growth methods are much easier than others. Adding width requires deciding how to initialize the new dimensions and preserve the old ones. Adding layers requires choosing how the inserted layers behave initially. Neither approach guarantees that the model's behavior will remain unchanged.

For your current alphabet-learning experiment, I'd eventually start with depth growth: a 4-layer model growing into an 8-layer model, since preserving the dimensions of the existing layers makes the experiment easier to isolate. We would first inspect your model implementation to determine the safest way to insert layers.

And I'd leave your current size comparison untouched. It answers a different question: what happens when you change model size while holding the training budget fixed.

The future growth experiment tests a more interesting possibility: perhaps a model doesn't need to be large from the beginning to become large and capable.

---


