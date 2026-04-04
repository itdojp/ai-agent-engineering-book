# Verification Checklist

## Before Edit
- どの behavior を守るか、spec / acceptance criteria / task brief で確認したか
- failing test を先に追加または更新すべきか判断したか
- local verify command と、対応する CI job を先に確定したか
- evidence bundle が必要か、不要ならその理由を説明できるか

## During Change
- diff を最小の work package に保ったか
- docs / brief / progress note の更新漏れがないか
- verify failure を failure mode ごとに分類したか
- 実行した verify command と pass / fail を current run の情報として記録したか

## Before Review
- local verify を回したか
- CI に同じ合格ラインを反映できているか、差分があるなら説明できるか
- UI または user-visible change なら evidence bundle を保存したか
- `Changed Files`、`Verification`、`Remaining Gaps` が current diff と一致しているか
- human approval が必要な点を明示したか
- skipped check がある場合、その理由を `Remaining Gaps` に残したか

## Stop Instead Of Merge
- 現在の diff と無関係な verify failure が残っている
- evidence が必要な変更なのに current run の証跡がない
- CI job が local verify とずれており、差分説明ができない
- approval が必要な変更を、承認なしで進めている
