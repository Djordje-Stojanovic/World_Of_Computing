# Bureaucracy Purge - I-0313

I-0313 executes the first rescue task after the direct override: remove visible project/audit bureaucracy from the reader-facing proof.

## Result

- Source PDF: `rendered/final_private_i0312/Next-Token-final-private-polished-matter-i0312.pdf`
- New local proof: `rendered/final_private_i0313/Next-Token-final-private-bureaucracy-purged-i0313.pdf`
- Pages: 549
- Image objects: 330
- Drawing objects: 4816
- Forbidden reader-facing string hits: 4123 -> 0
- Captions cleaned: 300
- SVG images sanitized: 201
- Chapter visual headings renamed: 24
- Paragraphs dropped as audit/process residue: 421
- Text nodes cleaned: 5638

## What Changed

Reader-facing captions no longer expose raw figure IDs, asset IDs, source IDs, use notes, boundary labels, blocked-claim boilerplate, provenance boilerplate, checksums, or local paths. Embedded SVG text was also sanitized so board/source-card internals do not leak into PDF text extraction.

## Still Open

This pass does not solve the chronological opening, endnotes-only source architecture, blank/sparse pages, image relocation, multi-image pages, or quantitative enrichment. Those are the next FIFO tasks.

QA: 5 pass / 0 fail.
