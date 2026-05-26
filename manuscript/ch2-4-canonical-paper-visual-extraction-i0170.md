# Chapters 2-4 Canonical Paper Visual Extraction - Pass I-0170

## Verdict

The early technical SVGs from I-0144 are useful, but they need firmer original-paper provenance before final layout. This pass adds that provenance layer without creating new art or copying paper figures.

`data/ch2_4_canonical_paper_visual_extraction_i0170.tsv` maps 17 paper-derived visual surfaces to Chapters 2-4. It links the existing early technical assets:

- `A-0115` / Chapter 2 pre-Transformer bottleneck map.
- `A-0116` / Chapter 3 self-attention information-flow schematic.
- `A-0117` / Chapter 4 scaling evidence-lane chart.

It also marks optional companion candidates from BERT, Chinchilla, GPT-3, PaLM, T5/C4, and subword-tokenization sources.

## Original-Figure Control

`data/ch2_4_original_figure_provenance_i0170.tsv` separates high-confidence known surfaces from surfaces that still require PDF-level page extraction. The strongest immediate provenance rows are:

- Transformer Figure 1 for architecture.
- Transformer Figure 2 for scaled dot-product and multi-head attention.
- BERT Figure 1 for encoder-side pretraining/fine-tuning context.

Scaling-law, Chinchilla, seq2seq, Bahdanau attention, word2vec, GPT-3, and BPE/subword surfaces remain useful but should be treated as `verify_page` candidates before any final caption, quantitative redraw, or source-excerpt card.

## Guardrails

This pass keeps all early technical visuals in redraw/cite/source-card lanes. It does not authorize copied paper art, exact plotted values, benchmark tables, priority crowns, human-like understanding claims, attention-as-explanation claims, architecture-alone causality, universal scaling laws, Chinchilla formula claims, product success, safety, revenue, adoption, or truth-from-scale claims.

## Next Use

The next execution pass should pick one figure family, extract PDF page/figure/caption provenance, and either update the existing SVG caption metadata or create a new house-style redraw. The best first target is still the Transformer Figure 1/Figure 2 pair because it has the highest provenance confidence and the highest explanatory value.
