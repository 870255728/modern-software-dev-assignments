# Warp Drive Prompt: Week 5 Quality Gate Reviewer

Create a Prompt in Warp Drive with the following fields, run it after importing the repository workflow, and paste the share URL into `writeup.md`.

## Name

`Week 5 Quality Gate Reviewer`

## Description

Review the current Week 5 diff, execute the reusable quality gate, and return a concise pass/fail report without hiding failures.

## Prompt

```text
Act as the quality-gate reviewer for the Week 5 assignment at {{week5_dir}}.

1. Read AGENTS.md and inspect git status plus the current diff.
2. Run: bash scripts/quality_gate.sh {{test_scope}}
3. Report each check as PASS or FAIL.
4. If a check fails, identify the first actionable cause and the smallest safe fix.
5. In {{mode}} mode, do not modify files. In fix mode, modify only files under
   week5/, rerun the complete gate, and show the final diff.
6. Never commit, merge, push, or remove worktrees.
```

## Arguments

| Argument | Default | Purpose |
| --- | --- | --- |
| `week5_dir` | `/root/modern-software-dev-assignments/week5` | Assignment path |
| `test_scope` | `backend/tests` | Full suite or one pytest selector |
| `mode` | `report` | Use `report` for read-only supervision |

## Evidence to save

1. Screenshot the Prompt editor with its arguments.
2. Run it in `report` mode after the two branches are integrated.
3. Screenshot the PASS summary and its reference to `AGENTS.md`.
4. Enable link viewing from **Share**, then add that URL to `writeup.md`.
