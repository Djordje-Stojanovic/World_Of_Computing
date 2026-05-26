# Canonical Paper Figure Redraw Shortlist (I-0190)

This pass narrows the broader I-0169 acquisition board into a 25-item figure-redraw execution shortlist. The point is not to copy canonical paper art into the book. It is to decide which paper mechanisms deserve house-style redraws, which should become small source cards, and which should stay cited but unseen.

The top redraw-now lane is deliberately mechanism-heavy:

- Transformer Figure 1/Figure 2 as a paired architecture and attention-flow redraw.
- Scaling laws and Chinchilla as bounded evidence-lane and compute/data balance visuals.
- RLHF and Constitutional AI as assistant-behavior training mechanisms.
- DeepSeek-R1 as reasoning-RL/distillation mechanism, not benchmark theater.
- SWE-bench and LiveCodeBench as benchmark-contract diagrams.
- ReAct and Toolformer as tool/agent lineage diagrams.

The lower lanes are held back for a reason. Word vectors, seq2seq/attention, GPT-3 prompt format, tokenization, dataset mixtures, deduplication, RAG, process supervision, Tree of Thoughts, FlashAttention, and FrugalGPT are valuable, but each needs page-level provenance and a clear chapter need before art starts. AlphaCode, Code Llama, and broad China/open-frontier family tables are cite-only for now because they risk becoming rank/adoption/productivity art before the evidence is normalized.

Execution rule: no paper redraw should enter `assets_manifest.tsv` until exact page/figure/table provenance, redraw scope, blocked claims, and caption contract are recorded. The first practical target remains the Transformer architecture/attention pair because it has the strongest explanatory value and the cleanest provenance path.
