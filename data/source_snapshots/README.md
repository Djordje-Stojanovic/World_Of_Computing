# Source Snapshots

This directory stores lightweight notes, manifests, hashes, and text/HTML captures for mutable sources. Use `manuscript/00-source-snapshot-protocol.md` as the authority for filenames, access dates, quote limits, and ledger updates.

Date-specific captures should live under:

```text
data/source_snapshots/YYYY-MM-DD/
```

Screenshots and visual captures belong under `assets/source_snapshots/YYYY-MM-DD/` and must also be recorded in `assets_manifest.tsv`.

Do not commit heavyweight pages, videos, audio, large rasters, caches, or private browser profiles. Commit the provenance row, normalized data, and hash or archive note instead.
