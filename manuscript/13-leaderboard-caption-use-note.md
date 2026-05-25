# Chapter 13 Caption And Use Note

Status: promoted claim-audit pass I-0044, 2026-05-25.

Paired assets:

- A-0014: `assets/visual_system/leaderboard-methodology-flow.svg`
- A-0013: `assets/visual_system/lmarena-may19-text-style-control-top12.svg`

Required order: A-0014 must appear before A-0013. The methodology figure teaches the reader how Arena-style rows become rank claims: votes, config/split/category filters, rating uncertainty, publication date, snapshot ID, and permission gates. Only after that should the historical top-row chart appear.

Caption pair:

Figure 13.y - How Arena Rows Become Rank Claims. Arena-style human preference votes become chartable only after filtering by config, split, category, publication date, and local snapshot. Source spine: S-0036, S-0056, S-0057, S-0080, SNAP-20260525-008; companion rows in `data/leaderboard_methodology_i0039.tsv`.

Figure 13.x - LMArena/Arena historical `text_style_control` leaderboard, `latest` split, `overall` category, top twelve rows published 2026-05-19. Source S-0080, snapshot SNAP-20260525-008; chart rows in `data/lmarena_may19_chart_i0034.tsv`.

Combined use rule: the pair can support a narrow historical claim that one official pre-cutoff Arena dataset slice had a tightly packed top cluster under `text_style_control`, `latest`, `overall`, published 2026-05-19. It cannot support live May 24 rank wording, model-release status, provider price-quality comparisons, task-specific superiority, coding-agent ability, safety, latency, enterprise usefulness, or broad "best model" prose.

Prohibited use checklist:

- Do not call A-0013 the live May 24 leaderboard.
- Do not infer product availability or release status from a model name in A-0013.
- Do not compare A-0013 rows to provider prices unless a later same-scope price-quality chart explicitly supersedes C-0046.
- Do not imply that Arena overall preference equals coding, agentic workflow, reasoning, safety, latency, or enterprise quality.
- Do not hide overlapping confidence intervals or clustered ratings behind ordinal rank drama.
