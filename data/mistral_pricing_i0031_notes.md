# Mistral Pricing Normalization Notes - I-0031

Pass date: 2026-05-25

Purpose: pair the previously captured Mistral model docs with an official pricing/API billing source and normalize Mistral rows into the same provider-pricing evidence pattern used for OpenAI, Anthropic, Google, and xAI.

## Captures

- SNAP-20260525-011 / S-0081: `https://mistral.ai/pricing`, captured as HTML at `data/source_snapshots/2026-05-25/2026-05-25__S-0081__pricing-page__mistral-ai-pricing__html.html`.
- SNAP-20260525-012 / S-0082: `https://docs.mistral.ai/deployment/laplateforme/pricing/`, captured as HTML at `data/source_snapshots/2026-05-25/2026-05-25__S-0082__pricing-page__mistral-docs-pricing__html.html`.

Both URLs resolved to the same captured HTML and SHA256 hash.

## Normalized Rows

`data/mistral_pricing_rows_i0031.tsv` normalizes 10 rows for Mistral chat/frontier, code, reasoning, and other-model pricing. The rows preserve:

- model name and API endpoint
- input and output USD price per 1M tokens
- source ID and snapshot ID
- chart-readiness caveats
- post-cutoff-capture caveats

## Publication Rule

This pass resolves the missing Mistral pricing-source pair from I-0026. It does not close C-0046. The capture happened on 2026-05-25, one day after the book cutoff, so final price-quality charts still need model cutoff-status checks, same-scope rank joins, and chart captions that separate general chat/frontier rows from code, reasoning, audio, OCR, and other non-comparable rows.
