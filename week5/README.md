# Week 5

Minimal full‑stack starter for experimenting with autonomous coding agents.

- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Tasks to practice agent-driven workflows

## Quickstart

1) Create and activate a virtualenv, then install dependencies

```bash
cd /Users/mihaileric/Documents/code/modern-software-dev-assignments
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

2) (Optional) Install pre-commit hooks

```bash
pre-commit install
```

3) Run the app (from `week5/`)

```bash
cd week5 && make run
```

Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

## Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent-driven workflows
```

## Tests

```bash
cd week5 && make test
```

## Formatting/Linting

```bash
cd week5 && make format
cd week5 && make lint
```

If GNU Make is unavailable, run the repository quality gate instead:

```bash
cd week5 && bash scripts/quality_gate.sh backend/tests
```

## Completed Assignment Tasks

- **Task 3 (medium):** full Notes update/delete APIs, validation, and optimistic UI updates with rollback.
- **Task 4 (medium):** Action Item completion filters, transactional bulk completion, and bulk-selection UI.

See [`docs/IMPLEMENTATION.md`](docs/IMPLEMENTATION.md) for API contracts and architecture. The reusable Warp YAML definitions are in [`.warp/workflows/`](.warp/workflows/), and [`docs/WARP_MULTI_AGENT_PLAYBOOK.md`](docs/WARP_MULTI_AGENT_PLAYBOOK.md) explains how to reproduce the concurrent Agent workflow. For a lab presentation, use [`docs/LAB_PRESENTATION_GUIDE.md`](docs/LAB_PRESENTATION_GUIDE.md).

## Configuration

Set `DATABASE_PATH` in the environment or a local `.env` file to override the default SQLite path (`./data/app.db`). Do not commit local databases, credentials, or machine-specific environment values.
