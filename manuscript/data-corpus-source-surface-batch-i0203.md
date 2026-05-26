# I-0203 Data/Corpus Source-Surface Batch

This pass converts the I-0195 data/corpus shortlist into source-card readiness for Chapter 17 and adjacent caution lanes. It promotes eight card contracts, not final artwork: tokenization, C4/Common Crawl, Pile/Dolma, deduplication, memorization/extraction, FineWeb, ROOTS, and BookCorpus.

The strongest first-wave surfaces are local and hashable. Tokenization has tiktoken, BPE, and SentencePiece handles; C4 has T5 and C4-documentation handles; open-corpus recipes have Pile and Dolma handles; deduplication and memorization have local arXiv-abstract handles. FineWeb is partly local through the Hugging Face page, while ROOTS and BookCorpus remain identified-only until capture. Those gaps stay visible in `data/data_corpus_source_cards_i0203.tsv`.

The caption rule is simple: every corpus surface must name the source type, date, transformation step, disclosed scope, and what it cannot prove. Open datasets do not reveal closed frontier training mixtures. C4 or Common Crawl does not settle legality, consent, representativeness, or quality. Deduplication and memorization papers do not license product-safety or model-specific leakage claims without same-scope evidence.

No `assets_manifest.tsv` rows were added, because this pass did not create final art, screenshots, rasters, or publication-ready source cards. The rights rows are deliberately quote-limit-zero until excerpt and figure review happens.
