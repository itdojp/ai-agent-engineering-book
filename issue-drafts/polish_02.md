## Goal
cross-reference と artifact drift を解消し、repo 外への参照を除去する。

## Reader Outcome
この issue の成果により、後続の執筆または sample-repo 実装を進められる状態にする。

## Inputs
- `AGENTS.md`
- 関連する local `AGENTS.md`
- `checklists/repo-hygiene.md`
- `manuscript/part-02-context/ch06-repo-context.md`
- `manuscript/part-02-context/ch07-task-context-and-memory.md`
- `manuscript/part-02-context/ch08-skills-and-context-pack.md`
- 関連 brief / docs / existing artifacts

## Deliverables
- `checklists/repo-hygiene.md`
- `issue-drafts/polish_02.md`
- `manuscript/part-02-context/ch06-repo-context.md`
- `manuscript/part-02-context/ch07-task-context-and-memory.md`
- `manuscript/part-02-context/ch08-skills-and-context-pack.md`


## Acceptance Criteria
- chapter 本文に repo 外を指す絶対パス参照が残っていない
- `checklists/repo-hygiene.md` で absolute path と cross-reference drift を review できる
- `issue-drafts/polish_02.md` が実際の修正対象と acceptance criteria を明示している
- verify が通る
- 残課題がある場合は明記する

## Out of Scope
- この issue に直接関係しない章や artifact の大規模な再編
- 用語定義の全面的変更
- figure 追加や図版設計

## Verification
- `./scripts/verify-book.sh`
- `./scripts/verify-sample.sh`


## Suggested Codex Prompt
```text
Read AGENTS.md and the relevant local AGENTS.md. Read the issue body and any referenced brief or artifact. Implement only the deliverables for POLISH-02. Keep the work artifact-driven. Run the required verify commands. Return only changed files, verification results, and remaining gaps if verification failed.
```
