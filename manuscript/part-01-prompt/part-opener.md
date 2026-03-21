# Part I Prompt Engineering

Prompt Engineering の仕事は、AIエージェントに何をしてほしいかを上手に頼むことではない。単一タスクの境界を契約として固定し、誤答を減らすことである。この Part では、曖昧な依頼をそのまま実装に流さず、Prompt Contract、spec、acceptance criteria、prompt eval へ変換する。

## この Part の役割

この Part が扱うのは、仕事の入口で起きる失敗である。対象は主に誤答だ。要件が曖昧なまま、目的と制約が混ざったまま、完了条件が抜けたままでは、AIエージェントはそれらしく動いても仕事を外す。

Prompt Engineering では次の 3 段階を踏む。

1. Prompt Contract で単一タスクの入出力契約を固定する
2. ChatGPT を使って曖昧要求を spec と設計判断へ変換する
3. prompt を eval case と rubric で評価し、偶然の成功を排除する

## この Part で増える artifact

この Part を読み終えると、少なくとも次の artifact が増える。

- Prompt Contract
- product spec
- acceptance criteria
- ADR
- prompt eval case
- prompt rubric

この時点では、まだ長時間タスクの memory や verify の運用までは扱わない。まずは単一タスクを外さない土台を作る。

## 章の見取り図

- CH02: prompt を契約として設計する
- CH03: ChatGPT で要求と設計を固める
- CH04: prompt を評価し、回帰を検知する

3 章の役割分担は明確である。CH02 が契約、CH03 が要求の収束、CH04 が評価である。どれか 1 つだけでは弱い。契約だけでは要求が曖昧なままであり、仕様だけでは実行境界がぶれ、評価がなければ改善が偶然に依存する。

## 読み終わりの到達点

この Part を終えた時点で、読者は「とりあえず良さそうな prompt」から離れ、単一タスクを実装準備ができた artifact に変換できる状態になる。次の Part では、その契約を長時間の作業に耐えさせるための Context Engineering を扱う。
