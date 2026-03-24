#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

python3 -m venv "$TMPDIR/.venv"
# shellcheck source=/dev/null
source "$TMPDIR/.venv/bin/activate"

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r "$ROOT/requirements-pages.txt"

OUT="$TMPDIR/site"
python "$ROOT/scripts/build-pages.py" --output "$OUT"

required=(
  "index.html"
  "en/index.html"
  "introduction/01/index.html"
  "chapters/ch01/index.html"
  "en/chapters/ch01/index.html"
  "assets/css/main.css"
  "assets/css/mobile-responsive.css"
  "assets/css/syntax-highlighting.css"
  "assets/css/book-custom.css"
  "assets/js/search.js"
  "assets/js/theme.js"
  "assets/js/code-copy-lightweight.js"
  "assets/images/favicon.svg"
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
grep -q "Start with CH01" "$OUT/en/index.html"
grep -q "AIエージェントはどこで失敗するか" "$OUT/chapters/ch01/index.html"
grep -q "Chapter 1" "$OUT/en/chapters/ch01/index.html"
grep -q 'meta name="author" content="株式会社アイティードゥ"' "$OUT/index.html"
grep -q 'link rel="canonical" href="https://itdojp.github.io/ai-agent-engineering-book/"' "$OUT/index.html"
grep -q 'meta property="og:title"' "$OUT/index.html"
grep -q 'meta name="twitter:card" content="summary"' "$OUT/index.html"
grep -q 'link rel="icon" type="image/svg+xml" href="assets/images/favicon.svg"' "$OUT/index.html"
grep -q 'link rel="canonical" href="https://itdojp.github.io/ai-agent-engineering-book/en/"' "$OUT/en/index.html"

if grep -q "Publishing Guide" "$OUT/index.html"; then
  echo "public landing page still exposes operator publishing wording"
  exit 1
fi

if grep -q "canonical source" "$OUT/index.html"; then
  echo "public landing page still exposes canonical source wording"
  exit 1
fi

echo "pages artifacts look consistent"
