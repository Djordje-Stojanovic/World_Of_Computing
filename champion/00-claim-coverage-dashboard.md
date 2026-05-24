# Champion Claim Coverage Dashboard

Current champion dashboard source: `manuscript/00-claim-coverage-dashboard.md`.

Promoted in pass I-0014 on 2026-05-24 and refreshed in passes I-0016, I-0017, I-0018, I-0019, I-0020, I-0021, I-0022, I-0023, I-0024, I-0025, and I-0026 on 2026-05-25 because it converts the claim ledger, source ledger, snapshot protocol, and chapter files into a visible quality gate:

- 54 claims audited.
- 45 supported claims.
- 9 needs-verification claims.
- 79 source rows.
- 7 captured snapshot rows.
- 7 snapshot gap rows.
- Chapter 6 is in target band at 242.7 words per source; Chapter 7 is in target band at 221.5 words per source; the Chapter 15 opening is in target band at 201.8 words per source.
- I-0026 normalized candidate Claude, Gemini, and xAI provider pricing rows while preserving C-0046 because Mistral pricing, same-scope rank joins, and batch/cache/tier semantics remain unresolved.

This champion marker should be replaced only when the underlying dashboard tables are regenerated and the replacement is recorded in `scoreboard.tsv`.
