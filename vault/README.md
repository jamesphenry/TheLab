# C Project Obsidian Vault Template

A reusable Obsidian knowledge vault designed to accompany a C project skeleton.

## Purpose

Keep the source repository and the project knowledge base connected without making either a duplicate of the other:

- **C repository:** source code, headers, tests, build files, scripts, and version history.
- **Obsidian vault:** project map, design rationale, experiments, test evidence, decisions, debugging notes, and lessons learned.
- **Agent instructions:** `AGENTS.md` defines how coding agents maintain the project and its documentation.

Copy this folder for each project, then replace the placeholders.

## Start here

1. Open this folder as an Obsidian vault.
2. Edit `Home.md` and `Project/Project Overview.md`.
3. Update the repository path and build/test commands in `Project/Project Overview.md`.
4. Read `AGENTS.md` before asking an agent to work.
5. Add your first dated session note under `Logs/`.
6. Keep the vault in its own Git repository, or place it beside the code repository if that fits your workflow. Do not accidentally commit secrets, credentials, generated binaries, or private data.

## Suggested naming

- Experiment: `YYYY-MM-DD Short Experiment Name.md`
- Session log: `YYYY-MM-DD.md`
- Decision: `ADR-0001 Short Decision Title.md`
- Debugging note: `YYYY-MM-DD Short Problem Name.md`

## Working principle

Record what happened, what evidence supports it, what remains uncertain, and what should happen next. Failed experiments are useful results when their conditions and observations are preserved.
