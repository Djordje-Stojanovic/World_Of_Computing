# Full-Book Visual Placement And Caption QA, I-0164

Status: promoted, 2026-05-26.

This pass audits the current visual/source-exhibit program instead of adding new art. The manifest has 120 rows. Of those, 90 are currently ready as `available`, `available_local_ignored`, or `local_ignored_raster_hashed`; 30 are acquisition-ready, pending, or blocked. Every manifest row has caption, source/provenance, rights/private-use note, and story purpose populated.

The placement matrix in `data/full_book_visual_placement_caption_qa_i0164.tsv` assigns chapter-level positions and flags balance problems. The readiness summary in `data/visual_readiness_path_to_100_i0164.tsv` shows the path to the hard floor: at least 10 more ready exhibits are needed to reach 100, and those should mostly be non-diagram surfaces rather than more automatic SVGs.

Main findings:

- Chapters 3 and 4 have zero ready exhibit rows and need canonical paper redraws or source-excerpt cards.
- Chapters 5, 6, 7, and 11 are under-illustrated and should receive targeted source surfaces, paper cards, or product/interface screenshots.
- Chapters 15 and 16 are overfull; GTC slide renders, GTC claim cards, and infrastructure schematics need pruning before final layout.
- The manifest is strong on diagrams and weak on photos, screenshots, and source-page texture.
- The current caption/provenance/rights/purpose completeness check passes, but final render QA still needs page-placement, caption length, and blocker visibility checks.

This pass does not promote new visual claims. It clarifies what belongs where and prevents the 100-exhibit target from becoming filler.
