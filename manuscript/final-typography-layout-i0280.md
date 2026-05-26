# I-0280 Final Typography And Layout Pass

Status: promoted production-layout QA surface, not publication clearance.

## Result

- Local PDF: `rendered/full_book_i0280/Next-Token-full-draft-i0280.pdf` (ignored, not committed)
- PDF pages: 267
- Embedded image objects: 100
- Pages with images: 100
- Blank-like pages: 0
- Figure rows audited: 100
- Figure status: 0 pass / 100 warn / 0 fail
- Defects: 100 total, 0 P0
- Caption/source-note minimum font: 6.20 pt
- Missing source-note labels: 0
- Missing rights-stage labels: 0
- Visual fatigue: max 4 consecutive image pages; max 11 image pages per 20-page window
- Final QA: 6 pass / 3 warn

## Layout Changes

- Raised embedded-figure caption/source-note type from the I-0262 render layer to an extracted minimum of 6.20 pt, which is improved but still below the 6.8 pt warning floor.
- Moved source note and rights-stage text ahead of the longer caption body so same-page provenance survives PDF text extraction.
- Reduced maximum figure image height and slightly tightened body spacing to keep figure/caption blocks together without creating blank pages.
- Rendered a fresh local PDF and fresh local chapter sample PNGs from the current I-0279 manuscript.

## Limits

This pass improves automated typography and layout evidence, but it is not final publication clearance. Final legal review, PDF/X or print production checks, EPUB conversion, manual page beauty review, cover/package work, and final gate decisions remain pending.
