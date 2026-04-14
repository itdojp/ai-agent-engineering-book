# Evidence Bundle

UI 変更や user-visible change の検証結果を保存する場所。verification harness の一部として、review 時に「何を確認し、何が変わったか」を共有できる形で残す。

## Related Artifacts
- verify log
  - current-run の command、timestamp、結果を示すログ
- trace
  - handoff、retry、状態遷移を示す履歴
- evidence bundle
  - reviewer が確認しやすいように verify log、trace 参照、repro、画像を束ねたもの

verify log と trace は evidence bundle に含められるが、同義ではない。bundle は review-ready に整形された成果物である。

## When To Create
- UI の見た目や操作手順が変わるとき
- 再現手順を reviewer に共有しないと差分が判断しにくいとき
- 長時間タスクで verify log や trace 参照を bundle 化したいとき

## Recommended Layout
```text
artifacts/evidence/<task-id>/<timestamp>/
  summary.md
  verify.log
  repro.md
  trace.md        # 必要な場合のみ
  before.png
  after.png
```

## Minimum Contents
- `summary.md`
  - 何を変えたか
  - どの verify を回したか
  - reviewer が見るべき点
  - evidence の timestamp
- `verify.log`
  - current-run の command と要点ログ
- `repro.md`
  - before / after の確認手順
- `trace.md`
  - handoff、retry、失敗分析に必要な履歴がある場合のみ
- `before.png`, `after.png`
  - UI 変更がある場合のみ

## Freshness Rule
- evidence bundle は review 時点で current-run の verify を指している必要がある
- 過去 run の verify log を流用する場合は、再実行できない理由と影響を `summary.md` に明記する
- stale な screenshot や trace だけを残して current-run verify を省略しない

## Redaction / Privacy
- secret、credential、個人情報、社内識別子が含まれる場合は bundle 化前に除く
- reviewer に不要な raw log をそのまま共有しない
- redaction した箇所が判断に影響する場合は `summary.md` で説明する

## Notes
- backend-only の変更では screenshot が不要なことがある。その場合も `summary.md` と `verify.log` は残せる。
- bundle が不要な場合は、PR summary で不要理由を短く明記する。
