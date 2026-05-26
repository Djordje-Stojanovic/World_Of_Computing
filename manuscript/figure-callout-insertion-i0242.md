# Figure-Callout Insertion Pass I-0242

Status: promoted assembly pass.

## What Changed

- Replaced the chapter-opening `## Figure Placeholders` inventory blocks in `manuscript/Next-Token-full-draft.md` with section-level `FIGURE-CALLOUT` blocks.
- Inserted all 100 selected figure IDs from `data/full_book_figure_list_i0229.tsv` into the manuscript near chapter section headings.
- Created `data/figure_callout_placement_i0242.tsv` as the placement ledger for future layout, caption, and rights passes.

## Measurements

- Figure callouts inserted: 100.
- Chapters with callouts: 24.
- Chapter-level placeholder inventory blocks remaining: 0.
- Post-callout rough PDF render: 413 pages, 2,620,944 bytes, 100 Markdown callouts recognized by the render pipeline.

## Caveat

These are manuscript callouts, not final figures. Each block keeps planned status, rights status, caption gate, provenance gate, manifest path, and next gate visible so the render pipeline cannot accidentally treat placeholder text as finished art.
