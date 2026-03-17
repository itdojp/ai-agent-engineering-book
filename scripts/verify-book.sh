#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"

required=(
  "AGENTS.md"
  "README.md"
  "docs/glossary.md"
  "manuscript/AGENTS.md"
  "sample-repo/AGENTS.md"
  ".github/ISSUE_TEMPLATE/task.yml"
  "issue-drafts/manifest.json"
  "scripts/bootstrap-github.sh"
  "scripts/create-issues.py"
  "scripts/verify-sample.sh"
)

for path in "${required[@]}"; do
  if [[ ! -f "$ROOT/$path" ]]; then
    echo "missing: $path"
    exit 1
  fi
done

python3 "$ROOT/scripts/run-prompt-evals.py"

if [[ -n "$TARGET" ]]; then
  brief="$ROOT/manuscript/briefs/${TARGET}.yaml"
  if [[ ! -f "$brief" ]]; then
    echo "missing brief: manuscript/briefs/${TARGET}.yaml"
    exit 1
  fi
fi

python3 - <<'PY' "$ROOT" "$TARGET"
from pathlib import Path
import re
import sys
root = Path(sys.argv[1])
target = sys.argv[2]

required_sections = ["## 学習目標", "## 小見出し", "## 演習", "## 参照する artifact"]


def parse_artifacts(brief: Path) -> list[str]:
    artifacts: list[str] = []
    in_artifacts = False
    for line in brief.read_text(encoding="utf-8").splitlines():
        if line.startswith("artifacts:"):
            in_artifacts = True
            continue
        if in_artifacts and re.match(r"^[A-Za-z0-9_]+:", line):
            break
        if in_artifacts:
            match = re.match(r"^\s*-\s+(.+)$", line)
            if match:
                artifacts.append(match.group(1).strip())
    return artifacts


def check_chapter(ch_id: str, brief: Path):
    paths = list(root.glob(f"manuscript/**/{ch_id}-*.md"))
    if not paths:
        raise SystemExit(f"missing chapter file for {ch_id}")
    text = paths[0].read_text(encoding="utf-8")
    missing = [item for item in required_sections if item not in text]
    if missing:
        raise SystemExit(f"chapter {ch_id} missing sections: {', '.join(missing)}")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"brief {brief.name} references missing artifact: {artifact}")


def check_appendix(app_id: str, brief: Path):
    paths = list(root.glob(f"manuscript/appendices/{app_id}-*.md"))
    if not paths:
        raise SystemExit(f"missing appendix file for {app_id}")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"brief {brief.name} references missing artifact: {artifact}")

if target:
    brief = root / "manuscript" / "briefs" / f"{target}.yaml"
    if target.startswith("app-"):
        check_appendix(target, brief)
    else:
        check_chapter(target, brief)
else:
    for brief in sorted((root / "manuscript" / "briefs").glob("ch*.yaml")):
        check_chapter(brief.stem, brief)
    for brief in sorted((root / "manuscript" / "briefs").glob("app-*.yaml")):
        check_appendix(brief.stem, brief)

print("book scaffold looks consistent")
PY
