# 安全優先トラブルシューティングフロー

AI エージェントの作業が期待どおりに進まない場合は、速く直すことよりも、影響を広げずに原因と判断材料を残すことを優先する。この flow は Prompt、Context、Harness のどこで失敗が起きているかを、最小の安全な操作で切り分けるための reader-facing な手順である。

## 0. 直ちに停止して保護する

次のいずれかに当たる場合は、再試行や追加操作をせずに停止する。

- production、顧客データ、認証情報、外部公開、課金、破壊的な command に影響する可能性がある
- Permission Policy、Tool Contract、Approval Gate の境界が不明確である
- 失敗の結果として、想定外のファイル変更、外部送信、権限昇格、データ欠損が観測された

停止は失敗ではない。安全境界を保ったまま、次の担当者が判断できる状態にするための操作である。

## 1. 症状を記録する

最初に、期待した behavior と実際の症状を分けて記録する。task、run timestamp または run ID、入力、実行 command、error、変更されたファイル、外部操作の有無を残す。過去の log や trace を current-run verify の代替にしない。

## 2. 再現を最小化する

同じ症状を、読み取り専用または隔離された最小入力で再現する。再現しない場合は、入力、環境、権限、タイミングなど、元の run と異なる条件を明示する。再現のために production データや承認済みでない外部操作を使わない。

## 3. 最小安全確認を行う

変更を加える前に、対象 repo、branch、working tree、許可された tool / command、network access、approval の要否を確認する。安全な確認で scope を確定できない場合は、原因仮説を増やさずに停止する。

## 4. Prompt を切り分ける

Objective、Inputs、Constraints、Tool Contract、Completion Criteria、Refusal / Stop Conditions が observable な形でそろっているかを確認する。曖昧な要求、競合する制約、欠落した出力契約は Prompt 側の failure mode として扱う。Prompt を変更する場合も、最小の再現入力で expected output を先に定義する。

## 5. Context を切り分ける

必要な artifact、対象ファイル、用語、既存の decision、current state が context に入っているかを確認する。古い情報、無関係な大量入力、JA/EN counterpart の取り違え、絶対パスなどは Context 側の failure mode である。context を追加する前に、必要な source of truth を一つずつ特定する。

## 6. Harness を切り分ける

実行順序、tool permission、timeout、retry、verify command、CI との差分、evidence の保存を確認する。Prompt と Context が正しくても、Harness の境界や verify が欠けていれば安全に完了したとは判定しない。Harness の失敗は、再試行の回数ではなく command と結果で切り分ける。

## 7. 停止とエスカレーションを判断する

次の場合は停止し、適切な owner または approver へエスカレーションする。

- 安全境界、Permission Policy、Approval Gate を越える判断が必要である
- 最小再現で data loss、security、privacy、外部影響の可能性が残る
- Prompt、Context、Harness のいずれにも単独で帰属できず、source of truth が衝突している
- current-run の verify が実行できない、または failure mode を説明できない

エスカレーションには、症状、再現条件、停止した理由、試した最小安全確認、必要な判断を添える。

## 8. 証跡を残す

Evidence / Approval には、実行 command、run timestamp または run ID、pass / fail、関連する diff、trace、redaction の要否、承認主体と判断材料を残す。証跡は次の再試行、review、handoff で同じ危険な操作を繰り返さないために必要である。
