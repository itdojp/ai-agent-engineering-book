# Prompt Contract Review Checklist

- Objective が 1 文で定義されている
- Inputs が artifact 名または情報源の種類まで書かれている
- Constraints が曖昧語ではなく observable な条件で書かれている
- Forbidden Actions があり、勝手な拡張や危険な近道を防いでいる
- Completion Criteria が verify 可能で、完了判定を主観に依存していない
- Output Format があり、作業結果の報告粒度と canonical な項目名 (`Changed Files`、`Verification`、`Remaining Gaps`) が固定されている
- 不足情報がある場合の扱いが明示されている
- out of scope が分かる
- 必要な artifact が参照されている
