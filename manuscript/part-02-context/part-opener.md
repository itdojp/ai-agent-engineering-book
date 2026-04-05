# Part II Context Engineering

Prompt Contract が強くても、AIエージェントに見せる情報が古い、足りない、重すぎる、混ざっているのいずれかなら、作業は途中で壊れる。Context Engineering の仕事は、AIエージェントに渡す判断材料を分解し、優先順位と鮮度を設計することである。

## この Part の役割

この Part が扱うのは主に忘却である。repo 全体の前提、今回の task の仕様、前セッションの `Progress Note`、再開時に必要な restart packet、再利用したい workflow を区別しなければ、AIエージェントは前提を落とし、summary drift を起こし、同じ説明を別 artifact に重複させる。

Context Engineering では次の順に積み上げる。

1. context の種類と budget を分ける
2. repo context で永続コンテキストの入口を作る
3. task brief と Session Memory で今回の作業と現在位置を固定する
4. skill と context pack で再利用可能な作業単位にする

## この Part で増える artifact

この Part を読み終えると、少なくとも次の artifact が増える。

- context model
- repo-map
- architecture / coding standards
- task brief
- Progress Note
- restart packet
- context pack
- SKILL.md

ここで重要なのは、情報を増やすことではない。source of truth を守りながら、approval pending や再開時に壊れた context を残さないことだ。

## 章の見取り図

- CH05: Prompt と Context の境界を定義する
- CH06: repo 全体の永続コンテキストを設計する
- CH07: issue を task brief、Session Memory、restart packet に変換する
- CH08: skill と context pack を再利用する

この Part は、単に docs を増やす Part ではない。Prompt Engineering で定義した契約を、途中で壊さずに持ち運ぶ Part である。

## 読み終わりの到達点

この Part を終えた時点で、読者は「何を見せれば AIエージェントが壊れにくくなるか」を repo、task、session の単位で設計できるようになる。加えて、summary をどこで止め、どこで live context を取り直すかも判断できるようになる。次の Part では、その前提をもとに、verify、retry、review、handoff を閉じる Harness Engineering を扱う。
