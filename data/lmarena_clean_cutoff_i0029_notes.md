# I-0029 LMArena Clean Cutoff Dataset Notes

Pass date: 2026-05-25

Purpose: replace the polluted live-page HTML evidence from SNAP-20260524-001 with a cleaner cutoff-bounded official dataset artifact for future model-ranking charts.

## Source

- Source ID: S-0080
- Snapshot ID: SNAP-20260525-008
- Dataset: `lmarena-ai/leaderboard-dataset`
- Endpoint captured: `https://datasets-server.huggingface.co/rows?dataset=lmarena-ai%2Fleaderboard-dataset&config=text_style_control&split=latest&offset=0&length=100`
- Raw JSON: `data/source_snapshots/2026-05-25/2026-05-25__S-0080__historical-dataset__lmarena-text-style-control-latest__json.json`
- Normalized rows: `data/lmarena_clean_cutoff_rows_i0029.tsv`

## Result

The normalized table contains 100 `overall` rows from the `text_style_control` config. Every row has `leaderboard_publish_date` `2026-05-19`, which is before the book cutoff of 2026-05-24.

This makes the rows usable as candidate chart data only with a precise date label: **LMArena/Arena historical text-style-control leaderboard, overall category, published 2026-05-19**.

## Caveats

- This is not a live May 24 screenshot.
- This does not repair SNAP-20260524-001; that artifact remains useful only as polluted live-page audit evidence.
- Do not mix these ranks with non-style-controlled text rows, code, search, vision, or other arena categories.
- Any final chart must include the dataset config, category, publish date, source ID, and snapshot ID.
