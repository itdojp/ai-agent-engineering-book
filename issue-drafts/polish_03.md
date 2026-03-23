## Goal
技術精度と編集品質の最終確認を行い、reader-facing な backmatter と verify の契約ずれを減らす。

## Reader Outcome
この issue の成果により、後続の執筆または sample-repo 実装を進められる状態にする。

## Inputs
- `AGENTS.md`
- 関連する local `AGENTS.md`
- 関連 brief / docs / existing artifacts
- `manuscript/backmatter/`
- `scripts/verify-book.sh`

## Deliverables
- `checklists/repo-hygiene.md`
- `issue-drafts/`
- `scripts/verify-book.sh`


## Acceptance Criteria
- deliverables が存在する
- 関連 artifact の drift がない
- `manuscript/backmatter/00-source-notes.md` が CH01-CH12 を取りこぼすと verify で検出できる
- `checklists/repo-hygiene.md` が backmatter の drift を review できる
- verify が通る
- 残課題がある場合は明記する

## Out of Scope
- この issue に直接関係しない章や artifact の大規模な再編
- 用語定義の全面的変更
- 英語版 manuscript の本格改稿

## Verification
- `./scripts/verify-book.sh`
- `./scripts/verify-sample.sh`


## Suggested Codex Prompt
```text
Read AGENTS.md and the relevant local AGENTS.md. Read the issue body and any referenced brief or artifact. Implement only the deliverables for POLISH-03. Keep the work artifact-driven. Run the required verify commands. Return only changed files, verification results, and remaining gaps if verification failed.
```
