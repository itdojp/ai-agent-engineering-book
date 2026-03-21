# Part III Harness Engineering

Prompt と Context が整っても、AIエージェントはまだ失敗する。verify 前に止まり、権限境界を越え、同じ失敗を盲目的に繰り返し、長時間タスクで state を失うからである。Harness Engineering の仕事は、実行境界、検証、再試行、再開、運用を設計して、仕事を最後まで閉じることにある。

## この Part の役割

この Part が扱うのは主に破壊と停止である。単一 session の実行手順、verification harness、long-running task の restart、チーム運用の review budget まで含めて設計しなければ、AIエージェントは「途中まで進んだ差分」を大量に作るだけで終わる。

Harness Engineering では次の順に積み上げる。

1. single-agent harness で開始条件、権限、done criteria を固定する
2. verification harness で test、CI、evidence、approval をまとめる
3. long-running task と multi-agent を restart 可能な形に分解する
4. operating model でチーム運用へ載せる

## この Part で増える artifact

この Part を読み終えると、少なくとも次の artifact が増える。

- runbook
- permission policy
- done criteria
- verification checklist
- evidence bundle
- restart protocol
- feature list
- operating model
- metrics

この Part の狙いは、AIエージェントを速く動かすことではない。壊れずに、止まりどころを持って、review-ready な形で仕事を閉じることにある。

## 章の見取り図

- CH09: single-agent harness の基本を定義する
- CH10: verification harness を作る
- CH11: long-running task と multi-agent を扱う
- CH12: operating model と組織導入を扱う

前半 2 章が execution と verification、後半 2 章が restart と運用である。ここまで来て初めて、Prompt と Context の設計が、実務で閉じた作業に変わる。

## 読み終わりの到達点

この Part を終えた時点で、読者は AIエージェントに「仕事を始めさせる」だけでなく、「verify させ、止まるべきところで止め、handoff 可能な形で終わらせる」設計を説明できるようになる。付録では、そのためのテンプレートと用語を再参照できる形でまとめる。
