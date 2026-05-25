# Chapter 13 Leaderboard Render QA

Pass I-0074 checks the Chapter 13 leaderboard appendix after the I-0069 heading fix and before any PDF promotion.

Result: the text-level reading path is ready for a real render. The appendix now has a single `## Leaderboard Reading Sequence`, then glossary, A-0014 methodology figure, transition, A-0013 historical chart, shared footnote, prohibited-use note, and only then the price-quality handoff. The asset manifest keeps A-0014 sourced to S-0036/S-0056/S-0057/S-0080/SNAP-20260525-008 and A-0013 sourced to S-0080/SNAP-20260525-008.

Promotion limit: this pass does not approve a PDF. The checks in `data/chapter13_leaderboard_render_qa_i0074.tsv` are preflight and text/order evidence, plus SVG dimension inspection. Final promotion still requires a page/spread render showing figure order, footnote proximity, prohibited-use visibility, source labels, and legibility at final size.

Decision: keep the Chapter 13 appendix sequence, but block PDF promotion until a real rendered page or spread proves the same gates visually.
