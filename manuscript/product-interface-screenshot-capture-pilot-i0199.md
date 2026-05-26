# Product Interface Screenshot Capture Pilot (I-0199)

Status: blocked, recorded.

Pass I-0199 attempted the first five product/interface screenshot targets from the I-0193 shortlist: ChatGPT launch, ChatGPT Enterprise, Gemini/Bard consumer relaunch, Claude product/model surface, and GitHub Copilot launch. The capture plan produced a queue row for each target and a hashed capture note for each failed attempt, but it did not create screenshot rasters, source HTML snapshots, page titles, viewport records, or manifest-ready exhibit rows.

The immediate blocker was runtime availability, not source selection. The Browser plugin setup reported the in-app browser backend `iab` unavailable. Local fallback checks found no Python `playwright`, `selenium`, `pyppeteer`, or `PIL` package, and no `msedge`, `chrome`, `chromium`, or `firefox` executable on `PATH`.

## Target Set

| Capture ID | Asset | Source IDs | Surface | URL | Result |
| --- | --- | --- | --- | --- | --- |
| CAP-20260526-001 | A-0121 | S-0006 | ChatGPT launch product surface | https://openai.com/index/chatgpt/ | capture_blocked |
| CAP-20260526-002 | A-0123 | S-0079; S-0089 | ChatGPT Enterprise source surface | https://openai.com/index/introducing-chatgpt-enterprise/ | capture_blocked |
| CAP-20260526-003 | A-0129 | S-0121; S-0119 | Gemini/Bard consumer relaunch surface | https://blog.google/products/gemini/bard-gemini-advanced-app/ | capture_blocked |
| CAP-20260526-004 | A-0130 | S-0007; S-0245 | Claude product/model surface | https://www.anthropic.com/news/claude-3-7-sonnet | capture_blocked |
| CAP-20260526-005 | A-0127 | S-0070 | GitHub Copilot coding assistant surface | https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/ | capture_blocked |

## Evidence Created

- `data/capture_queues/i0199_product_interface_queue.tsv` records the intended targets, target screenshot paths, expected hash fields, allowed private-use scope, and blocked claims.
- `data/capture_logs/i0199_product_interface_capture_log.tsv` records that no output raster, HTML, PDF, or image hash exists; only note hashes exist.
- `data/capture_logs/i0199_product_interface_failure_records.tsv` records the runtime failure category and retry action for each target.
- `data/rights_reviews/i0199_product_interface_rights_review.tsv` records rights review as blocked, with zero quote allowance and no publication use.
- `data/source_snapshots/2026-05-26/` contains five capture notes, each hashed in the capture log and failure record.

## Claim Firewall

The I-0199 notes are provenance handles only. They do not support exact quotations, current user-interface claims, adoption, usage, market share, revenue, productivity, code quality, security effectiveness, safety success, benchmark superiority, model-rank, enterprise deployment, developer-replacement, or daily-usage claims.

Next action: rerun the product/interface capture batch only after an approved screenshot runtime is available, then populate raster hashes, viewport, page title, source snapshot hash, rights decision, and manifest sync rows before any exhibit promotion.
