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

### 0. Motif Layer

Use the recurring motif system from I-0224 as a thin claim-control layer, not decoration. The seven approved motifs are token, prompt, time, chip, power, context, and agency. Each motif has a defined shape, palette role, chapter range, allowed use, blocked claims, and render rule in `data/recurring_motif_system_i0224.tsv`.

Core rule: a motif may recur only when it clarifies mechanism, chronology, source boundary, or blocked inference. If it merely makes a page look designed, remove it.

Reference atlas: `assets/visual_system/recurring-motif-atlas-i0224.svg`.

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

Whole-book spine package: `data/timeline_spine_package_i0225.tsv`, with master orientation art in `assets/visual_system/master-timeline-spine-i0225.svg` and chapter-strip atlas art in `assets/visual_system/chapter-timeline-strip-atlas-i0225.svg`.

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

## AI Factory Systems Spread

`A-0223` adds a wide systems-diagram grammar for the industrial chapters. It can connect user demand, training, model artifacts, inference serving, accelerators, networking/storage, software control, facility/cooling, power/interconnection, and token output on one page, but it must stay schematic until a separate quantitative chart supports any numbers.

Rules:

- Treat NVIDIA/GTC and DSX language as source-actor framing unless an independent source supports the same claim.
- Use power and facility sources for electricity, interconnection, cooling, and scenario language.
- Keep training and inference as related but distinct capacity loops.
- Never let the spread imply exact throughput, energy per token, cost per token, revenue, margin, PUE, water use, emissions outcome, deployed capacity, model quality, or productivity.

## Token Economics Boards

`A-0224` and `A-0225` extend the Chapter 22 economics grammar. Use the control board when the reader needs the whole meter-and-margin distinction; use the ladder when the prose is about service-contract choices such as fast answers, reasoning paths, tool calls, caching, or batch processing.

Rules:

- Exact prices require provider, model, source, snapshot date, pricing basis, and tier.
- OpenAI rows captured on 2026-05-25 remain audit evidence, not May 24 exact price truth, unless corroborated.
- Batch, cache, priority, long-context, data-sharing, and fine-tuning rows must not be merged into standard inference pricing.
- Margin, cost-per-token, revenue, utilization, ROI, productivity, price-quality frontier, hidden reasoning budget, and exact latency remain blocked unless separately sourced at the same scope.

## Figure IDs And Anchors

`data/full_book_figure_list_i0229.tsv` is the temporary canonical selected-figure ledger. Book-facing references use `Fcc.nn` IDs and `chcc-fignn` anchors; asset IDs remain production handles only.

Rules:

- Use the figure list before writing any figure cross-reference or render-smoke checklist.
- Update the figure list in the same pass as any selected-exhibit insertion, removal, or chapter move.
- Do not treat generated alt text as final accessibility proof; revise it during page layout when the exact crop and surrounding prose are known.
- Do not mark selected exhibits as publication-ready until render, rights, caption, and source-note gates pass.

## Render-Smoke Samples

`manuscript/render-smoke-sample-pages-i0230.html` is a lightweight smoke sheet for figure-family defects. It may be used to preview whether families are likely to fail before a full PDF render, but it is not a final page design.

Rules:

- Treat `data/render_smoke_defects_i0230.tsv` as open production debt until each defect is closed by a later page-flow, rights, capture, or render pass.
- Screenshot, source-screenshot, raw-slide, and photo placeholders must not become publication-ready merely because they appear in a smoke sheet.
- Source-card replacements should be tested in the page-flow mock before they replace selected screenshots or photos.
- Dense blocker grids and claim cards must keep caveat text legible at final trim.

## Page-Flow Mock

`data/full_book_visual_page_flow_mock_i0231.tsv` and `manuscript/full-book-visual-page-flow-storyboard-i0231.html` are the current full-book visual rhythm mock. They show chapter pressure and mock placement bands, not final pages.

Rules:

- Use white-space and fatigue labels to decide replacements, not to inflate figure count.
- Chapters marked `too_open` need source/scene relief only when rights and provenance are strong.
- Chapters marked `crowded` need pruning or substitution before full render.
- Late-book mechanism runs need human/source texture or prose breathing room before final layout.

## Competitor Benchmark Standard

`data/competitor_visual_benchmark_audit_i0232.tsv` and `data/competitor_visual_scorecard_i0232.tsv` define the current market-facing visual standard. The audit is qualitative: it compares *Next Token* against shelf expectations for semiconductor history, energy/infrastructure history, AI history, and product/company biography without asserting exact competitor figure counts.

Rules:

- Exceed chip-history expectations by making industrial constraints physical, not just schematic.
- Exceed energy-history expectations with useful maps or place cues only where they clarify bottlenecks.
- Exceed AI-history and biography expectations with product, source, lab, object, or human texture when provenance is strong.
- Treat company-sourced slides and product surfaces as source-actor evidence, not neutral proof.
- Cut or demote any figure that only demonstrates diligence and does not orient, prove, humanize, or slow the reader.
- Use the benchmark scorecard as an input to reader-addiction, rights, prose-around-figures, and visual-readiness passes.

## Reader-Addiction Visual Jobs

`data/reader_addiction_visual_audit_i0233.tsv` assigns every chapter a reader-effect job. This is a selection gate, not a decorative layer.

Rules:

- A visual should create shock, suspense, surprise, delight, clarity, memory, or responsibility.
- A figure that proves diligence but does not change the reader's state should move to apparatus, reserve, or source notes.
- Early sparse chapters may add texture only when it increases warmth or tension.
- Crowded industrial chapters should prune before they add.
- The final chapter must end on judgment and motif, not visual inventory.

## Prose Around Figures

`data/prose_around_figures_quality_i0234.tsv` defines bridge prose for high-risk exhibits. Use it during chapter assembly and layout editing.

Rules:

- The paragraph before a figure must tell the reader why to look.
- The paragraph after a figure must tell the reader what not to overread.
- Do not let captions carry all claim safety; surrounding prose must block the tempting inference too.
- Source-actor visuals need source-actor setup before the image and independent-evidence return after it.
- Final synthesis visuals must hand back to prose responsibility rather than ending on inventory.

## Promotion Rationale

Before this pass, the book had visual candidates but no visual grammar and no manifest-tracked diagrams. This pass adds the first three lightweight prototypes and establishes design rules for timelines, systems, family trees, tradeoffs, caveats, screenshots, and photo slots. It improves visual/data usefulness without introducing unsupported factual claims.
