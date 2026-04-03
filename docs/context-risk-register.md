# Context Risk Register

| Risk | Signal | Failure Mode | Mitigation |
|---|---|---|---|
| Stale docs | docs と tests の主張が食い違う | 古い仕様を正として実装する | artifact-consistency pass を定期実行し、verify 時に docs drift を確認する |
| Summary drift | progress note が事実より解釈を増やす | handoff 後に誤った前提で再開する | `Decided`, `Open Questions`, `Next Step` を分離し、verify 後にだけ更新する |
| Instruction bloat | `AGENTS.md` が長く、検索起点が埋もれる | 重要な制約が読まれず、勝手な推測が増える | instruction を root / local / skill に分割し、詳細は docs へ逃がす |
| Context poisoning | 未検証の仮説が progress note や context pack に残る | 誤答や破壊が連鎖する | acceptance criteria と最新 verify を優先し、仮説は `Open Questions` に隔離する |
| Hidden done criteria | 完了条件が issue の会話にしかない | stopping early が起きる | task brief に done と verification を明記する |
| Tool spam | 長いログをそのまま常駐させる | live context が stale context を押し流す | ログは要点のみ残し、全文は evidence として分離する |
| Secret leakage | progress note や context pack に token / credential / 個人情報が残る | credential 漏洩、危険な再利用、監査不能 | 値ではなく参照名だけを残し、secret scan と redact を必須にする |
| Resume drift | progress note を読んだだけで再開し、live context を再取得しない | 古い verify 結果や stale state を前提に作業を続ける | resume 時に verify / status command を再実行し、summary を source of truth にしない |
