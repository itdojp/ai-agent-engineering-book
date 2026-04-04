# Coding Standards

## Code Changes

- Python 標準ライブラリ中心で維持する
- public behavior の変更には test を必須とする
- `service.py` の挙動変更は最小差分を優先する
- silent fallback を増やさない

## Docs and Task Artifacts

- docstring より task brief / architecture docs を優先する
- 仕様変更時は product spec、acceptance criteria、ADR を同時更新する
- 中断や handoff が発生する変更では `Progress Note` を更新する
- TODO を残す場合は task brief または issue と結びつける

## Scope Guard

- issue にない API 拡張をしない
- 無関係な整理や rename を混ぜない
- verify を実行せずに done と判断しない
