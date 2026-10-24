# Harness Rules & Invariants

## Core Principles
1. **Separation of Coordinator and Agents:** The harness is the non-agentic technical coordinator. It enforces boundaries, records history, and executes tools.
2. **Access Controls in Code, Not Just Prompts:** Folder access, file read/write limits, and tool permissions must be enforced by harness logic, not by asking LLMs to behave.
3. **Evidence-Based Evaluation:** Claims of mastery must be substantiated with reproducible, recorded test artifacts and rubrics.
4. **Three Distinct Knowledge Layers:**
   - *Model capability* (weights/pretrained baseline)
   - *External memory* (vault notes/logs)
   - *Self-assessment* (metacognition, tracked for accuracy)

## Technical Safety Rules
- Reject all directory traversal attempts (e.g. `../` or absolute symlinks escaping permitted roots).
- Sandbox any execution tools (subprocesses, code runners, network requests).
- Immutable records: Assessment rubrics and historical test grades cannot be overwritten by student or teacher instances once recorded.
