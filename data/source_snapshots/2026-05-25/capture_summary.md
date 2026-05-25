# Source Snapshot Capture Summary

Passes: I-0016; I-0025; I-0028; I-0029; I-0030; I-0031

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

## I-0030 ChatGPT Product Page Browser Attempt

Pass I-0030 attempted the alternate in-app browser workflow for S-0078 and S-0079 after the shell capture remained blocked in I-0025. The browser backend was unavailable and returned `Browser is not available: iab`, so no local HTML or screenshot snapshot was created.

The result is recorded in `data/source_snapshots/2026-05-25/chatgpt_product_pages_i0030_browser_attempt.md`. SNAP-20260525-002 and SNAP-20260525-003 remain blocked-capture records, and Chapter 7 must continue using these pages only for structural paraphrase until a working local capture path exists.

## I-0028 Chapter 6 Alignment Source Attempt

- SNAP-20260525-004 / S-0074: OpenAI instruction-following product-post shell HTML capture returned HTTP 403. Local capture note: `data/source_snapshots/2026-05-25/2026-05-25__S-0074__html__capture-note.txt`.
- SNAP-20260525-005 / S-0075: OpenAI Model Spec 2024-05-08 HTML captured from `https://cdn.openai.com/spec/model-spec-2024-05-08.html`.
- SNAP-20260525-006 / S-0076: GPT-4 System Card PDF captured from `https://cdn.openai.com/papers/gpt-4-system-card.pdf`.
- SNAP-20260525-007 / S-0077: GPT-4o System Card PDF captured from `https://cdn.openai.com/gpt-4o-system-card.pdf`.

This pass improves Chapter 6 provenance but does not close C-0044. Exact instruction-following quotations, labeler-process wording, and any direct language from the blocked product post remain gated until a browser screenshot, alternate archive, or local HTML capture exists. Exact policy/system-card wording from the captured artifacts still needs quote-limit extraction before final prose.

## I-0029 LMArena Historical Dataset Capture

- SNAP-20260525-008 / S-0080: Hugging Face dataset-server JSON for `lmarena-ai/leaderboard-dataset`, config `text_style_control`, split `latest`, first 100 rows captured at `data/source_snapshots/2026-05-25/2026-05-25__S-0080__historical-dataset__lmarena-text-style-control-latest__json.json`.
- HTTP status: 200.
- Bytes: 35,143.
- SHA256: `3083B424CB6D48A30571A42C39861C622022003D6904EEAB634F6FBC0FDCE198`.
- Normalized table: `data/lmarena_clean_cutoff_rows_i0029.tsv`, 100 `overall` rows, all with `leaderboard_publish_date` 2026-05-19 and `cutoff_status` `pre_cutoff_published_snapshot`.

This pass resolves the C-0045 clean cutoff-bounded leaderboard-row blocker for a May 19 historical dataset chart. It does not support wording that claims the rows are a live May 24 screenshot or that they represent every LMArena category.

## I-0031 Mistral Pricing Capture

- SNAP-20260525-011 / S-0081: Mistral AI pricing HTML captured from `https://mistral.ai/pricing`.
- SNAP-20260525-012 / S-0082: Mistral docs pricing HTML captured from `https://docs.mistral.ai/deployment/laplateforme/pricing/`.
- Both captures returned HTTP 200, 452,618 bytes, SHA256 `E6A5B230881BDC253537D06DD0BBB8CB210AF894CC13380B450D4E6ADEB366AB`.
- Normalized table: `data/mistral_pricing_rows_i0031.tsv`.

This pass resolves the missing Mistral pricing-source pair from I-0026. It does not close C-0046 because the captures happened one day after cutoff and final price-quality charts still need cutoff-status checks and same-scope rank joins.

## I-0075 ChatGPT Enterprise Text Render

- SNAP-20260525-026 / S-0079: OpenAI `Introducing ChatGPT Enterprise` product post captured through the established r.jina.ai text-render route at `data/source_snapshots/2026-05-25/2026-05-25__S-0079__product-post__chatgpt-enterprise__text-render.md`.
- Direct shell HTML capture of the official OpenAI page still returned a JavaScript/cookie challenge during I-0075.
- HTTP status: 200 for the text-render route.
- Bytes: 6,172.
- SHA256: `62C0C6AF6F8DC89A9F1E5DE7FEF6CD003E9E7962FAA1D797D35B8243B5828DCD`.
- Extraction table: `data/chatgpt_enterprise_quote_safe_rows_i0075.tsv`.

This pass upgrades S-0079 from original-post quotation blocked to quote-ready with a renderer caveat for short OpenAI-attributed product-post wording, the Fortune 500 registered-account statement and footnote definition, and vendor-hosted customer quote context. It does not authorize paid Enterprise adoption, neutral named-customer deployment, or productivity-outcome prose without customer-side or independent corroboration.
