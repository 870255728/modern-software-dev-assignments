# Repository Guidelines

## Project Structure & Module Organization

Week 5 is a small FastAPI application. Backend code lives in `backend/app/`: `main.py` configures the app, `routers/` defines HTTP endpoints, `models.py` contains SQLAlchemy models, `schemas.py` contains Pydantic contracts, and `services/` holds domain logic. Backend tests are in `backend/tests/` and mirror the feature areas. The dependency-free browser UI is in `frontend/` (`index.html`, `app.js`, and `styles.css`). SQLite seed data and the local database live in `data/`; assignment requirements are in `assignment.md` and `docs/TASKS.md`.

## Build, Test, and Development Commands

Activate the course environment before working: `conda activate cs146s`. From `week5/`, use:

- `make run` - start Uvicorn with reload at `http://localhost:8000`.
- `make test` - run the backend pytest suite.
- `make format` - format Python with Black and apply Ruff fixes.
- `make lint` - run Ruff without modifying files.
- `make seed` - initialize the SQLite database from seed data.

Install dependencies from the repository root with `poetry install --no-interaction`. If `make` is unavailable, run `PYTHONPATH=. python -m pytest -q backend/tests` directly.

## Coding Style & Naming Conventions

Use four spaces for Python and follow Black's 100-character line length plus the Ruff rules configured in `pyproject.toml`. Use `snake_case` for modules, functions, and variables; `PascalCase` for Pydantic and SQLAlchemy classes; and descriptive REST paths such as `/action-items/{item_id}`. Keep JavaScript dependency-free and consistent with the existing two-space indentation and `camelCase` functions.

## Testing Guidelines

Use pytest. Name files `test_<feature>.py` and tests `test_<behavior>`. Add success, validation, and missing-resource cases for every endpoint change. Use fixtures from `backend/tests/conftest.py`; do not depend on the persistent `data/app.db`. Run tests and lint before committing.

## Commit & Pull Request Guidelines

History favors short, focused subjects. Prefer an imperative scoped form such as `feat(week5): add bulk action completion` or `test(week5): cover note validation`. Keep commits limited to one task. Pull requests should summarize behavior, list verification commands, link the relevant task or issue, and include UI screenshots when frontend behavior changes.

## Agent-Specific Instructions

Modify only files under `week5/`. Inspect existing behavior before editing, preserve unrelated user changes, and never hide failing checks. Agents working concurrently must use separate branches or Git worktrees, review their diffs, and leave final integration and pushing to the supervising contributor.
