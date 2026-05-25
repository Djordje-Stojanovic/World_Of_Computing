# Chapter 16 N16-1 Live PDF Render QA

Pass I-0083 reruns the true local PDF/page-image proof after the N16-1 note anchor is integrated into the live LBNL/DOE paragraph. The generated PDFs, extracted text files, and 2x PNG page images live under `rendered/chapter16_i0083/` and remain untracked because rendered PDFs/PNGs are intentionally ignored.

Gate summary: 14 pass or pass-with-caveat rows, 0 fail rows in `data/chapter16_n16_1_live_pdf_render_qa_i0083.tsv`.

Decision: N16-1 passes the production-text PDF gate for the current Chapter 16 opening, including same-page placement, text extraction, row-mapping integrity, inline CH16Q-017 and CH16Q-018 blocker visibility, operator-signal stability, no-new-quant control, and parent/candidate reversibility. The live prose change remains narrow: only CH16Q-003 through CH16Q-006 moved from inline LBNL/DOE cue clusters into N16-1.
