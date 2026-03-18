# Evidence Bundle

UI 変更や user-visible change の検証結果を保存する場所。verification harness の一部として、review 時に「何を確認し、何が変わったか」を共有できる形で残す。

## When To Create
- UI の見た目や操作手順が変わるとき
- 再現手順を reviewer に共有しないと差分が判断しにくいとき
- 長時間タスクで verify log や review note を bundle 化したいとき

## Recommended Layout
```text
artifacts/evidence/<task-id>/<timestamp>/
  summary.md
  verify.log
  repro.md
  before.png
  after.png
```

## Minimum Contents
- `summary.md`
  - 何を変えたか
  - どの verify を回したか
  - reviewer が見るべき点
- `verify.log`
  - 実行した command と要点ログ
- `repro.md`
  - before / after の確認手順
- `before.png`, `after.png`
  - UI 変更がある場合のみ

## Notes
- backend-only の変更では screenshot が不要なことがある。その場合も `summary.md` と `verify.log` は残せる。
- bundle が不要な場合は、PR summary で不要理由を短く明記する。
