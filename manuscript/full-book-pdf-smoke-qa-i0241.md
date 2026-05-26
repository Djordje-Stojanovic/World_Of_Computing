# Full-Book PDF Smoke QA I-0241

Status: promoted defect-ledger pass.

## Executive Read

The first rough full-book PDF is structurally present and searchable enough for smoke QA: the artifact has a valid PDF header, 401 pages, all 24 canonical chapter titles survive text extraction, all 100 figure IDs survive text extraction, and the generated internal TOC anchors resolve in HTML.

It is not a layout pass. The same QA records serious next-step defects: all figures are still text placeholders, overflow is unproven, and page-image review has not judged readability, source-note proximity, caption flow, or visual polish.

## Results

- QA rows: 10.
- Passing rows: 8.
- Warning rows: 2.
- Failing rows: 0.
- Defect rows: 2.
- PDF pages: 401.
- Chapter titles found: 24 / 24.
- Figure IDs found: 100 / 100.

## Deliverables

- `data/full_book_pdf_smoke_qa_i0241.tsv` - machine-readable smoke checks.
- `data/full_book_pdf_smoke_defects_i0241.tsv` - actionable defect list.

## Promotion Rationale

This pass makes the rough PDF useful by turning it into an inspectable defect surface. It promotes the QA ledger, not the PDF design. The next render work should attack the P0/P1 defects before beautifying typography.
