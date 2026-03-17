#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SAMPLE="$ROOT/sample-repo"

required=(
  "README.md"
  "AGENTS.md"
  "docs/repo-map.md"
  "docs/architecture.md"
  "docs/harness/single-agent-runbook.md"
  "docs/harness/permission-policy.md"
  "docs/harness/done-criteria.md"
  "src/support_hub/service.py"
  "tests/test_service.py"
)

for path in "${required[@]}"; do
  if [[ ! -f "$SAMPLE/$path" ]]; then
    echo "missing init prerequisite: sample-repo/$path"
    exit 1
  fi
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required"
  exit 1
fi

echo "workspace_root=$ROOT"
echo "sample_repo=$SAMPLE"
echo "python=$(python3 --version 2>&1)"
echo "next=./scripts/verify-sample.sh"
