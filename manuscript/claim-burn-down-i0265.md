# I-0265 Claim Burn-Down

Pass I-0265 resolves the last eight active `needs-verification` rows in `claims.tsv` by turning each into a supported guardrail, quarantine, or attribution rule. No risky metric, benchmark, release, price frontier, safety, adoption, productivity, or GTC performance claim was promoted as a neutral fact.

## Result

- Starting active blockers in `claims.tsv`: 8.
- Ending active blockers in `claims.tsv`: 0.
- Ending claim ledger count: 281 supported / 0 needs-verification.
- QA: 5 pass / 0 fail in `data/claim_burn_down_qa_i0265.tsv`.

## Resolutions

- `C-0007`: Qwen 3.5, Qwen 3.6, and DeepSeek V4-era names stay gap-only unless a later cutoff-compatible source pack supports narrative use.
- `C-0010`: ChatGPT adoption prose remains attributed and unit-separated; fastest-growing, paid-user, revenue, named-customer, and productivity claims stay blocked.
- `C-0013`: Claude 4 coding benchmarks may explain harnesses and caveats; numeric scores, ranks, and superiority claims stay out until normalized.
- `C-0021`: NVIDIA GTC performance, cost, throughput, revenue, and benchmark statements remain NVIDIA-attributed source-actor claims.
- `C-0029`: GPT-3 API and Copilot sources support product-positioning history, not ecosystem counts, productivity, correctness, or replacement claims.
- `C-0044`: Chapter 6 now relies on local snapshots and quote-safe rows; longer policy wording and safety-outcome claims stay separately gated.
- `C-0046`: Price-quality data may support candidate/exclusion rows and methodology caveats, not a final exact frontier chart.
- `C-0047`: GTC slide-derived quantitative, partner, roadmap, availability, and deployment statements remain attributed slide claims unless corroborated.

## Publication Meaning

This pass reduces the active unsupported-claim count to zero in the current claim ledger, but it does not mean the book is fact-finished. The next pass still needs full-book source-density repair, because many paragraphs can be true yet still too far from citations or too thinly contextualized for a publishable nonfiction apparatus.
