# Next Token Visual Grammar

Status: promoted visual-system pass I-0005 on 2026-05-24.

Purpose: define a consistent visual language for **Next Token** before chart production begins. This pass creates a grammar, not a finished art program. Every future chart, diagram, screenshot, photo slot, and extracted slide must still carry source/provenance in `assets_manifest.tsv`.

## Visual Thesis

The book should feel like a serious industrial history with a native computing interface: clear enough for repeated reference, elegant enough for prize nonfiction, and precise enough that every image earns its space. The visual system should avoid generic "AI glow" cliches. It should show mechanisms, timelines, systems, tradeoffs, evidence, and physical infrastructure.

Core rule: every visual must answer one of five reader questions.

1. What changed over time?
2. How does this system work?
3. Who or what is related to whom?
4. What is the tradeoff or ranking?
5. Where is the hidden physical or economic substrate?

## Palette

Use a restrained multi-hue palette, not a one-note blue/purple gradient.

- Ink: `#1f2933` for text and axes.
- Paper: `#f7f4ee` for warm page background.
- Rule: `#c8c1b5` for subtle dividers and gridlines.
- Compute blue: `#2563eb` for model/compute paths.
- Signal green: `#0f8b6f` for data, retrieval, and validated evidence.
- Heat red: `#c2412d` for risk, failure, cost pressure, and caveats.
- Brass: `#b7791f` for institutions, money, and power.
- Violet: `#6d5bd0` only as a secondary accent, never the dominant system.

Accessibility rule: charts must remain readable in grayscale by varying stroke weight, shape, labels, and direct annotation rather than relying only on color.

## Type And Layout

- Primary chart typeface target: a clean humanist sans for labels, with a serif companion only in book layout, not inside dense charts.
- Minimum print label size target: 7.5 pt equivalent for secondary labels; 9 pt equivalent for primary labels.
- Prefer direct labeling over legends when space allows.
- Put source/provenance below every figure in small but readable text.
- Avoid crowded chart titles. Use active, factual figure titles.
- Use consistent 16:9 SVG artboards for widescreen diagrams and 4:3 or portrait artboards for book-page figures.

## Recurring Visual Families

### 1. Chronology Rails

Use for chapter timelines, launch sequences, and source chronologies.

Grammar:

- Horizontal rail.
- Event nodes by category: paper, model, product, hardware, infrastructure, benchmark.
- Short labels above or below the rail.
- Highlight the chapter's narrative pivot in brass or heat red.
- Include a cutoff marker when the figure reaches May 24, 2026.

First uses:

- ChatGPT launch-to-platform timeline.
- GPT-1 to GPT-4 lineage.
- Claude Code and coding-agent chronology.
- GTC 2026 roadmap vs shipped status.

Prototype: `assets/visual_system/chronology-rail-prototype.svg`.

### 2. System Stack Diagrams

Use for mechanisms: Transformer block, RLHF, RAG, tool use, coding-agent loops, AI factories.

Grammar:

- Left-to-right flow for process.
- Vertical stack for infrastructure layers.
- Separate model, data, tool, human, and hardware layers by color and shape.
- Use callouts for failure modes and verification points.

First uses:

- RLHF pipeline.
- Coding-agent repository lifecycle.
- Power-to-token flow.
- RAG/tool loop.

Prototype: `assets/visual_system/agent-loop-prototype.svg`.

### 3. Family Trees And Landscapes

Use for model families, labs, open-weight diffusion, and Chinese frontier systems.

Grammar:

- Tree when lineage matters.
- Matrix when access/licensing/capability matters.
- Map-like landscape only when geography or ecosystem clusters matter.
- Every family tree must distinguish model, product, and company.

First uses:

- Llama open-weight family.
- Qwen/DeepSeek/GLM/Kimi/MiniMax landscape.
- Google/DeepMind Gemini lineage.

### 4. Tradeoff Curves

Use for scaling laws, price/performance, latency/cost, data/compute balance, and inference economics.

Grammar:

- Clean axes with units.
- Sparse grid.
- Directly label inflection points.
- Use shaded uncertainty/caveat bands where data is partial.
- Never chart live prices or leaderboard rank without a source snapshot and access date.

First uses:

- Scaling-law curve.
- Price-quality frontier.
- Token-price trend.
- Train-time vs test-time compute.

Prototype: `assets/visual_system/tradeoff-curve-prototype.svg`.

### 5. Evidence And Caveat Panels

Use wherever the book risks false precision.

Grammar:

- Small boxed sidebars attached to a chart.
- Include source status: primary, secondary, snapshot needed, support pending.
- Use heat red sparingly for unsupported or contested claims.

First uses:

- Benchmark caveat chart.
- Qwen 3.5/3.6 and DeepSeek V4 support-pending notes.
- GTC announced-vs-shipped status.

## Photo And Screenshot Slots

The book target is now at least 100 curated visual/source exhibits across charts, diagrams, photos, screenshots, extracted slides, paper-figure redraws, source-page screenshots, and short source-excerpt cards. This visual grammar does not add raster assets. It creates slots and rules.

High-value slot types:

- Product screenshots: ChatGPT, Claude Code, benchmark pages, provider dashboards, model cards.
- Presentation extracts: GTC 2026 keynote, with page-level provenance.
- Hardware/infrastructure photos: GPUs, racks, datacenters, power equipment, only when sourced and relevant.
- Documentary screenshots: official repos, docs, release pages, benchmark pages, pricing pages.

Rules:

- Never use a screenshot without source URL/path, access date, and story purpose.
- Never use a found photo as decorative atmosphere.
- Never crop away the evidence-bearing part of a screenshot.
- For private-use visuals, record rights/private-use note in `assets_manifest.tsv`.

## Chapter-Level Visual Quota

Working target: at least 100 curated visual/source exhibits, averaging 3-4 strong candidates per chapter before final layout selection.

Initial exhibit mix:

- Chapter-opening micro-timelines or chapter maps where they clarify the reading path.
- Mechanism diagrams for architecture, tools, data, evaluation, economics, and infrastructure.
- Model/lab family trees or landscapes where lineage or ecosystem position matters.
- Benchmark, scaling, economics, and evidence-lane charts where the data is scoped.
- Infrastructure, power, chip, fab, and physical-system visuals where they explain LLM scaling.
- Evidence/caveat panels and source-excerpt cards where the reader needs claim discipline.
- Product, documentation, source-page, GTC, paper, benchmark, dataset, and interface screenshots when the actual surface carries history.

This allocation is adjustable, but every future pass should improve the curated exhibit program rather than merely increasing raw asset count. Every exhibit must have provenance, rights status, story purpose, and blocked-claim language before final layout use.

## Promotion Rationale

Before this pass, the book had visual candidates but no visual grammar and no manifest-tracked diagrams. This pass adds the first three lightweight prototypes and establishes design rules for timelines, systems, family trees, tradeoffs, caveats, screenshots, and photo slots. It improves visual/data usefulness without introducing unsupported factual claims.
