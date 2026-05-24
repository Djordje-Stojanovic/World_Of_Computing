# Champion Claim Coverage Dashboard

Current champion dashboard source: `manuscript/00-claim-coverage-dashboard.md`.

Promoted in pass I-0014 on 2026-05-24 and refreshed in passes I-0016, I-0017, I-0018, I-0019, I-0020, and I-0021 on 2026-05-25 because it converts the claim ledger, source ledger, snapshot protocol, and chapter files into a visible quality gate:

- 49 claims audited.
- 40 supported claims.
- 9 needs-verification claims.
- 79 source rows.
- 7 captured snapshot rows.
- 5 snapshot gap rows.
- Chapter 6 is in target band at 240.0 words per source; Chapter 7 is now in target band at 220.4 words per source after I-0020.
- I-0021 normalized visible OpenAI pricing rows with cutoff caveats and explicit post-cutoff model-name exclusions; C-0046 still blocks exact price-quality charts.

This champion marker should be replaced only when the underlying dashboard tables are regenerated and the replacement is recorded in `scoreboard.tsv`.
