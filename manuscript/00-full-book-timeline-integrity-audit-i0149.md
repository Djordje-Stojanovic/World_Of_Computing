# Full-Book Chapter-Order And Timeline Integrity Audit

Status: promoted structure/truth audit, pass I-0149, 2026-05-26.

This pass re-baselines the whole book as a dated sequence. The current manuscript is much stronger than the older I-0110 continuity audit: all 24 outline slots now have substantial draft material or a dedicated synthesis draft, and the source/visual ledgers have enough rows to support a real timeline check. The remaining risk is not absence. It is drift.

## Executive Finding

The book's broad chronology works:

- public shock and mechanism backstory;
- early neural language modeling through Transformer and scaling;
- GPT/OpenAI/ChatGPT/Microsoft/Google platform competition;
- open weights and Chinese/frontier labs;
- benchmarks;
- hardware, GTC, datacenters, and data supply chains;
- tools, code, Claude Code, reasoning, economics, trust, and final synthesis through the May 24, 2026 cutoff.

The most serious defect is Chapter 12. The official outline still says "Europe, xAI, and the Rest of the Frontier," while later passes have built an Anthropic/Claude Chapter 12 lane with Constitutional AI, Claude family chronology, computer use, MCP, Claude Code bridge material, and screenshot acquisition. Both topics matter. They cannot both silently occupy the same chapter number in a finished 24-chapter book.

## Deliverables

- `data/full_book_timeline_integrity_audit_i0149.tsv` maps all 24 chapters to chronology spans, dated beats, source rows, cutoff status, handoff beats, risks, and next actions.
- `data/full_book_timeline_handoff_defects_i0149.tsv` lists the six structural defects that should steer the next structure/prose passes.

## Major Defects

1. `Chapter 12 conflict`: Decide whether Chapter 12 becomes Anthropic/Claude, a composite frontier-lab chapter, or Europe/xAI/rest-frontier with Anthropic relocated. Do this before the Chapter 12 prose placement pass.
2. `Early filename drift`: The live files for Chapters 2-4 are still numbered `01`, `02`, and `03`, which can confuse captions, references, and final layout.
3. `Roadmap laundering risk`: GTC 2026 roadmap and AI-factory slides must remain attributed stagecraft and roadmap evidence, not shipped-history evidence.
4. `Agent-loop repetition`: Chapters 18-20 need a clean escalation from tools to code to terminal/repository agents.
5. `Late-book essay risk`: Chapters 21-24 are ordered well, but they need handoffs that make reasoning cost, economics, trust, and human judgment feel like one machine.
6. `Global date-control gap`: Existing sources are strong locally, but this new table should become the compact chapter-date control surface for future passes.

## Promotion Rationale

This audit improves BookScore by protecting truth and structure before the next prose-polish wave. It does not add words or visuals, but it makes the 24-chapter sequence harder to break: every chapter now has a chronology span, source-row cluster, cutoff status, handoff beat, and named repair path. It also exposes the one structural contradiction that could otherwise survive until final layout.
