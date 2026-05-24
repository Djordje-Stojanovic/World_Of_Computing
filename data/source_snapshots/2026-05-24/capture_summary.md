# Source Snapshot Capture Summary

Pass: I-0011

Access date: 2026-05-24

Purpose: capture local, commit-safe snapshots for mutable leaderboard, pricing, and model-documentation pages used by the model-rankings appendix.

## Captured HTML

- SNAP-20260524-001 / S-0056: LMArena leaderboard HTML captured at `data/source_snapshots/2026-05-24/2026-05-24__S-0056__live-leaderboard__lmarena-text-leaderboard__html.html`.
- SNAP-20260524-003 / S-0060: Anthropic Claude API pricing HTML captured at `data/source_snapshots/2026-05-24/2026-05-24__S-0060__pricing-page__anthropic-claude-api-pricing__html.html`.
- SNAP-20260524-004 / S-0061: Gemini Developer API pricing HTML captured at `data/source_snapshots/2026-05-24/2026-05-24__S-0061__pricing-page__gemini-developer-api-pricing__html.html`.
- SNAP-20260524-005 / S-0062: xAI models/pricing documentation HTML captured at `data/source_snapshots/2026-05-24/2026-05-24__S-0062__pricing-page__xai-models-and-pricing__html.html`.
- SNAP-20260524-006 / S-0063: Mistral model documentation HTML captured at `data/source_snapshots/2026-05-24/2026-05-24__S-0063__model-docs__mistral-model-docs__html.html`.

## Blocked Capture

- SNAP-20260524-002 / S-0058: OpenAI API pricing shell HTML capture returned HTTP 403 despite browser-like headers. A local capture note is stored at `data/source_snapshots/2026-05-24/2026-05-24__S-0058__pricing-page__openai-api-pricing__capture-note.txt`.
- The official OpenAI pricing page was browser-readable during the pass, but because the local shell capture failed, final OpenAI price rows remain support-pending until a browser screenshot, alternate official docs capture, or approved manual archival path is recorded.

## Safe Use

These captures improve provenance, but they are not yet final chart data. Before a price-quality frontier or exact leaderboard table is promoted, future passes must normalize table rows, record model/version strings, preserve pricing caveats, and cite snapshot IDs in the data matrix.
