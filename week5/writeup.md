# Week 5 Write-up

## Submission details

Name: **XYP**

SUNet ID: **[enter your SUNet ID]**

Selected tasks: **Task 3 - Full Notes CRUD (medium)** and **Task 4 - Action-item filters and bulk completion (medium)**

Time spent: **approximately 3.5 hours; replace with your actual total**

References: [assignment](assignment.md), [Warp YAML Workflows](https://docs.warp.dev/terminal/entry/yaml-workflows), [Warp Rules](https://docs.warp.dev/agent-platform/capabilities/rules), [Warp Drive Prompts](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/prompts), [Warp multi-agent guide](https://docs.warp.dev/guides/agent-workflows/how-to-run-multiple-ai-coding-agents/), [Git worktrees in Warp](https://docs.warp.dev/code/git-worktrees), and [Warp SSH feature support](https://docs.warp.dev/code/ssh-feature-support).

> **Evidence checkpoint:** before submitting, replace the bracketed SUNet ID and Warp URLs, export the real Warp Drive Prompt, and attach the screenshots listed in [`docs/warp/EVIDENCE.md`](docs/warp/EVIDENCE.md). The repository does not pretend that a non-Warp run is Warp evidence.

## Automation A: Warp Drive quality gate and project rule

### a. Design: goals, inputs, outputs, and steps

Automation A combines three reusable pieces:

1. `AGENTS.md` is a project Rule. It tells every Agent to work only in `week5/`, preserve existing behavior, add tests, use isolated branches/worktrees, review its diff, and leave integration/pushing to the supervisor.
2. `.warp/workflows/week5-quality-gate.yaml` is a parameterized repository Workflow. Its inputs are the Week 5 directory and pytest scope. It calls `scripts/quality_gate.sh`, which resolves the project directory and Python environment, then runs pytest, Ruff, Black, and `git diff --check` with fail-fast behavior.
3. The saved Prompt template in `docs/warp/QUALITY_GATE_PROMPT.md` adds an Agent review layer. Its `mode` input is `report` or `fix`; report mode is deliberately read-only. Its output is a concise PASS/FAIL summary with the first actionable cause and changed-file list.

The Workflow and helper script are idempotent and headless. The Warp Drive Prompt share URL is **[paste real Warp share URL]**.

### b. Before versus after

Before the automation, I had to remember four commands, run them in the correct environment, inspect failures separately, and risk reporting success after running only a subset. Afterward, one searchable Warp entry executes the same quality gate on a whole suite or a single test selector. The shell script is also usable from SSH and CI, so the validation policy is not coupled to the UI.

The initial baseline was 3 passing tests with four dependency deprecation warnings. After both features and a small compatibility cleanup, the same gate reports **20 passing tests, Ruff PASS, Black PASS, and Git whitespace PASS with no warnings**.

### c. Autonomy level and supervision

I used the least privilege appropriate to each stage. The review Prompt defaults to report-only: it may read files, inspect Git, and run tests but may not edit, commit, merge, delete, or push. Feature Agents may edit only their assigned `week5/` worktree and run local verification. Git merge and push remain manual supervisor actions. I reviewed the changed-file list, endpoint behavior, test assertions, and final diff before accepting each branch. Destructive commands and unrestricted “run until completion” were not required.

### d. Multi-agent notes

The Rule gave both feature Agents the same definition of done, so their prompts could focus on task-specific behavior. This reduced duplicated instructions and made their completion reports comparable. The quality gate acted as the fan-in contract: a branch was not ready for integration until all four checks passed.

### e. How I used it and the pain point addressed

I ran the gate on the untouched starter, on the Action Items merge, and after resolving the final Notes merge. It caught a real integration issue during the compatibility cleanup: Ruff rejected an unsorted import block even though all 20 tests passed. Running Ruff with its safe import fix and rerunning the entire gate produced a clean result. This demonstrates why functional tests alone are not a sufficient completion signal.

## Automation B: concurrent Agent workflow with Git worktrees

### a. Design: goals, inputs, outputs, and steps

The goal was to implement two medium tasks concurrently without allowing Agents to overwrite one another. `scripts/setup_agent_worktrees.sh`, exposed through `.warp/workflows/week5-agent-worktrees.yaml`, creates or reuses:

| Role | Branch | Worktree | Output |
| --- | --- | --- | --- |
| Notes Agent | `week5-task3` | `/root/worktrees/week5-task3` | Commit `59c3a4c` |
| Action Agent | `week5-task4` | `/root/worktrees/week5-task4` | Commit `afd9a76` |
| Supervisor | `xyp` | `/root/modern-software-dev-assignments` | Reviewed merge and final gate |

Agent A implemented `PUT /notes/{id}`, `DELETE /notes/{id}`, bounded Pydantic payloads, and optimistic edit/delete UI with rollback. Its isolated suite ended at 15 passing tests. Agent B implemented boolean completion filters, atomic bulk completion with missing-ID rollback, and filter/selection UI. Its isolated suite ended at 8 passing tests. The exact Warp prompts and reproduction steps are in [`docs/WARP_MULTI_AGENT_PLAYBOOK.md`](docs/WARP_MULTI_AGENT_PLAYBOOK.md).

Warp Agent session URLs: **Notes [paste URL]**; **Action Items [paste URL]**.

### b. Before versus after

The manual alternative is sequential: implement one task, reload its context, then implement the other. Opening two ordinary terminals in one checkout would be faster but unsafe because both tasks modify `schemas.py`, `app.js`, `index.html`, and `styles.css`. Worktrees let both Agents write and commit concurrently while preserving independent file states and reviewable history.

The workflow does not eliminate integration work; it makes that work explicit. Each Agent produced a focused commit and test report, after which the supervisor merged one branch at a time.

### c. Autonomy level and supervision

Each Agent received write and command permission only in its worktree. It could inspect the app, edit its six task files, run pytest/lint/format checks, and create one feature commit. It was explicitly forbidden from changing `writeup.md`, merging, deleting files, or pushing. I supervised through branch status, commit hashes, test counts, and diff review. The supervisor alone resolved conflicts and ran the integrated suite.

### d. Roles, coordination, wins, risks, and failures

The tasks were API-independent but shared frontend and schema files. Task ownership prevented scope drift; worktrees prevented concurrent filesystem clobbering; commit hashes provided a clear handoff. The first merge (Action Items) was clean and passed 8 tests. The second merge (Notes) produced real conflicts in `backend/app/schemas.py` and `frontend/styles.css`. I combined the Pydantic imports/classes and preserved both sets of CSS selectors instead of choosing one branch wholesale. `app.js` and `index.html` merged automatically. The integrated gate then passed all 20 tests.

This conflict was the main concurrency cost and a useful result: isolation prevents accidental overwrites, but overlapping design surfaces still require human integration judgment. The SSH environment also limited Warp's native indexing, file tree, editor, and code-review UI, so Agents used terminal commands and Git diffs; Agent conversations and command execution remain supported over Warpified SSH.

### e. How I used it and the pain point addressed

The workflow accelerated two self-contained feature implementations while keeping their histories and failure domains separate. It also produced a reproducible teaching artifact: another contributor can import the workflows, run the idempotent setup, paste the two task contracts into separate Warp tabs, and compare their outputs. The final runtime smoke test returned HTTP 200 for `/`, `/openapi.json`, `/notes/`, and filtered `/action-items/`; a valid update to a missing Note returned the expected 404.

## Final result

- Task 3 and Task 4 are implemented in the backend and vanilla JavaScript UI.
- Transaction rollback, filtering, CRUD, validation, and missing-resource behavior are tested.
- Final quality gate: **20 passed**, Ruff PASS, Black PASS, `git diff --check` PASS.
- Warp automation definitions, helper scripts, Prompt template, multi-Agent playbook, evidence index, implementation guide, and lab presentation guide are versioned under `week5/`.
