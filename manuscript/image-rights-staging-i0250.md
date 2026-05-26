# I-0250 Image Rights Staging

Status: promoted rights-staging board, not legal clearance.

## Result

- Figure callouts classified: 100
- Publish path rows: 74
- Local-only rows: 2
- Redraw rows: 3
- Permission-needed rows: 21
- Replace rows: 0
- Drop rows: 0

## Decision Rule

Original SVG/chart/card assets are staged as `publish` only after render, caption, and source-note QA. Raw slide/page renders are `local-only`. Source screenshots should become source cards or redraws. Product screenshots and photos remain `permission-needed` until capture, license, attribution, and blocker gates close.

## Deliverables

- `data/image_rights_staging_i0250.tsv` - one row per selected figure callout.
- `data/image_rights_staging_summary_i0250.tsv` - count summary and unresolved-risk totals.

## Next

Work the permission-needed rows first if the book needs real-world texture, or convert the redraw rows into original source cards if publication risk needs to fall fastest.
