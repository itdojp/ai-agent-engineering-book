#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SAMPLE="$ROOT/sample-repo"

required=(
  "README.md"
  "AGENTS.md"
  "docs/repo-map.md"
  "docs/architecture.md"
  "docs/coding-standards.md"
  "tasks/FEATURE-001-brief.md"
  "src/support_hub/service.py"
  "tests/test_service.py"
  "tests/test_ticket_search.py"
)

for path in "${required[@]}"; do
  if [[ ! -f "$SAMPLE/$path" ]]; then
    echo "missing sample artifact: $path"
    exit 1
  fi
done

PYTHONPATH="$SAMPLE/src" python3 -m unittest discover -s "$SAMPLE/tests" -v
echo "sample scaffold looks consistent"
