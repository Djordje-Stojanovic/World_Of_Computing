# Chapter 13 Leaderboard Appendix Pre-Render Fix

Pass I-0069 resolves the heading-flow defect found by I-0064 before any PDF render.

The integrated appendix previously placed the inserted `## Leaderboard Reading Sequence` between two identical `## Ranking Sources To Use` headings. That made the source-package section look as if it restarted after the leaderboard caveats. The fix removes the first duplicate heading and lets the leaderboard material stand as its own section; the remaining `## Ranking Sources To Use` heading now introduces the LMArena, benchmark, and provider-price source subsections.

The fix does not change the I-0059 reading order: orientation paragraph, condensed glossary, A-0014 methodology figure, narrow transition, A-0013 historical chart, shared footnote, prohibited-use note, then any price-quality handoff. It also preserves every I-0064 gate: glossary before method, method before rank rows, historical-slice caption scope, visible footnote, prohibited-use language before prices, C-0046 price-quality blocker, source/provenance visibility, and the ban on new rank or task claims without a source row.

Next render QA should check exactly one `## Leaderboard Reading Sequence` heading, exactly one `## Ranking Sources To Use` heading, and no visual separation that lets A-0013 be read before A-0014.
