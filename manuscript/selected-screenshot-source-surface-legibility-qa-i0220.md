# I-0220 Screenshot And Source-Surface Legibility QA

This pass audits the 26 selected-100 rows that are screenshots, source screenshots, photo candidates, or extracted slide/source surfaces. It joins the selected matrix, manifest, caption QA, source-note QA, local hash ledgers, and GTC rendered-page ledger.

## Result

- 26 selected screenshot/source/photo/slide rows audited.
- 12 rows still require raster capture before publication.
- 6 rows have source HTML/hash evidence but no book-grade screenshot.
- 7 photo rows remain blocked by rights, creator/attribution, local resolution, crop, and caption-inference review.
- 1 row, A-0004, has a high-resolution private GTC page render with hash and dimensions, but still needs crop, small-type, rights, and caption/source-note page proof.
- 0 rows are publication-ready from this audit alone.

## Main Finding

The screenshot program is valuable as a provenance system, but not yet as a finished image program. Hash-recorded HTML source surfaces are useful production handles; they do not prove crop, resolution, small-type readability, PII/secrets safety, quote-limit compliance, caption neutrality, or final page fit.

## Gate

The next production work should either capture rasters with viewport/hash/crop metadata or deliberately convert weaker screenshot slots into source cards. Product and interface surfaces must remain claim-firewalled: they can show historical surfaces, not adoption, revenue, productivity, safety, autonomy, current UI, market share, or customer outcomes.
