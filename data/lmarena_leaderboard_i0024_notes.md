# LMArena Leaderboard Row Normalization Notes - I-0024

Pass I-0024 inspected `SNAP-20260524-001` / `S-0056`, the local LMArena leaderboard HTML capture at `data/source_snapshots/2026-05-24/2026-05-24__S-0056__live-leaderboard__lmarena-text-leaderboard__html.html`.

## Finding

The captured HTML is useful, but not clean cutoff-day chart data. The visible model-title stream includes many names that are plainly inconsistent with a May 24, 2026 book cutoff, including `gpt-5.5-high`, `gemini-3.1-pro-preview`, `claude-opus-4-7-thinking`, and `deepseek-r1-0528`. Because the same artifact contains cutoff-plausible and post-cutoff-looking rows, exact ranks should remain quarantined until a clean cutoff-bounded capture or corroborating archive is available.

## Method

- Used only the local HTML snapshot already recorded in `data/source_snapshot_protocol.tsv`.
- Normalized a conservative subset of visible title-order rows into `data/lmarena_leaderboard_rows_i0024.tsv`.
- Split rows into exclusion examples, cutoff-status-unclear examples, and cutoff-plausible candidate rows.
- Preserved `visible_order` as an audit handle, not as final arena rank.
- Left C-0045 open because final chart use still needs a clean cutoff-bounded snapshot, category/filter confirmation, methodology notes, and exact score/rank extraction.

## I-0029 Update

Pass I-0029 did not repair this polluted live HTML artifact. It added a cleaner official historical dataset alternate in `data/lmarena_clean_cutoff_rows_i0029.tsv` / SNAP-20260525-008. Use the I-0024 rows only as audit evidence for live-page contamination; use the I-0029 rows for chart candidates labeled as `text_style_control`, `overall`, published 2026-05-19.

## Use Rules

Rows marked `exclude_from_cutoff_rank_chart` must not enter the book's May 24 ranking charts. Rows marked `candidate_only_requires_clean_cutoff_snapshot` may guide future extraction and cross-checking, but they are not chart-ready until the capture pollution is resolved.
