# 100-Exhibit Readiness Dashboard - Pass I-0196

This pass makes the current top-100 exhibit program measurable without pretending that selected means publication-ready. The current matrix has exactly 100 selected rows, but only 74 are immediately ready lightweight SVG/chart rows. Another 26 selected rows still need capture, rights review, duplicate-resolution, or replacement.

## Current State

- Selected top-100 rows: 100.
- Chapter-placed selected rows: 100.
- Immediately ready SVG/chart rows: 74.
- Selected rows not publication-ready: 26.
- Private screenshot/source captures needed: 17.
- Photo rights reviews needed: 7.
- Local hashed GTC surfaces still needing rights/duplicate decisions: 2.
- Reserve rows outside the top 100: 17.
- Dropped top-100 rows: 4.

The most important shape problem is uneven distribution. Chapters 2-5 are under target and need roughly eight early technical source/redraw exhibits. Eleven chapters are over target, with 19 selected rows above a four-per-chapter ceiling. The next readiness gains should come from capture, rights review, canonical-paper execution, and pruning, not from adding more rows.

## Burn-Down Logic

The path to a publication-ready 100 is:

1. Capture and hash the 17 selected screenshot/source-screenshot rows.
2. Verify or replace the 7 selected photo candidates.
3. Resolve the 2 local hashed GTC surfaces against safer claim-card alternatives.
4. Execute early technical source cards and canonical redraws for Chapters 2-5.
5. Prune overfull Chapters 7, 9-12, 14-16, and 18-20 after render tests.
6. Promote reserves only by replacement, never by count inflation.
7. Synchronize every finished capture/redraw into `assets_manifest.tsv`.
8. Render the full book and fail any exhibit that cannot carry caption, provenance, rights, and blocker text legibly.

## Outputs

- `data/exhibit_readiness_dashboard_i0196.tsv`: top-level selected, rights-ready, capture-needed, dropped, reserve, redraw, and chapter-balance metrics.
- `data/exhibit_readiness_chapter_dashboard_i0196.tsv`: 24 chapter rows with readiness problems and next actions.
- `data/exhibit_readiness_burndown_i0196.tsv`: 10-step burn-down path to a publication-ready exhibit program.

No new exhibit, screenshot, raster, source-card artwork, or manifest row was created in this pass.
