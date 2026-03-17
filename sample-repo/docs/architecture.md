# Architecture

support-hub は、小さな Python repo を題材に artifact-driven な作業を説明するための最小構成である。

## Layers
1. `models.py`
   - 純粋なドメインルール
   - `Ticket.update_status` などの不変条件を保持する
2. `store.py`
   - 永続化の抽象を最小限で提供する
   - read / write で copy を返し、共有参照の事故を避ける
3. `service.py`
   - ユースケースの入口
   - filter、status update、search などの application behavior を集約する
4. `tests/`
   - 振る舞い検証
   - public behavior の回帰 guard として扱う

## Design Notes
- 例示用 repo のため、外部依存は極力減らす
- 変更は service layer 経由を原則とする
- 機能追加時は docs / tests / task artifacts を同時更新する

## Change Rules
- `models.py` を変える前に、domain constraint を docs で確認する
- `service.py` の挙動変更時は関連する acceptance criteria と tests を先に確認する
- repo 構造の説明は `docs/repo-map.md` に置き、設計理由はこの文書に置く

## Search-specific Note
`FEATURE-001` の検索は `service.py` 内の in-memory 実装で扱う。外部検索 abstraction は将来の review trigger とし、現在の repo では導入しない。
