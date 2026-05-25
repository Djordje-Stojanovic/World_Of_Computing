# Appendix Draft: Model Rankings, Prices, and Caveats

Status: promoted data appendix pass I-0006 on 2026-05-24.

Purpose: create the first auditable appendix package for model rankings and provider economics. This is not yet a finished leaderboard chart. It is a source-backed scaffolding for Chapter 13 and Chapter 22 that records where ranking, price, context-window, and caveat data must come from.

## Rule Of The Appendix

No model rank, price, context window, or benchmark-superiority claim should enter prose or charts unless the relevant source row has:

- source URL or local path,
- access date,
- model/version string,
- metric or price basis,
- capture status,
- caveat note,
- and, for live pages, a local snapshot note or screenshot/HTML capture path.

The reason is simple: leaderboards and prices change faster than book chapters. A model can move rank because another model was added, the vote pool changed, methodology changed, a provider changed aliases, or the page was crawled after the cutoff. A price can change because a provider repriced input/output tokens, cached input, batch processing, tool calls, long context, or regional services.

## Current Source Package

Data files created in this pass:

- `data/model_rankings_sources.tsv` - source registry for ranking, benchmark, provider pricing, and model-card pages.
- `data/model_rankings_matrix.tsv` - provisional rows for the appendix data model.
- `data/source_snapshots/model_rankings_snapshot_notes_2026-05-24.md` - snapshot notes and caveats for sources discovered by this pass.

These files are intentionally lightweight and commit-safe. They do not preserve full webpages or large screenshots. Future passes should add HTML/screenshot snapshots where rights and repository size permit, and must record any such assets in `assets_manifest.tsv`.

## Ranking Sources To Use

## Leaderboard Reading Sequence

The first leaderboard spread should teach how rank evidence is made before it shows any sorted model rows. The appendix is not a live crown for "the best model." It is an evidence path: votes become ratings only inside a stated config, split, category, publication date, and local snapshot, then a permission gate decides what prose the row can safely support.

Condensed glossary for the spread:

- **vote** - a human preference judgment used as Arena-style evidence, not a universal quality verdict.
- **config** - the row universe being read; A-0013 uses `text_style_control`.
- **split** - the selected dataset slice; A-0013 uses `latest`.
- **category** - the leaderboard filter; A-0013 uses `overall`, not coding, safety, latency, or enterprise quality.
- **rating** - the central estimated score under that config, split, category, date, and snapshot.
- **confidence interval** - the uncertainty band around a rating; overlapping intervals should be discussed as clusters.
- **publication date** - the date attached to the official historical rows; A-0013 uses rows published 2026-05-19.
- **snapshot** - the local evidence handle used for the manuscript, here S-0080/SNAP-20260525-008.
- **permission gate** - the editorial check that blocks release-status, price-quality, task-superiority, safety, latency, enterprise-usefulness, and broad "best model" inferences.

Place A-0014, `assets/visual_system/leaderboard-methodology-flow.svg`, before A-0013. Caption it:

> Figure 13.y - How Arena Rows Become Rank Claims. Human preference votes become chartable only after config, split, category, rating uncertainty, publication date, snapshot, and permission gates are visible.

After the methodology figure, the chart can make one narrow point: in the published `text_style_control` / `latest` / `overall` slice, the top rows were tightly clustered.

Then place A-0013, `assets/visual_system/lmarena-may19-text-style-control-top12.svg`. Caption it:

> Figure 13.x - Historical Arena dataset slice: `text_style_control`, `latest` split, `overall` category, top twelve rows published 2026-05-19 from S-0080/SNAP-20260525-008. Adjacent top rows should be read as an uncertainty-overlap cluster, not a live ranking.

Shared footnote directly below A-0013 or in the nearest sidenote:

> Model names in this figure are row labels in one historical dataset slice; they do not prove release status, pricing, API access, safety, latency, coding ability, enterprise usefulness, or broad model quality.

Compact prohibited-use note before any price or benchmark material: do not caption the pair as "the best models," "the current leaderboard," "price-performance frontier," "released frontier models," or "best coding/safety/enterprise systems." If the appendix later moves from this historical rank chart into prices, insert a hard divider stating that A-0013 is not a price-quality chart and that C-0046 remains active until a same-scope price/rank join is chart-ready.

Integration check for final layout: orientation paragraph, glossary, A-0014, narrow transition, A-0013, shared footnote, prohibited-use note, then any price-quality handoff. This order keeps methodology and permission gates in the reader's path before the sorted rows create drama.

## Ranking Sources To Use

### LMArena / Chatbot Arena

Use LMArena for human-preference ranking context, not as the single definition of "best model." The source package records both the Chatbot Arena methodology paper and live LMArena leaderboard pages. [S-0036] [S-0056] [S-0057]

Required caveats:

- human-preference votes reflect the prompt/user mix of the arena,
- rank can change with new models and votes,
- methodology and inclusion policy can change,
- aggregate rank hides task-specific performance,
- leaderboard pages can include multimodal or non-text arenas that should not be confused with LLM text ranking.

### Coding And Agent Benchmarks

Use SWE-bench and LiveCodeBench as coding-specific benchmark sources, with the Claude Code chapter's existing caveats. [S-0035] [S-0037]

Required caveats:

- harness configuration matters,
- contamination risk is real,
- "verified" subsets and agent scaffolds must be named,
- passing benchmark tasks is not the same as shipping production software.

### Provider Price And Context Sources

Use official provider pages first:

- OpenAI API pricing and model docs. [S-0058] [S-0059]
- Anthropic Claude pricing and Claude Code/model docs. [S-0060]
- Google Gemini API pricing. [S-0061]
- xAI model/pricing docs. [S-0062]
- Mistral model/API docs. [S-0063]

Required caveats:

- prices are per 1M tokens unless stated otherwise,
- input, cached input, output, batch, tool calls, grounding, and storage may have different rates,
- context-window claims require model-specific docs,
- provider console availability may differ by account or region,
- page contents can change after the cutoff.

## Chart Plan

This appendix should eventually produce four charts:

1. **Leaderboard Anatomy** - how rank is produced, where votes enter, and where caveats attach. Use A-0014 before A-0013, with the glossary and shared footnote above, so the historical `text_style_control` rows published 2026-05-19 read as a tight uncertainty-overlap cluster rather than a live crown.
2. **Price-Quality Frontier** - model/provider rows plotted only after price and rank snapshots are captured.
3. **Context Window vs Price Basis** - context length, input price, output price, and caveat flags.
4. **Benchmark Caveat Matrix** - Arena, SWE-bench, LiveCodeBench, provider evals, and what each can/cannot prove.

The visual grammar's tradeoff-curve prototype should guide charts 2 and 3. `assets/visual_system/tradeoff-curve-prototype.svg` is a style guide, not data evidence. [A-0003]

## Promotion Rationale

Before this pass, the book had benchmark/ranking source ideas but no appendix data model. This pass adds the first ranking/pricing appendix, source registry, provisional matrix, and snapshot notes. It improves source integrity and chart provenance while refusing to promote a live leaderboard rank as stable truth.
