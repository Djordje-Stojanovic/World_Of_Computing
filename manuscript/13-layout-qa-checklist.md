# Chapter 13 Layout QA Checklist

Status: promoted design-control pass I-0064 on 2026-05-25.

Companion table: `data/chapter13_layout_qa_checklist_i0064.tsv`.

This pass defines the acceptance gate for rendering the integrated leaderboard appendix. It does not edit `manuscript/13-model-rankings-appendix.md`. The checklist protects the I-0059 reading order before any PDF/layout pass: orientation, glossary, A-0014 methodology figure, narrow transition, A-0013 historical chart, shared footnote, prohibited-use note, then any price-quality handoff.

Acceptance summary:

- A-0014 must appear before A-0013.
- The glossary must precede A-0014 and include vote, config, split, category, rating, confidence interval, publication date, snapshot, and permission gate.
- A-0013 captions must state `text_style_control`, `latest`, `overall`, top-twelve scope, published 2026-05-19, S-0080/SNAP-20260525-008, and uncertainty-overlap reading.
- The shared footnote must sit directly below A-0013 or in the nearest same-page sidenote.
- Prohibited-use language must remain visible before price, benchmark, coding, safety, latency, or enterprise material.
- Any price-quality section needs a hard divider preserving C-0046.
- A-0013/A-0014 must stay legible at final size, with source/provenance handles visible.
- The current draft's repeated `Ranking Sources To Use` heading should be fixed before PDF render.

Gate for the next Chapter 13 layout pass: do not render or merge a PDF spread unless every checklist row is either passed or explicitly failed with a corrective action.
