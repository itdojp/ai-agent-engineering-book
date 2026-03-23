#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"

required=(
  "AGENTS.md"
  "README.md"
  "docs/glossary.md"
  "manuscript/AGENTS.md"
  "manuscript/front-matter/00-はじめに.md"
  "manuscript/front-matter/01-本書の読み方.md"
  "manuscript/part-01-prompt/part-opener.md"
  "manuscript/part-02-context/part-opener.md"
  "manuscript/part-03-harness/part-opener.md"
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
required_frontmatter = {
    "manuscript/front-matter/00-はじめに.md": ["## 本書の約束", "## 想定読者", "## 想定しない読者"],
    "manuscript/front-matter/01-本書の読み方.md": ["## 3部構成", "## 3つの読み進め方", "## 読み終わりの到達点"],
}
required_part_opener_sections = [
    "## この Part の役割",
    "## この Part で増える artifact",
    "## 章の見取り図",
    "## 読み終わりの到達点",
]
required_part_openers = {
    "manuscript/part-01-prompt/part-opener.md": required_part_opener_sections,
    "manuscript/part-02-context/part-opener.md": required_part_opener_sections,
    "manuscript/part-03-harness/part-opener.md": required_part_opener_sections,
}

required_english_chapter_sections = {
    "manuscript-en/part-00/ch01-failure-model.md": [
        "## Role in This Book",
        "## Learning Objectives",
        "## Outline",
        "## Bad / Good Example",
    ],
}


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
    paths = sorted(root.glob(f"manuscript/**/{ch_id}-*.md"))
    if len(paths) != 1:
        raise SystemExit(f"expected exactly one chapter file for {ch_id}, found {len(paths)}")
    text = paths[0].read_text(encoding="utf-8")
    missing = [item for item in required_sections if item not in text]
    if missing:
        raise SystemExit(f"chapter {ch_id} missing sections: {', '.join(missing)}")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"brief {brief.name} references missing artifact: {artifact}")


def check_appendix(app_id: str, brief: Path):
    paths = sorted(root.glob(f"manuscript/appendices/{app_id}-*.md"))
    if len(paths) != 1:
        raise SystemExit(f"expected exactly one appendix file for {app_id}, found {len(paths)}")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"brief {brief.name} references missing artifact: {artifact}")


def check_english_chapter(rel: str, sections: list[str]):
    paths = sorted(root.glob(rel))
    if len(paths) != 1:
        raise SystemExit(f"expected exactly one English chapter file for {rel}, found {len(paths)}")
    text = paths[0].read_text(encoding="utf-8")
    missing = [item for item in sections if item not in text]
    if missing:
        raise SystemExit(f"English chapter {rel} missing sections: {', '.join(missing)}")


def check_english_appendix(rel: str, sections: list[str]):
    paths = sorted(root.glob(rel))
    if len(paths) != 1:
        raise SystemExit(f"expected exactly one English appendix file for {rel}, found {len(paths)}")
    text = paths[0].read_text(encoding="utf-8")
    missing = [item for item in sections if item not in text]
    if missing:
        raise SystemExit(f"English appendix {rel} missing sections: {', '.join(missing)}")


english_root = root / "manuscript-en"
if not english_root.exists():
    raise SystemExit("missing: manuscript-en")


for rel, sections in required_frontmatter.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [item for item in sections if item not in text]
    if missing:
        raise SystemExit(f"front matter {rel} missing sections: {', '.join(missing)}")

for rel, sections in required_part_openers.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [item for item in sections if item not in text]
    if missing:
        raise SystemExit(f"part opener {rel} missing sections: {', '.join(missing)}")

for rel, sections in required_english_chapter_sections.items():
    check_english_chapter(rel, sections)

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
