# World Of Computing

Autonomous Codex workspace for building **Next Token: The Race to Build the Machines That Learned Language, Code, and Computing**.

This repository is the working memory, manuscript lab, source ledger, visual system, and pass-by-pass audit trail for a 24-chapter, deeply sourced nonfiction book about large language models through the hard factual cutoff of **May 24, 2026**.

## Current Book State

Updated **2026-05-26** after pass `I-0240`.

- **Latest recorded pass:** `I-0240`, first full-book render pipeline.
- **Latest exhibit dashboard pass:** `I-0236`, fail-closed visual readiness recomputation.
- **Words:** 102,196 assembled source words across the canonical 24-chapter draft, including 3,911 retained supplemental Anthropic/Claude words; the primary-only spine is 98,285 words, so the floor is conditionally cleared rather than permanently solved.
- **Chapters:** 24 / 24.
- **Charts/diagrams:** 142.
- **Photo/screenshot/source-surface slots:** 78.
- **Sources:** 299.
- **Claims:** 251 supported / 8 needs-verification.
- **Asset/provenance rows:** 144.
- **Idea queue:** active FIFO continues; next pending pass is recorded in `ideas.tsv`.
- **Ledger BookScore:** 100.0, but this is a loop scoring proxy, not a publication certificate.
- **First rough PDF:** `rendered/full_book_i0240/Next-Token-full-draft-i0240.pdf` exists locally; it is 401 pages and intentionally not committed.

The book is a real manuscript with a serious spine, but it is **not yet publication-ready**. The strongest current distinction is this: the top-100 exhibit program has stable IDs, chapter placement, caption/provenance scaffolding, page-flow mocks, reader-effect audits, prose bridges, and rights triage, but the fail-closed recomputation still gives 0 final publication-ready visual rows because render, capture, rights, caption, and source-note gates have not closed together.

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
- **69** original SVG/chart rows are conditionally publishable after render/caption/source-note gates.
- **30** selected rows are high-risk.
- **17** private/source screenshot captures still needed.
- **7** photo-rights reviews still needed.
- **6** company/source-surface rows need fair-use/source-actor review or redraw.
- **67** selected rows still have caption warning/fail gates.
- **9** chapters still show crowding or reader-fatigue defects.
- **0** selected rows have final full-book render proof.
- **0** selected rows should be called publication-ready yet.

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
