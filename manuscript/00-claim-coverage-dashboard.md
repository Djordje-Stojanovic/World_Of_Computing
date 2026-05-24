# Claim Coverage Dashboard

Status: promoted data pass I-0014 on 2026-05-24; refreshed by source-capture pass I-0016 on 2026-05-25.

This dashboard turns the project ledgers into a recurring quality gate. It does not make new historical claims about LLMs; it exposes which existing claims are supported, which claims are still quarantined, and where chapter drafts are drifting away from the source-density target.

## Current Snapshot

- Claims audited: 40.
- Supported claims: 32.
- Needs-verification claims: 8.
- Source rows: 72.
- Primary or local-primary source rows: 72.
- Captured snapshot rows: 7.
- Snapshot gap rows: 5.
- Visual asset rows: 10.
- Main chapter count: 24.
- Pending idea rows after pass I-0016: 5.

The eight needs-verification rows are C-0007, C-0010, C-0013, C-0017, C-0018, C-0021, C-0029, and C-0033. They should be treated as a work queue, not as acceptable residue.

## Priority Groups

First priority: mutable rank and price facts. C-0017 and C-0018 block exact LMArena, provider-pricing, and price-quality chart claims until same-date snapshots are normalized into rows with model names, filters, access dates, and caveats. C-0031's no-local-capture gap is resolved by SNAP-20260525-001, but OpenAI API pricing still cannot be used for exact cutoff-day chart rows until post-cutoff model rows are filtered and caveats are normalized.

Second priority: benchmark and performance claims. C-0013, C-0021, and C-0033 should stay caveated until benchmark harnesses, NVIDIA keynote slide wording, roadmap status, availability language, and independent triangulation are separated. The GTC material is valuable, but the book must label NVIDIA claims as NVIDIA claims.

Third priority: source-exactness gaps. C-0007, C-0010, and C-0029 need cutoff-bounded support before they become clean prose: Qwen/DeepSeek frontier-release naming, ChatGPT adoption and reception, and GPT-3 API/Copilot ecosystem figures.

## Chapter Source Density

The prose-draft chapters are close to the target:

- Chapter 5, `05-gpt-1-to-gpt-3-door-opens.md`: 1,919 words, 9 unique source references, 213.2 words per source, target band.
- Chapter 7, `07-chatgpt-interface-event.md`: 2,282 words, 9 unique source references, 253.6 words per source, slightly sparse.
- Chapter 20, `20-claude-code-industrialized-pair-programming.md`: 2,050 words, 13 unique source references, 157.7 words per source, target band.

Appendices, protocols, source packs, and scaffolds are not judged as prose-density targets, but they still carry claim rows when they make project-control assertions or quarantine factual risks.

## Snapshot Notes

The source-snapshot protocol has seven captured rows and five gap rows. The gap list includes captured-but-not-normalized rows, the post-cutoff OpenAI alternate-docs capture, and local PDF render/caption caveats. A captured file is evidence that a page was saved; it is not yet permission to publish exact rank, price, context-window, performance, or availability claims.

## Promotion Gates

- No new factual chapter should be promoted without claim rows and source IDs for its major assertions.
- Exact rank, price, benchmark, performance, and context-window claims remain blocked until normalized from snapshots or triangulated sources.
- Private-use visual evidence can support internal drafting only after `assets_manifest.tsv` records source, provenance, caption intent, and story purpose.
- Unsupported factual claim count must keep trending toward zero before any full-book render or final layout pass.
