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

## Production Gate（該当する場合）

### Before Merge / Production-ready Plan
- target environmentと公開URLを記録したか
- merge後のSHA/versionの記録場所とproductionで照合するsemantic markerを決めたか
- deploy owner、production confirmation owner、必要な承認者を決めたか
- root smoke、代表route、期待HTTP status / content markerを決めたか
- metricのbaseline、threshold、window、source、ownerを決めたか
- halt条件、rollback手段、restart条件、evidence locationを決めたか

### After Merge / Production Evidence
- 対象SHA/versionとdeployment/workflow runが一致しているか
- 対象runが後続runにcancelされた場合、後続SHAが対象changeを含むこと、両run URL、後続deploymentの確認結果を `Superseded` evidenceとして残したか
- deployment approval、deployment success、production confirmationを別々に記録したか
- rootと代表routeのHTTP status、semantic markerを確認したか
- metricを定義したwindowで確認したか、対象外なら `N/A` と理由を残したか
- owner、UTC timestamp、観測値、evidence URLをPRまたはlinked Issueへ記録したか
- rollback後は新しいmain SHAのdeployment、HTTP、marker、metricを再確認したか

## Stop Instead Of Merge
- 現在の diff と無関係な verify failure が残っている
- evidence が必要な変更なのに current run の証跡がない
- CI job が local verify とずれており、差分説明ができない
- approval が必要な変更を、承認なしで進めている
- review comment / suggestion / unresolved thread が残っているのに merge しようとしている
- model/runtime profile が変わったのに eval や smoke check を再実行していない
- production-ready planが未記入なのにproductionへ影響する変更をmergeしようとしている
- deploymentがfailed / unknown、SHAまたはmarkerが不一致、代表routeが異常、metricがthresholdを超えているのに完了扱いにしようとしている
- deployment successまたはapprovalだけでproduction confirmationを代替している
- `cancelled`を、後続SHAの包含関係とproduction確認なしに `Superseded` または成功として扱っている
