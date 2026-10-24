---
title: AI Learner Laboratory — Discussion Notes
type: blueprint
status: active
tags:
  - ai-school
  - notes
  - blueprint
created: 2026-10-23
updated: 2026-10-23
---

# AI Learner Laboratory — Discussion Notes

**Status:** Early-stage concept; let it simmer before committing to an architecture  
**Purpose:** Capture the ideas discussed so far in a format that can be edited in an Obsidian vault.

## 1. The central idea

Build an experimental AI learning environment around a pretrained language model. Rather than treating the model as a one-shot chatbot, give it an ongoing environment in which it can:

- Have ordinary conversations with its human guide.
- Attend structured lessons and complete assignments.
- Take tests and participate in practical labs.
- Receive grades and identify areas that need work.
- Choose whether to study further, practice, ask a teacher for help, or move on.
- Reflect on experiences during idle periods.
- Build a persistent history that can be inspected and edited by the human.

The human role is to guide and shape the learner: set expectations, provide direction, introduce interests, give feedback, and have conversations that are not always schoolwork.

This is an experiment in education, memory, adaptation, and self-directed learning. Human-like behavior or subjective experience should not be assumed merely because the system displays certain behaviors.

## 2. The school metaphor

The learner has a school environment with subject-specific teachers. A teacher could be another LLM instance prompted for a subject, or eventually a different model.

Possible subjects include:

- Mathematics
- Science
- Programming
- Language
- History
- Other subjects added later

### Lesson lifecycle

A typical learning cycle could be:

1. **Lesson:** A teacher introduces a concept and provides explanations and examples.
2. **Practice:** The learner attempts exercises.
3. **Examination:** The learner answers new questions independently.
4. **Grading:** The teacher evaluates the work against a rubric.
5. **Review:** The system records strengths, weaknesses, and evidence.
6. **Decision:** The learner chooses a reasonable next step, within the goals and boundaries established by the human.
7. **Follow-up:** The learner studies further, completes a lab, asks questions, or takes another assessment.

### Tests and grading

Grades should be based on evidence, not simply the learner's claim that it understands something.

Useful assessments include:

- Questions the learner has not seen before.
- Practical tasks that require applying a concept.
- Rubrics that explain how answers are graded.
- Recording the learner's answer, the grade, the rubric, and the conditions of the test.
- Retesting with different questions to see whether performance improves.

A test should measure transfer to unfamiliar problems, not just the ability to repeat a lesson.

Teachers can be wrong, too. Where practical, use independent checks, objective test results, or explicit evidence for grades. Keep the teacher's judgment distinguishable from verified outcomes.

### Learner-directed study

The learner should be able to inspect its performance and decide what to work on next. For example:

- Weak performance may prompt remedial lessons.
- Strong performance may prompt harder work.
- Repeated mistakes may trigger prerequisite exercises.
- Uncertainty may prompt the learner to ask a teacher for help.

The important behavior to measure is whether the learner can identify a weakness, choose an appropriate response, and improve on a subsequent assessment.

## 3. Ordinary conversation and human guidance

School should not consume the learner's entire existence. It should also be able to have ordinary conversations with its human guide.

The human can:

- Set broad expectations.
- Praise effort and improvement.
- Challenge avoidance or careless work.
- Suggest new interests.
- Give advice and feedback.
- Talk without turning every exchange into a lesson or test.

An example of a guiding expectation:

> I don't expect you to know everything. I expect you to try, learn from mistakes, and ask for help when you need it.

The experiment could examine whether such guidance corresponds to measurable changes in behavior, such as checking answers, requesting help sooner, revisiting failed work, or persisting on difficult tasks.

These are observable behavioral outcomes, not proof of human-like emotions or motives.

## 4. Proposed architecture: custom tool harness

Use a custom harness to coordinate the system. The harness should be separate from the learner model and should enforce permissions, record events, and execute approved actions.

Potential components:

- **Learner:** The language model, its current context, and its decision policy.
- **Teacher system:** Subject-specific instruction, assignments, grading, and remediation.
- **Assessment system:** Rubrics, tests, grading records, and repeatable evaluation.
- **Environment/tools:** Calculator, controlled code execution, browser, and other approved tools.
- **Scheduler:** Lessons, work periods, idle periods, reflection, and rest.
- **Memory/reflection:** Experience review, summaries, associations, and hypothesis generation.
- **Human interface:** Conversations, guidance, and inspection of progress.
- **Experiment recorder:** A traceable record of decisions, actions, results, and configuration changes.

The harness coordinates these pieces but should not be conflated with any one of them. The learner proposes actions; the harness checks permissions and executes them.

## 5. Obsidian vault as the shared, editable environment

The current preference is to use an Obsidian vault rather than a database as the primary human-readable record.

Advantages:

- Ordinary Markdown files that the human can edit.
- Instructions and teacher definitions can be changed without rewriting application code.
- Human-readable learning history and progress.
- Easy inspection, backup, and version control.
- The human can guide the system by changing its environment directly.
- The vault can act as both an experimental notebook and an editable part of the learner's world.

A possible starting layout:

```text
AI-School/
├── 00-System/
│   ├── Harness-Rules.md
│   ├── Permissions.md
│   └── Schedule.md
├── 01-Learner/
│   ├── Goals.md
│   ├── Self-Assessment.md
│   └── Current-Questions.md
├── 02-School/
│   ├── Mathematics/
│   │   ├── Teacher.md
│   │   ├── Curriculum.md
│   │   ├── Lessons/
│   │   ├── Assignments/
│   │   └── Assessments/
│   ├── Science/
│   ├── Programming/
│   └── Language/
├── 03-Experiences/
├── 04-Memory/
├── 05-Dreams/
├── 06-Labs/
└── 07-Reports/
```

This is a starting proposal, not a fixed schema. The folders can be renamed, simplified, or expanded as the design develops.

### Example teacher note

```markdown
# Role
You are the programming teacher.

# Teaching approach
- Teach one concept at a time.
- Require practical exercises.
- Do not reveal complete solutions before the learner attempts the problem.
- Explain mistakes and provide targeted follow-up work.

# Assessment
- Grade correctness, reasoning, and testing.
- Use unfamiliar problems to assess transfer.
- Record the rubric and evidence supporting each grade.

# Remediation
If the learner repeatedly fails a concept,
assign prerequisite exercises before advancing.
```

The harness can load the teacher's current instructions at the appropriate time. Editing the note changes the teaching setup without requiring a code change.

Teacher instructions influence model behavior but do not guarantee it. Critical permissions and grading-record protections should be enforced by the harness itself.

## 6. Folder-scoped access and security

The harness should enforce which folders each component may read or modify. Access rules should be technical controls, not merely instructions in a prompt.

Possible policy:

- A teacher can access its designated teaching workspace.
- The assessment component can read submitted answers and write assessment results.
- The learner can read permitted school material and its own memories, and write to designated experience and reflection folders.
- System rules and protected grading records are not writable by components that should not control them.
- The human retains unrestricted access to the vault.
- Code execution and other powerful tools have their own sandbox and permissions.

The harness should reject path traversal attempts (for example, `../`) and avoid giving the model unrestricted filesystem access.

A teacher should not be able to quietly rewrite its own grading rules or alter the learner's grades if those files are outside its permissions.

## 7. Keep three kinds of knowledge separate

A useful foundational distinction:

1. **What the model can do:** Capabilities from pretrained weights and any later parameter updates.
2. **What the learner remembers:** Persistent experiences and notes it can retrieve.
3. **What the learner thinks it can do:** Its self-assessment, which may be inaccurate.

These can disagree. For example, the learner may remember a lesson about C pointers and confidently claim to understand them, yet fail a practical test.

That disagreement is useful evidence. It can help the learner revise its self-assessment and choose what to study next.

Writing a memory note is not the same as changing the neural network's weights. Persistent external memory and actual model training should be treated as distinct mechanisms and measured separately.

## 8. Dreams, reflection, and idle time

A possible future feature is a reflection or “dream” cycle during idle periods.

Two possible modes:

- **Consolidation:** Revisit experiences, questions, corrections, predictions, and unresolved problems.
- **Free association:** Generate unusual connections and hypotheses, potentially using higher sampling temperature.

Higher temperature changes the diversity of generated text; it does not itself cause learning or change model weights.

A possible cycle:

**Experience → Reflection/Dream → Hypothesis → Evaluation → Experiment → Learning**

Dream-generated ideas should remain hypotheses until checked. A supervisor or evaluation process can identify testable claims and arrange experiments. Surprising ideas should not be rejected merely because they are unusual, but they should not be treated as facts merely because the model generated them.

## 9. Time and scheduling

Time could be represented as part of the learner's environment, not merely inserted as a timestamp in a prompt.

Potential capabilities to explore:

1. Know the current time.
2. Learn temporal relations: before, after, duration, routine, delay.
3. Anticipate scheduled or expected events.
4. Eventually choose how to allocate time based on goals, uncertainty, and unresolved questions.

An initial schedule could include review, lessons, exploration, reflection, dream cycles, and rest. Later, the schedule could be varied to test adaptation.

A fixed schedule is useful as a baseline before allowing the learner to choose its own schedule.

## 10. Possible experimental comparisons

Run two learner instances from the same initial model and comparable initial conditions.

Give them the same school curriculum but different teaching approaches, experiences, or human guidance. Compare their behavior over time.

Potential measurable outcomes:

- Performance on unfamiliar test problems.
- Improvement after remediation.
- Whether self-assessment matches actual results.
- How often the learner seeks help.
- Whether it checks its own work.
- Whether it revisits failed tasks.
- Whether it persists on difficult tasks.
- Whether behavioral differences remain when immediate prompts and recent conversation are removed.
- Whether different learning histories produce different persistent behavioral tendencies.

Control for the pretrained model's existing behavior. A behavior that appears immediately may be a pretrained default rather than something the learner acquired through this experiment.

Self-directed information seeking is worth measuring, but it is not by itself proof of subjective curiosity or consciousness.

## 11. Suggested first milestone

Avoid implementing every idea at once. Start with one complete, testable learning cycle:

1. One local learner model.
2. One teacher model or teacher configuration.
3. One subject, such as C programming or mathematics.
4. One assignment and a grading rubric.
5. An Obsidian vault to store instructions, attempts, and grades.
6. A harness that enforces folder permissions.
7. A decision step where the learner chooses further study, practice, or progression.
8. A fresh follow-up test to measure improvement.

The initial milestone is:

> The learner takes a lesson, fails a test, identifies a weakness, chooses to work on it, and demonstrably improves on a different test.

No dream engine, elaborate dashboard, complex personality system, or full-network training pipeline is required for the first milestone.

Once the basic cycle works, add reflection, time scheduling, multiple teachers, additional subjects, or model-weight updates as separate experiments.

## 12. Core design principles to preserve

- Keep components modular and independently replaceable.
- Keep the vault human-readable and editable.
- Enforce access controls in the harness, not only in prompts.
- Record evidence behind grades and claims of mastery.
- Separate external memory from neural-weight changes.
- Separate verified results from hypotheses and self-assessment.
- Test learning on unfamiliar problems.
- Preserve enough history and configuration to reproduce experiments.
- Allow the human to guide the learner without turning every conversation into schoolwork.
- Treat human-like behavior as something to investigate empirically, not assume.

## Open questions for later

These do not need to be answered before the idea has had time to develop:

- Which local model should be the initial learner?
- Should teachers share the learner's base model or use separate models?
- What exact permissions should each component have?
- How should grades be independently verified?
- How should the learner estimate mastery and uncertainty?
- How much learning should occur through persistent notes versus parameter updates?
- When should reflection and dream cycles run?
- How should the learner's chosen activities be balanced against human guidance?
- What would count as convincing evidence of durable improvement?

---

**Current direction:** A custom, modular harness; an Obsidian vault as the editable record and environment; subject-specific teachers; formal lessons, labs, and exams; evidence-based grading; learner-directed remediation; and ordinary conversation with a human guide.



---

## 13. Critical questions for experimental rigor

A few areas to actively investigate and test against:
- **Learning vs. Retrieval:** Are you measuring learning, or just better use of external notes? If the learner improves because it retrieves a previous explanation, that's useful—but it's different from changing its underlying capabilities.
- **Genuine Transfer vs. Prompting Artifacts:** Can you distinguish genuine improvement from prompting effects? A teacher might teach the learner to produce answers that look better without improving its ability to solve unfamiliar problems.
- **Shared Model Blind Spots:** Are the grades meaningful? If the same family of models teaches, examines, and grades the learner, they could share the same blind spots. Independent tests and objective checks will matter.
- **Predetermined Outcomes:** Are you accidentally designing the outcome? Your instructions, reward structure, and available tools could predetermine the behavior you're hoping to observe.
- **Falsifiability:** What would prove your hypothesis wrong? If every outcome can be explained as evidence that the learner is developing, the experiment isn't falsifiable.
- **Defining Behavioral Change:** What does “persistent behavioral change” actually mean? You need to distinguish changes caused by memory, changing prompts, accumulated experience, and actual weight updates.
- **Causal Attribution:** If two identical base models receive different educational experiences and eventually behave differently, how will you establish that the experiences caused the difference?

