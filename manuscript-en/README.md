# English Manuscript Scaffold

This directory holds the English manuscript scaffold for the book. Its purpose is not to replace the Japanese manuscript immediately. Its purpose is to keep the English edition structurally aligned so translation and editorial work can proceed issue by issue.

## Scope

- Mirror the Japanese chapter and appendix layout
- Keep one English brief for every Japanese brief
- Keep one English skeleton for every Japanese chapter and appendix
- Track parity status in `manuscript-en/STATUS.md`

## Directory Layout

```text
manuscript-en/
  briefs/          # English briefs mirrored from manuscript/briefs
  part-00/         # Chapter 1
  part-01-prompt/  # Chapters 2-4
  part-02-context/ # Chapters 5-8
  part-03-harness/ # Chapters 9-12
  backmatter/      # English source notes, reading guide, index seed, figure/table policy
  appendices/      # Appendix A-D
```

## Parity Policy

1. The Japanese manuscript remains the source for structure and artifact references.
2. The English scaffold must preserve the same chapter ids, appendix ids, and referenced artifacts.
3. Each English file should identify its Japanese source in `## Parity Notes`.
4. Full English prose can be added later, but the scaffold must stay structurally complete.

## Editing Workflow

1. Read the matching Japanese brief and chapter.
2. Update the English brief first if scope changes.
3. Update the English skeleton or draft.
4. Update `manuscript-en/STATUS.md` if parity status changes.
5. Run `./scripts/verify-book.sh`.
