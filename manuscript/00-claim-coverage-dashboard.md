# Claim Coverage Dashboard

Status: promoted data pass I-0014 on 2026-05-24; refreshed by source-capture pass I-0016, caption/provenance pass I-0017, chapter-draft pass I-0018, claim-audit pass I-0019, source-density pass I-0020, OpenAI pricing-normalization pass I-0021, GTC chapter-opening pass I-0022, and alignment-visual pass I-0023 on 2026-05-25.

This dashboard turns the project ledgers into a recurring quality gate. It does not make new historical claims about LLMs; it exposes which existing claims are supported, which claims are still quarantined, and where chapter drafts are drifting away from the source-density target.

## Current Snapshot

- Claims audited: 51.
- Supported claims: 42.
- Needs-verification claims: 9.
- Source rows: 79.
- Primary or local-primary source rows: 79.
- Captured snapshot rows: 7.
- Snapshot gap rows: 5.
- Visual asset rows: 11.
- Main chapter count: 24.
- Pending idea rows after pass I-0023: 5.

The nine needs-verification rows are C-0007, C-0010, C-0013, C-0021, C-0029, C-0044, C-0045, C-0046, and C-0047. They should be treated as a work queue, not as acceptable residue.

## Priority Groups

First priority: mutable rank and price facts. Pass I-0019 resolved the stale capture-gap rows C-0017 and C-0018 because local or clearly labeled alternate official captures now exist. The active blockers are sharper: C-0045 blocks exact LMArena ranks until SNAP-20260524-001 is normalized into rows with model names, filters, access dates, and caveats; C-0046 blocks price-quality charts until provider price rows are normalized and same-date/same-scope joins are defined. Pass I-0021 normalized visible OpenAI pricing rows from SNAP-20260525-001 with row-level cutoff caveats and post-cutoff model-name exclusions, but the rows still cannot be used as exact cutoff-day chart data until corroborated.

Second priority: benchmark, performance, and behavior-policy claims. C-0013, C-0021, C-0044, and C-0047 should stay caveated until benchmark harnesses, NVIDIA keynote claims, roadmap status, availability language, assistant-behavior policy wording, and independent triangulation are separated. Pass I-0023 adds a source-bearing Chapter 6 alignment pipeline visual, but C-0044 still blocks exact quotations, labeler-process details, red-team examples, and policy wording until local snapshots exist. Pass I-0019 resolved C-0033's exact-slide-wording gap because GTC slide captions now carry row-level caveats, and pass I-0022 used those caveats in the Chapter 15 opening; C-0047 still keeps the remaining rule visible: slide-derived quantitative, partner, roadmap, availability, and deployment claims are not independent facts.

Third priority: source-exactness gaps. C-0007, C-0010, and C-0029 need cutoff-bounded support before they become clean prose: Qwen/DeepSeek frontier-release naming, ChatGPT adoption and reception, and GPT-3 API/Copilot ecosystem figures.

## Chapter Source Density

The prose-draft chapters are close to the target:

- Chapter 5, `05-gpt-1-to-gpt-3-door-opens.md`: 2,006 words, 9 unique source references, 222.9 words per source, target band.
- Chapter 6, `06-alignment-enters-product.md`: 2,427 words, 10 unique source references, 242.7 words per source, target band.
- Chapter 7, `07-chatgpt-interface-event.md`: 2,437 words, 11 unique source references, 221.5 words per source, target band.
- Chapter 15 opening, `15-gtc-2026-ai-factory-sells-itself.md`: 1,614 words, 8 unique source references, 201.8 words per source, target band.
- Chapter 20, `20-claude-code-industrialized-pair-programming.md`: 2,064 words, 13 unique source references, 158.8 words per source, target band.

Appendices, protocols, source packs, and scaffolds are not judged as prose-density targets, but they still carry claim rows when they make project-control assertions or quarantine factual risks.

## Snapshot Notes

The source-snapshot protocol has seven captured rows and five gap rows. The gap list now means captured-but-not-normalized rows, post-cutoff OpenAI alternate-docs rows that are normalized but not cutoff-day price truth, local PDF/GTC material that still needs independent triangulation, and Chapter 6 alignment sources that need snapshots before exact wording. A captured file, normalized row, rendered slide, or source-bearing SVG is evidence of provenance; it is not permission to publish exact rank, price, context-window, performance, availability, or policy-language claims.

## Promotion Gates

- No new factual chapter should be promoted without claim rows and source IDs for its major assertions.
- Exact rank, price, benchmark, performance, and context-window claims remain blocked until normalized from snapshots or triangulated sources.
- Private-use visual evidence can support internal drafting only after `assets_manifest.tsv` records source, provenance, caption intent, and story purpose.
- Unsupported factual claim count must keep trending toward zero before any full-book render or final layout pass.
