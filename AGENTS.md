# AGENTS.md

This workspace is for the Codex `/goal` loop defined in `GOAL.md`.

## FINAL PHASE: Page-by-Page Perfection (I-0337)

The book is in its FINAL phase. No more passes. No more batches. No more automated sweeps.

### Current State

- **PDF:** 61.9 MB, ~713 pages, 300 images
- **HTML:** 97 MB, base from I-0320 with title/verso/TOC/captions/relocations applied
- **Log:** `data/page_perfection_log_i0337.tsv` — tracking every page
- **Pages done:** 1 (title), 2 (verso), 3 (TOC) — PERFECT
- **Page in progress:** 4 (Chapter 1 opening) — PENDING verification

### Per-Page Perfection Criteria

Mark a page PERFECT only when ALL hold:
1. Not blank (<10 words + 0 images = FAIL)
2. Not sparse (<50 words + 0 images = FAIL)
3. Images have text context (image + <15 words = FAIL)
4. Image belongs in correct chapter (no Blackwell in Ch1, no BERT in Transformer chapter)
5. Zero process language (Date span, Cutoff guard, notes ledger, Place Figure, this/later/future pass, remains blocked, shown as a public web page)
6. Zero editorial labels (ARCHITECTURE, PREHISTORY, etc.)
7. Clean captions (plain English, no ledger IDs, no manifest paths)
8. Chronological flow (narrative moves forward in time)
9. Professional typography (good breaks, proper hierarchy)
10. Reads like a book, not a project artifact

### Page Protocol

1. Inspect page N in `rendered/final_i0337/Next-Token-final-i0337.pdf`
2. If issues found, edit `rendered/final_i0337/Next-Token-final-i0337.html` surgically
3. Re-render via Chrome headless
4. Verify page N is perfect
5. Log in `data/page_perfection_log_i0337.tsv`
6. Commit + push
7. Move to page N+1

## Operating Rules

- Read `GOAL.md` fully before every serious pass.
- Optimize for Codex with shell, file I/O, web search, local rendering, and normal workspace files.
- Do not use DGX Spark as a judge for this project.
- Do not ask the user for routine research. Search the web, inspect local files, and update ledgers yourself.
- Treat `GTC-2026-Keynote.pdf` as an available local source asset.
- Keep provenance for every source, chart, photo, screenshot, and extracted slide.
- Use `rg` before repeating work.
- Keep edits scoped to one pass category.
- Never overwrite `champion/` without preserving the previous champion or recording the replacement.
- No destructive git commands.
- Use GitHub for autonomous progress. Commit each completed loop pass and push `main` when possible.
- Never force-push, reset hard, or rewrite history.
- Do not commit rendered PDFs, large images, videos, audio, caches, or heavyweight source media. Commit manuscripts, ledgers, outlines, scripts, small data tables, SVG/lightweight diagrams, and provenance records.
- If a pass is rejected, revert candidate artifact changes but commit the rejection result in `scoreboard.tsv`, `ideas.tsv`, and `insights.md`.

## Project Shape

- `GOAL.md` - loop contract.
- `ideas.tsv` - FIFO queue.
- `scoreboard.tsv` - append-only pass ledger.
- `insights.md` - distilled cognition base.
- `sources.tsv` - source ledger.
- `claims.tsv` - claim audit ledger.
- `assets_manifest.tsv` - visual provenance ledger.
- `manuscript/` - working book files.
- `champion/` - current best book state.
- `archive/` - stepping-stone variants.
- `assets/` - visual/data/source assets.
- `rendered/` - PDF outputs and render QA.
- `data/page_perfection_log_i0337.tsv` - FINAL PHASE: page-by-page perfection tracking.

## GitHub

Remote:

`https://github.com/Djordje-Stojanovic/World_Of_Computing.git`

Per-pass practice:

1. `git status --short --branch`
2. `git pull --ff-only origin main` when a remote exists and network is available
3. make one loop pass
4. `git diff --stat`
5. `git add` only pass-relevant lightweight/source files
6. `git commit -m "pass I-XXXX: <verdict/action>"`
7. `git push origin main`
