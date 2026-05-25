# I-0035 ChatGPT Product Alternate Capture Notes

Pass date: 2026-05-25

Purpose: find an auditable non-browser archive or official alternate capture path for ChatGPT Plus and ChatGPT Enterprise after direct shell capture returned HTTP 403 and the in-app browser backend was unavailable.

## Result

The direct OpenAI product pages and official localized product pages still returned HTTP 403 to shell capture. A text-render path through `r.jina.ai` produced commit-safe Markdown snapshots for:

- `SNAP-20260525-013` / `S-0078` / ChatGPT Plus, using an official OpenAI blog URL variant surfaced by search.
- `SNAP-20260525-014` / `S-0089` / OpenAI Help Center ChatGPT Release Notes, including the August 28, 2023 ChatGPT Enterprise entry.
- `SNAP-20260525-015` / `S-0090` / OpenAI Help Center "What is ChatGPT Plus?"

## Use Rules

These captures improve Chapter 7 quote readiness for structural product-evolution facts, but they are not a blanket substitute for original product-page HTML.

- ChatGPT Plus: short quotations or exact facts about launch date, $20/month launch price, response-time/access benefits, and availability can use `SNAP-20260525-013` with a text-render caveat.
- ChatGPT Enterprise: launch date and feature-list wording can use the official release-notes entry in `SNAP-20260525-014`; original product-post quotations, adoption percentages, customer productivity claims, and named-customer claims still require original-page capture or triangulation.
- Current Plus help article: `SNAP-20260525-015` is a mutable Help Center article with an as-of February 13, 2026 notice; use it only for cutoff-compatible plan-description/pricing facts and as exclusion evidence for later model-list drift.

Companion line references live in `data/chatgpt_product_alternate_captures_i0035.tsv`.
