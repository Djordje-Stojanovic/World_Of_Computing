# Final Rights-Risk Triage Board - I-0235

This pass classifies all 100 selected exhibits from `data/full_book_figure_list_i0229.tsv` by publication risk. It does not clear rights. It makes the remaining decisions visible before the full-book assembly and render passes.

## Verdict

The selected visual program is strong as a planning system, but not yet publication-ready. Original SVG/data visuals are the safest class, while screenshots, source screenshots, real-world photos, and company/source surfaces remain high-risk until capture, crop, permission, attribution, and blocked-claim gates close.

Generated outputs:

- `data/selected_exhibit_rights_triage_i0235.tsv` classifies every selected figure.
- `data/selected_exhibit_rights_triage_summary_i0235.tsv` summarizes class/severity counts.
- `data/selected_exhibit_rights_triage_by_chapter_i0235.tsv` identifies the main chapter-level gate.
- `data/selected_exhibit_rights_triage_actions_i0235.tsv` gives the next production actions.

Every high-risk row includes a replacement candidate. Those candidates are intentionally conservative: source cards, original schematic redraws, verified public-domain/permissioned photos, or reserve/cut decisions.

## Main Rule

`selected` is not the same as `publishable`.

An original SVG may be close to publishable after render, caption, and source-note proof. A screenshot slot is only a slot until the viewport, hash, date, rights/private-use note, and claim firewall exist. A photo candidate is only a candidate until the original license trail and attribution are verified. A company slide or product surface is source-actor evidence, not neutral proof.

## Production Implication

The next visual readiness pass should fail closed on unresolved high-risk rows. If a screenshot or photo cannot be cleared quickly, the better book move is often a source card or redraw, not a quiet placeholder. Rights triage is now a pruning tool as much as a legal caution.
