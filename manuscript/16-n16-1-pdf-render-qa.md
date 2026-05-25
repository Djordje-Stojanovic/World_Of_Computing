# Chapter 16 N16-1 PDF Render QA

Pass I-0078 runs a true local PDF/page-image proof for the N16-1 note candidate using PyMuPDF. The generated PDFs, extracted text files, and 2x PNG page images live under `rendered/chapter16_i0078/` and remain untracked because rendered PDFs/PNGs are intentionally ignored.

Gate summary: 10 pass or pass-with-caveat rows, 0 fail rows in `data/chapter16_n16_1_pdf_render_qa_i0078.tsv`.

Decision: N16-1 passes the production-text PDF gate for the current Chapter 16 opening, including same-page placement, text extraction, row-mapping integrity, inline CH16Q-017 and CH16Q-018 blocker visibility, and parent/candidate reversibility. It is still not merged into live prose in this pass; the next useful move is a narrow live-prose integration that keeps the source cues and reruns the same render proof after the manuscript edit.
