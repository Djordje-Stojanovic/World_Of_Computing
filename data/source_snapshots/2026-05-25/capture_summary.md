# Source Snapshot Capture Summary

Pass: I-0016

Access date: 2026-05-25

Purpose: resolve the OpenAI API pricing local-capture gap left by pass I-0011, where `https://openai.com/api/pricing/` returned HTTP 403 to shell capture.

## Captured Official Alternate

- SNAP-20260525-001 / S-0072: OpenAI API developer-docs pricing HTML captured from `https://developers.openai.com/api/docs/pricing` at `data/source_snapshots/2026-05-25/2026-05-25__S-0072__pricing-page__openai-api-docs-pricing__html.html`.
- HTTP status: 200.
- Bytes: 471,595.
- SHA256: `87AC01E1FF35173C8B0D7BDA68EC1326974E53C2633B01EF982E2D4188A1866D`.

## Still Blocked

The original `https://openai.com/api/pricing/` URL still returned HTTP 403 to shell capture during this pass. The browser screenshot path was also unavailable because the in-app browser backend was not available in this session.

This alternate official-docs snapshot resolves C-0031's local-capture gap. It does not by itself authorize exact OpenAI price rows in final prose or charts, because the capture happened on 2026-05-25, one day after the book's factual cutoff. Any exact OpenAI price comparison still needs row normalization, model-version filtering, and a clear cutoff-status caveat under C-0018.
