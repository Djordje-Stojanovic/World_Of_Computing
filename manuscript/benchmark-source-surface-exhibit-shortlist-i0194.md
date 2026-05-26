# Benchmark Source-Surface Exhibit Shortlist - Pass I-0194

This pass turns the I-0178 benchmark board into a ranked exhibit shortlist. The governing principle is simple: a benchmark exhibit should teach what a measurement licenses, what it cannot license, and which fields make a score citeable. It should not crown a live model.

## First-Wave Exhibits

The strongest first wave is LMArena/Arena, SWE-bench, LiveCodeBench, Terminal-Bench, the Chapter 21 inference-contract matrix, and the Chapter 23 blind-spot matrix. Together they cover human preference, repository repair, contamination-aware code evaluation, terminal-agent harnesses, reasoning-score scaffolds, and trust limits.

Existing diagrams should carry much of the load: A-0013 and A-0014 for Arena, A-0092 for coding benchmark families, A-0080 for inference contracts, and A-0076 for trust blind spots. Source-page screenshots should be added only when they bring real provenance value and the required caption fields are complete.

## Reserves

Artificial Analysis is high-value but snapshot-fragile. It belongs in the reserve lane until methodology version, evaluation basket, measurement window, model/provider identifiers, and selected rows are frozen. MMLU, GPQA, MATH, HumanEval, and TruthfulQA belong mostly as genealogy or source-card surfaces, not as modern leaderboard art.

## Caption Firewall

Every benchmark caption must name benchmark/version/date, task or sample scope, model/date if applicable, scaffold/tools, metric or scoring rule, source IDs, and blocked claims. Prohibited language includes "best model," "winner," "objective rank," "dominates," "general intelligence," "safe model," "truthful model," "proves productivity," and "real-world value."

## Outputs

- `data/benchmark_source_surface_exhibit_shortlist_i0194.tsv`: 15 ranked benchmark/source-surface exhibit candidates.
- `data/benchmark_source_surface_choose_drop_i0194.tsv`: 8 choose/drop decisions for first-wave exhibits, dynamic reserves, genealogy surfaces, caption contracts, and manifest timing.

No new screenshot, raster, source-card artwork, or manifest asset was created in this pass.
