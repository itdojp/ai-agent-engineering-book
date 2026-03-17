#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SAMPLE="$ROOT/sample-repo"
TASK_BRIEF="${1:-}"

root_required=(
  "README.md"
  "AGENTS.md"
)

sample_required=(
  "docs/repo-map.md"
  "docs/architecture.md"
  "docs/harness/single-agent-runbook.md"
  "docs/harness/permission-policy.md"
  "docs/harness/done-criteria.md"
  "src/support_hub/service.py"
  "tests/test_service.py"
)

for path in "${root_required[@]}"; do
  if [[ ! -f "$ROOT/$path" ]]; then
    echo "missing init prerequisite: $path"
    exit 1
  fi
done

for path in "${sample_required[@]}"; do
  if [[ ! -f "$SAMPLE/$path" ]]; then
    echo "missing init prerequisite: sample-repo/$path"
    exit 1
  fi
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required"
  exit 1
fi

if [[ -n "$TASK_BRIEF" && ! -f "$ROOT/$TASK_BRIEF" ]]; then
  echo "missing task brief: $TASK_BRIEF"
  exit 1
fi

echo "workspace_root=$ROOT"
echo "sample_repo=$SAMPLE"
if [[ -n "$TASK_BRIEF" ]]; then
  echo "task_brief=$ROOT/$TASK_BRIEF"
else
  echo "task_brief=<not-set>"
fi
echo "read_first_1=$ROOT/AGENTS.md"
echo "read_first_2=$SAMPLE/AGENTS.md"
echo "read_first_3=$SAMPLE/docs/repo-map.md"
echo "read_first_4=$SAMPLE/docs/architecture.md"
echo "runbook=$SAMPLE/docs/harness/single-agent-runbook.md"
echo "permission_policy=$SAMPLE/docs/harness/permission-policy.md"
echo "done_criteria=$SAMPLE/docs/harness/done-criteria.md"
echo "verify=./scripts/verify-sample.sh"
echo "python=$(python3 --version 2>&1)"
