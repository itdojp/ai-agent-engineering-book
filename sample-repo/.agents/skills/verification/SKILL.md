# Verification

## Purpose
support-hub の変更に対する検証を標準化する。

## Use When
- code または docs を変更した後
- handoff 前に verify 証跡を残したいとき

## Steps
1. impacted tests を確認する
2. `python -m unittest discover -s tests -v` を実行する
3. docs drift がないか確認する
4. `Progress Note` を更新する

## Output Contract
- 実行した verify command
- pass / fail
- docs drift の有無
- `Progress Note` へ残す要点
