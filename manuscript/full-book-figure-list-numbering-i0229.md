# Full-Book Figure List And Numbering Pass - I-0229

Pass I-0229 creates a temporary canonical figure ledger for the selected-100 exhibit program. The source of truth is `data/full_book_figure_list_i0229.tsv`, derived from:

- `data/master_100_exhibit_selection_matrix_i0182.tsv`
- `data/selected_100_caption_excellence_i0216.tsv`
- `data/selected_100_source_note_attribution_qa_i0217.tsv`
- `assets_manifest.tsv`

The ledger assigns one stable figure ID and one chapter anchor to every currently selected exhibit. The format is `Fcc.nn`, where `cc` is the two-digit chapter number and `nn` is the selected exhibit sequence inside that chapter. Example: `F01.01` maps to `ch01-fig01` and asset `A-0068`.

## Current Counts

- Selected figures numbered: 100
- Chapters represented: 24
- Duplicate figure IDs: 0
- `selected_pending_render`: 74
- `selected_pending_capture`: 17
- `selected_pending_rights_review`: 7
- `selected_pending_source_surface_review`: 2

## What This Pass Fixes

The book now has a single production table where each selected exhibit carries:

- stable `figure_id`
- `chapter_anchor`
- selected-rank order
- asset ID and type
- figure title
- final role
- planned status
- rights status
- source IDs
- manifest file path
- generated claim-safe alt text
- caption gate
- provenance gate
- next gate

## Claim Contract

Allowed:

- Use `figure_id` and `chapter_anchor` as production references for selected exhibits.
- Use `planned_status` to route render, capture, rights, and source-surface review work.
- Use generated alt text as a first-pass accessibility scaffold.

Blocked:

- Treating the list as final page numbering, final placement, publication-ready accessibility, rights clearance, or source-note proximity proof.
- Marking selected exhibits as publishable without render proof and rights/source gates.
- Silent renumbering after later selection changes.

Promotion rationale: this reduces render, caption, and cross-reference failure risk across the whole book without changing the selected exhibit set or adding unsupported claims.
