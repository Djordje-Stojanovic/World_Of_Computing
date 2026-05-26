# Source Download Automation and Provenance Plan - Pass I-0183

This pass extends the existing source snapshot protocol into an execution plan. The repository already has naming rules, quote limits, and snapshot metadata; the missing layer is a capture queue, typed workflows, output paths, hash requirements, rights notes, and failure handling that keep future downloads auditable without pulling heavyweight media into Git.

## Planned Machinery

The planned capture workflow should be queue-driven. A future `scripts/source_capture.ps1` or `scripts/source_capture.py` can read rows shaped like `data/source_download_capture_queue_i0183.tsv`, validate required fields, perform one capture method, write a capture log row, and refuse to promote claims until the source has the necessary hash, access date, allowed-use field, cutoff status, and blocker text.

Capture types should stay distinct:

- Static PDFs and papers: hash source files, commit notes and metadata, keep heavyweight PDFs ignored unless explicitly allowlisted.
- Mutable web pages: capture lightweight HTML/text when allowed; otherwise write a capture-note row that records 403, dynamic render, robots, or paywall limits.
- Screenshots and source-page images: save rasters under ignored `assets/` paths, commit only hashes, viewport/title/URL metadata, rights notes, and manifest rows.
- Decks and local PDFs: render selected pages to ignored rasters, record source PDF hash, page number, rendered image hash, dimensions, captions, and blocked claims.
- Leaderboards/pricing/API rows: normalize captured source data into TSV rows with snapshot IDs before charting.

## Git Safety

The current `.gitignore` already blocks PDFs, raster/video/audio assets, archives, caches, and rendered outputs while allowing SVG/CSV/TSV/JSON/MD/TXT provenance files. The automation should enforce that policy before commit: source media can exist locally, but committed evidence should be ledgers, hashes, notes, normalized rows, captions, and redraw source files.

## Failure Handling

Blocked captures are useful evidence when recorded honestly. A 403, binary payload, account-specific console, robots concern, paywall, or dynamic-render failure should create a capture-note row with a hash and status such as `capture_blocked`, `rejected`, or `superseded`, not a silent gap. Such rows can support provenance planning, but they cannot support new claims until stronger evidence exists.

## Outputs

- `data/source_download_automation_plan_i0183.tsv`: 10 planned workflows for source intake, PDFs, web captures, screenshots, decks, normalized data extraction, rights/quote review, manifest sync, git safety, and error handling.
- `data/source_download_capture_queue_i0183.tsv`: required queue fields and validation rules for future capture jobs.
- `data/source_download_gitignore_audit_i0183.tsv`: audit of the current ignore/allowlist policy for heavyweight source media.

No download, screenshot, PDF render, or manifest row was created in this pass.
