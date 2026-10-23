---
title: Build and Test
type: procedure
status: in-progress
tags:
  - build
  - testing
  - c
created: {{date}}
updated: {{date}}
---

# Build and Test

## Environment

- OS:
- Architecture:
- Compiler and version:
- Build tools:
- Optional analysis tools:
- Required libraries:

## Canonical Commands

Fill these in only after verifying the project's actual targets.

| Purpose | Command | Expected evidence |
| --- | --- | --- |
| Build | `{{command}}` | Successful exit and expected artifacts |
| Unit tests | `{{command}}` | Test summary |
| Quick checks | `{{command}}` | Actual check output |
| Sanitizers | `{{command}}` | No sanitizer findings in this run |
| Static analysis | `{{command}}` | Tool output and exit status |
| Memory analysis | `{{command}}` | Tool output and exit status |

## Clean Build Procedure

1. Record the current commit and working-tree status.
2. Use the project's documented clean/build procedure.
3. Run the canonical tests.
4. Record compiler and test output, including failures.
5. Confirm the working tree and generated artifacts afterward.

## Test Inventory

| Test group | What it verifies | Known gaps |
| --- | --- | --- |
| `{{test_group}}` | `{{purpose}}` | `{{gaps}}` |

## Environment-Specific Notes

Record differences across architectures, compilers, operating systems, and build modes. Do not assume a successful build on one architecture proves portability.

## Last Verified Run

- **Date:**
- **Commit:**
- **Environment:**
- **Commands actually run:**
- **Results:**
- **Not run / limitations:**
- **Log:** [[Logs/Logs Index]]
