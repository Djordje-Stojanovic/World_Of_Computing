# I-0283 Table And Excerpt Integration Toolchain

Status: promoted setup pass, with 8 pass / 0 warn / 0 fail QA.

## Verified

- A yearly benchmark/model-landscape table schema can render as a lightweight SVG while carrying source IDs and claim-boundary text.
- `GTC-2026-Keynote.pdf` can be page-rendered locally with PyMuPDF for source-surface/excerpt workflows.
- A paraphrase-first PDF/page excerpt-card SVG can point to a rendered page handle without copying a full page into a committed asset.
- A local model-card-style HTML page can be screenshot by headless Chrome, proving the route needed for Hugging Face, model-card, repo, docs, and benchmark surfaces.
- Draft placement-manifest rows bind figure ID, chapter, asset ID, source file, hash, caption contract, claim boundary, and next gate.
- The smoke HTML/PDF route embeds table, excerpt-card, PDF-page, and screenshot media in one PDF and verifies image objects with PyMuPDF.

## Probe Outputs

- benchmark_table_generator_by_year: pass - rows=9; svg=assets/benchmarks/i0283/benchmark-year-table-probe-i0283.svg
- paper_pdf_page_render: pass - rendered GTC-2026-Keynote.pdf page 1 to rendered/i0283_table_excerpt_smoke/media/gtc_2026_page_1_probe.png
- paper_pdf_excerpt_card_builder: pass - excerpt_card=assets/papers/i0283/pdf-excerpt-card-probe-i0283.svg with blocked-claim footer
- model_card_screenshot_capture: pass - chrome screenshot from assets/model_cards/i0283/model-card-screenshot-probe-i0283.html to rendered/i0283_table_excerpt_smoke/media/model_card_screenshot_probe_i0283.png
- figure_placement_manifest_updater: pass - draft placement rows=3; chapters={'CH13': 1, 'CH15': 1, 'CH12': 1}
- render_smoke_pdf: pass - pdf_pages=3; image_xobjects=2; text_i0283=True
- provenance_hashing: pass - placement rows include sha256 for all source files; ignored smoke rasters/PDF have probe hashes
- claim_boundary_carriage: pass - all draft placements carry explicit claim boundaries and next gates

## Limits

- This pass does not acquire or promote real benchmark tables, paper excerpts, model cards, Hugging Face pages, or documentation screenshots.
- Rendered PNG/PDF/HTML outputs live under ignored `rendered/i0283_table_excerpt_smoke/`.
- Future acquisition rows still need live/local source provenance, access dates, cutoff-status checks, quote limits, rights notes, and final page-legibility QA.
