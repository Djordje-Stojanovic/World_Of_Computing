# Source Snapshot Capture Summary

Passes: I-0016; I-0025

Access date: 2026-05-25

Purpose: resolve or document OpenAI local-capture gaps for mutable OpenAI pages used in the model-rankings appendix and ChatGPT chapter.

## Captured Official Alternate

- SNAP-20260525-001 / S-0072: OpenAI API developer-docs pricing HTML captured from `https://developers.openai.com/api/docs/pricing` at `data/source_snapshots/2026-05-25/2026-05-25__S-0072__pricing-page__openai-api-docs-pricing__html.html`.
- HTTP status: 200.
- Bytes: 471,595.
- SHA256: `87AC01E1FF35173C8B0D7BDA68EC1326974E53C2633B01EF982E2D4188A1866D`.

## Still Blocked

The original `https://openai.com/api/pricing/` URL still returned HTTP 403 to shell capture during this pass. The browser screenshot path was also unavailable because the in-app browser backend was not available in this session.

This alternate official-docs snapshot resolves C-0031's local-capture gap. It does not by itself authorize exact OpenAI price rows in final prose or charts, because the capture happened on 2026-05-25, one day after the book's factual cutoff. Any exact OpenAI price comparison still needs row normalization, model-version filtering, and a clear cutoff-status caveat under C-0018.

## I-0025 ChatGPT Product Page Attempt

- SNAP-20260525-002 / S-0078: ChatGPT Plus shell HTML capture returned HTTP 403. Local capture note: `data/source_snapshots/2026-05-25/2026-05-25__S-0078__product-post__chatgpt-plus__capture-note.txt`.
- SNAP-20260525-003 / S-0079: ChatGPT Enterprise shell HTML capture returned HTTP 403. Local capture note: `data/source_snapshots/2026-05-25/2026-05-25__S-0079__product-post__chatgpt-enterprise__capture-note.txt`.
- Browser/web-reader verification confirmed both official pages are readable and support Chapter 7's structural product-evolution use, but direct quotation, exact Plus pricing, Enterprise adoption percentages, customer productivity claims, and detailed availability language remain snapshot-gated.

Details are in `data/source_snapshots/2026-05-25/chatgpt_product_pages_i0025_notes.md`.
