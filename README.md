# World Of Computing

Autonomous Codex workspace for building **Next Token: The Race to Build the Machines That Learned Language, Code, and Computing**.

This repository is the working memory, manuscript lab, source ledger, visual system, and pass-by-pass audit trail for a 24-chapter, deeply sourced nonfiction book about large language models through the hard factual cutoff of **May 24, 2026**.

## Current Book State

Updated **2026-05-27** after pass `I-0264`.

- **Latest recorded pass:** `I-0264`, rights-closure reconciliation.
- **Latest exhibit dashboard pass:** `I-0236`, fail-closed visual readiness recomputation.
- **Words:** 102,196 assembled source words across the canonical 24-chapter draft, including 3,911 retained supplemental Anthropic/Claude words; the primary-only spine is 98,285 words, so the floor is conditionally cleared rather than permanently solved.
- **Chapters:** 24 / 24.
- **Charts/diagrams:** 142.
- **Photo/screenshot/source-surface slots:** 78.
- **Sources:** 299.
- **Claims:** 273 supported / 8 needs-verification.
- **Asset/provenance rows:** 267.
- **Idea queue:** active FIFO continues; next pending pass is recorded in `ideas.tsv`.
- **Ledger BookScore:** 100.0, but this is a loop scoring proxy, not a publication certificate.
- **Current rough PDF:** `rendered/full_book_i0240/Next-Token-full-draft-i0240.pdf` exists locally; after the figure-callout pass it is 413 pages and intentionally not committed. Prior smoke QA passed artifact, chapter, figure-ID, link, blank-page, and code-block checks; final overflow/layout quality remains unproven.
- **Current visual PDF:** `rendered/full_book_i0262/Next-Token-full-draft-i0262.pdf` exists locally and is intentionally not committed. It rasterizes and embeds 100/100 selected figure callouts as PNG-backed figures, preserves 24/24 chapter headings and 100/100 figure IDs, records 10 pass / 0 warn / 0 fail object-level QA rows, and is still not publication-ready until the I-0263 layout warnings, caption/source-note typography, rights review, and final design QA pass.
- **Current visual manifest:** `data/visual_embedding_manifest_i0258.tsv` maps all 100 selected figure IDs to caption, alt text, source note, rights stage, publication decision, source file, render embed file where available, fallback action, claim boundary, proof gate, and fail-closed status. Its QA ledger has 8 pass / 0 fail rows, including 74/74 unique render hashes.
- **Current source-surface pack:** `data/source_surface_acquisition_i0259.tsv` records 25 private-use source surfaces across company HTML, company text-render pages, PDF page renders, arXiv HTML, dataset JSON, repository HTML, and GTC slide renders. Its QA ledger has 7 pass / 0 fail rows and 25/25 unique hashes; the raster outputs are local and intentionally ignored.
- **Current source-card excerpt pack:** `data/source_card_excerpt_i0260.tsv` records 25 quote-safe SVG source cards derived from the I-0259 surfaces. Its QA ledger has 8 pass / 0 fail rows; the cards are committed as lightweight SVGs, but they still require final page placement, caption/source-note proof, and rights review before publication.
- **Current selected-exhibit repair manifest:** `data/selected_exhibit_manifest_i0261.tsv` preserves exactly 100 selected figure IDs with 100 existing lightweight source files and 0 empty callouts; 26 previously blocked rows are replaced or cut/replaced in `data/selected_exhibit_repair_i0261.tsv`.
- **Current page-image QA:** `data/page_image_legibility_i0263.tsv` audits 100 figure pages and `data/page_image_legibility_samples_i0263.tsv` records 24 local chapter sample PNGs; 100 figures need layout review and 0 P0 defects were found.
- **Current rights closure:** I-0264 closes 26/26 old non-publish rows ({'closed_replaced_by_source_card': 18, 'closed_cut_replaced_by_original_card': 6, 'closed_local_only_reserve_replaced_by_source_card': 2}) while keeping final rights/legal review pending for the finished PDF.
- **Critical visual defect now narrowed:** the current visual PDF has 100 raster image XObjects across 100 pages and embeds 100/100 selected figure callouts from the I-0261 successor manifest. Page-image legibility QA now has an I-0263 defect register; caption compression, final source-note typography, final rights review, and final design remain pending.
- **Real-world/source-surface layer:** 24 blocked candidate callouts are marked in the assembled draft across 12 chapters, and I-0259 adds 25 local source-media handles with hashes and blocker notes for product pages, PDFs, arXiv pages, repository HTML, dataset JSON, and GTC slides. These are still private-use/source-review assets; 0 are publication-ready.
- **Source-card extraction layer:** 22 I-0244 quote-safe extraction rows and 25 I-0260 paraphrase-first source-card SVGs now have local line/page/slide-note anchors across chapters 6, 7, 9-13, 15-16, 18-20, and 22; I-0260 keeps quote fragments at 4 words or fewer per card, with per-source totals under 5 words, and final page-layout proof remains pending.
- **Front matter package:** `manuscript/front-matter-reader-promise-i0245.md` now drafts the title-page language, reader promise, back-cover copy, six-promise reader contract, introduction, exact 24-entry TOC, cutoff notice, and integration gates; it is not yet inserted into the assembled full draft or render-tested.
- **Chapter-opener package:** `data/chapter_openers_package_i0246.tsv` now gives all 24 chapters a one-sentence promise, opening beat, unique candidate opening figure, reader-effect job, claim guardrail, and integration gate; live chapter prose is not yet rewritten from this board.
- **Continuity stitch layer:** `manuscript/Next-Token-full-draft.md` now contains 23 marked I-0247 candidate boundary stitches from CH01-CH02 through CH23-CH24, backed by `data/prose_continuity_stitch_i0247.tsv`; I-0248 adds visible bounded source lanes to all 23 stitch blocks, totaling 99 source-ID placements while preserving guardrails against new quotations, exact metrics, rankings, market claims, or scene detail.
- **Source apparatus prototype:** `data/endnote_placeholders_i0249.tsv` now contains 315 source-ID-first placeholder endnotes covering 153 unique source IDs. A local ignored 461-page full-book prototype PDF with bracketed back-of-book endnotes passed 6/6 render QA checks in `data/endnote_render_qa_i0249.tsv`; final bibliography prose, page anchors, note compression, and typography remain open.
- **Image rights closure:** `data/rights_closure_i0264.tsv` closes the 26 old I-0250 non-publish rows: screenshot/source-surface/photo placeholders are no longer active publication slots, and the current selected path uses source cards or original repair cards. This is rights-path closure, not final legal/publication clearance.
- **Page template and visual render:** `assets/book_design/full_book_page_template_i0251.css` defines the first full-book typography/page template, backed by 12 rule rows and 9/9 passing CSS checks; I-0252 applies it to produce the 407-page designed render, I-0257 proves the first 74 embedded raster figures, and I-0262 now renders 100/100 selected figure callouts in the current local visual PDF.
- **Publication sprint queue:** I-0253 rejects the premature outside-reader packet and replaces the next 30 FIFO items with I-0257-I-0286, a hard publishability sprint covering embedded visuals, source captures, excerpt cards, render QA, rights, verification, rewrites, deletion, addiction, prose quality, design polish, commercial packaging, review packet, production QA, final gate, and publication candidate assembly.

The book is a real manuscript with a serious spine, but it is **not yet publication-ready**. The strongest current distinction is this: the top-100 exhibit program has stable IDs, chapter placement, caption/provenance scaffolding, page-flow mocks, reader-effect audits, prose bridges, rights triage, a first real-world candidate layer, a first quote-safe source-card extraction layer, a reader-facing front door, a 24-chapter opener contract, a source-laned continuity-stitch layer, a render-tested endnote prototype, a full rights-staging board, a reusable page-template contract, a second full-book designed render, a 30-pass publication sprint queue, a current visual PDF with 100 embedded chart/card/source-card images, a hard all-100 visual embedding manifest, 25 auditable source-surface handles, and a 25-card quote-safe excerpt layer from those handles. The remaining visual risk is no longer "zero visuals" or empty selected slots; it is page-level legibility, caption/source-note quality, rights review, and final design QA.

## Readiness Snapshot

Rough editorial/commercial estimates as of 2026-05-26:

- **Manuscript substance:** 80-85%.
- **Structural completeness:** 85-90%.
- **Hard invariant compliance:** 75-80% because the assembled draft now clears the word-count target only conditionally, while 8 claims still need verification and full render QA is not complete.
- **Source/claim discipline:** 75-80%.
- **Visual ambition:** 85-90%.
- **Visual planning maturity:** 60-65%.
- **Visual publication readiness:** 25-35% under fail-closed render/rights/caption gates.
- **Commercial launch-ready:** 35-45%.
- **Award/shortlist-ready:** 25-35%.
- **Revenue-generating beautiful book:** 40-50% for a disciplined self-published launch after package, rights, render, and cover work; lower for traditional/major-prize lanes until a finished packet exists.

Prize-winning potential is real because the subject, scope, source base, and industrial narrative are strong. Prize readiness is still gated by finishing work: claims, rights, layout, render QA, editorial polish, and a coherent public package.

## 100-Exhibit Dashboard

Current selected-exhibit program:

- **100** selected rows.
- **100** selected rows assigned to chapters.
- **74** original SVG/chart/card rows are staged as publish-after-render/caption/source-note QA.
- **0** selected rows remain active non-publish placeholders under the current I-0264 closure board.
- **21** old permission-needed screenshot/photo rows are retired, cut/replaced, or converted to source-card paths in I-0264.
- **3** old source-screenshot rows are converted to source-card replacements in I-0264.
- **2** old raw slide/source-surface rows remain local-only reserves and are replaced in publication path by source cards.
- **67** selected rows still have caption warning/fail gates.
- **9** chapters still show crowding or reader-fatigue defects.
- **100** selected rows have a hard I-0258 embedding-manifest row.
- **100** selected rows have first full-book embedded render proof; I-0263 audits all 100 figure pages plus 24 chapter sample PNGs, with 100 warning rows and 0 P0 defects.
- **24** selected rows are blocked because their planned source/acquisition files are still missing.
- **25** local source-surface handles exist for later source-card/redraw/permission/replacement work.
- **25** quote-safe I-0260 source-card SVGs now convert those handles into paraphrase-first evidence cards with anchors, tiny/zero quote fragments, blocked claims, and redraw paths.
- **0** selected rows should be called publication-ready yet.
- **100** selected figure callouts now render as image-bearing exhibits in the I-0262 local PDF.
- **100** selected figure callouts now render as image-bearing exhibits in the I-0262 local PDF.
- **100** selected figure callouts now render as image-bearing exhibits in the I-0262 local PDF.
- **100** selected rows now have an I-0261 no-empty-callout successor manifest with existing lightweight source files.

## Most Useful Reader Samples

For a fast feel of the book, read:

- `manuscript/01-the-shock.md` - opening narrative and reader hook.
- `manuscript/08-microsoft-openai-cloud-bargain.md` - platform/business narrative.
- `manuscript/17-data-tokens-library-problem.md` - data, tokens, and source texture.
- `manuscript/20-claude-code-industrialized-pair-programming.md` - coding-agent chapter.
- `manuscript/24-next-token.md` - final synthesis.

For production/readiness context, read:

- `manuscript/visual-readiness-recompute-i0236.md`.
- `manuscript/exhibit-readiness-dashboard-i0196.md`.
- `manuscript/commercial-publishing-package-i0167.md`.
- `manuscript/award-shortlist-readiness-package-i0168.md`.
- `manuscript/source-download-automation-provenance-plan-i0183.md`.
- `manuscript/project-status-2026-05-26.md`.

## Mission

Build a 100,000-120,000 word, exactly 24-chapter, visually beautiful, prize-aspiring book about LLMs: models, labs, chips, data, tools, coding agents, inference economics, infrastructure, and trust. The visual/source program should reach at least 100 curated exhibits, with roughly 3-4 strong candidates per chapter and every exhibit carrying provenance, rights status, story purpose, and blocked-claim notes.

Quality targets include the seriousness, narrative force, and durability of books such as:

- *Chip War*
- *The Prize*
- *The Thinking Machine*
- Walter Isaacson's *Steve Jobs*
- Walter Isaacson's *Elon Musk*

Truth outranks beauty. Beauty outranks completeness when both versions are equally true.

## Start The Loop

Use:

```text
/goal Read GOAL.md fully, then run the loop forever per its protocol.
```

Every serious pass should begin by reading `GOAL.md`, checking git state, and consulting the current ledgers.

## Core Ledgers

- `GOAL.md` - loop contract, invariants, evaluator, and mandatory topic spine.
- `ideas.tsv` - append-only FIFO queue of pending/done/rejected passes.
- `scoreboard.tsv` - append-only pass ledger and metric history.
- `insights.md` - distilled lessons from completed passes.
- `sources.tsv` - source ledger.
- `claims.tsv` - claim audit ledger.
- `assets_manifest.tsv` - visual/photo/screenshot provenance ledger.
- `manuscript/` - working chapter files, notes, plans, and audits.
- `champion/` - current best promoted chapter/manuscript artifacts.
- `archive/` - useful variants, rejected-but-interesting work, and stepping stones.
- `assets/` - lightweight visuals, data tables, source snapshots, and local asset records.
- `rendered/` - render outputs and QA artifacts.

## Current Work Direction

The immediate next phase should prioritize:

1. Add the missing 700+ high-quality words only where the book genuinely needs them.
2. Verify or rewrite the 8 remaining needs-verification claims.
3. Execute the source-download/capture automation plan without committing heavyweight media.
4. Convert the 30 high-risk selected exhibits into captured, permissioned, redrawn, replaced, reserved, or cut decisions.
5. Close 67 caption warning/fail gates, fill the early chapter visual gap in chapters 2-5, and prune overfull later chapters.
6. Run full-book render QA, page QA, caption QA, and source-note QA.
7. Freeze commercial metadata, cover direction, reader sample, launch plan, and award packet only after the book gates close.

## Git And Asset Rules

- Commit and push every completed pass.
- Never force-push, reset hard, or rewrite shared history.
- Do not commit heavyweight rendered PDFs, large rasters, videos, audio, caches, or private-use media.
- Do commit manuscripts, ledgers, outlines, scripts, small data tables, SVG/lightweight diagrams, and provenance records.
- Every visual, screenshot slot, chart, or extracted slide needs provenance in `assets_manifest.tsv`.
- `GTC-2026-Keynote.pdf` is available locally as a major source asset, but derived claims still need page-level provenance.

## Publication Reality

The project is past idea stage. It is now in the conversion phase: turning a substantial, sourced manuscript into a finished object. The next decisive gains come from truth cleanup, rights cleanup, source capture, page design, render QA, cover/package work, reader sampling, pricing, launch mechanics, and award calendar discipline.
