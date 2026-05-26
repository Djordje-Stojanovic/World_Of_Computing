# I-0219 Selected SVG/Chart Legibility QA

This pass audits the 74 selected-100 rows that point to local SVG files. It applies the I-0218 style contract to source files and separates print-scale risk from annotation and metadata risk before the later page-image render passes.

## Result

- 74 selected SVG rows audited.
- 25 rows pass the source-file legibility proxy.
- 31 rows need render-scale review, usually because declared text falls below the 14 px warning floor.
- 3 rows need annotation review for missing or implicit source/caveat/axis language.
- 15 rows need style or metadata review after scale and annotation defects are separated.

The only selected row typed as `svg_chart`, A-0013, passes this proxy: it has readable declared text, source/snapshot language, axis/rating annotations, and the no-live-rank caveat. That does not certify final placement; it only means A-0013 should move to page-image proof rather than source-file repair.

## Hotspots

Chapters 17 and 18 are the main danger zone, with all four selected SVG rows in each chapter requiring render-scale review. Chapter 8 also has four of four in scale review. The risk is not that the diagrams are conceptually wrong; it is that dense technical chapters may become visually tiring if small labels, caveat lines, and muted text are squeezed into final trim size.

## Gate

I-0219 does not replace PDF QA. It turns legibility into a burn-down: text scale first, source/caveat annotation second, contrast/stroke/metadata third, then page-image proof.
