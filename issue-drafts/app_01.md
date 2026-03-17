## Goal
Appendix A-D の原稿を整備する。

## Reader Outcome
この issue の成果により、後続の執筆または sample-repo 実装を進められる状態にする。

## Inputs
- `AGENTS.md`
- 関連する local `AGENTS.md`
- 関連 brief / docs / existing artifacts

## Deliverables
- `manuscript/appendices/`
- `templates/`
- `docs/glossary.md`


## Acceptance Criteria
- deliverables が存在する
- 関連 artifact の drift がない
- verify が通る
- 残課題がある場合は明記する

## Out of Scope
- この issue に直接関係しない章や artifact の大規模な再編
- 用語定義の全面的変更

## Verification
- `./scripts/verify-book.sh`


## Suggested Codex Prompt
```text
Read AGENTS.md and the relevant local AGENTS.md. Read the issue body and any referenced brief or artifact. Implement only the deliverables for APP-01. Keep the work artifact-driven. Run the required verify commands. Return only changed files, verification results, and remaining gaps if verification failed.
```
