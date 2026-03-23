## Goal
`docs/glossary.md` を source of truth として、terminology drift を減らす。

## Reader Outcome
この issue の成果により、後続の執筆または sample-repo 実装を進められる状態にする。

## Inputs
- `AGENTS.md`
- 関連する local `AGENTS.md`
- `docs/glossary.md`
- `checklists/repo-hygiene.md`
- 関連 brief / docs / existing artifacts

## Deliverables
- `docs/glossary.md`
- `checklists/repo-hygiene.md`
- `issue-drafts/polish_01.md`


## Acceptance Criteria
- `docs/glossary.md` に主要用語と表記ルールが揃っている
- `checklists/repo-hygiene.md` が `docs/glossary.md` を参照して terminology drift を review できる
- `issue-drafts/polish_01.md` の wording が `docs/glossary.md` と矛盾しない
- verify が通る
- 残課題がある場合は明記する

## Out of Scope
- この issue に直接関係しない章や artifact の大規模な再編
- 用語定義の全面的変更
- cross-reference 切れや absolute path 修正

## Verification
- `./scripts/verify-book.sh`
- `./scripts/verify-sample.sh`


## Suggested Codex Prompt
```text
Read AGENTS.md and the relevant local AGENTS.md. Read the issue body and any referenced brief or artifact. Implement only the deliverables for POLISH-01. Keep the work artifact-driven. Run the required verify commands. Return only changed files, verification results, and remaining gaps if verification failed.
```
