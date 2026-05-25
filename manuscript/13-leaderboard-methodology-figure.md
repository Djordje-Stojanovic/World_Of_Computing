# Chapter 13 Figure Package: Leaderboard Methodology Flow

Pass: I-0039  
Asset: `assets/visual_system/leaderboard-methodology-flow.svg`  
Companion table: `data/leaderboard_methodology_i0039.tsv`

## Purpose

This figure should appear before any Chapter 13 leaderboard chart. It teaches the reader that an Arena rank row is not a natural property of a model. It is the result of a source pipeline: human preference votes, a selected config/split/category, rating estimates with uncertainty, a publication date, and a local snapshot.

## Use Rules

- Use with A-0013 or any future leaderboard chart.
- Always label config, split, category, publication date, source ID, and snapshot ID.
- Treat overlapping confidence intervals as clustered ranks, not as clean separations.
- Do not use this figure to support live May 24 ranks, product-release status, price-quality claims, or task-specific superiority.

## Caption Draft

Figure 13.y - How Arena Rows Become Rank Claims. Arena-style human preference votes become chartable only after filtering by config, split, category, publication date, and local snapshot. Source spine: S-0036, S-0056, S-0057, S-0080, SNAP-20260525-008; companion rows in `data/leaderboard_methodology_i0039.tsv`.
