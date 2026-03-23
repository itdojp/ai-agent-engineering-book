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
  "ja/index.html"
  "en/index.html"
  "ja/front-matter/00.html"
  "en/front-matter/00.html"
  "ja/part-00/ch01.html"
  "en/part-00/ch01.html"
  "assets/book.css"
  ".nojekyll"
)

for path in "${required[@]}"; do
  if [[ ! -f "$OUT/$path" ]]; then
    echo "missing pages artifact: $path"
    exit 1
  fi
done

grep -q "AIエージェント実践" "$OUT/index.html"
grep -q "日本語版" "$OUT/ja/index.html"
grep -q "English Edition" "$OUT/en/index.html"
grep -q "AIエージェントはどこで失敗するか" "$OUT/ja/part-00/ch01.html"
grep -q "Where AI Agents Fail" "$OUT/en/part-00/ch01.html"

echo "pages artifacts look consistent"
