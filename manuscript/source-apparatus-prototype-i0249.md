# I-0249 Source Apparatus Prototype

Status: promoted full-book note-style prototype.

## Style Decision

Use bracketed endnote markers in the reading text, grouped chapter endnotes at the back, and source-ID-first placeholders during production. Do not use page-bottom footnotes yet; the current rough renderer needs typography and page-flow work before footnotes can be trusted.

## Results

- Placeholder note rows: 315
- Unique source IDs represented: 153
- Render QA rows: 6 (6 pass, 0 warn, 0 fail)
- Local full-book prototype PDF: `C:\AI\TEMP\World_Of_Computing\rendered\full_book_i0249\Next-Token-full-draft-i0240.pdf` (ignored, not committed)

## Guardrails

- Notes are placeholders, not final bibliography entries.
- Source IDs are preserved for traceability, but page anchors and publisher-style citations still need a later pass.
- The prototype proves render survivability, not final note beauty or page-bottom proximity.

## Deliverables

- `data/endnote_placeholders_i0249.tsv`
- `data/endnote_render_qa_i0249.tsv`
- `scripts/endnote_system_i0249.py`
