# Compression Pass - I-0272

Pass I-0272 removes low-value apparatus paragraphs from the reader-facing full draft.

## Result

- Word count before: 102685.
- Word count after: 101678.
- Net words removed: 1007.
- Cut rows recorded: 15.

## What Was Cut

The pass removes `Source boundary:` paragraphs plus a small number of remaining editorial/audit-work notes. The evidence is not discarded: source and claim controls remain in `claims.tsv`, `sources.tsv`, `data/final_endnotes_i0267.tsv`, `data/bibliography_i0267.tsv`, and the chapter-level audit files.

## Guardrail

The pass intentionally stops above 101,000 words so later caption/source-note and print-layout work has room without crossing the 100,000-word floor.
