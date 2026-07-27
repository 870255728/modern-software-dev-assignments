# Warp Evidence Index

This file indexes the reproducible evidence available in the repository. No public Warp links or screenshots were generated in the remote environment, so those facts are recorded explicitly rather than represented by placeholders.

## Automation A - Warp Drive and Project Rule

| Evidence | Value |
| --- | --- |
| Project Rule | `week5/AGENTS.md` |
| Repository workflow | `week5/.warp/workflows/week5-quality-gate.yaml` |
| Helper script | `week5/scripts/quality_gate.sh` |
| Saved Prompt template | `week5/docs/warp/QUALITY_GATE_PROMPT.md` |
| Saved Prompt share URL | Not generated; use the versioned Prompt template above |
| Workflow definitions | `week5/.warp/workflows/week5-quality-gate.yaml` and `week5/.warp/workflows/week5-agent-worktrees.yaml` |
| Prompt editor screenshot | Not captured in the remote-only run |
| Final PASS evidence | `20 passed`; reproduce with the command below |

## Automation B - Concurrent Agents

| Role | Branch | Worktree | Commit/session evidence |
| --- | --- | --- | --- |
| Integration | `xyp` | `/root/modern-software-dev-assignments` | Final merge log |
| Notes Agent | `week5-task3` | `/root/worktrees/week5-task3` | Feature commit `59c3a4c`; no public session URL |
| Action Agent | `week5-task4` | `/root/worktrees/week5-task4` | Feature commit `afd9a76`; no public session URL |

## Evidence availability

| Artifact | Availability |
| --- | --- |
| Concurrent Warp Agent tabs | Not captured; paid Agent quota was unavailable |
| Notes feature result | Commit `59c3a4c` and isolated test result |
| Action Items feature result | Commit `afd9a76` and isolated test result |
| Integration result | Merge history, resolved conflict files, and final Quality Gate PASS |

## Reproducible verification

```bash
cd /root/modern-software-dev-assignments/week5
bash scripts/quality_gate.sh backend/tests
git log --oneline --decorate --graph -10
git status --short
```

The final test count and commit hashes are already recorded in `writeup.md`. The first feature merge was clean; the second produced resolved conflicts in `backend/app/schemas.py` and `frontend/styles.css`.
