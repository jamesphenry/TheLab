---
title: Build and Test
type: procedure
status: in-progress
tags:
  - build
  - testing
  - python
created: 2026-10-23
updated: 2026-10-23
---

# Build and Test — AI School Harness

## Environment
- **Language:** Python 3.13+
- **Test Framework:** `unittest` (standard library) / `pytest`
- **Typing:** `mypy` / standard Python typing
- **Package Management:** Standard virtualenv + `pyproject.toml`

## Canonical Commands

| Purpose | Command | Expected Evidence |
| :--- | :--- | :--- |
| Run all unit tests | `python3 -m unittest discover tests` | All tests pass (0 failures) |
| Test specific module | `python3 -m unittest tests/test_vault.py` | Targeted test results |
| Run test cycle | `python3 -m harness.cli --run-cycle` | End-to-end execution log |
| Type check | `python3 -m mypy harness` (if installed) | Clean type check |

## Verification Invariants
1. Unit tests must run without external network dependencies by using mock LLM drivers.
2. Permission tests must strictly verify path traversal prevention (e.g. attempting to read `../../etc/passwd` or write to unauthorized folders must raise `PermissionDeniedError`).
