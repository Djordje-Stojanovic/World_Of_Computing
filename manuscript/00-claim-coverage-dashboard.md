# Claim Coverage Dashboard

Status: promoted data pass I-0014 on 2026-05-24; refreshed by source-capture pass I-0016, caption/provenance pass I-0017, chapter-draft pass I-0018, claim-audit pass I-0019, source-density pass I-0020, OpenAI pricing-normalization pass I-0021, GTC chapter-opening pass I-0022, alignment-visual pass I-0023, LMArena normalization pass I-0024, ChatGPT product-page capture pass I-0025, provider-pricing normalization pass I-0026, AI-factory visual pass I-0027, alignment-source capture pass I-0028, clean LMArena dataset pass I-0029, and Mistral pricing pass I-0031 on 2026-05-25.

This dashboard turns the project ledgers into a recurring quality gate. It does not make new historical claims about LLMs; it exposes which existing claims are supported, which claims are still quarantined, and where chapter drafts are drifting away from the source-density target.

## Current Snapshot

- Claims audited: 58.
- Supported claims: 50.
- Needs-verification claims: 8.
- Source rows: 82.
- Primary or local-primary source rows: 82.
- Captured snapshot rows: 13.
- Snapshot gap rows: 8.
- Visual asset rows: 12.
- Main chapter count: 24.
- Pending idea rows after pass I-0031: 5.

The eight needs-verification rows are C-0007, C-0010, C-0013, C-0021, C-0029, C-0044, C-0046, and C-0047. They should be treated as a work queue, not as acceptable residue.

## Priority Groups

First priority: mutable rank and price facts. Pass I-0019 resolved the stale capture-gap rows C-0017 and C-0018 because local or clearly labeled alternate official captures now exist. Pass I-0029 resolves C-0045 by capturing and normalizing 100 official LMArena/Arena historical `text_style_control` `overall` rows published 2026-05-19; those rows are chart candidates only with source, config, category, and publish-date labels, not live May 24 wording. Pass I-0031 resolves the missing Mistral pricing pair by capturing official Mistral pricing pages and normalizing candidate rows, but C-0046 still blocks price-quality charts until model cutoff status, provider price rows, and same-date/same-scope joins are defined. Pass I-0024 normalized a conservative subset of LMArena visible-order rows from SNAP-20260524-001, but the captured title stream contains post-cutoff-looking model names, so it remains an audit/filtering artifact rather than final rank data. Pass I-0021 normalized visible OpenAI pricing rows from SNAP-20260525-001 with row-level cutoff caveats and post-cutoff model-name exclusions, but the rows still cannot be used as exact cutoff-day chart data until corroborated. Pass I-0026 normalized candidate Claude, Gemini, and xAI rows from cutoff-day snapshots; C-0046 remains active until those rows are joined to same-scope ranks with batch, cache, tier, cutoff-status, and provider-specific billing caveats separated.

Second priority: benchmark, performance, and behavior-policy claims. C-0013, C-0021, C-0044, and C-0047 should stay caveated until benchmark harnesses, NVIDIA keynote claims, roadmap status, availability language, assistant-behavior policy wording, and independent triangulation are separated. Pass I-0023 adds a source-bearing Chapter 6 alignment pipeline visual, and pass I-0028 captures the OpenAI Model Spec plus GPT-4/GPT-4o system-card artifacts, but C-0044 still blocks exact instruction-following quotations, labeler-process details, red-team examples, and policy wording because the OpenAI instruction-following product post remains shell-blocked and all exact wording needs quote-limit extraction. Pass I-0019 resolved C-0033's exact-slide-wording gap because GTC slide captions now carry row-level caveats, and pass I-0022 used those caveats in the Chapter 15 opening; C-0047 still keeps the remaining rule visible: slide-derived quantitative, partner, roadmap, availability, and deployment claims are not independent facts. Pass I-0027 adds a Chapter 15 AI factory stack diagram as explanatory infrastructure synthesis, not as validation of NVIDIA performance, revenue, partner, roadmap, availability, or deployment claims.

Third priority: source-exactness gaps. C-0007, C-0010, and C-0029 need cutoff-bounded support before they become clean prose: Qwen/DeepSeek frontier-release naming, ChatGPT adoption and reception, and GPT-3 API/Copilot ecosystem figures. Pass I-0025 documented that ChatGPT Plus and Enterprise official pages are browser-readable but shell-blocked with HTTP 403, so Chapter 7 may keep structural product-evolution paraphrases but still cannot use direct quotes, exact Plus pricing, Enterprise adoption percentages, customer productivity claims, or detailed availability language as final facts.

## Chapter Source Density

The prose-draft chapters are close to the target:

- Chapter 5, `05-gpt-1-to-gpt-3-door-opens.md`: 2,006 words, 9 unique source references, 222.9 words per source, target band.
- Chapter 6, `06-alignment-enters-product.md`: 2,427 words, 10 unique source references, 242.7 words per source, target band.
- Chapter 7, `07-chatgpt-interface-event.md`: 2,437 words, 11 unique source references, 221.5 words per source, target band.
- Chapter 15 opening, `15-gtc-2026-ai-factory-sells-itself.md`: 1,703 words, 8 unique source references, 212.9 words per source, target band.
- Chapter 20, `20-claude-code-industrialized-pair-programming.md`: 2,064 words, 13 unique source references, 158.8 words per source, target band.

Appendices, protocols, source packs, and scaffolds are not judged as prose-density targets, but they still carry claim rows when they make project-control assertions or quarantine factual risks.

## Snapshot Notes

The source-snapshot protocol has thirteen captured rows and eight gap rows. The gap list now means captured-but-not-clean-enough pricing/source rows, post-cutoff OpenAI and Mistral pricing captures that are normalized but not cutoff-day price truth, local PDF/GTC material that still needs independent triangulation, captured-but-quote-unextracted Chapter 6 policy/system-card sources, and shell-blocked OpenAI product pages that need archive or browser-based local capture before exact quotes or quantitative claims. A captured file, normalized row, rendered slide, source-bearing SVG, or capture-note file is evidence of provenance; it is not permission to publish exact price, context-window, performance, availability, policy-language, adoption, or productivity claims without the row-specific caveats.

## Promotion Gates

- No new factual chapter should be promoted without claim rows and source IDs for its major assertions.
- Exact rank, price, benchmark, performance, and context-window claims remain blocked until normalized from snapshots or triangulated sources.
- Private-use visual evidence can support internal drafting only after `assets_manifest.tsv` records source, provenance, caption intent, and story purpose.
- Unsupported factual claim count must keep trending toward zero before any full-book render or final layout pass.
