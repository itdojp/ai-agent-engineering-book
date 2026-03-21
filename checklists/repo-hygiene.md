# Repo Hygiene Checklist

## Before Merge
- stale docs を更新したか
- 参照パス切れがないか
- manuscript や docs に絶対パス参照が残っていないか
- verify script と実態がずれていないか
- `docs/glossary.md` を source of truth として表記を揃えたか
- `Prompt Contract`、`Progress Note`、`verification harness` の固有表記がぶれていないか

## Weekly Cleanup
- orphaned task brief がないか
- `Progress Note` が古い状態で残っていないか
- `AI slop` に当たる stale docs や未使用 artifact が積み上がっていないか
- 同じ説明を別名で持つ artifact が増えていないか
- `repo hygiene` と `entropy cleanup` の担当と cadence が曖昧になっていないか

## Escalate When
- source of truth が衝突している
- stale artifact が複数の chapter / task に波及している
- cleanup だけでは直らず、構成再編が必要
