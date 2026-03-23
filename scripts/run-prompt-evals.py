#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = {
    "bugfix-contract": ROOT / "prompts" / "bugfix-contract.md",
    "feature-contract": ROOT / "prompts" / "feature-contract.md",
}
PROMPT_HEADINGS = [
    "## Objective",
    "## Inputs",
    "## Constraints",
    "## Forbidden Actions",
    "## Missing Information Policy",
    "## Completion Criteria",
    "## Output Format",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_prompt_contracts() -> None:
    for prompt_name, path in PROMPTS.items():
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in PROMPT_HEADINGS if heading not in text]
        if missing:
            joined = ", ".join(missing)
            raise SystemExit(f"prompt {prompt_name} missing sections: {joined}")


def validate_cases(cases_doc: dict[str, Any]) -> None:
    if not isinstance(cases_doc, dict):
        raise SystemExit("eval cases must be a mapping")
    if "suite" not in cases_doc or "cases" not in cases_doc:
        raise SystemExit("eval cases must define suite and cases")
    if not isinstance(cases_doc["cases"], list):
        raise SystemExit("eval cases must define a cases list")
    if len(cases_doc["cases"]) < 5:
        raise SystemExit("eval cases should contain at least 5 cases")

    seen_ids: set[str] = set()
    for case in cases_doc["cases"]:
        if not isinstance(case, dict):
            raise SystemExit("each eval case must be a mapping")
        required = ["id", "prompt", "task", "input", "must_include", "must_not_include"]
        missing = [key for key in required if key not in case]
        if missing:
            joined = ", ".join(missing)
            raise SystemExit(f"eval case missing keys: {joined}")
        case_id = case["id"]
        if case_id in seen_ids:
            raise SystemExit(f"duplicate eval case id: {case_id}")
        seen_ids.add(case_id)
        prompt_name = case["prompt"]
        if prompt_name not in PROMPTS:
            raise SystemExit(f"unknown prompt in eval case {case_id}: {prompt_name}")
        for key in ["must_include", "must_not_include"]:
            value = case[key]
            if not isinstance(value, list) or not value:
                raise SystemExit(f"eval case {case_id} key {key} must be a non-empty list")


def validate_rubric(rubric: dict[str, Any]) -> None:
    required = ["name", "pass_threshold", "criteria"]
    missing = [key for key in required if key not in rubric]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"rubric missing keys: {joined}")
    if not isinstance(rubric["criteria"], list) or not rubric["criteria"]:
        raise SystemExit("rubric criteria must be a non-empty list")

    seen_ids: set[str] = set()
    for criterion in rubric["criteria"]:
        if not isinstance(criterion, dict):
            raise SystemExit("each rubric criterion must be a mapping")
        missing = [key for key in ["id", "description", "weight"] if key not in criterion]
        if missing:
            joined = ", ".join(missing)
            raise SystemExit(f"rubric criterion missing keys: {joined}")
        criterion_id = criterion["id"]
        if criterion_id in seen_ids:
            raise SystemExit(f"duplicate rubric criterion id: {criterion_id}")
        seen_ids.add(criterion_id)
        if not isinstance(criterion["weight"], int) or criterion["weight"] <= 0:
            raise SystemExit(f"rubric criterion {criterion_id} must have a positive integer weight")


def main() -> int:
    required = [
        *PROMPTS.values(),
        ROOT / "evals" / "prompt-contract-cases.json",
        ROOT / "evals" / "rubrics" / "feature-spec.json",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        print("missing:")
        for item in missing:
            print(f"  - {item}")
        return 1

    validate_prompt_contracts()
    cases_doc = load_json(ROOT / "evals" / "prompt-contract-cases.json")
    rubric = load_json(ROOT / "evals" / "rubrics" / "feature-spec.json")
    validate_cases(cases_doc)
    validate_rubric(rubric)

    print(f"suite: {cases_doc['suite']}")
    print(f"cases: {len(cases_doc['cases'])}")
    print(f"rubric: {rubric['name']}")
    print(f"criteria: {len(rubric['criteria'])}")
    print("prompt eval artifacts look consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
