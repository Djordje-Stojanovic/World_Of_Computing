# Full-Book Render Pipeline Pass I-0240

Status: promoted first-render pipeline.

## Render Path

This pass chooses the simplest local path available: a Python standard-library Markdown-to-HTML converter, followed by Chrome headless print-to-PDF.

Command:

```powershell
python scripts\render_full_book_i0240.py
```

Primary outputs:

- `rendered/full_book_i0240/Next-Token-full-draft-i0240.html`
- `rendered/full_book_i0240/Next-Token-full-draft-i0240.pdf`
- `data/full_book_render_pipeline_i0240.tsv`

## Measurements

- Chapter headings in source Markdown: 24.
- Figure placeholders in source Markdown: 100.
- Markdown words including production apparatus: 107,047.
- HTML bytes: 703,026.
- PDF bytes: 2,477,713.
- PDF header: `%PDF-1.4`.
- PDF page count by `/Type /Page` marker scan: 401.
- PDF SHA-256: `e7bde893c46f2c2a97f2582862b97601f8a9defbb6745000635cd2b987a643ae`.

## Known Defects

This is not a design pass. The PDF is a tangible first render, not a publication proof. Known defects:

- CSS is intentionally rough.
- Figure rows are placeholder text, not placed final figures.
- No page-level QA has checked missing chapters, broken headings, overflows, widows, or orphaned source notes.
- No text extraction QA has confirmed searchability or source-note integrity.
- No visual-legibility QA has checked charts, screenshots, or captions.
- Caption, rights, and source-note gates remain unresolved.

## Promotion Rationale

The project now has a reproducible full-book render command and a local rough PDF artifact. That improves the loop because future render QA passes can inspect a real 401-page object rather than speculating from Markdown. The pass is promoted as pipeline infrastructure only; it does not improve prose, visual polish, rights readiness, or publication readiness by itself.
