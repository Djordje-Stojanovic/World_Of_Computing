# Model Rankings Snapshot Notes

Access date: 2026-05-24.

These notes are a lightweight source snapshot for pass I-0006. They are not a substitute for future HTML or screenshot capture. They record what was discoverable in this pass and which claims are safe to use.

## LMArena

- Source URL: `https://lmarena.ai/leaderboard/`
- Source IDs: S-0056, plus methodology source S-0036 and policy source S-0057.
- Capture status: notes only.
- Safe use now: cite LMArena as a live human-preference leaderboard source and explain why live rank requires snapshotting.
- Unsafe use now: exact rank chart in prose or figure without local screenshot/HTML capture.
- Caveats to preserve: prompt mix, user preference distribution, model inclusion policy, vote volume, methodology updates, category selection, and live page mutation.

## Provider Pricing

- OpenAI source URLs: `https://openai.com/api/pricing/`, `https://platform.openai.com/docs/models/gpt-4.1`
- Anthropic source URL: `https://platform.claude.com/docs/en/about-claude/pricing`
- Google source URL: `https://ai.google.dev/gemini-api/docs/pricing`
- xAI source URL: `https://docs.x.ai/docs/models`
- Mistral source URL: `https://docs.mistral.ai/models`
- Capture status: notes only.
- Safe use now: cite official provider pages as required sources for price/context tables.
- Unsafe use now: final price-quality chart without captured table rows and model-version IDs.

## Provisional Values Captured From Search Results

- OpenAI GPT-4.1 model docs search result reported a 1M token context window.
- Google Gemini pricing search result reported Gemini 2.5 Pro input at `$1.25` per 1M tokens for prompts up to 200k tokens.
- Google Gemini pricing search result reported Gemini 2.5 Flash input at `$0.30` per 1M text/image/video tokens and output at `$2.50` per 1M tokens including thinking tokens.

These provisional values are allowed in `data/model_rankings_matrix.tsv` as `supported_snapshot_note`, but not in final book charts until the source page is locally captured or otherwise archived.

## Next Capture Requirements

1. Save HTML or screenshots for LMArena text leaderboard, including timestamp and visible top rows.
2. Save official provider pricing pages for OpenAI, Anthropic, Google, xAI, and Mistral.
3. Normalize each model row to provider, model ID, access mode, context window, input price, cached input price, output price, batch price, tool-call caveats, and source ID.
4. Build a price-quality frontier only after both rank and price rows share the same access date or clearly labeled access dates.
5. Record every screenshot or rendered chart in `assets_manifest.tsv`.
