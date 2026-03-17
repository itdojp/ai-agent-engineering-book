# sample-repo/AGENTS.md

## Scope
support-hub サンプル実装向けの instructions。

## Code Rules
- まず `docs/repo-map.md` と `docs/architecture.md` を読む
- public API を壊す場合は brief と docs を更新する
- test を追加または更新してから本体を変える
- `tasks/` の task brief / progress note を更新する
- 変更が docs に影響するなら同時に更新する

## Verification
- `python -m unittest discover -s tests -v`
- 変更が docs のみであっても path の整合性を確認する
- verify に失敗したら failure mode を明記する

## Domain Constraints
- `Ticket.status` は `open`, `in_progress`, `resolved` のいずれか
- search は title / description / tags を対象とする
- history は監査ログの前身であり、消さない
