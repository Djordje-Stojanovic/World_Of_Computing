# I-0210 Real-World Source-Media Acquisition Wave 1

## Pass Result

This pass created the first local ignored source-media bank for the real-world image program. It attempted 30 downloads and retained 16 local source-media files under `assets/source_media/i0210_wave1/`: five Commons/physical images, nine official HTML source surfaces, and two DeepSeek arXiv PDFs. The files are deliberately ignored by Git; the committed evidence is the queue, log, rights review, manifest-sync draft, source rows, asset rows, and claim row.

## Captured Set

Captured images:

- A-0168 Jensen Huang cropped portrait
- A-0169 TSMC Fab5 building
- A-0170 Google data center in The Dalles
- A-0171 Electrical substation
- A-0177 Silicon wafer

Captured official/source surfaces:

- A-0183 Anthropic Claude 4 news page
- A-0184 Google Gemini announcement page
- A-0185 Meta Llama 3.1 announcement page
- A-0186 DeepSeek-R1 arXiv PDF
- A-0187 DeepSeek-V3 arXiv PDF
- A-0188 Microsoft/OpenAI extended partnership page
- A-0189 NVIDIA H100 product page
- A-0190 ASML EUV lithography systems page
- A-0192 Anthropic Claude Code page
- A-0193 Anthropic Claude Code overview docs
- A-0197 DeepSeek home page

## Evidence And Gates

Committed evidence:

- `data/capture_queues/i0210_real_world_media_queue.tsv`
- `data/capture_logs/i0210_real_world_media_download_log.tsv`
- `data/rights_reviews/i0210_real_world_media_rights.tsv`
- `data/manifest_sync/i0210_real_world_media_manifest_sync.tsv`
- `sources.tsv`
- `assets_manifest.tsv`
- `claims.tsv`

The capture log records sha256 hashes, file sizes, access dates, source URLs, status, and failure caveats. Failed rows are retained because they tell later passes which filenames or pages need replacement rather than silent retry.

## Claim Firewall

These captures are not publication-ready exhibits yet. They do not clear final rights, attribution, quote limits, fair-use treatment, mutable-page cutoff status, final layout placement, image quality, or render QA. Captions must continue blocking adoption, revenue, market share, capacity, workload, performance-rank, safety, current-UI, delivered-power, and model-superiority claims unless a later same-scope source row supports them.

## A/B Judgment

Against the pre-pass champion, this is a clear improvement in substrate rather than final beauty: the book now has a locally hashed real-world/source-surface bank spanning people, fabs, data centers, chips/materials, product/model pages, coding-agent pages, and DeepSeek reports. The hard limitation is equally visible: 14 targets failed or remain rights-blocked, so the pass improves production readiness only as private-use evidence and provenance, not as final image placement.
