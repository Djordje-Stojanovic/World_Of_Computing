# Token Economics Visual Package - I-0228

Pass I-0228 turns the Chapter 22 economics material into a reader-facing visual system for "intelligence on tap." The existing chapter already had four core exhibits: token meter, routing/caching/batching levers, subscription/API/bundle routes, and margin/ROI blockers. This pass adds a synthesis layer so those exhibits can read as one mechanism rather than four separate warnings.

New package files:

- `data/token_economics_package_i0228.tsv` defines twelve economic surfaces: training tokens, input tokens, cached input, output tokens, context window, reasoning/test-time compute, latency, routing, batching, smaller-model/distillation choices, sales channel, and margin/marginal-cost blockers.
- `data/token_economics_diagram_plan_i0228.tsv` defines two new planning assets.
- `data/token_economics_actions_i0228.tsv` records eight gates for cutoff pricing, tier scope, reasoning claims, context-window claims, margin language, figure selection, and render proof.
- `A-0224`, `token-economics-control-board-i0228.svg`, is the chapter control board.
- `A-0225`, `token-economics-cost-latency-ladder-i0228.svg`, is the service-contract ladder for fast, think, tool, cache, and batch paths.

## Claim Contract

Allowed:

- Explain token economics as a visible meter wrapped around hidden cost surfaces.
- Separate training tokens from inference tokens.
- Show input, cached input, and output tokens as distinct public meter lanes when source scope is labeled.
- Show context length, reasoning/test-time compute, caching, batching, routing, and latency as service-contract levers.

Blocked:

- Live prices without dated snapshot labels.
- OpenAI May 24 exact price truth from rows captured on May 25 without corroboration.
- Provider margin, cost per token, revenue, profitability, utilization, customer ROI, active use, productivity, price-quality frontier, exact latency, exact hidden reasoning budget, or guaranteed savings.
- Treating batch, cache, priority, long-context, data-sharing, or fine-tuning rows as interchangeable standard inference prices.

Promotion rationale: this improves Chapter 22's concreteness and surprise without weakening truth. The reader can now see why a token price table is not an economics proof, and why context, reasoning, caching, batching, routing, latency, and market channel are part of the same machine.
