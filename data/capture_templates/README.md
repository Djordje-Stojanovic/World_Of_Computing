# Capture Template Kit (I-0198)

These lightweight TSV templates implement the I-0183 source-capture contract without downloading or committing heavy media.

Use this sequence for capture passes:

1. Copy `capture_queue_template.tsv` into a pass-specific queue such as `data/capture_queues/i0199_product_interface_queue.tsv`.
2. Fill one row per intended capture before running a browser, downloader, renderer, or manual capture.
3. Save heavyweight rasters/PDFs only under ignored `assets/` paths.
4. Record completed, blocked, rejected, or superseded jobs in a pass-specific log shaped like `capture_log_template.tsv`.
5. Add rights/quote rows before a screenshot, source card, photo, or quote enters final-art consideration.
6. Use `manifest_sync_template.tsv` to draft `assets_manifest.tsv` rows only after hashes, captions, story purpose, and blockers exist.
7. Use `failure_record_template.tsv` when a capture fails; blocked evidence is better than a silent gap.

Required invariant: a capture hash proves only that a local source surface exists. It never proves adoption, revenue, productivity, benchmark rank, safety, roadmap delivery, physical deployment, or model superiority.
