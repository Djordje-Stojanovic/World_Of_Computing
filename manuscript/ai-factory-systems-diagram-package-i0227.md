# AI Factory Systems Diagram Package - I-0227

Pass I-0227 builds a wider systems spread around the existing Chapter 15 AI-factory stack and Chapter 16 power-to-token flow. The new package treats an "AI factory" as an explainable service machine: user demand enters as prompts, API calls, code-agent tasks, and queued work; training and post-training produce model artifacts; serving converts artifacts plus requests into streamed tokens and actions; chips, networking, software, cooling, facilities, power, and metering make the invisible chat surface physically possible.

The package adds three source-side controls:

- `data/ai_factory_system_package_i0227.tsv` defines ten layers from demand to token output, with source anchors, allowed visual language, and blocked claims.
- `data/ai_factory_system_edges_i0227.tsv` defines thirteen flows so the diagram has verbs instead of decorative boxes.
- `data/ai_factory_system_actions_i0227.tsv` defines eight gates for final page proof, NVIDIA source-actor attribution, independent power sourcing, schematic-vs-quantitative boundaries, motif use, and figure-selection discipline.

The new planning asset is `A-0223`, `assets/visual_system/ai-factory-system-layers-i0227.svg`. It is meant as a signature-spread candidate, not a final page proof. Its strongest use is as a cross-chapter bridge: Chapter 14 explains the hardware/software substrate, Chapter 15 explains NVIDIA's GTC source-actor argument, and Chapter 16 tests the physical power and facility constraints.

## Claim Contract

Allowed:

- Explain the AI factory as a stack of demand, model training, release gates, inference serving, accelerator systems, networking/storage, software, facilities, power, and token output.
- Attribute AI-factory thesis, DSX, token-economics, roadmap, partner, and performance language to NVIDIA/GTC when those are the sources.
- Use independent power/facility sources for electricity-demand, interconnection, cooling, and local-load language.

Blocked:

- Exact training cost, FLOPs, utilization, throughput, energy-per-token, cost-per-token, revenue, margin, PUE, water use, emissions outcome, delivered power, customer deployment, model quality, benchmark crown, or productivity claims.
- Treating NVIDIA's AI-factory rhetoric as neutral proof that the economics, performance, deployment scale, or power solution already exists.
- Treating scenario/forecast sources as happened history beyond the May 24, 2026 cutoff.

Promotion rationale: this pass improves the book's industrial explanation by integrating software demand, model production, serving, chips, networking, cooling, power, and economics into one auditable visual grammar without adding unsupported numbers.
