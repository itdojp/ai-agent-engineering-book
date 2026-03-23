# English Manuscript

This directory holds the English manuscript counterpart for the book. The English edition is maintained in parity with the Japanese manuscript so translation and editorial work can proceed issue by issue without breaking chapter, appendix, or artifact alignment.

## Scope

- Mirror the Japanese front matter, chapter, appendix, backmatter, and figure layout
- Keep one English brief for every Japanese brief
- Keep one English counterpart for every Japanese reader-facing artifact
- Keep the English support-artifact surfaces under `docs/en/`, `prompts/en/`, `checklists/en/`, `templates/en/`, and `artifacts/en/` aligned with the Japanese source
- Track parity status in `manuscript-en/STATUS.md`

## Directory Layout

```text
manuscript-en/
  briefs/          # English briefs mirrored from manuscript/briefs
  figures/         # English figure plan and Mermaid sources
  front-matter/    # English introduction and reading guide
  part-00/         # Chapter 1
  part-01-prompt/  # Chapters 2-4
  part-02-context/ # Chapters 5-8
  part-03-harness/ # Chapters 9-12
  backmatter/      # English source notes, reading guide, index seed, figure/table policy
  appendices/      # Appendix A-D
```

## Parity Policy

1. The Japanese manuscript remains the source for structure and artifact references.
2. The English manuscript must preserve the same chapter ids, appendix ids, and referenced artifacts.
3. Each English file should identify its Japanese source in `## Parity Notes` when the file contract requires it.
4. When the Japanese manuscript or a reader-facing support artifact changes structure or artifacts, the English counterpart and `manuscript-en/STATUS.md` must be updated in the same issue.

## Editing Workflow

1. Read the matching Japanese brief and chapter.
2. Update the English brief first if scope changes.
3. Update the English counterpart, draft, or reader-entry artifact, including support artifacts when the chapter depends on them.
4. Update `manuscript-en/STATUS.md` if parity status changes.
5. Run `./scripts/verify-book.sh`.
