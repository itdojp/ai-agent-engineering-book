# Figure Sources

このディレクトリは、本書の reader-facing 図版 source を置く。正本は text diff しやすい `mermaid` の `.mmd` とし、caption、挿入候補、読者価値は `figure-plan.md` で管理する。

## Source Of Truth
- `figure-plan.md`
  図 ID、対象章、caption、挿入候補、読者価値の正本
- `fig-*.mmd`
  図そのものの source

## 更新方針
- 章の中心概念が変わったら、対応する `.mmd` と `figure-plan.md` を同じ issue / PR で更新する
- final の図番号や組版用の SVG / PNG は派生物とし、repo では `.mmd` を正本にする
- 1 図 = 1 主メッセージを守る。複数の判断軸を 1 枚に詰め込みすぎない

## Print / Ebook Rule
- node 数は原則 7 個前後に抑える
- label は短くし、1 つの box に長文を入れない
- caption は「図から何を理解してほしいか」を 1 文で言い切る
