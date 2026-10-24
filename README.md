# AI Learner Laboratory (AI School)

An experimental developmental environment for an AI learner model. Rather than treating a pretrained language model as a one-shot chatbot, this project provides an ongoing environment with structured schooling, evidence-based evaluations, metacognitive self-direction, idle reflection, and ordinary human guidance.

## Key Concepts

- **Subject Teachers:** Dedicated teacher instances (Programming, Mathematics, Science, etc.) with specific curricula, lesson plans, and assignments.
- **Evidence-Based Grading:** Objective transfer tests and rubrics with recorded evidence, separating verified performance from subjective claims of understanding.
- **Learner Self-Direction:** The learner model inspects its performance, evaluates strengths/weaknesses, and decides whether to practice, remediate, or advance.
- **Obsidian Vault World:** The primary environment and memory store is an Obsidian vault (`vault/`), keeping curricula, lesson histories, and learner memories human-readable and directly inspectable.
- **Enforced Security Harness:** A Python-based technical harness coordinates components, enforcing strict folder-level read/write permissions and sandboxing execution tools.

## Repository Layout

```
.
├── vault/                # The Obsidian knowledge vault & world environment
│   ├── 00-System/        # Harness rules, permission policies, schedules
│   ├── 01-Learner/       # Learner goals, self-assessment, pending questions
│   ├── 02-School/        # Curricula, lessons, assignments, assessments
│   ├── 03-Experiences/   # Chronological session logs and exchanges
│   ├── 04-Memory/        # Synthesized memory notes & concept summaries
│   ├── 05-Dreams/        # Idle reflection logs and generated hypotheses
│   ├── 06-Labs/          # Practical problem sandboxes
│   ├── 07-Reports/       # Finalized assessment rubrics and test records
│   ├── Development/      # System architecture, build procedures, ADRs, logs, and roadmap
│   ├── Home.md           # Obsidian entry point
│   └── NOTES.md          # Comprehensive project blueprint & notes
├── harness/              # Python coordination harness
│   ├── core/             # Event loop & lifecycle coordinator
│   ├── vault/            # Sandboxed filesystem & permission manager
│   ├── models/           # LLM client abstractions (local/API/mock)
│   └── school/           # Lesson dispatchers & rubric evaluators
├── tests/                # Test suite for the harness
└── pyproject.toml        # Python project metadata
```

## Getting Started

1. Open `vault/` in [Obsidian](https://obsidian.md/) to explore the environment.
2. Run harness unit tests:
   ```bash
   python3 -m unittest discover tests
   ```
