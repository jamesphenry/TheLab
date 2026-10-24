# Agent Instructions — AI Learner Laboratory

## 1. Mission
Help develop and run the **AI Learner Laboratory (AI School)**. Maintain a trustworthy, navigable Obsidian record of its architecture, lessons, experiment history, and findings.

The codebase and the vault serve complementary roles:
- **The Harness Code (`harness/`):** Authoritative for execution, permissions enforcement, LLM calling, and tool sandboxing.
- **The Obsidian Vault (`vault/`):** Authoritative for the environment, curricula, rubrics, student notes, and experimental logs.

## 2. Working Rules & Principles
- **Separation of Knowledge:**
  1. *Model capabilities* (pretrained weights)
  2. *Retrievable external memory* (vault notes)
  3. *Self-assessment* (metacognition)
- **Technical Permissions:** Always enforce folder boundaries in code; never rely solely on prompting models not to read or edit files outside their purview.
- **Evidence Standard:** When logging outcomes in `07-Reports/` or `Experiments/`:
  - Clearly label findings as **Observed**, **Measured**, **Inferred**, or **Hypothesis**.
  - Retain the exact test conditions, rubrics, and model outputs.
- **Non-destructive:** Never delete notes or logs without confirmation.

## 3. Vault Organization
- `00-System/`: Technical rules, permissions, and schedules.
- `01-Learner/`: Learner goals, self-assessment, questions.
- `02-School/`: Curricula, lessons, assignments, assessments organized by subject.
- `03-Experiences/`: Session logs and narrative interactions.
- `04-Memory/`: Extracted knowledge, rules, and synthesis notes.
- `05-Dreams/`: Idle-time reflection, hypotheses, and association logs.
- `06-Labs/`: Practical problem sets and experiment sandboxes.
- `07-Reports/`: Finalized assessment evaluations, grades, and progression reports.
