# Figure Sources

This directory holds the reader-facing figure sources for the English edition. Keep the source of truth in text-diffable `mermaid` `.mmd` files, and manage captions, suggested placement, and reader value in `figure-plan.md`.

## Source Of Truth

- `figure-plan.md`
  The source of truth for figure ID, chapter mapping, caption, suggested placement, reader value, and source file
- `fig-*.mmd`
  The source files for the figures themselves

## Update Policy

- When the core idea of a chapter changes, update the matching `.mmd` file and `figure-plan.md` in the same issue or PR
- Treat final figure numbers and production SVG or PNG output as derived artifacts; keep `.mmd` as the repo source of truth
- Keep one figure focused on one main message, and avoid packing multiple decision axes into the same image
- Keep figure IDs aligned with the Japanese edition so editorial comparison stays stable across languages

## Print / Ebook Rule

- Keep the node count around seven when possible
- Keep labels short and avoid long text inside a single box
- Write each caption as one sentence that states what the reader should understand from the figure
