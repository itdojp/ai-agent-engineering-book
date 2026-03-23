#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"

required=(
  "AGENTS.md"
  "README.md"
  "STATUS.md"
  "docs/glossary.md"
  "docs/en/README.md"
  "docs/en/glossary.md"
  "docs/en/context-model.md"
  "docs/en/context-budget.md"
  "docs/en/context-risk-register.md"
  "docs/en/session-memory-policy.md"
  "docs/en/operating-model.md"
  "docs/en/metrics.md"
  "manuscript/AGENTS.md"
  "manuscript/front-matter/00-はじめに.md"
  "manuscript/front-matter/01-本書の読み方.md"
  "manuscript/figures/README.md"
  "manuscript/figures/figure-plan.md"
  "manuscript/backmatter/00-source-notes.md"
  "manuscript/backmatter/01-読書案内.md"
  "manuscript/backmatter/02-索引seed.md"
  "manuscript/backmatter/03-図表一覧方針.md"
  "manuscript-en/front-matter/00-introduction.md"
  "manuscript-en/front-matter/01-how-to-read-this-book.md"
  "manuscript-en/figures/README.md"
  "manuscript-en/figures/figure-plan.md"
  "manuscript-en/backmatter/00-source-notes.md"
  "manuscript-en/backmatter/01-reading-guide.md"
  "manuscript-en/backmatter/02-index-seed.md"
  "manuscript-en/backmatter/03-figure-table-list-policy.md"
  "manuscript/part-01-prompt/part-opener.md"
  "manuscript/part-02-context/part-opener.md"
  "manuscript/part-03-harness/part-opener.md"
  "manuscript-en/part-01-prompt/part-opener.md"
  "manuscript-en/part-02-context/part-opener.md"
  "manuscript-en/part-03-harness/part-opener.md"
  "sample-repo/AGENTS.md"
  ".github/ISSUE_TEMPLATE/task.yml"
  "issue-drafts/manifest.json"
  "prompts/en/README.md"
  "prompts/en/bugfix-contract.md"
  "prompts/en/feature-contract.md"
  "checklists/en/README.md"
  "checklists/en/prompt-contract-review.md"
  "checklists/en/verification.md"
  "checklists/en/repo-hygiene.md"
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

required_sections = ["## 学習目標", "## 小見出し", "## 演習", "## 参照する artifact", "## Source Notes / Further Reading"]
required_frontmatter = {
    "manuscript/front-matter/00-はじめに.md": ["## 本書の約束", "## 想定読者", "## 想定しない読者"],
    "manuscript/front-matter/01-本書の読み方.md": ["## 3部構成", "## 3つの読み進め方", "## 読み終わりの到達点"],
}
required_frontmatter_en = {
    "front-matter/00-introduction.md": ["## What This Book Promises", "## Intended Reader", "## Not the Intended Reader"],
    "front-matter/01-how-to-read-this-book.md": ["## Three-Part Structure", "## Three Ways to Read This Book", "## What You Should Be Able to Do by the End"],
}
required_backmatter = {
    "manuscript/backmatter/00-source-notes.md": ["## この後付けの役割", "## Source Policy", "## 章別 Source Notes"],
    "manuscript/backmatter/01-読書案内.md": ["## 使い方", "## Prompt と要求定義", "## 検証・信頼性・運用"],
    "manuscript/backmatter/02-索引seed.md": ["## 使い方", "## 索引 seed"],
    "manuscript/backmatter/03-図表一覧方針.md": ["## 役割", "## 図一覧の方針", "## 表一覧の方針"],
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
required_part_opener_sections_en = [
    "## Role of This Part",
    "## Artifacts Added in This Part",
    "## Chapter Map",
    "## What You Should Be Able to Do by the End of This Part",
]
required_part_openers_en = {
    "part-01-prompt/part-opener.md": required_part_opener_sections_en,
    "part-02-context/part-opener.md": required_part_opener_sections_en,
    "part-03-harness/part-opener.md": required_part_opener_sections_en,
}
required_sections_en = ["## Learning Objectives", "## Outline", "## Exercises", "## Referenced Artifacts", "## Source Notes / Further Reading"]
required_backmatter_en = {
    "manuscript-en/backmatter/00-source-notes.md": ["## What This Backmatter Does", "## Source Policy", "## Chapter-by-Chapter Source Notes"],
    "manuscript-en/backmatter/01-reading-guide.md": ["## How to Use This Guide", "## Prompts and Requirements Shaping", "## Verification, Reliability, and Operations"],
    "manuscript-en/backmatter/02-index-seed.md": ["## How to Use This Seed", "## Index Seed"],
    "manuscript-en/backmatter/03-figure-table-list-policy.md": ["## Role", "## Figure List Policy", "## Table List Policy"],
}
forbidden_english_root_refs = [
    "docs/context-model.md",
    "docs/context-budget.md",
    "docs/context-risk-register.md",
    "docs/session-memory-policy.md",
    "docs/operating-model.md",
    "docs/metrics.md",
    "prompts/bugfix-contract.md",
    "prompts/feature-contract.md",
    "checklists/prompt-contract-review.md",
    "checklists/verification.md",
    "checklists/repo-hygiene.md",
]
required_figure_readme_en = {
    "manuscript-en/figures/README.md": ["## Source Of Truth", "## Update Policy", "## Print / Ebook Rule"],
    "manuscript-en/figures/figure-plan.md": ["| Figure ID | Chapter | Suggested Placement | Caption | Reader Value | Source |", "`fig-01`", "`fig-07`"],
}
required_figure_sources_en = [
    "fig-01-maturity-model.mmd",
    "fig-02-context-classes.mmd",
    "fig-03-resume-packet.mmd",
    "fig-04-single-agent-harness.mmd",
    "fig-05-verification-pipeline.mmd",
    "fig-06-long-running-multi-agent.mmd",
    "fig-07-operating-model.mmd",
]
forbidden_root_onboarding_phrases = {
    "README.md": [
        "GitHub 上に空 repo を作成し、この内容を push する",
        "`REPO-01` から順に issue を処理する",
    ],
    "STATUS.md": [
        "GitHub に空 repo を作成する",
        "この scaffold を push する",
        "`REPO-01` から Codex CLI に投入する",
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


def chapter_title(ch_id: str) -> str:
    chapter = expect_single_path(f"manuscript/**/{ch_id}-*.md", f"chapter file for {ch_id}")
    for line in chapter.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    raise SystemExit(f"chapter {ch_id} is missing a title heading")


def english_chapter_title(ch_id: str) -> str:
    chapter = expect_single_path(f"manuscript-en/**/{ch_id}-*.md", f"English chapter file for {ch_id}")
    for line in chapter.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    raise SystemExit(f"English chapter {ch_id} is missing a title heading")

def expect_single_path(pattern: str, label: str) -> Path:
    paths = sorted(root.glob(pattern))
    if not paths:
        raise SystemExit(f"missing {label}")
    if len(paths) != 1:
        raise SystemExit(f"{label} is ambiguous: expected 1 match for {pattern}, found {len(paths)}")
    return paths[0]


def check_english_chapter(ch_id: str, brief: Path):
    chapter = expect_single_path(f"manuscript-en/**/{ch_id}-*.md", f"English chapter file for {ch_id}")
    text = chapter.read_text(encoding="utf-8")
    missing = [item for item in required_sections_en if item not in text]
    if missing:
        raise SystemExit(f"English chapter {ch_id} missing sections: {', '.join(missing)}")
    if "manuscript/backmatter/" in text:
        raise SystemExit(f"English chapter {ch_id} still points to Japanese backmatter")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"English brief {brief.name} references missing artifact: {artifact}")


def check_english_appendix(app_id: str, brief: Path):
    expect_single_path(f"manuscript-en/appendices/{app_id}-*.md", f"English appendix file for {app_id}")
    for artifact in parse_artifacts(brief):
        if not (root / artifact).exists():
            raise SystemExit(f"English brief {brief.name} references missing artifact: {artifact}")


def check_english_backmatter(en_root: Path):
    for rel, sections in required_backmatter_en.items():
        text = (root / rel).read_text(encoding="utf-8")
        missing = [item for item in sections if item not in text]
        if missing:
            raise SystemExit(f"English backmatter {rel} missing sections: {', '.join(missing)}")

    source_notes = (en_root / "backmatter" / "00-source-notes.md").read_text(encoding="utf-8")
    for brief in sorted((en_root / "briefs").glob("ch*.yaml")):
        heading = f"### {brief.stem.upper()} {english_chapter_title(brief.stem)}"
        if heading not in source_notes:
            raise SystemExit(f"English source notes missing chapter heading: {heading}")

def check_english_root_artifact_refs(en_root: Path):
    scan_paths = sorted(en_root.rglob("*.md")) + sorted((en_root / "briefs").glob("*.yaml"))
    for path in scan_paths:
        text = path.read_text(encoding="utf-8")
        for ref in forbidden_english_root_refs:
            if ref in text:
                rel = path.relative_to(root)
                raise SystemExit(f"English manuscript still points to Japanese root artifact {ref}: {rel}")
def check_english_figures(en_root: Path):
    for rel, sections in required_figure_readme_en.items():
        text = (root / rel).read_text(encoding="utf-8")
        missing = [item for item in sections if item not in text]
        if missing:
            raise SystemExit(f"English figure artifact {rel} missing sections: {', '.join(missing)}")

    figure_root = en_root / "figures"
    for rel in required_figure_sources_en:
        if not (figure_root / rel).exists():
            raise SystemExit(f"missing English figure source: manuscript-en/figures/{rel}")

    figure_backmatter = (en_root / "backmatter" / "03-figure-table-list-policy.md").read_text(encoding="utf-8")
    if "manuscript/figures/" in figure_backmatter:
        raise SystemExit("English figure/table policy still points to Japanese figure sources")
    if "manuscript-en/figures/figure-plan.md" not in figure_backmatter:
        raise SystemExit("English figure/table policy is missing manuscript-en figure-plan reference")
def check_english_reader_entry(en_root: Path):
    for rel, sections in required_frontmatter_en.items():
        text = (en_root / rel).read_text(encoding="utf-8")
        missing = [item for item in sections if item not in text]
        if missing:
            raise SystemExit(f"English front matter manuscript-en/{rel} missing sections: {', '.join(missing)}")

    for rel, sections in required_part_openers_en.items():
        text = (en_root / rel).read_text(encoding="utf-8")
        missing = [item for item in sections if item not in text]
        if missing:
            raise SystemExit(f"English part opener manuscript-en/{rel} missing sections: {', '.join(missing)}")

def check_root_onboarding_docs():
    for rel, phrases in forbidden_root_onboarding_phrases.items():
        path = root / rel
        if not path.exists():
            raise SystemExit(f"missing root onboarding doc: {rel}")
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase in text:
                raise SystemExit(f"root onboarding doc still contains stale pre-bootstrap guidance in {rel}: {phrase}")

def check_english_scaffold(target: str):
    en_root = root / "manuscript-en"
    if not en_root.exists():
        raise SystemExit("missing English manuscript scaffold: manuscript-en/")
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

    check_english_reader_entry(en_root)
    check_english_backmatter(en_root)
    check_english_root_artifact_refs(en_root)
    check_english_figures(en_root)

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

for rel, sections in required_frontmatter.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [item for item in sections if item not in text]
    if missing:
        raise SystemExit(f"front matter {rel} missing sections: {', '.join(missing)}")

for rel, sections in required_backmatter.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [item for item in sections if item not in text]
    if missing:
        raise SystemExit(f"backmatter {rel} missing sections: {', '.join(missing)}")

source_notes = (root / "manuscript/backmatter/00-source-notes.md").read_text(encoding="utf-8")
for brief in sorted((root / "manuscript" / "briefs").glob("ch*.yaml")):
    heading = f"### {brief.stem.upper()} {chapter_title(brief.stem)}"
    if heading not in source_notes:
        raise SystemExit(f"source notes missing chapter heading: {heading}")

for rel, sections in required_part_openers.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [item for item in sections if item not in text]
    if missing:
        raise SystemExit(f"part opener {rel} missing sections: {', '.join(missing)}")

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
check_root_onboarding_docs()

print("book scaffold looks consistent")
PY
