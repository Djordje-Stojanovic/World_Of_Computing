# AGENTS.md

This workspace is for the Codex `/goal` loop defined in `GOAL.md`.

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
