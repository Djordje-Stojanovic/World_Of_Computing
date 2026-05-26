# Frontier Model Pages Capture Batch (I-0200)

Status: blocked, recorded.

Pass I-0200 attempted the second product/interface screenshot batch for frontier model pages and model-card-adjacent surfaces. It selected seven targets across OpenAI, Anthropic, Google, Meta, Qwen, DeepSeek, and LMArena/Hugging Face so the failure record would cover the intended breadth of the queue item rather than repeating only the first product screenshots.

The Browser plugin was reloaded according to its skill instructions and a fresh connection attempt was made. The in-app browser backend again reported `iab` unavailable. Local fallback checks again found no Python `playwright`, `selenium`, `pyppeteer`, or `PIL` package, and no `msedge`, `chrome`, `chromium`, or `firefox` executable on `PATH`.

## Target Set

| Capture ID | Asset | Source IDs | Surface | URL or path | Result |
| --- | --- | --- | --- | --- | --- |
| CAP-20260526-006 | A-0037 | S-0078 | ChatGPT Plus productization surface | https://openai.com/blog/chatgpt-plus | capture_blocked |
| CAP-20260526-007 | A-0040 | S-0007 | Claude 4 launch/model-line surface | https://www.anthropic.com/news/claude-4 | capture_blocked |
| CAP-20260526-008 | A-0053 | S-0121 | Gemini launch product/research banner | assets/source_docs/google_deepmind/S-0121_google-gemini-ai-launch-blog.html | capture_blocked |
| CAP-20260526-009 | A-0046 | S-0113 | Llama 3.1 open-weight strategy surface | https://ai.meta.com/blog/meta-llama-3-1/ | capture_blocked |
| CAP-20260526-010 | A-0049 | S-0027 | Qwen3 arXiv source surface | https://arxiv.org/abs/2505.09388 | capture_blocked |
| CAP-20260526-011 | A-0050 | S-0029 | DeepSeek-R1 arXiv source surface | https://arxiv.org/abs/2501.12948 | capture_blocked |
| CAP-20260526-012 | A-0013 | S-0080 | Arena historical dataset source page | https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset | capture_blocked |

## Evidence Created

- `data/capture_queues/i0200_frontier_model_pages_queue.tsv` records the seven intended targets and the expected screenshot/hash fields.
- `data/capture_logs/i0200_frontier_model_pages_capture_log.tsv` records that no raster, source HTML, page title, viewport, or publication-ready output exists.
- `data/capture_logs/i0200_frontier_model_pages_failure_records.tsv` records runtime unavailability and retry action for each target.
- `data/rights_reviews/i0200_frontier_model_pages_rights_review.tsv` keeps rights review blocked with zero quote allowance.
- `data/source_snapshots/2026-05-26/` contains seven new hashed capture notes for CAP-20260526-006 through CAP-20260526-012.

## Claim Firewall

The I-0200 notes are provenance handles only. They do not support exact quotation, live/current UI, model rank, benchmark superiority, safety success, adoption, revenue, productivity, subscriber count, current availability, license interpretation, open-weight impact, reasoning dominance, price-quality, or broad-intelligence claims.

Next action: stop scheduling additional screenshot batches until a browser/runtime preflight passes, then retry I-0199 and I-0200 targets before manifest promotion.
