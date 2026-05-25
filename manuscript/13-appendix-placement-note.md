# Chapter 13 Appendix Placement Note

Status: promoted claim-audit pass I-0055 on 2026-05-25.

This note decides the reading order for the Chapter 13 methodology figure, historical rank chart, glossary, microstyle footnote, and prohibited-use note. The companion table is `data/leaderboard_appendix_placement_i0055.tsv`.

## Final Reading Order

1. Orientation paragraph: this appendix explains how ranking evidence is made, not who is "best."
2. Condensed glossary: vote, config, split, category, rating, confidence interval, publication date, snapshot, and permission gate.
3. A-0014 methodology figure: how Arena rows become rank claims.
4. Transition sentence: the chart can make one narrow historical-slice point about a tight top cluster.
5. A-0013 historical rank chart: `text_style_control`, `latest` split, `overall` category, published 2026-05-19.
6. Shared chart footnote: not live ranks, not release-status evidence, intervals overlap, and C-0046 still blocks price-quality claims.
7. Prohibited-use note: no broad best-model, coding, safety, latency, enterprise, or price-performance inference.
8. Price-quality handoff: if prices appear later, insert a hard divider saying the historical rank chart is not a price-quality chart.

## Placement Rule

A-0014 must appear before A-0013. The glossary should appear before A-0014 because readers need the vocabulary before the methodology diagram. The shared footnote should sit directly below A-0013 or in the nearest sidenote, not buried in an endnote. The prohibited-use note can be compact, but it should appear before any transition to price, benchmark, or task-specific material.

## Allowed Claim

The sequence supports one narrow claim: in the official historical Arena `text_style_control` / `latest` / `overall` slice published 2026-05-19, the top rows were tightly clustered. It does not support live May 24 rank wording, product release status, price-quality comparison, coding superiority, safety, latency, enterprise usefulness, or generic "best model" prose.

