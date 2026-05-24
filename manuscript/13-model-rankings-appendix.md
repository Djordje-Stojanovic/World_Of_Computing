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

1. **Leaderboard Anatomy** - how rank is produced, where votes enter, and where caveats attach.
2. **Price-Quality Frontier** - model/provider rows plotted only after price and rank snapshots are captured.
3. **Context Window vs Price Basis** - context length, input price, output price, and caveat flags.
4. **Benchmark Caveat Matrix** - Arena, SWE-bench, LiveCodeBench, provider evals, and what each can/cannot prove.

The visual grammar's tradeoff-curve prototype should guide charts 2 and 3. `assets/visual_system/tradeoff-curve-prototype.svg` is a style guide, not data evidence. [A-0003]

## Promotion Rationale

Before this pass, the book had benchmark/ranking source ideas but no appendix data model. This pass adds the first ranking/pricing appendix, source registry, provisional matrix, and snapshot notes. It improves source integrity and chart provenance while refusing to promote a live leaderboard rank as stable truth.
