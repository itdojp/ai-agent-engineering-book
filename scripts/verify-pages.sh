#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$ROOT/.tmp"
mkdir -p "$TMP_ROOT"
TMPDIR="$(mktemp -d "$TMP_ROOT/verify-pages.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

python3 -m venv "$TMPDIR/.venv"
# shellcheck source=/dev/null
source "$TMPDIR/.venv/bin/activate"

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r "$ROOT/requirements-pages.txt"

OUT="$TMPDIR/site"
TEST_REVISION="0123456789abcdef0123456789abcdef01234567"
python "$ROOT/scripts/build-pages.py" --verify-reader-resources
if python "$ROOT/scripts/build-pages.py" --output "$TMPDIR/missing-revision" >/dev/null 2>&1; then
  echo "pages build accepted a missing immutable revision"
  exit 1
fi
python "$ROOT/scripts/build-pages.py" --output "$OUT" --build-revision "$TEST_REVISION"

required=(
  "index.html"
  "en/index.html"
  "introduction/01/index.html"
  "chapters/ch01/index.html"
  "chapters/ch12/index.html"
  "en/chapters/ch01/index.html"
  "en/chapters/ch12/index.html"
  "checklists/index.html"
  "checklists/prompt-contract-review/index.html"
  "checklists/verification/index.html"
  "checklists/repo-hygiene/index.html"
  "troubleshooting/index.html"
  "en/checklists/index.html"
  "en/checklists/prompt-contract-review/index.html"
  "en/checklists/verification/index.html"
  "en/checklists/repo-hygiene/index.html"
  "en/troubleshooting/index.html"
  "assets/css/main.css"
  "assets/css/mobile-responsive.css"
  "assets/css/syntax-highlighting.css"
  "assets/css/book-custom.css"
  "assets/js/search.js"
  "assets/js/theme.js"
  "assets/js/code-copy-lightweight.js"
  "assets/images/favicon.svg"
  "build-revision.txt"
  ".nojekyll"
)

for path in "${required[@]}"; do
  if [[ ! -f "$OUT/$path" ]]; then
    echo "missing pages artifact: $path"
    exit 1
  fi
done

grep -q "AIエージェント実践" "$OUT/index.html"
grep -q "book-layout" "$OUT/index.html"
grep -q "CH01 から読む" "$OUT/index.html"
grep -q "AI Agent Engineering in Practice" "$OUT/en/index.html"
grep -q "Start with CH01" "$OUT/en/index.html"
grep -q "AIエージェントはどこで失敗するか" "$OUT/chapters/ch01/index.html"
grep -q "mergeからproduction確認までを閉じる" "$OUT/chapters/ch12/index.html"
grep -q "Production Confirmed" "$OUT/chapters/ch12/index.html"
grep -q "Superseded" "$OUT/chapters/ch12/index.html"
grep -q "Chapter 1" "$OUT/en/chapters/ch01/index.html"
grep -q "Where AI Agents Fail - AI Agent Engineering in Practice" "$OUT/en/chapters/ch01/index.html"
grep -q "Close the path from merge to production confirmation" "$OUT/en/chapters/ch12/index.html"
grep -q "Production Confirmed" "$OUT/en/chapters/ch12/index.html"
grep -q "Superseded" "$OUT/en/chapters/ch12/index.html"
grep -q 'meta name="author" content="株式会社アイティードゥ"' "$OUT/index.html"
grep -q "meta name=\"book-build-revision\" content=\"$TEST_REVISION\"" "$OUT/index.html"
grep -q "meta name=\"book-build-revision\" content=\"$TEST_REVISION\"" "$OUT/chapters/ch12/index.html"
test "$(cat "$OUT/build-revision.txt")" = "$TEST_REVISION"
grep -q 'link rel="canonical" href="https://itdojp.github.io/ai-agent-engineering-book/"' "$OUT/index.html"
grep -q 'meta property="og:title"' "$OUT/index.html"
grep -q 'meta name="twitter:card" content="summary"' "$OUT/index.html"
grep -q 'link rel="icon" type="image/svg+xml" href="assets/images/favicon.svg"' "$OUT/index.html"
grep -q 'meta name="author" content="株式会社アイティードゥ"' "$OUT/en/index.html"
grep -q 'link rel="canonical" href="https://itdojp.github.io/ai-agent-engineering-book/en/"' "$OUT/en/index.html"
grep -q 'meta property="og:title"' "$OUT/en/index.html"
grep -q 'meta property="og:site_name" content="AI Agent Engineering in Practice: Prompt / Context / Harness Engineering"' "$OUT/en/index.html"
grep -q 'meta name="twitter:card" content="summary"' "$OUT/en/index.html"
grep -q 'link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg"' "$OUT/en/index.html"
grep -q 'Refusal / Stop Conditions' "$OUT/checklists/prompt-contract-review/index.html"
grep -q 'Stop Instead Of Merge' "$OUT/checklists/verification/index.html"
grep -q 'Production-ready Plan' "$OUT/checklists/verification/index.html"
grep -q 'Production Evidence' "$OUT/checklists/verification/index.html"
grep -q 'Superseded' "$OUT/checklists/verification/index.html"
grep -q 'Escalate When' "$OUT/checklists/repo-hygiene/index.html"
grep -q '最小安全確認' "$OUT/troubleshooting/index.html"
grep -q '停止とエスカレーション' "$OUT/troubleshooting/index.html"
grep -q '証跡を残す' "$OUT/troubleshooting/index.html"
grep -q 'Minimum Safe Check' "$OUT/en/troubleshooting/index.html"
grep -q 'Production-ready Plan' "$OUT/en/checklists/verification/index.html"
grep -q 'Production Evidence' "$OUT/en/checklists/verification/index.html"
grep -q 'Superseded' "$OUT/en/checklists/verification/index.html"
grep -q 'Stop and Escalate' "$OUT/en/troubleshooting/index.html"
grep -q 'Preserve Evidence' "$OUT/en/troubleshooting/index.html"

if grep -q "AIエージェント実践" "$OUT/en/index.html" || \
   grep -q "AIエージェント実践" "$OUT/en/chapters/ch01/index.html"; then
  echo "english pages still expose the Japanese book title"
  exit 1
fi

if grep -q 'book-toc-panel' "$OUT/chapters/ch01/index.html" || \
   grep -q 'book-toc-panel' "$OUT/en/chapters/ch01/index.html"; then
  echo "chapter page still renders a redundant page-level TOC"
  exit 1
fi

if grep -q "Publishing Guide" "$OUT/index.html"; then
  echo "public landing page still exposes operator publishing wording"
  exit 1
fi

if grep -q "canonical source" "$OUT/index.html"; then
  echo "public landing page still exposes canonical source wording"
  exit 1
fi

python - <<'PY' "$OUT"
from pathlib import Path
import posixpath
import sys

out = Path(sys.argv[1])
routes = [
    "checklists",
    "checklists/prompt-contract-review",
    "checklists/verification",
    "checklists/repo-hygiene",
    "troubleshooting",
]

def route_file(route: str) -> Path:
    return Path(route) / "index.html"

def href_to(source: Path, destination: Path) -> str:
    return posixpath.relpath(destination.as_posix(), source.parent.as_posix())

def require(path: Path, text: str) -> None:
    content = path.read_text(encoding="utf-8")
    if text not in content:
        raise SystemExit(f"generated page {path.relative_to(out)} is missing: {text}")

for language, group_title, index_title, counterpart_label in (
    ("ja", "読者向けリソース", "チェックリスト集", "English"),
    ("en", "Reader Resources", "Checklists", "日本語"),
):
    prefix = Path() if language == "ja" else Path("en")
    counterpart_prefix = Path("en") if language == "ja" else Path()
    for route in routes:
        source = prefix / route_file(route)
        counterpart = counterpart_prefix / route_file(route)
        require(out / source, group_title)
        require(out / source, counterpart_label)
        require(out / source, f'href="{href_to(source, counterpart)}" class="external-link"')
        for nav_route in routes:
            destination = prefix / route_file(nav_route)
            require(out / source, f'href="{href_to(source, destination)}" class="toc-link')

    index = prefix / route_file("checklists")
    require(out / index, index_title)
    for checklist_route in routes[1:4]:
        destination = prefix / route_file(checklist_route)
        require(out / index, f'href="{href_to(index, destination)}"')

    first = prefix / route_file("checklists")
    prompt = prefix / route_file("checklists/prompt-contract-review")
    verification = prefix / route_file("checklists/verification")
    hygiene = prefix / route_file("checklists/repo-hygiene")
    troubleshooting = prefix / route_file("troubleshooting")
    require(out / first, f'href="{href_to(first, prompt)}" class="nav-next"')
    require(out / prompt, f'href="{href_to(prompt, first)}" class="nav-prev"')
    require(out / prompt, f'href="{href_to(prompt, verification)}" class="nav-next"')
    require(out / verification, f'href="{href_to(verification, hygiene)}" class="nav-next"')
    require(out / hygiene, f'href="{href_to(hygiene, troubleshooting)}" class="nav-next"')
    require(out / troubleshooting, f'href="{href_to(troubleshooting, hygiene)}" class="nav-prev"')
    require(out / first, '<span class="nav-disabled nav-prev">')

    # Reader resources have their own pager sequence. Existing manuscript
    # backmatter must remain terminal instead of acquiring a new next link.
    terminal = prefix / Path("backmatter/03/index.html")
    require(out / terminal, '<span class="nav-disabled nav-next">')

print("reader resource routes, navigation, counterparts, and flow look consistent")
PY

echo "pages artifacts look consistent"
