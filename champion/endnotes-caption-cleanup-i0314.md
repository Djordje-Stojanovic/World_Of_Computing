# Endnotes Caption Cleanup - I-0314

I-0314 executes the second rescue task: convert the visible caption/source layer toward trade-book captions while keeping old source detail in local ledgers.

## Result

- Source PDF: `rendered/final_private_i0313/Next-Token-final-private-bureaucracy-purged-i0313.pdf`
- New local proof: `rendered/final_private_i0314/Next-Token-final-private-endnotes-captions-i0314.pdf`
- Pages: 537
- Image objects: 356
- Drawing objects: 3424
- Visible source/caption mechanics hits: 1099 -> 0
- Captions rewritten: 267 / 300
- Caption endnote rows: 267
- SVG/HTML visual assets sanitized: 200
- Nodes removed as source-note/caveat mechanics: 204

## What Changed

Visible captions now aim to say what the reader is seeing in plain English. URLs, source-note boilerplate, provenance wording, caveat labels, role tokens, and old caption detail were moved into `data/endnotes_caption_cleanup_endnotes_i0314.tsv` and related ledgers instead of remaining on the page.

## Still Open

This pass does not fix chronology, sparse pages, image relocation, multi-image pages, or missing quantitative density. Those remain queued in I-0315 through I-0322.

QA: 7 pass / 0 fail.
