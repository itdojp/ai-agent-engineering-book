# Done Criteria

## Core
- task brief の Goal と Acceptance Criteria を満たす
- 変更ファイルが current issue / work package の範囲に収まっている
- code、docs、tests、task artifact の間に drift がない
- `./scripts/verify-sample.sh` が current session で通っている
- `Changed Files`、`Verification`、`Remaining Gaps` を報告できる

## Approval Boundary Check
- approval が必要な変更を、承認なしで実行していない
- approval 待ちの項目がある場合、exit state を `done` にしない

## Evidence Minimum
- 実行した verify command をそのまま言える
- pass / fail と、未実行の check があればその理由を言える
- verify が古い実行結果ではなく current run に紐づいている

## Bugfix Addendum
- failing behavior を test で再現した、または既存 test で回帰 guard を確認した
- Root Cause を 1 段落で説明できる
- 不要な public interface 変更を入れていない

## Feature Or Docs Addendum
- spec、acceptance criteria、design doc の差分が現行挙動と一致している
- non-goals を scope に混ぜていない

## Exit States
- `done`: Core、Approval Boundary Check、Evidence Minimum と task 種別の追加条件を満たす
- `blocked`: 入力不足、矛盾する artifact、未解決の verify failure がある
- `needs-human-approval`: permission policy の approval 条件に入った
