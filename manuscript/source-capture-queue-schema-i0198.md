# Source-Capture Queue Schema (I-0198)

This pass implements the I-0183 capture plan as lightweight repository structure.

New committed template roots:

- `data/capture_templates/` - queue, log, rights/quote, manifest-sync, and failure-record TSV templates.
- `data/capture_queues/` - pass-specific planned capture queues.
- `data/capture_logs/` - pass-specific capture/failure logs.
- `data/rights_reviews/` - rights and quote review rows.
- `data/manifest_sync/` - draft manifest rows before editing `assets_manifest.tsv`.
- `data/source_snapshots/README.md` - date-folder convention for lightweight snapshots and capture notes.
- `assets/private_use_screenshots/README.md` and `assets/source_media/README.md` - ignored-heavy-media conventions.

The schema keeps one rule central: capture evidence is not claim evidence by itself. A hash can prove that a local screenshot, source page, rendered slide, or capture note exists. It cannot prove adoption, revenue, productivity, live rank, safety, roadmap delivery, physical deployment, or model superiority. Those claims still need normalized source rows, claim rows, captions, and blockers.

Gate result: promote as tooling+sourcing. This pass does not capture screenshots, download PDFs, render pages, clear rights, or add manifest assets. It makes future capture passes safer by giving them a queue shape, log shape, review path, and failure-record path.
