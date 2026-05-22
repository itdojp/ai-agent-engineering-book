# Verification Checklist

## Before Edit
- どの behavior を守るか、spec / acceptance criteria / task brief で確認したか
- failing test を先に追加または更新すべきか判断したか
- local verify command と、対応する CI job を先に確定したか
- evidence bundle が必要か、不要ならその理由を説明できるか
- モデル名、API、SDK、vendor 固有機能を扱う場合、model/runtime profile と公式 docs 確認日を残す場所を決めたか
- AI / 外部サービスへ issue、PR、log、eval case、trace、evidence を投入する可能性がある場合、分類、redaction、provider 条件、approval 要否を確認したか
- 参照している trace や過去 log が current-run verify の代わりになっていないか

## During Change
- diff を最小の work package に保ったか
- docs / brief / `Progress Note` の更新漏れがないか
- verify failure を failure mode ごとに分類したか
- 実行した verify command と pass / fail を current run の情報として記録したか
- 長時間タスクなら trace に残すべき handoff / retry が整理されているか
- trace を残す場合、task / work-package id、run timestamp または run id、owner / handoff、retry / restart reason を残したか

## Before Review
- local verify を回したか
- verify log に command、timestamp、pass / fail が残っているか
- CI に同じ合格ラインを反映できているか、差分があるなら説明できるか
- UI または user-visible change なら evidence bundle を保存したか
- evidence が current-run の結果を指しているか
- `Changed Files`、`Verification`、`Remaining Gaps` が current diff と一致しているか
- trace を review で参照する場合、verify reference と evidence linkage が明示されているか
- trace や screenshot に redaction / privacy consideration が必要か確認したか
- model/runtime profile が変わった場合、eval または smoke check を再実行したか
- AI / 外部サービス投入がある場合、投入データ、redaction、provider 条件、approval 判断を `Evidence / Approval` に残したか
- evidence が不要な場合、その理由を説明できるか
- human approval が必要な点を明示したか
- review body、inline comment、suggestion を確認し、未解決 review thread が 0 であることを確認する段取りがあるか
- skipped check がある場合、その理由を `Remaining Gaps` に残したか

## Stop Instead Of Merge
- 現在の diff と無関係な verify failure が残っている
- evidence が必要な変更なのに current run の証跡がない
- CI job が local verify とずれており、差分説明ができない
- approval が必要な変更を、承認なしで進めている
- review comment / suggestion / unresolved thread が残っているのに merge しようとしている
- model/runtime profile が変わったのに eval や smoke check を再実行していない
