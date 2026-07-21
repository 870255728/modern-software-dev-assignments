#!/usr/bin/env bash
set -euo pipefail

WEEK5_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(git -C "$WEEK5_DIR" rev-parse --show-toplevel)"
WORKTREE_ROOT="${1:-/root/worktrees}"
BASE_REF="${2:-HEAD}"

mkdir -p "$WORKTREE_ROOT"

ensure_worktree() {
  local branch="$1"
  local path="$2"

  if git -C "$REPO_ROOT" worktree list --porcelain | grep -Fxq "worktree $path"; then
    printf '%s already ready at %s\n' "$branch" "$path"
  elif git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$branch"; then
    git -C "$REPO_ROOT" worktree add "$path" "$branch"
  else
    git -C "$REPO_ROOT" worktree add -b "$branch" "$path" "$BASE_REF"
  fi
}

ensure_worktree week5-task3 "$WORKTREE_ROOT/week5-task3"
ensure_worktree week5-task4 "$WORKTREE_ROOT/week5-task4"

printf '\nOpen two Warp tabs and start one Agent conversation in each:\n'
printf 'Task 3: %s/week5-task3/week5\n' "$WORKTREE_ROOT"
printf 'Task 4: %s/week5-task4/week5\n\n' "$WORKTREE_ROOT"
git -C "$REPO_ROOT" worktree list
