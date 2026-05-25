# Chapters 2-4 Early Technical Visual Plan

Status: visual planning pass, I-0139, 2026-05-26.

Purpose: close the early-technical visual gap identified by the full-book visual inventory without immediately adding generic diagrams. Chapters 2, 3, and 4 need mechanism visuals because later chapters now have many product, benchmark, economics, trust, and agent diagrams. The early book should teach the machinery that later figures assume.

This plan does not add new visual assets or increment the chart count. It defines the figure package to draw later.

## Current Gap

The full-book visual inventory shows Chapters 2, 3, and 4 with zero committed chapter-specific visuals. That is structurally dangerous because these chapters carry the technical foundation:

- Chapter 2 / `01-before-the-transformer.md`: sparsity, distributed representation, word vectors, sequence models, fixed-vector bottlenecks, and attention as relief.
- Chapter 3 / `02-attention-catches-fire.md`: Transformer self-attention, query/key/value mixing, positional encodings, multi-head attention, residual/feed-forward block grammar, and parallelism.
- Chapter 4 / `03-scaling-bet.md`: Kaplan-style scaling laws, GPT-3 as bounded example, Chinchilla compute/data balance, and the blocker that loss is not truth, safety, or product success.

The right move is not another chronology. It is a compact mechanism sequence.

## Recommended Package

### Figure 2.x: Pre-Transformer Bottleneck Map

Visual type: pressure-chain diagram.

Source spine: `S-0104`, `S-0105`, `S-0106`, `S-0107`, `S-0002`.

Story purpose: show the pressure chain that makes the Transformer feel earned rather than magically appearing:

- sparse counts and n-gram limits
- learned word representations
- recurrent sequence state
- encoder-decoder fixed-vector bottleneck
- attention as addressable context
- Transformer handoff

Caption contract: this is a pressure chain, not a complete NLP history or priority claim.

Blocked claims: first invention, exact state-of-the-art rankings, hidden industrial adoption, attention as consciousness, complete history of NLP.

### Figure 3.x: Self-Attention Information Flow

Visual type: architecture schematic.

Source spine: `S-0002`, `S-0108`.

Story purpose: give readers the missing mental model for attention:

- token embedding plus position signal
- query, key, and value projections
- query/key comparison
- attention weights
- weighted value mixture
- multi-head branch
- feed-forward/residual/layer-normalization wrapper

Caption contract: attention is a learned mixing operation, not a mind. The schematic is simplified from the original Transformer paper and is not a full modern LLM implementation.

Blocked claims: human intention, consciousness, truth, grounding, faithful explanation, distance-is-free, stable human-interpretable head roles, exact modern decoder-only implementation.

### Figure 4.x: Scaling Evidence-Lane Chart

Visual type: schematic curve plus permission lanes.

Source spine: `S-0003`, `S-0015`, `S-0004`, `S-0016`.

Story purpose: show the reader how to read scaling laws without turning them into prophecy:

- measured loss/performance lane
- modeled extrapolation lane
- industry interpretation lane
- bounded GPT-3/PaLM example lane
- blocked claims lane

Caption contract: loss is a map, not a product guarantee.

Blocked claims: exact exponents, plotted Kaplan values, universal token/parameter formulas, emergence thresholds, benchmark values, revenue, product success, safety, truth, cheap inference, or trust from scale.

## Optional Companion Figures

### Recurrence Versus Self-Attention

Use only if the self-attention schematic becomes too dense. This should contrast recurrent stepwise state passing with attention routes across positions and accelerator-friendly parallelism.

Blocked claims: context cost disappearance, parallelism-alone causality, long-context solved, product dominance from architecture alone.

### Compute-Data-Parameter Triangle

Use only if Chapter 4 needs a second figure. It should show compute allocation among model size, training tokens, and data/optimization quality.

Blocked claims: bigger-is-always-better, exact Chinchilla formula, universal token ratio, dataset-specific claims, compute as business proof.

## Anti-Duplication Rules

- Do not use a generic timeline.
- Do not reuse the Chapter 13/19/21 benchmark ladder grammar.
- Do not use the Chapter 18/20 agent-loop grammar.
- Do not use the Chapter 8/9/10/11 product-surface map grammar.
- Do not add decorative diagrams just to increase count.
- Do not let "attention" language drift into consciousness or intention.
- Do not let scaling curves imply truth, safety, revenue, or product inevitability.

## Later Build Order

1. Build `Pre-Transformer Bottleneck Map`.
2. Build `Self-Attention Information Flow`.
3. Build `Scaling Evidence-Lane Chart`.
4. Build optional companions only if render or reader flow proves the first three are insufficient.

## Promotion Rationale

This pass improves the champion because it turns a known zero-visual gap into a disciplined package plan. It gives the early chapters a distinct visual job: teach mechanism before the book enters company strategy, benchmarks, agents, infrastructure, and economics. It also prevents the obvious failure mode of drawing attractive but generic timelines that do not improve technical understanding.
