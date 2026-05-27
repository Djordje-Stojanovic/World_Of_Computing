# I-0293 Full Private-Edition Render

Status: promoted first final render/polish QA surface, not final delivery.

## Result

- Local PDF: `rendered/full_book_i0293/Next-Token-full-draft-i0293.pdf` (ignored, not committed)
- PDF SHA-256: `4e9445b7927cbf8a724c99c9d8b3c94741f4652bedc5eba3abb73deb7bae61ef`
- PDF bytes: 18449203
- PDF pages: 234
- Embedded image objects: 100
- Pages with images: 100
- Blank-like pages: 0
- Figure pages audited: 100
- Figure status: 0 pass / 100 warn / 0 fail
- Defects: 120 total, 0 P0
- Minimum extracted caption/source-note font: 5.40 pt
- Median largest-image area: 27.7%
- Visual fatigue: max 4 consecutive image pages; max 12 image pages per 20-page window
- Final QA: 5 pass / 5 warn

## Render Changes

- Rendered from the post-I-0292 active selected exhibit manifest, so real-world images, source-surface page renders, model-card screenshots, leaderboard surfaces, repo surfaces, and yearly benchmark tables all enter one full PDF.
- Applied a new I-0293 image-first CSS layer with wider usable page area, larger maximum image frames for source pages and benchmark tables, and caption ordering that foregrounds caption, source note, rights stage, type, and claim boundary.
- Generated chapter sample PNGs locally and recorded per-chapter visual density so I-0294 can target ugly or overcrowded stretches instead of guessing.

## Defect Backlog For I-0294

- Figure warnings: 100
- Small-image warnings: 20
- Missing source-note labels in extracted text: 0
- Missing rights-stage labels in extracted text: 0
- Chapters in density ledger: 24

The local PDF is now the right object to inspect, but the warning rows are not cosmetic paperwork: they are the correction map for I-0294.
