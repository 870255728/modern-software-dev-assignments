# Warp Multi-Agent Playbook

This playbook reproduces the Week 5 development workflow in Warp. It is deliberately separate from the implementation so that the Agent run is repeatable and auditable.

## 1. Prerequisites

Install and sign in to Warp on the local computer. Connect with `ssh root@190.92.200.190`, change to `/root/modern-software-dev-assignments/week5`, and Warpify the SSH session if offered. Remote Agent Mode works through terminal commands even though native remote indexing and the file tree are limited.

Import both YAML files from `.warp/workflows/` into Warp Drive. Run **Week 5 Agent Worktrees** once. The helper is idempotent: existing branches or attached worktrees are reused.

## 2. Start two concurrent Agents

Open two Warp tabs. In each tab, reconnect over SSH, enter the indicated directory, press `Ctrl+I` on Windows/Linux (`Cmd+I` on macOS), and start a fresh Agent conversation.

### Agent A - Notes CRUD (medium)

Directory: `/root/worktrees/week5-task3/week5`

```text
Read AGENTS.md and implement Task 3 from docs/TASKS.md. Add PUT and DELETE
note endpoints, payload validation, optimistic edit/delete UI with rollback,
and tests for success, 404, and invalid input. Change only week5/. Run the
quality gate, review the diff, and commit only this task. Do not merge or push.
```

### Agent B - Action filters and bulk completion (medium)

Directory: `/root/worktrees/week5-task4/week5`

```text
Read AGENTS.md and implement Task 4 from docs/TASKS.md. Add completed filtering,
transactional bulk completion with rollback when any ID is missing, filter and
selection UI, and backend tests. Change only week5/. Run the quality gate,
review the diff, and commit only this task. Do not merge or push.
```

## 3. Supervise and integrate

Keep both conversations visible in Warp's Agent management/conversation panel. Approve read-only inspection and routine test commands. Review every write and do not enable unrestricted auto-approval for `git`, file deletion, or network commands.

After both Agents commit, return to the integration directory:

```bash
cd /root/modern-software-dev-assignments
git switch xyp
git merge --no-ff week5-task3
git merge --no-ff week5-task4
```

If the second merge conflicts in `frontend/app.js` or `frontend/index.html`, ask a third coordinator conversation to preserve both feature sets. Inspect the resolved diff before committing, then run **Week 5 Quality Gate**.

## 4. Audit contract

A complete Agent run should retain:

- Each named Agent's task prompt and final commit hash.
- Start/end times and permission decisions.
- The merge conflict or clean merge result.
- The final Quality Gate PASS result.
- The Saved Prompt link when Warp generates one.

Codex, Claude Code, and ordinary shell runs are not equivalent to Warp Agent sessions. Only evidence produced by the Warp interface should be identified as Warp Agent evidence.
