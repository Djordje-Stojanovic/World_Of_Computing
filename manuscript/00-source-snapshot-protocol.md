# Source Snapshot Protocol

Status: promoted sourcing protocol pass I-0009 on 2026-05-24.

Purpose: define the book-wide capture rules for live or mutable sources: model cards, system cards, product docs, pricing pages, leaderboards, benchmark dashboards, repository pages, and provider consoles. This protocol exists because the book's factual cutoff is fixed at 2026-05-24, while many source pages continue to change.

## Scope

Use this protocol before turning any mutable source into:

- a direct quotation,
- an exact rank, score, price, context-window, throughput, latency, or release-status claim,
- a chart row,
- a screenshot/photo slot,
- a caption,
- or a claim-ledger row marked `supported`.

Stable papers, PDFs, filings, archived release posts, and local files still need source IDs and access dates, but they do not need full live-page capture unless their public landing page is the source of the claim.

## Storage

Snapshots must be commit-safe unless a later pass explicitly records a private-use heavy asset outside Git.

Preferred locations:

- `data/source_snapshots/YYYY-MM-DD/` for lightweight HTML, Markdown notes, text extracts, JSON/API outputs, hashes, and manifest TSVs.
- `assets/source_snapshots/YYYY-MM-DD/` for screenshots or other visual snapshots that must also appear in `assets_manifest.tsv`.
- `data/source_snapshots/` for protocol files and cross-date README notes.

Canonical filename shape:

```text
YYYY-MM-DD__SOURCEID__source-kind__short-slug__capture-method.ext
```

Examples:

```text
2026-05-24__S-0056__live-leaderboard__lmarena-text-leaderboard__screenshot.png
2026-05-24__S-0058__pricing-page__openai-api-pricing__html.html
2026-05-24__S-0060__pricing-page__anthropic-claude-api-pricing__md.md
2026-05-24__S-0059__model-docs__openai-gpt-4-1__text.txt
2026-05-24__S-0001__local-pdf__gtc-2026-keynote-p45__render-note.md
```

Rules:

- Use lowercase slugs with hyphens.
- Put the source ID near the front so files sort by evidence chain.
- If a source supports multiple tables, capture once and reference many rows.
- If a page requires dynamic rendering, preserve both the browser screenshot and a short capture note explaining what was visible.
- If a provider console is account-specific, label it `console-limited` and do not generalize it without a public source.

## Required Metadata

Every snapshot set should have a TSV row in `data/source_snapshot_protocol.tsv` or a date-specific manifest with the same fields:

- `snapshot_id`
- `status`
- `source_ids`
- `source_kind`
- `title_or_page`
- `url_or_path`
- `accessed_at`
- `capture_method`
- `local_path`
- `content_hash`
- `quote_limit_words`
- `allowed_use`
- `cutoff_status`
- `claims_supported`
- `asset_ids`
- `caveats`

Field guidance:

- `snapshot_id`: use `SNAP-YYYYMMDD-NNN`.
- `status`: `planned`, `captured`, `superseded`, `rejected`, or `external_archive`.
- `source_ids`: semicolon-separated `sources.tsv` IDs.
- `source_kind`: `model_card`, `system_card`, `documentation`, `pricing_page`, `live_leaderboard`, `benchmark_dashboard`, `repo`, `api_output`, `local_pdf`, or `press_page`.
- `accessed_at`: ISO timestamp with timezone when known; date-only is acceptable for manual notes.
- `capture_method`: `html`, `screenshot`, `pdf_print`, `markdown_note`, `text_extract`, `api_json`, `hash_only`, or `external_archive`.
- `content_hash`: SHA256 for local files when feasible; `pending` for planned rows.
- `quote_limit_words`: default `25` for public web pages unless a stricter source limit applies; `0` for screenshot-only or no-quote captures.
- `allowed_use`: `paraphrase_only`, `short_quote_ok`, `data_row_ok`, `chart_ok_after_normalization`, `caption_ok`, or `private_visual_reference`.
- `cutoff_status`: `pre_cutoff_artifact`, `cutoff_day_capture`, `post_cutoff_page_for_pre_cutoff_artifact`, `roadmap_or_announced`, or `support_pending`.
- `claims_supported`: semicolon-separated claim IDs, or `none_yet`.
- `asset_ids`: semicolon-separated asset IDs for screenshots/images, or `none`.
- `caveats`: the exact warning future prose must preserve.

## Quote Limits

The default rule is paraphrase first. Direct quotations from mutable web pages are allowed only when the wording itself matters and the capture row says `short_quote_ok`.

Book-wide limits:

- Do not paste full pages into manuscript files.
- Do not use long verbatim excerpts from live docs, pricing pages, leaderboards, blog posts, or model cards.
- Keep any single direct quotation from one public non-lyrical source to 25 words or fewer unless a stricter project or legal rule applies.
- Record the quote-bearing source ID and snapshot path near the claim before final prose promotion.
- For pricing/rank/model-card data, prefer normalized data rows over quotation.

If a page is only needed for chart data, capture the table or screenshot, normalize the rows in a separate TSV, and cite the snapshot ID in the chart notes.

## Capture Methods

Preferred order by source type:

- Model/system cards: save official PDF or page HTML when available; add text notes for model name, release date, context, modalities, eval caveats, and safety caveats.
- Documentation: save HTML or Markdown/text extract; record page version if visible.
- Pricing pages: save screenshot plus HTML/text extract when feasible; normalize input, cached input, output, batch, tool, storage, grounding, and regional caveats separately.
- Leaderboards: save screenshot with visible date/time if possible; record selected category, filters, top rows, methodology link, and whether the page is text-only or multimodal.
- Benchmark dashboards: save visible configuration, model list, score columns, date, and methodology link; record contamination or harness caveats.
- Repositories: save commit hash, release tag, license, README excerpt path, and archive URL if available.
- Local PDFs: record local path, page numbers, SHA256, and any rendered private-use image path.

## Ledger Updates

After capture:

- Update `sources.tsv` notes from "snapshot before use" to the actual snapshot path if the source has become claim-ready.
- Update `claims.tsv` only when the source supports a concrete claim, not merely because it was captured.
- Update `assets_manifest.tsv` for every screenshot, rendered slide, or visual snapshot.
- Update chapter appendices or data matrices with `snapshot_id`, source ID, access date, and caveat fields.
- Keep heavyweight captures out of Git unless explicitly approved; commit lightweight manifests, notes, hashes, and normalized tables.

## Validation Checklist

Before a snapshot-supported claim is promoted:

1. The source artifact predates or is valid through the 2026-05-24 cutoff, or the row explicitly says `post_cutoff_page_for_pre_cutoff_artifact`.
2. The local path exists or the row explains why the capture is an external archive.
3. The access date is present.
4. The filename includes date, source ID, source kind, slug, and method.
5. The claim or chart row cites the snapshot ID.
6. The caveat field names any live-page, ranking, pricing, region, model-version, or methodology limitation.
7. Quoted language is short, necessary, and traceable.

## Promotion Rationale

Pass I-0009 raises the sourcing floor: future leaderboard, pricing, docs, and model-card work now has a repeatable naming scheme, metadata schema, quote rule, and ledger path. It improves claim coverage and visual provenance without pretending that a live page is stable historical evidence.
