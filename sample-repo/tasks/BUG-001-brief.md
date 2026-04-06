# BUG-001 Brief

## Source
- `docs/seed-issues.md` の `BUG-001`
- `../.github/ISSUE_TEMPLATE/task.yml`

## Goal
ステータス更新後の再読み込みで旧状態が見える、という仮想バグの再現条件を固定し、bugfix harness で扱える修正方針まで落とし込む。

## Scope
- stale read の再現条件を failing test の形で固定する
- root cause hypothesis を service / store 境界で整理する
- verify、変更対象、handoff 前提を含む fix plan を作る
- `Progress Note` に判断と verify 結果を残す

## Inputs
- `docs/repo-map.md`
- `docs/architecture.md`
- `docs/harness/single-agent-runbook.md`
- `docs/harness/permission-policy.md`
- `docs/harness/done-criteria.md`
- `src/support_hub/service.py`
- `src/support_hub/store.py`
- `tests/test_service.py`

## Deliverables
- failing test design
- root cause hypothesis
- fix plan
- `Progress Note`

## Constraints
- UI 層は扱わない
- public contract を変える場合は approval boundary を越える前に止まる
- verify、docs、task artifact の更新境界を先に固定する

## Acceptance Criteria
- stale read の再現条件が failing test の候補として説明できる
- root cause hypothesis が `service.py` と `store.py` のどこを見るべきか示している
- fix plan に verify、変更対象、stop condition が入っている
- `Progress Note` に再開可能な状態が残る

## Verification
`PYTHONPATH=src python -m unittest discover -s tests -v`

## Open Questions
- stale read は detached copy の扱いか、status 更新後の再取得手順か、どちらが主因か

## Out of Scope
- UI 層の実装
- unrelated な repo 再編
