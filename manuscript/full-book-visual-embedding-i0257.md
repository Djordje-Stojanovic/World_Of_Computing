# I-0257 Full-Book Visual Embedding

Status: promoted visual-embedding render surface.

## Result

- Local PDF: `rendered\full_book_i0257\Next-Token-full-draft-i0257.pdf` (ignored, not committed)
- PDF pages: 442
- Publishable SVG/chart/card assets embedded: 74 / 74
- Remaining blocked callout blocks: 26
- HTML image tags: 74 (74 raster PNG, 0 SVG)
- Local raster staging: `rendered\full_book_i0257\embedded_rasters` (ignored, not committed)
- PDF visual-object evidence: 74 raster image XObjects, 74 pages with raster images
- QA rows: 7 (6 pass, 1 warn, 0 fail)
- Defect rows: 1

## Promotion Rationale

The previous designed render preserved figure IDs as text only. This pass changes the render pipeline so every selected figure row that is both marked `publish` and has an available local SVG/chart/card file is rasterized to a local PNG and inserted as an actual image-bearing figure with caption, sources, rights stage, and claim boundary.

## Limits

This is still not publication-ready. Twenty-six selected slots remain blocked as local-only, permission-needed, or redraw rows. The SVGs still need page-image legibility QA, caption compression, final source-note treatment, and the next file-level manifest pass.
