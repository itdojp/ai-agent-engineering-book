# Prompt Contract Review Checklist

- Objective が 1 文で定義されている
- Inputs が artifact 名または情報源の種類まで書かれている
- Constraints が曖昧語ではなく observable な条件で書かれている
- Tool Contract があり、許可された tool / command / external access が明示されている
- Approval Gate があり、human approval が必要な操作が明示されている
- Forbidden Actions があり、勝手な拡張や危険な近道を防いでいる
- Completion Criteria が verify 可能で、完了判定を主観に依存していない
- Refusal / Stop Conditions があり、止まるべき場面を定義している
- Output Schema と output version があり、作業結果の報告粒度と互換性が固定されている
- Output Format があり、canonical な項目名として少なくとも `Changed Files`、`Verification`、`Remaining Gaps` が固定され、feature では `Implemented Scope`、bugfix では `Root Cause` など契約種別ごとの必須セクションが Output Schema と矛盾なく定義されている
- 不足情報がある場合の扱いが明示されている
- out of scope が分かる
- 必要な artifact が参照されている
