# Champion Claim Coverage Dashboard

Current champion dashboard source: `manuscript/00-claim-coverage-dashboard.md`.

Promoted in pass I-0014 on 2026-05-24 and refreshed in passes I-0016, I-0017, I-0018, I-0019, and I-0020 on 2026-05-25 because it converts the claim ledger, source ledger, snapshot protocol, and chapter files into a visible quality gate:

- 48 claims audited.
- 39 supported claims.
- 9 needs-verification claims.
- 79 source rows.
- 7 captured snapshot rows.
- 5 snapshot gap rows.
- Chapter 6 is in target band at 240.0 words per source; Chapter 7 is now in target band at 220.4 words per source after I-0020.
- I-0019 resolved stale LMArena/pricing/GTC capture and exact-wording blockers while replacing them with sharper row-normalization and triangulation blockers.

This champion marker should be replaced only when the underlying dashboard tables are regenerated and the replacement is recorded in `scoreboard.tsv`.
