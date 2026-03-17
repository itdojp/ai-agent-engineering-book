# Verification Checklist

## Before Edit
- どの behavior を守るか、spec / acceptance criteria / task brief で確認したか
- failing test を先に追加または更新すべきか判断したか
- local verify command を先に確定したか

## During Change
- diff を最小の work package に保ったか
- docs / brief / progress note の更新漏れがないか
- verify failure を failure mode ごとに分類したか

## Before Review
- local verify を回したか
- CI に同じ合格ラインを反映できているか
- UI または user-visible change なら evidence bundle を保存したか
- evidence が不要な場合、その理由を説明できるか
- human approval が必要な点を明示したか
