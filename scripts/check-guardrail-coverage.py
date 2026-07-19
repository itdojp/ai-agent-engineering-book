#!/usr/bin/env python3
"""Deterministically verify the guardrail surface coverage fixture.

The fixture is intentionally repository-relative: verification evidence must
point at an artifact in this repository, not at a machine-specific path.
This checker uses only the Python standard library and supports Python 3.9+.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CASES = ROOT / "evals" / "guardrail-surface-cases.json"

REQUIRED_SURFACES = {
    "external-input",
    "model-output",
    "tool-definition",
    "tool-call",
    "tool-execution",
    "tool-result",
    "resource-content",
    "trace-log",
    "session-memory",
    "external-service",
    "protocol-prompts-roots",
    "protocol-sampling-elicitation",
}
REQUIRED_CONTROLS = {
    "classification",
    "redaction",
    "permission",
    "approval",
    "storage-retention",
    "verification",
}
MINIMUM_CASE_SURFACES = {
    "hostile-input": "external-input",
    "hostile-tool-output": "tool-result",
    "tainted-tool-metadata": "tool-definition",
    "unsafe-side-effect": "tool-execution",
    "trace-leakage": "trace-log",
    "stale-sensitive-session": "session-memory",
    "external-provider-boundary": "external-service",
}
MINIMUM_HOSTILE_CASES = set(MINIMUM_CASE_SURFACES)
DECISIONS = {"allow", "deny", "escalate"}
HOSTILE_DECISIONS = {"deny", "escalate"}
MINIMUM_CASE_EVIDENCE_PATH = "docs/guardrail-coverage-matrix.md"


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_object(value: Any) -> bool:
    return isinstance(value, dict)


def _is_repository_path(path: Path, root: Path = ROOT) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _missing_or_extra_keys(
    value: Dict[str, Any], expected: Set[str], path: str, errors: List[str]
) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(f"{path} missing keys: {', '.join(missing)}")
    if extra:
        errors.append(f"{path} has unknown keys: {', '.join(extra)}")


def _validate_evidence(
    value: Any,
    case_id: Any,
    case_path: str,
    root: Path,
    errors: List[str],
) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{case_path}.verification_evidence must be a non-empty list")
        return

    for index, artifact in enumerate(value):
        evidence_path = f"{case_path}.verification_evidence[{index}]"
        if not _is_object(artifact):
            errors.append(f"{evidence_path} must be an object with path and contains")
            continue
        _missing_or_extra_keys(artifact, {"path", "contains"}, evidence_path, errors)
        path_value = artifact.get("path")
        marker = artifact.get("contains")
        if not _non_empty_string(path_value):
            errors.append(f"{evidence_path}.path must be a non-empty repository-relative path")
            continue
        if not _non_empty_string(marker):
            errors.append(f"{evidence_path}.contains must be a non-empty string")
            continue
        if isinstance(case_id, str) and case_id in MINIMUM_HOSTILE_CASES:
            expected_marker = f"`{case_id}`"
            if marker != expected_marker:
                errors.append(
                    f"{evidence_path}.contains for {case_id} must be exact marker: "
                    f"{expected_marker}"
                )
            if path_value != MINIMUM_CASE_EVIDENCE_PATH:
                errors.append(
                    f"{evidence_path}.path for {case_id} must be canonical artifact: "
                    f"{MINIMUM_CASE_EVIDENCE_PATH}"
                )

        candidate = Path(path_value)
        if candidate.is_absolute():
            errors.append(f"{evidence_path}.path must be repository-relative: {path_value}")
            continue

        resolved = (root / candidate).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f"{evidence_path}.path escapes repository root: {path_value}")
            continue
        if not resolved.is_file():
            errors.append(f"{evidence_path}.path references missing file: {path_value}")
            continue
        try:
            evidence_text = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{evidence_path}.path cannot be read: {path_value}: {error}")
            continue
        if marker not in evidence_text:
            errors.append(
                f"{evidence_path}.contains marker not found in {path_value}: {marker}"
            )


def validate_document(document: Any, root: Path = ROOT) -> List[str]:
    """Return all validation errors in stable order; an empty list means valid."""

    errors: List[str] = []
    if not _is_object(document):
        return ["document must be a JSON object"]

    _missing_or_extra_keys(document, {"surfaces", "cases"}, "document", errors)

    surfaces = document.get("surfaces")
    surface_ids: Set[str] = set()
    if not isinstance(surfaces, list) or not surfaces:
        errors.append("surfaces must be a non-empty list")
        surfaces = []

    for index, surface in enumerate(surfaces):
        surface_path = f"surfaces[{index}]"
        if not _is_object(surface):
            errors.append(f"{surface_path} must be an object")
            continue
        _missing_or_extra_keys(surface, {"id", "controls"}, surface_path, errors)

        surface_id = surface.get("id")
        if not _non_empty_string(surface_id):
            errors.append(f"{surface_path}.id must be a non-empty string")
            continue
        if surface_id in surface_ids:
            errors.append(f"duplicate surface id: {surface_id}")
        surface_ids.add(surface_id)

        controls = surface.get("controls")
        if not _is_object(controls):
            errors.append(f"{surface_path}.controls must be an object")
            continue
        _missing_or_extra_keys(controls, REQUIRED_CONTROLS, f"{surface_path}.controls", errors)
        for control in sorted(REQUIRED_CONTROLS):
            if control not in controls:
                continue
            if not _non_empty_string(controls[control]):
                errors.append(
                    f"{surface_path}.controls.{control} must be a non-empty string"
                )

    missing_surfaces = sorted(REQUIRED_SURFACES - surface_ids)
    if missing_surfaces:
        errors.append(f"missing required surface(s): {', '.join(missing_surfaces)}")

    cases = document.get("cases")
    case_ids: Set[str] = set()
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list")
        cases = []

    expected_case_keys = {
        "id",
        "surface",
        "threat",
        "required_controls",
        "expected_decision",
        "verification_evidence",
    }
    for index, case in enumerate(cases):
        case_path = f"cases[{index}]"
        if not _is_object(case):
            errors.append(f"{case_path} must be an object")
            continue
        _missing_or_extra_keys(case, expected_case_keys, case_path, errors)

        case_id = case.get("id")
        if not _non_empty_string(case_id):
            errors.append(f"{case_path}.id must be a non-empty string")
        elif case_id in case_ids:
            errors.append(f"duplicate case id: {case_id}")
        else:
            case_ids.add(case_id)

        surface = case.get("surface")
        if not _non_empty_string(surface):
            errors.append(f"{case_path}.surface must be a non-empty string")
        elif surface not in surface_ids:
            errors.append(f"{case_path}.surface references unknown surface: {surface}")
        elif isinstance(case_id, str) and case_id in MINIMUM_CASE_SURFACES:
            expected_surface = MINIMUM_CASE_SURFACES[case_id]
            if surface != expected_surface:
                errors.append(
                    f"hostile case {case_id} must target surface {expected_surface}, not {surface}"
                )

        if not _non_empty_string(case.get("threat")):
            errors.append(f"{case_path}.threat must be a non-empty string")

        required_controls = case.get("required_controls")
        if not isinstance(required_controls, list) or not required_controls:
            errors.append(f"{case_path}.required_controls must be a non-empty list")
        else:
            seen_controls: Set[str] = set()
            for control_index, control in enumerate(required_controls):
                control_path = f"{case_path}.required_controls[{control_index}]"
                if not _non_empty_string(control):
                    errors.append(f"{control_path} must be a non-empty string")
                    continue
                if control in seen_controls:
                    errors.append(f"{case_path}.required_controls has duplicate: {control}")
                seen_controls.add(control)
                if control not in REQUIRED_CONTROLS:
                    errors.append(f"{control_path} is not a required control: {control}")
            if isinstance(case_id, str) and case_id in MINIMUM_HOSTILE_CASES:
                missing_controls = sorted(REQUIRED_CONTROLS - seen_controls)
                if missing_controls:
                    errors.append(
                        f"hostile case {case_id} missing required control(s): "
                        f"{', '.join(missing_controls)}"
                    )

        decision = case.get("expected_decision")
        if not isinstance(decision, str) or decision not in DECISIONS:
            errors.append(
                f"{case_path}.expected_decision must be one of: {', '.join(sorted(DECISIONS))}"
            )
        elif isinstance(case_id, str) and case_id in MINIMUM_HOSTILE_CASES and decision not in HOSTILE_DECISIONS:
            errors.append(
                f"hostile case {case_id} must expect deny or escalate, not {decision}"
            )

        _validate_evidence(
            case.get("verification_evidence"), case_id, case_path, root, errors
        )

    missing_cases = sorted(MINIMUM_HOSTILE_CASES - case_ids)
    if missing_cases:
        errors.append(f"missing minimum hostile case(s): {', '.join(missing_cases)}")

    return sorted(set(errors))


def load_document(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_negative_self_test() -> int:
    """Exercise required rejection paths without writing a temporary fixture."""

    try:
        baseline = load_document(DEFAULT_CASES)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"negative self-test cannot load default fixture: {error}", file=sys.stderr)
        return 1

    baseline_errors = validate_document(baseline)
    if baseline_errors:
        print("negative self-test baseline is invalid:", file=sys.stderr)
        for error in baseline_errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    missing_surface = copy.deepcopy(baseline)
    missing_surface["surfaces"] = [
        surface
        for surface in missing_surface["surfaces"]
        if surface.get("id") != "external-input"
    ]
    surface_errors = validate_document(missing_surface)
    if not any("missing required surface(s): external-input" in error for error in surface_errors):
        print("negative self-test failed: missing surface was accepted", file=sys.stderr)
        return 1

    missing_control = copy.deepcopy(baseline)
    for surface in missing_control["surfaces"]:
        if surface.get("id") == "external-input":
            del surface["controls"]["classification"]
            break
    control_errors = validate_document(missing_control)
    if not any(".controls missing keys: classification" in error for error in control_errors):
        print("negative self-test failed: missing control was accepted", file=sys.stderr)
        return 1

    missing_case = copy.deepcopy(baseline)
    missing_case["cases"] = [
        case
        for case in missing_case["cases"]
        if case.get("id") != "hostile-input"
    ]
    case_errors = validate_document(missing_case)
    if not any(
        "missing minimum hostile case(s): hostile-input" in error
        for error in case_errors
    ):
        print("negative self-test failed: missing hostile case was accepted", file=sys.stderr)
        return 1

    missing_case_control = copy.deepcopy(baseline)
    for case in missing_case_control["cases"]:
        if case.get("id") == "hostile-input":
            case["required_controls"].remove("approval")
            break
    case_control_errors = validate_document(missing_case_control)
    if not any(
        "hostile case hostile-input missing required control(s): approval" in error
        for error in case_control_errors
    ):
        print(
            "negative self-test failed: hostile case missing a control was accepted",
            file=sys.stderr,
        )
        return 1

    wrong_case_surface = copy.deepcopy(baseline)
    for case in wrong_case_surface["cases"]:
        if case.get("id") == "hostile-tool-output":
            case["surface"] = "external-input"
            break
    wrong_surface_errors = validate_document(wrong_case_surface)
    if not any(
        "hostile case hostile-tool-output must target surface tool-result, not external-input"
        in error
        for error in wrong_surface_errors
    ):
        print("negative self-test failed: hostile case surface drift was accepted", file=sys.stderr)
        return 1

    if _is_repository_path(ROOT.parent / "outside-guardrail-fixture.json"):
        print("negative self-test failed: out-of-root fixture path was accepted", file=sys.stderr)
        return 1

    escaped_evidence = copy.deepcopy(baseline)
    escaped_evidence["cases"][0]["verification_evidence"] = [
        {"path": "../outside-evidence.md", "contains": "hostile-input"}
    ]
    escaped_evidence_errors = validate_document(escaped_evidence)
    if not any("escapes repository root" in error for error in escaped_evidence_errors):
        print("negative self-test failed: escaped evidence path was accepted", file=sys.stderr)
        return 1

    absolute_evidence = copy.deepcopy(baseline)
    absolute_evidence["cases"][0]["verification_evidence"] = [
        {
            "path": str(ROOT / "docs" / "guardrail-coverage-matrix.md"),
            "contains": "hostile-input",
        }
    ]
    absolute_evidence_errors = validate_document(absolute_evidence)
    if not any("must be repository-relative" in error for error in absolute_evidence_errors):
        print("negative self-test failed: absolute evidence path was accepted", file=sys.stderr)
        return 1

    unrelated_evidence = copy.deepcopy(baseline)
    unrelated_evidence["cases"][0]["verification_evidence"] = [
        {"path": "README.md", "contains": "`hostile-input`"}
    ]
    unrelated_evidence_errors = validate_document(unrelated_evidence)
    if not any("contains marker not found" in error for error in unrelated_evidence_errors):
        print("negative self-test failed: unrelated evidence was accepted", file=sys.stderr)
        return 1

    generic_marker = copy.deepcopy(baseline)
    generic_marker["cases"][0]["verification_evidence"] = [
        {"path": MINIMUM_CASE_EVIDENCE_PATH, "contains": "Case"}
    ]
    generic_marker_errors = validate_document(generic_marker)
    if not any("must be exact marker" in error for error in generic_marker_errors):
        print("negative self-test failed: generic evidence marker was accepted", file=sys.stderr)
        return 1

    print("guardrail coverage negative self-test passed")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=DEFAULT_CASES,
        help="JSON fixture to verify (default: evals/guardrail-surface-cases.json)",
    )
    parser.add_argument(
        "--negative-self-test",
        "--self-test",
        dest="negative_self_test",
        action="store_true",
        help=(
            "run in-memory fail-closed checks for missing surfaces, controls, and cases; "
            "case mappings; and fixture/evidence path and marker constraints"
        ),
    )
    args = parser.parse_args(argv)

    if args.negative_self_test:
        return run_negative_self_test()

    cases_path = args.cases
    if not cases_path.is_absolute():
        cases_path = ROOT / cases_path
    cases_path = cases_path.resolve()
    if not _is_repository_path(cases_path):
        print(
            f"guardrail coverage fixture must be inside repository root: {cases_path}",
            file=sys.stderr,
        )
        return 1
    try:
        document = load_document(cases_path)
    except FileNotFoundError:
        print(f"guardrail coverage fixture not found: {cases_path}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"cannot read guardrail coverage fixture {cases_path}: {error}", file=sys.stderr)
        return 1

    errors = validate_document(document)
    if errors:
        print(f"guardrail coverage fixture rejected: {cases_path}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"guardrail coverage fixture accepted: {cases_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
