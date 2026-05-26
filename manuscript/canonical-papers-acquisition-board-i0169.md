# Canonical Papers Acquisition And Figure-Rights Board - Pass I-0169

## Verdict

The book already cites many of the canonical technical papers, but the evidence is scattered across chapter audits, source packs, and visual sidecars. This pass consolidates the technical-paper spine into a single acquisition board so later passes can choose figures deliberately instead of grabbing famous diagrams because they are famous.

`data/canonical_papers_acquisition_i0169.tsv` now tracks 55 paper/source rows across early language models, word vectors, seq2seq, attention, Transformer, scaling laws, GPT lineage, instruction tuning, RLHF, Constitutional AI, open/frontier models, tool use, coding benchmarks, reasoning/test-time compute, inference economics, and data/tokenization.

`data/canonical_paper_figure_rights_i0169.tsv` identifies the first 20 figure or source-surface candidates and assigns a rights lane:

- `redraw_required` for central figures where copying the original would be risky or visually inconsistent.
- `redraw_preferred` for mechanisms that should enter the book in house style.
- `cite_mostly` where tables or benchmark figures are too easy to misuse.
- `private_screenshot_or_excerpt_card` for official pages whose value is source texture rather than neutral evidence.

## Immediate Redraw Priorities

The highest-value technical visuals are the Transformer architecture, RLHF pipeline, scaling-law evidence lanes, Chinchilla compute/data balance, DeepSeek-R1 reasoning/distillation, SWE-bench and LiveCodeBench benchmark contracts, ReAct, Toolformer, and the early word-vector/attention/tokenization mechanisms.

Those figures should be redrawn as explanatory diagrams with blocker captions on the canvas. They should not import benchmark crowns, priority fights, safety guarantees, adoption claims, productivity claims, cost claims, or live-rank claims.

## Source Gaps Added

This pass adds missing high-priority sources S-0188 through S-0199 for BERT, GPT-2 paper PDF, Chinchilla, LLaMA, WebGPT, Training Verifiers, AlphaCode, Code Llama, latent reasoning, FrugalGPT, FlexGen, and FlashAttention. Lower-priority candidate rows remain in the board without new source rows until a later chapter-specific pass actually needs them.

## Next Use

The next paper-visual pass should not start from a blank search. It should pick from the board, extract exact page/figure provenance, decide redraw versus cite-only, and then update `assets_manifest.tsv` only when a concrete figure slot exists.
