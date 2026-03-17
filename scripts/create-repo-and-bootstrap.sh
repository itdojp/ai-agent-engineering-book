#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 owner/repo"
  exit 1
fi

REPO="$1"

gh repo create "$REPO" --private --source=. --remote=origin --push
"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/bootstrap-github.sh" "$REPO"
