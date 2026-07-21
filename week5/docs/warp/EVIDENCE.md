# Warp Evidence Index

This file separates reproducible repository evidence from actions that must be captured in the Warp application. Replace every bracketed field after the real Warp run; do not invent links or screenshots.

## Automation A - Warp Drive and Project Rule

| Evidence | Value |
| --- | --- |
| Project Rule | `week5/AGENTS.md` |
| Repository workflow | `week5/.warp/workflows/week5-quality-gate.yaml` |
| Helper script | `week5/scripts/quality_gate.sh` |
| Saved Prompt template | `week5/docs/warp/QUALITY_GATE_PROMPT.md` |
| Saved Prompt share URL | `[PASTE WARP DRIVE SHARE URL]` |
| Real Prompt export | `[ADD EXPORTED FILE UNDER docs/warp/exports/]` |
| Prompt editor screenshot | `[ADD FILE OR SUBMISSION SCREENSHOT NAME]` |
| Final PASS screenshot | `[ADD FILE OR SUBMISSION SCREENSHOT NAME]` |

## Automation B - Concurrent Agents

| Role | Branch | Worktree | Commit/session evidence |
| --- | --- | --- | --- |
| Integration | `xyp` | `/root/modern-software-dev-assignments` | Final merge log |
| Notes Agent | `week5-task3` | `/root/worktrees/week5-task3` | Feature commit + `[WARP SESSION URL]` |
| Action Agent | `week5-task4` | `/root/worktrees/week5-task4` | Feature commit + `[WARP SESSION URL]` |

Required screenshots:

1. Both Warp Agent tabs active at the same time, with each branch/path visible.
2. Notes Agent final summary and commit.
3. Action Agent final summary and commit.
4. Integration merge result and final Quality Gate PASS.

## Reproducible verification

```bash
cd /root/modern-software-dev-assignments/week5
bash scripts/quality_gate.sh backend/tests
git log --oneline --decorate --graph -10
git status --short
```

Record the final test count, commit hashes, and whether the frontend merge was clean or conflicted in `writeup.md` after integration.
