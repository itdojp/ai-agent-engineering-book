#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 owner/repo"
  exit 1
fi

REPO="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

labels=(
  "type/scaffold:0E8A16"
  "type/chapter:5319E7"
  "type/appendix:5319E7"
  "type/polish:5319E7"
  "area/manuscript:1D76DB"
  "area/sample-repo:1D76DB"
  "part/prompt:FBCA04"
  "part/context:D4C5F9"
  "part/harness:0E8A16"
)

for item in "${labels[@]}"; do
  name="${item%%:*}"
  color="${item##*:}"
  gh label create "$name" --repo "$REPO" --color "$color" --force >/dev/null 2>&1 || true
done

for milestone in M0-scaffold M1-prompt M2-context M3-harness M4-polish; do
  gh api "repos/$REPO/milestones" --method POST -f title="$milestone" >/dev/null 2>&1 || true
done

python3 "$ROOT/scripts/create-issues.py" "$REPO"
