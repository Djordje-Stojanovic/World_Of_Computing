# Chapter 10/11 Open-Weight Frontier Visual Continuity Audit

Status: visual continuity audit, pass I-0137, 2026-05-25.

Purpose: decide how Chapters 10 and 11 should use visuals before adding more diagrams or screenshots. The audit covers Llama, Qwen, DeepSeek, GLM, Kimi/Moonshot, and currently unsupported source-gap labs. It improves visual decision quality; it does not add a new figure or raster asset.

## Current State

Chapter 10 has one committed diagram:

- `A-0030`, `llama-family-open-weight-map.svg`, a Llama release-and-claim map.

Chapter 11 has one committed diagram:

- `A-0031`, `china-open-model-source-map.svg`, a China/open-model source-permission map for Qwen, DeepSeek, GLM, Kimi, and source-gap lanes.

Both chapters also have acquisition-ready screenshot or source-screenshot slots:

- Chapter 10: `A-0044` through `A-0047` for Meta launch pages and the Llama GitHub surface.
- Chapter 11: `A-0048` through `A-0051` for Qwen and DeepSeek arXiv source pages.

This is a useful but risky state. The chapters are photo-rich on paper, but only as acquisition slots. They are diagram-thin, but the next diagram should not be another family timeline. Chapter 10 and Chapter 11 must not become two adjacent chapters of logos, dates, and caveat bands.

## Core Decision

Chapter 10 should own the **open-weight control stack**:

- weights
- license
- training transparency
- hosting burden
- safety and governance
- ecosystem work
- benchmark permission

Chapter 11 should own **source-permission lanes**:

- supported Qwen2/Qwen3 lane
- supported DeepSeek-V3/R1 lane
- supported GLM-4 lane
- supported Kimi k1.5 lane
- explicit source-gap lane for Qwen 3.5/3.6, DeepSeek V4-era claims, MiniMax, Baidu, Tencent, Xiaomi MiMo, and StepFun

That split keeps the chapters visually distinct. Llama becomes a strategy/control chapter. China/open-frontier becomes a source-permission and multipolar-frontier chapter.

## Figure Recommendations

### Chapter 10

Keep `A-0030` as Figure 10.1. It should remain a release-and-permission map, not a capability leaderboard.

The next best Chapter 10 diagram is not a second timeline. It is an **Open-Weight Control Stack** matrix:

- What is available: weights, code, model card, license, paper, repository, API, benchmarks.
- What remains controlled or unknown: training data, exact filtering, deployment scale, safety performance, current adoption, fine-tune quality, price-quality position.
- What shifts to the adopter: hosting, monitoring, updates, evals, security, governance.

Screenshot priority:

- First choice: `A-0047`, the Llama GitHub repository, because it shows open weights as a developer artifact.
- Second choice: `A-0044`, the original LLaMA launch page, because it anchors the research-release moment.
- Lower priority: `A-0045` and `A-0046`, unless final layout needs a release-sequence texture.

Caption boundary: mutable repository pages and launch pages do not prove adoption, popularity, license freedom, ecosystem size, or current deployment.

### Chapter 11

Keep `A-0031` as Figure 11.1. It should remain a source-permission map, not a model-ranking board.

The next best Chapter 11 visual is not a leaderboard. It is a **Supported vs Gap Source Board**:

- Qwen2/Qwen3 supported by `S-0026` and `S-0027`.
- DeepSeek-V3/R1 supported by `S-0028` and `S-0029`.
- GLM-4 supported by `S-0030`.
- Kimi k1.5 supported by `S-0031`.
- Qwen 3.5/3.6, DeepSeek V4-era systems, MiniMax, Baidu, Tencent, Xiaomi MiMo, and StepFun stay in a source-gap lane until cutoff-bounded primary evidence is captured.

Screenshot priority:

- First choice: `A-0049`, Qwen3 arXiv/source surface, because it shows the supported Qwen lane while protecting Qwen 3.5/3.6.
- Second choice: `A-0050` or `A-0051`, depending whether the chapter spread needs the DeepSeek-R1 reasoning bridge or the DeepSeek-V3 technical lane.
- Future candidate: add GLM and Kimi source-screenshot slots in a later acquisition pass if Chapter 11 remains visually overdependent on Qwen/DeepSeek.

Caption boundary: arXiv source surfaces prove provenance and source existence, not benchmark superiority, national rank, adoption, product traction, or market impact.

## Anti-Duplication Rules

- Do not add Chapter 10 and Chapter 11 family trees with the same visual grammar.
- Do not add a leaderboard unless exact model/date/task/source/rank scope is normalized elsewhere.
- Do not add a price-quality chart; Chapter 13 and Chapter 22 already carry that blocker.
- Do not turn Qwen, DeepSeek, GLM, and Kimi into a logo parade.
- Do not give unsupported labs a visual slot merely to satisfy breadth.
- Do not use screenshot slots as proof of popularity.

## Recommended Cross-Chapter Sequence

The strongest final visual rhythm is:

1. Chapter 10: Llama family release-and-permission map.
2. Chapter 10: one Meta source/developer screenshot, preferably GitHub or the original LLaMA launch page.
3. Chapter 11: China/open-model source-permission map.
4. Chapter 11: one Qwen or DeepSeek source screenshot.

This gives the book visual variety: a release map, a developer surface, a source-permission board, and a primary-source surface. It avoids stacking four similar diagrams or four similar web screenshots.

## Promotion Rationale

This audit improves the champion because the full-book visual inventory showed Chapters 10 and 11 as thin in committed diagrams but rich in acquisition slots. The pass prevents the obvious bad move: adding more logos, timelines, or leaderboard-like charts before source permissions are normalized. It assigns Chapter 10 to the open-weight control stack and Chapter 11 to source-permission lanes, which gives future visual work a cleaner division of labor.
