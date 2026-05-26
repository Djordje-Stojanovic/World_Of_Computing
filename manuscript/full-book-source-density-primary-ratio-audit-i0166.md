# Full-Book Source-Density And Primary-Ratio Audit

Pass I-0166 audits the canonical 24-chapter primary-file map in `data/full_book_timeline_integrity_audit_i0149.tsv`, not every sidecar manuscript file. That distinction matters: the primary map currently measures 98,529 words, while broader loop-ledger manuscript counts have exceeded 100,000. The final book should not claim the hard word-count invariant from sidecar mass; the live spine needs either more integrated prose or a final map update that proves which files are actually part of the book.

## Findings

- Six chapters meet the 150-250 words-per-source target by the current source-ID heuristic: Chapters 1, 7, 9, 17, 22, and 23.
- Seven chapters are thin but repairable: Chapters 12, 13, 14, 18, 19, 20, and 21.
- Eleven chapters are critical density risks: Chapters 2, 3, 4, 5, 6, 8, 10, 11, 15, 16, and 24.
- The source mix is strongly primary-source weighted, which is good for technical authority, but it also means several chapters lack independent/contextual secondary corroboration where market, adoption, infrastructure, or reception claims could overreach.
- Quote permission remains a local-work problem: alignment, ChatGPT reception, GTC slides, rankings, and vendor product pages need row-level quote or paraphrase permissions before pull quotes, source-excerpt cards, or long epigraph-like passages are typeset.

## Repairs

The highest-value repair is not adding a bibliography dump. It is moving source IDs and claim blockers to the exact factual sections that can misuse them. The biggest weak spots are early technical chapters with apparatus-level citations, Chapter 8's cloud-business framing, Chapter 11's gap-lane material, Chapter 15/16 physical and roadmap claims, and Chapter 24's source-invisible synthesis.

The section audit in `data/full_book_weak_source_sections_i0166.tsv` should drive future prose passes: cite or recast the named weak sections before adding more decorative visuals, marketing copy, or final-layout polish.

## Gate

This pass improves the champion because it converts an invisible credibility problem into a chapter-by-chapter repair board. It does not resolve source density, quote permissions, primary/secondary balance, the 24-file map conflict, or the final word-count invariant.
