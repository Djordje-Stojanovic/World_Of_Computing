# AGENTS.md

This workspace is for the Codex `/goal` loop defined in `GOAL.md`.

## FINAL PHASE: Page-by-Page Perfection (I-0337)

The book is now in its FINAL phase. No more passes. No more batches. No more automated sweeps.

**The only remaining work:** go through every page of the rendered PDF ONE AT A TIME, make that single page perfect, log it in `data/page_perfection_log_i0337.tsv`, re-render, verify, then move to the next page. When every page is perfect, the book is published.

### Page Perfection Protocol

1. Open `rendered/final_i0337/Next-Token-final-i0337.pdf` and inspect page N.
2. Determine what would make this page perfect: correct image placement, proper text context, right image for the right chapter, good caption, no blankness, no process language, correct chronology.
3. Edit `rendered/final_i0337/Next-Token-final-i0337.html` to fix the page.
4. Re-render the PDF via Chrome headless.
5. Verify page N is perfect.
6. Log the page in `data/page_perfection_log_i0337.tsv` with columns: page, status, words, images, issue, action_taken, new_words, new_images, notes.
7. Commit and push after every page or small batch.
8. Move to page N+1.

### Rules for this phase

- Work ONE page at a time. Do not skip ahead.
- Every image must have text context above and below it.
- Images must be placed in their correct chronological chapter context.
- No blank pages. No sparse pages. No process language. No bad captions.
- Log every page fix in `data/page_perfection_log_i0337.tsv`.
- After each page is perfect, describe it to the user and ask if ready to proceed.

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
