# Selected-100 Source-Note And Attribution QA - I-0217

Pass I-0217 audits the selected-100 exhibit program for source-note and attribution completeness. It joins the selected exhibit matrix to `assets_manifest.tsv`, `sources.tsv`, and the I-0216 caption audit, then checks each planned exhibit for manifest row, source IDs, access date, rights/private-use status, story purpose, blocked-claim note, and source-ledger consistency.

## Findings

The selected-100 program is close on provenance structure:

- 100 selected exhibits audited.
- 98 rows pass the source-note provenance contract.
- 2 rows require correction before publication readiness.
- A-0004 needs an explicit S-0001 source-note bridge for the local GTC page 29 render.
- A-0106 has a selected-matrix versus manifest status mismatch that must be reconciled before final readiness claims.

This pass does not clear publication rights, rewrite manifest rows, create rendered source notes, or prove final PDF note proximity. It creates the QA surface that should guide the next correction pass and later render QA.

## Source-Note Rule

Final source notes must keep six fields together whenever possible: source ID or local path, creator/org, page/date, access date, rights/private-use status, and blocked-claim note. Captions can stay elegant only if the source note carries the dense provenance burden nearby.

## Files

- QA table: `data/selected_100_source_note_attribution_qa_i0217.tsv`
- Chapter summary: `data/selected_100_source_note_attribution_summary_i0217.tsv`
- Action table: `data/selected_100_source_note_attribution_actions_i0217.tsv`
