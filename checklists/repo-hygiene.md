# Repo Hygiene Checklist

## Before Merge
- stale docs を更新したか
- 参照パス切れがないか
- manuscript や docs に絶対パス参照が残っていないか
- verify script と実態がずれていないか
- `docs/glossary.md` を source of truth として表記を揃えたか
- `Prompt Contract`、`Progress Note`、`verification harness` の固有表記がぶれていないか
- approval boundary に触れる差分で、`Evidence / Approval` に承認主体と判断材料が残っているか
- `needs-human-approval` の表記が `sample-repo/docs/harness/done-criteria.md` と矛盾していないか
- verify log、trace、evidence bundle の用語を混同していないか
- review に使う evidence が current-run のものか確認したか
- redaction / privacy consideration が必要な artifact をそのまま残していないか
- 各章の `Source Notes / Further Reading` が `manuscript/backmatter/00-source-notes.md` と矛盾していないか
- `manuscript/backmatter/00-source-notes.md` が CH01-CH12 を取りこぼしていないか
- 出力契約の報告項目が `Goal`、`Scope and Non-goals`、`Changed Files`、`Verification`、`Evidence / Approval`、`Remaining Gaps` に揃っているか
- local verify、CI、evidence の用語が chapter と checklist で矛盾していないか

## Weekly Cleanup
- orphaned task brief がないか
- `Progress Note` が古い状態で残っていないか
- `AI slop` に当たる stale docs や未使用 artifact が積み上がっていないか
- trace や evidence 参照が失効したまま残っていないか
- 同じ説明を別名で持つ artifact が増えていないか
- `repo hygiene` と `entropy cleanup` の担当と cadence が曖昧になっていないか
- source notes、読書案内、索引 seed のどれかだけ更新されて backmatter 内 drift が起きていないか

## Escalate When
- source of truth が衝突している
- stale artifact が複数の chapter / task に波及している
- cleanup だけでは直らず、構成再編が必要
