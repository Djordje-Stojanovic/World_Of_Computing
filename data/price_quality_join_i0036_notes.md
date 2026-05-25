# I-0036 Price-Quality Join Audit Notes

Pass date: 2026-05-25

Purpose: join the clean LMArena May 19 historical `text_style_control` `overall` rows with normalized provider pricing rows without making a false price-quality frontier.

## Inputs

- Rank rows: `data/lmarena_clean_cutoff_rows_i0029.tsv` / `S-0080` / `SNAP-20260525-008`.
- OpenAI pricing rows: `data/openai_pricing_rows_i0021.tsv` / `S-0072` / `SNAP-20260525-001`.
- Anthropic, Google, xAI pricing rows: `data/provider_pricing_rows_i0026.tsv` / `S-0060` through `S-0062`.
- Mistral pricing rows: `data/mistral_pricing_rows_i0031.tsv` / `S-0081` / `SNAP-20260525-011`.

## Result

The audit table is `data/price_quality_join_audit_i0036.tsv`.

This pass found six candidate same-scope rows:

- xAI Grok 4.3.
- Google Gemini 2.5 Pro, split into <=200k and >200k prompt tiers.
- Google Gemini 2.5 Flash text/image/video.
- Anthropic Claude Opus 4.1, with model-alias caveat.
- Anthropic Claude Haiku 4.5, with model-alias caveat.

Mistral Large 3 is a plausible candidate but remains blocked because the pricing capture is dated 2026-05-25, one day after the book cutoff. OpenAI rows remain excluded from a general price-quality join because the normalized OpenAI table currently contains fine-tuning prices or missing comparable standard inference prices, not same-scope serving/API rows for the LMArena models.

## Use Rules

- Do not build a final price-quality frontier from this pass alone. Coverage is too sparse and tier semantics are still uneven.
- Do not average Gemini prompt-length tiers.
- Do not mix batch, data-sharing, code-only, reasoning-only, deprecated, or fine-tuning rows into a general chat/text-style chart.
- Use excluded rows as negative evidence in chart notes: the audit is valuable because it shows which tempting comparisons are not honest.
- C-0046 remains active for final chart promotion, but it is narrowed: the next blocker is broader same-scope coverage and cutoff-price corroboration, not the absence of a join protocol.
