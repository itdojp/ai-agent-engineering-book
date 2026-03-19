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
required_sections_en = ["## Learning Objectives", "## Outline", "## Exercises", "## Referenced Artifacts"]


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


def check_english_chapter(ch_id: str, brief: Path):
    paths = list(root.glob(f"manuscript-en/**/{ch_id}-*.md"))
    if not paths:
        raise SystemExit(f"missing English chapter file for {ch_id}")
    text = paths[0].read_text(encoding="utf-8")
    missing = [item for item in required_sections_en if item not in text]
    if missing:
        raise SystemExit(f"English chapter {ch_id} missing sections: {', '.join(missing)}")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"English brief {brief.name} references missing artifact: {artifact}")


def check_english_appendix(app_id: str, brief: Path):
    paths = list(root.glob(f"manuscript-en/appendices/{app_id}-*.md"))
    if not paths:
        raise SystemExit(f"missing English appendix file for {app_id}")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"English brief {brief.name} references missing artifact: {artifact}")


def check_english_scaffold(target: str):
    en_root = root / "manuscript-en"
    if not en_root.exists():
        return
    for rel in ["AGENTS.md", "README.md", "STATUS.md"]:
        if not (en_root / rel).exists():
            raise SystemExit(f"missing English manuscript file: manuscript-en/{rel}")

    ja_ch = sorted((root / "manuscript" / "briefs").glob("ch*.yaml"))
    ja_app = sorted((root / "manuscript" / "briefs").glob("app-*.yaml"))
    en_ch = sorted((en_root / "briefs").glob("ch*.yaml"))
    en_app = sorted((en_root / "briefs").glob("app-*.yaml"))

    if [p.stem for p in ja_ch] != [p.stem for p in en_ch]:
        raise SystemExit("English chapter briefs do not match Japanese chapter briefs")
    if [p.stem for p in ja_app] != [p.stem for p in en_app]:
        raise SystemExit("English appendix briefs do not match Japanese appendix briefs")

    if target:
        brief = en_root / "briefs" / f"{target}.yaml"
        if not brief.exists():
            raise SystemExit(f"missing English brief: manuscript-en/briefs/{target}.yaml")
        if target.startswith("app-"):
            check_english_appendix(target, brief)
        else:
            check_english_chapter(target, brief)
        return

    for brief in en_ch:
        check_english_chapter(brief.stem, brief)
    for brief in en_app:
        check_english_appendix(brief.stem, brief)

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

check_english_scaffold(target)

print("book scaffold looks consistent")
PY
