# Provider Pricing Normalization Notes - I-0026

Pass I-0026 normalized a conservative subset of provider pricing rows from the local cutoff-day snapshots already recorded in `data/source_snapshot_protocol.tsv`.

## Scope

- Anthropic rows come from SNAP-20260524-003 (`S-0060`) and preserve base input, cache-hit, and output prices. Five-minute and one-hour cache-write prices were not folded into the general cached-input field because they are a different billing action.
- Google Gemini rows come from SNAP-20260524-004 (`S-0061`). Gemini 2.5 Pro long-context tiers are split into separate rows, and Gemini 2.5 Flash rows are limited to text/image/video pricing because audio uses a different rate.
- xAI rows come from SNAP-20260524-005 (`S-0062`). The captured models page exposes Grok 4.3 input and output prices, but does not expose cache or batch terms in the same model-card section.
- Mistral remains intentionally unpriced. SNAP-20260524-006 (`S-0063`) is model documentation, not pricing evidence.

## Publication Rule

`data/provider_pricing_rows_i0026.tsv` is candidate chart input, not final price-quality evidence. C-0046 remains needs-verification until these provider rows are joined to same-scope ranking rows, non-comparable batch/cache/tier rows are separated, and any remaining provider-specific billing semantics are explained in chart notes.
