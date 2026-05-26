# Full-Draft Word-Count and Gap Audit I-0239

Status: promoted book-QA audit.

## Executive Read

The assembled source draft now measures 102196 words across the 24 canonical chapter rows when Chapter 12 supplemental Anthropic/Claude material is counted. That clears the hard 100,000-120,000 word invariant, but only narrowly and with a structural caveat: the primary-only spine is 98285 words, so the book falls below the floor if the Anthropic/Claude supplemental section is removed or moved out of the main draft without replacement.

This pass therefore changes the status from below-floor to conditionally in-range. It does not authorize padding. The next writing work should repair balance: give the ending more force, resolve the Chapter 12 compound length, and add sourced scene/mechanism texture to thin chapters rather than inflating the manuscript.

## Measurements

- Primary-only canonical source words: 98285
- Supplemental source words currently retained in assembly: 3911
- Assembled canonical source words: 102196
- Generated Markdown total including front matter, assembly notes, and figure placeholders: 107047
- Hard target: >100,000 and <120,000 source words; assembled source status: pass
- Critical-thin chapters below 3,500 words: 1
- Thin chapters below the 4,200-word planning band: 16
- Target-band chapters, 4,200-4,800 words: 1
- Long-acceptable chapters, 4,801-5,200 words: 3
- Overlong or compound-review chapters above 5,200 words: 3

## Highest-Priority Actions

- CH24 needs a true ending expansion, not only a bookkeeping close.
- CH12 needs a structural decision: trim/move Anthropic/Claude sidecar material or explicitly keep the chapter long after source-density and render review.
- CH02-04, CH08-11, CH13-14, CH17-19, CH22-23 need selective sourced expansion, mostly 300-700 words each, where the current prose is efficient but under-textured.
- CH05 and CH16 are useful but long; later edits should look for repetition with visuals, apparatus, and neighboring chapters.

## Deliverables

- `data/full_draft_word_count_gap_audit_i0239.tsv` - chapter-level counts, bands, gaps, and recommendations.
- `data/full_draft_word_count_actions_i0239.tsv` - prioritized expansion/compression actions.

## Caveat

The generated Markdown file contains front matter, assembly notes, source-path notes, and figure-placeholder text. Those words are useful for production but should not be used to inflate the book-length claim. The source-word audit is the stricter count for manuscript readiness.
