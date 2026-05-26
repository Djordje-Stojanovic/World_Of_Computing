# Full-Book Unsupported-Claim Burn-Down Board

Status: claim audit, pass I-0150, 2026-05-26.

This pass turns unsupported, soft, blocked, and tempting claims into an executable burn-down board. It does not resolve the blockers. It makes the work visible enough that future prose, visual, and source passes can drive the unsupported-claim count toward zero instead of hiding uncertainty in fluent paragraphs.

## Live Ledger State

Fresh import of `claims.tsv` shows:

- `161` supported rows.
- `8` needs-verification rows.

The eight live blockers are still the same dangerous core: `C-0007`, `C-0010`, `C-0013`, `C-0021`, `C-0029`, `C-0044`, `C-0046`, and `C-0047`. They cover frontier-release chronology, ChatGPT adoption/reception, Claude 4 benchmark numbers, NVIDIA/GTC performance and roadmap claims, GPT-3/Copilot adoption-productivity claims, Chapter 6 quote/policy exactness, and provider price-quality joins.

## Deliverables

- `data/full_book_unsupported_claim_burndown_i0150.tsv` gives 20 burn-down rows: the 8 live claim-ledger blockers plus 12 chapter-level tempting-claim families.
- `data/full_book_unsupported_claim_burndown_summary_i0150.tsv` groups those rows into 8 work queues.

## Highest-Risk Work Queues

1. `Live needs-verification rows`: resolve, support, quarantine, or delete the eight active rows before final prose/layout.
2. `Chapter 12 structure`: decide whether Anthropic/Claude, Europe/xAI, and rest-of-frontier occupy one composite chapter or move into explicit homes.
3. `Outcome claims`: adoption, revenue, ROI, productivity, named customers, replacement, enterprise impact, and margin must never be inferred from product pages, screenshots, demos, benchmark scores, or vendor docs.
4. `Benchmark and price-quality claims`: every rank, benchmark, and price-quality sentence needs model/version/date/task/scaffold/price-basis fields.
5. `GTC and physical-infrastructure claims`: slides, specs, and photos are source surfaces unless separately corroborated; they do not prove deployment, energy-per-token, facility performance, supply, or market power.
6. `Safety, trust, and autonomy`: screenshots and docs can show product direction and workflow, not solved safety, reliable autonomy, MCP dominance, secure-by-default agents, or mitigation prevalence.

## Promotion Rationale

This audit improves the book by converting claim anxiety into a usable queue. The board is deliberately unforgiving: if a claim cannot be supported with same-scope evidence, the fastest route is often quarantine or deletion, not more elegant prose. That discipline is now explicit before the next wave of chapter-polish passes.
