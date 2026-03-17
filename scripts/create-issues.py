#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: create-issues.py owner/repo")

repo = sys.argv[1]
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "issue-drafts" / "manifest.json").read_text(encoding="utf-8"))

for issue in manifest["issues"]:
    cmd = [
        "gh", "issue", "create",
        "--repo", repo,
        "--title", issue["title"],
        "--body-file", str(root / issue["body_file"]),
    ]
    for label in issue["labels"]:
        cmd += ["--label", label]
    if issue.get("milestone"):
        cmd += ["--milestone", issue["milestone"]]
    subprocess.run(cmd, check=True)
    print(f"created: {issue['title']}")
