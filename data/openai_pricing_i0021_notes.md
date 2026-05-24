# OpenAI Pricing Row Normalization Notes - I-0021

Pass I-0021 normalized a conservative subset of visible OpenAI pricing rows from `SNAP-20260525-001` / `S-0072`, the official OpenAI developer-docs pricing HTML captured at `data/source_snapshots/2026-05-25/2026-05-25__S-0072__pricing-page__openai-api-docs-pricing__html.html`.

## Method

- Used only the local official snapshot already recorded in `data/source_snapshot_protocol.tsv`.
- Preserved the capture caveat: the HTML was captured on 2026-05-25, one day after the book cutoff of 2026-05-24.
- Normalized visible rows into dollars per 1M tokens for input, cached input, and output, plus dollars per training hour where the fine-tuning table exposed that field.
- Split rows by scope: standard fine-tuning, legacy fine-tuning, data-sharing discount, batch tier, tool preview, and priority Codex rows.
- Marked candidate rows as requiring cutoff-day corroboration rather than chart-ready May 24 price facts.
- Recorded obvious post-cutoff model rows as exclusions so later chart work can filter them mechanically.

## Use Rules

`data/openai_pricing_rows_i0021.tsv` may be used as a normalization and filtering artifact, not as final chart data. Exact OpenAI price-quality charts remain blocked by C-0046 until the OpenAI rows are corroborated against cutoff-day evidence and joined to same-scope rank rows.

Rows with `chart_readiness` set to `candidate_only_requires_cutoff_day_corroboration` are candidates for a later cutoff-bounded price table. Rows marked `exclude_from_general_price_chart`, `exclude_until_cutoff_status_resolved`, or `exclude_from_cutoff_book` must not enter broad price-quality comparisons.

## Result

This pass improves the data pipeline by converting a captured page into auditable rows with row-level cutoff status. It does not claim that the listed prices were true on May 24, 2026.
