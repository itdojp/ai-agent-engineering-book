# Done Criteria

## Core
- task brief の Goal と Acceptance Criteria を満たす
- 変更ファイルが current issue / work package の範囲に収まっている
- code、docs、tests、task artifact の間に drift がない
- `./scripts/verify-sample.sh` が通っている
- `Changed Files`、`Verification`、`Remaining Gaps` を報告できる

## Bugfix Addendum
- failing behavior を test で再現した、または既存 test で回帰 guard を確認した
- Root Cause を 1 段落で説明できる
- 不要な public interface 変更を入れていない

## Feature Or Docs Addendum
- spec、acceptance criteria、design doc の差分が現行挙動と一致している
- non-goals を scope に混ぜていない

## Exit States
- `done`: Core と task 種別の追加条件を満たす
- `blocked`: 入力不足、矛盾する artifact、未解決の verify failure がある
- `needs-human-approval`: permission policy の approval 条件に入った
