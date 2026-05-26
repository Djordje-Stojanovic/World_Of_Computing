# GOAL.md - Next Token Book Loop

Read this file fully before acting. Then run exactly one loop pass per invocation, record what happened, and continue forever when launched with `/goal`.

## 0. Mission

Build and finish, in the next focused 15 FIFO passes, **Next Token: The Race to Build the Machines That Learned Language, Code, and Computing** as a 100,000-120,000 word, exactly 24-chapter, deeply sourced, visually maximal **private personal edition** about large language models through the hard factual cutoff of **May 24, 2026**.

The book is no longer optimized for publication, awards submission, commercial release, permissions clearance, or legal public-use readiness. It is optimized for the user's private reading experience: the felt quality, density, visual richness, truth, narrative force, technical depth, rare insight, and visual elegance of a book that can sit beside or exceed *Chip War*, *The Prize*, *The Thinking Machine*, Walter Isaacson's *Steve Jobs*, and Walter Isaacson's *Elon Musk* in craft, while remaining a private-use artifact.

## 1. Invariants

These never change. If a candidate violates any item, revert or reject it immediately.

- Factual cutoff: May 24, 2026. No post-cutoff event may be written as happened history. Announced roadmaps, expectations, and forecasts known by the cutoff may appear only with clear labels.
- Topic: LLMs specifically. Include hardware, datacenters, power, CUDA, chips, CPUs, datasets, tools, coding agents, evaluation, and companies only where they explain LLM progress.
- Final private-edition target: exactly 24 main chapters, >100,000 and <120,000 words, **at least 100 curated charts/data/SVG/visualization exhibits**, **at least 50 real photos/screenshots/source images**, **25-30 paper/arXiv/report excerpt or figure/page exhibits**, **25-30 PDF, annual-report, slide, presentation, or technical-report page/image exhibits**, **20 model-card, Hugging Face, benchmark, leaderboard, repo, or documentation screenshot/excerpt exhibits**, **at least 50 company/lab/product logos placed with narrative purpose**, **at least 10 benchmarking tables**, including **at least one benchmark/model-landscape table for every year from GPT-1 through the May 24, 2026 cutoff**, and **at least 30 CEO/founder/research-leader/person photographs or public-profile images** where they make the story feel real. These targets are for the private edition and may use found web, Google image, company, source-page, PDF, screenshot, and presentation material without publication permission as long as local provenance is recorded.
- Sourcing standard: investigative. No fabricated quotes, interviews, scenes, captions, leaked claims, or insider access.
- Unsupported factual claim count must trend to zero and must be zero before done-enough.
- Truth outranks beauty; beauty outranks completeness when both versions are equally true.
- No generic "AI will change everything" futurism unless tightly grounded in sources available by the cutoff.
- No robotics. No image/video diffusion history except brief contrast or context. No regulation/copyright/bureaucracy chapters except unavoidable brief context.
- Private-use visuals may use found/company/presentation/screenshot material, including Google image results and source screenshots, without waiting for rights clearance or publication approval. Every asset must still record provenance in `assets_manifest.tsv` or a linked acquisition ledger: URL or search/source context when available, access date, local path, checksum, source type, visual role, and any uncertainty.
- The loop may download large batches of real-world/source-media items per visual acquisition pass from Google, NVIDIA, DeepSeek, OpenAI, Anthropic, Meta, Microsoft, AMD, CoreWeave, ASML, TSMC, Wikimedia, company sites, papers, PDFs, HTML pages, annual reports, presentations, newsrooms, blogs, documentation, model cards, Hugging Face pages, benchmark sites, and other relevant web sources. "Real-world image" includes photos, screenshots, logos, CEO/person images, paper excerpts, PDF/page renders, NVIDIA GTC and other presentations, DeepSeek papers/reports, company annual reports, technical reports, product pages, docs, model-card pages, benchmark tables, and other real source surfaces. Downloaded PDFs, HTML, images, extracted page renders, and source screenshots should be kept locally in the workspace for private book production, extraction, QA, and layout use, with provenance and quality metadata recorded.
- `GTC-2026-Keynote.pdf` is a major local source candidate for NVIDIA/GTC chapters; use it with page-level provenance.
- Never overwrite `champion/` without a backup or clearly recorded replacement.
- Never use destructive git operations. Never delete user files. Never leak secrets. Avoid irreversible edits.

## 2. State

Maintain these files and directories:

- `champion/` - current best manuscript, design files, rendered PDF, and scorecard.
- `archive/` - stepping-stone variants. Archive suboptimal work if it contains a rare source, superior scene, better voice, stronger explanation, useful visual design, or promising structure.
- `scoreboard.tsv` - append-only experiment ledger with one row per pass.
- `ideas.tsv` - append-only FIFO queue. Execute the first pending idea unless specific evidence rules it out; never cherry-pick silently.
- `insights.md` - distilled reusable lessons, separate from raw experiment results.
- `sources.tsv` - source ledger.
- `claims.tsv` - claim audit ledger.
- `assets/` - charts, photos, screenshots, extracted presentation images, generated diagrams, source snapshots, and data tables.
- `assets_manifest.tsv` - visual provenance ledger.
- `manuscript/` - working manuscript files by chapter.
- `rendered/` - PDFs and render QA outputs.
- Git repository - canonical version-control trail for source files, ledgers, lightweight charts/data, outlines, manuscripts, and loop state.

Before planning each pass, read `insights.md`, the tail of `scoreboard.tsv`, and the first pending rows in `ideas.tsv`. Search with `rg` before repeating work.

GitHub remote:

- Repository: `https://github.com/Djordje-Stojanovic/World_Of_Computing.git`
- Branch: `main` is the durable autonomous-progress branch.
- Never force-push. Never rewrite shared history. Never run destructive git commands.
- Keep heavyweight/private-use media out of Git by default while keeping it locally in the workspace for book production. Track provenance, captions, data tables, SVG/lightweight diagrams, source notes, and manuscripts; exclude rendered PDFs and large raster/video/audio assets from commits unless the user explicitly asks to commit them.

## 3. The Loop

One pass means one chapter/section-level revision or one visual/data package, capped by one agent invocation and one rendered PDF/check cycle.

1. **Re-baseline.** Inspect the champion and re-measure relevant objective checks fresh. Do not trust stale scorecards. Note drift.
2. **Refresh bounded substrate.** The cutoff is fixed, but sources that existed by May 24, 2026 may still be discovered. Search aggressively for the current chapter/topic.
3. **Plan.** Consult `insights.md`; pop the first pending idea from `ideas.tsv`. Choose a parent: 50% champion, 50% archive. After structure stabilizes, shift to 70% champion only if the discovery curve supports it.
4. **Act surgically.** Make one change category: one chapter draft, one section rewrite, one source pack, one visual system, one chart package, one claim audit, or one PDF/design pass. Avoid whole-book rewrites unless the idea explicitly concerns structure.
5. **Verify.** Run all feasible programmatic checks for the changed surface. Use self-judging LLM critique with hostile honesty. Compare candidate vs parent in A/B and B/A order when practical.
6. **Gate.** Promote only if BookScore improves by at least +1.0 or a hard invariant is fixed with no meaningful regression. If not champion-worthy but novel/valuable, archive it. Otherwise reject.
7. **Record.** Append `scoreboard.tsv`; update source, claim, and asset ledgers; mark the idea done or rejected with evidence.
8. **Distill.** Add one transferable lesson to `insights.md`: what this pass proved or ruled out and why.
9. **Version.** Commit every completed pass. If promoted, commit the changed manuscript/design/ledger state. If archived, commit the archive entry plus ledgers. If rejected, revert candidate artifact changes but still commit the scoreboard/insight/idea result so failures become memory. Push `main` after each commit when network/auth is available.
10. **Refill queue.** If fewer than 5 pending ideas remain, append dimension-diverse ideas biased toward weak metrics and unexplored topics.

## 4. Evaluator

The evaluator is the product. Be harsh. It is better to call the book bad and improve it than to ship beautiful garbage.

Primary scalar: **Private Masterpiece BookScore**, 0-100, higher is better.

Weights:

- 20% private reading awe: does the book feel like a rich, finished, physical world rather than text plus placeholders?
- 15% visual density and variety: photos, screenshots, logos, papers, PDFs, tables, model cards, benchmark surfaces, chips, clusters, fabs, and people.
- 15% serious tech/history canon durability, benchmarked against *Chip War*, *The Prize*, and *The Thinking Machine* for quality, not award eligibility.
- 10% Goodreads-style reader addiction, fun, and word-of-mouth appeal.
- 10% narrative quality: scenes, pacing, stakes, character, chapter endings.
- 10% technical depth and correctness.
- 8% originality and rare insight: non-obvious sources, overlooked mechanisms, hard-to-find details.
- 7% visual/data beauty and usefulness.
- 5% prose beauty: rhythm, clarity, compression, wit, sentence-level force.

Programmatic metrics:

- Word count is >100,000 and <120,000.
- Chapter count is exactly 24 main chapters.
- Curated charts/data/SVG/visualization exhibit count is at least 100, separate from the private-edition real-world/source-surface targets: 50+ real photos/screenshots/source images, 25-30 paper/report excerpt exhibits, 25-30 PDF/presentation/report page exhibits, 20 model-card/Hugging Face/benchmark/repo/docs screenshots or excerpts, 50+ logos, 10+ benchmark tables with yearly coverage from GPT-1 through cutoff, and 30+ CEO/founder/research-leader/person images.
- Every chapter has 3-4 strong exhibit candidates on average, while final layout may use fewer where prose rhythm or rights constraints demand restraint.
- Every visual/source exhibit has caption, source/provenance, private-use status, story purpose, and blocked-claim note.
- Every downloaded source-media item has local path, original URL or search/source context when available, source ID when applicable, access date, file size, checksum, private-use note, extraction status, quality score, diversity role, story-fit note, and blocked-claim note before it is treated as an exhibit candidate.
- Source density target is one citation per 150-250 words in factual/reporting-heavy sections.
- Unsupported factual claim count trends to zero.
- Primary-source ratio is tracked and raised when possible.
- Claim coverage ratio is tracked.
- Duplicate section/story similarity is below threshold.
- Technical terms are explained for smart business readers and software engineers.
- Timeline coverage spans early language modeling through May 24, 2026.
- Company/person/topic balance is tracked.
- PDF render has no broken refs, missing captions, overflows, unreadable charts, or ugly layout failures.

Subjective judged metrics:

- Beautiful prose.
- Addictive readability.
- Seriousness and honesty.
- Data/visual elegance.
- Fun, surprise, humor, and inspiration.
- Genuine superiority to the benchmark canon as a private reading object, not just length or polish.

Debiasing:

- When judging prose or structure, compare candidate vs champion both A/B and B/A when practical.
- Penalize verbosity explicitly.
- Penalize generic AI futurism, hype-bro tone, fake insider vibes, unsupported drama, and textbook dryness.
- Demand evidence. If a claim sounds exciting but is not sourced, score it as a defect.

Ground-truth anchors:

- Factual claims need cited support.
- Technical claims need papers, docs, code, benchmarks, talks, or credible primary/secondary sources.
- Model rankings, prices, and context windows need source snapshots and access dates.
- Visuals need provenance in `assets_manifest.tsv` or linked acquisition ledgers, but public-use permission is not a gate for the private edition.

## 5. Archive And Quality-Diversity

Do not collapse into single-champion hill-climbing. The archive is how this loop avoids a local optimum.

Niche descriptors:

- Narrative mode: investigative thriller, explanatory epic, character-driven, technical deep dive, comic/sharp, visual-data driven.
- Topic axis: model architecture, lab politics, product launch, hardware, datacenter/power, open source, coding agents, benchmarks, economics, obscure history.
- Reader effect: awe, clarity, suspense, anger, delight, surprise, intellectual snap.
- Visual mode: timeline, map, architecture schematic, leaderboard, system diagram, cost curve, datacenter/power diagram, family tree.

Keep at least one elite variant per important niche. Parent sampling must sometimes draw from `archive/`, not only `champion/`.

Novelty score:

- +2 for a new primary-source cluster.
- +2 for a new visual grammar.
- +2 for a structurally different chapter approach.
- +1 for a rare model/lab/source not already represented.
- +1 for a prose voice that improves reader pull without sacrificing truth.

## 6. Open-Endedness Engine

The artifact is cutoff-bounded, not creativity-bounded. Continue improving through:

- Combinatorial recombination of chapter orders, scenes, explanations, source clusters, visual treatments, and voice.
- A self-raising rubric: every 5 passes, add one harder criterion the current champion fails.
- Forced beyond-space jumps on plateau: new structure, new source axis, new visual grammar, new recurring motif, new scoring harness, or new chapter mechanism.

Plateau rules:

- No promotion after 5 experiments: force parent selection from `archive/`.
- No promotion after 10 experiments: perform a beyond-space jump.
- Repeated full-book passes with all hard constraints satisfied and no meaningful score gain: mark done-enough with evidence, but do not pretend perfection.

## 7. Anti-Reward-Hacking And Anti-Degradation

- Never improve prose by weakening truth.
- Never improve visual beauty by making charts less legible or less sourced.
- Never increase word count with filler.
- Never add a model/lab because it is trendy unless it matters to the LLM story.
- Never write future events as fact.
- Never copy benchmark-book prose. Use them as quality targets, not templates.
- Every major edit must preserve or improve claim support.
- Every PDF/design pass must verify readability and layout.
- If the loop starts optimizing easy counts instead of private-edition quality, stop and tighten the evaluator before continuing.
- Git history is part of the safety system. Commit small, auditable steps. Do not hide failed experiments; record them and revert candidate artifact changes cleanly.

## 8. Scaling Self-Monitor

Track cumulative BookScore, promotions, archive additions, hard-constraint fixes, source count, claim coverage, visual count, and rendered-PDF quality vs cumulative passes in `scoreboard.tsv`.

A flattening discovery curve is not victory. It triggers exploration, archive sampling, beyond-space jumps, source refresh, or rubric hardening.

## 9. Budget, Transfer, And Observability

Budget unit: one chapter/section-level revision or one visual/data package per pass.

Cheap proxy: local section/chapter checks plus targeted judge critique.

True target: full-book PDF review and full BookScore recomputation.

Transfer checks:

- After every major chapter batch.
- After every visual-system change.
- After any promotion affecting structure or voice globally.
- Before declaring done-enough.

Human-facing outputs:

- Current champion PDF in `rendered/`.
- Scoreboard tail in `scoreboard.tsv`.
- Latest distilled lessons in `insights.md`.
- Source and asset ledgers.
- Discovery curve notes in scoreboard reason fields.
- GitHub commit history and pushed `main`.

Git protocol per pass:

1. Start with `git status --short --branch`.
2. If remote work may exist, run `git pull --ff-only origin main` before editing.
3. Do the loop pass.
4. Run targeted checks and `git diff --stat`.
5. Stage only source/ledger/lightweight files that belong to the pass. Do not stage ignored heavy assets.
6. Commit with `pass <idea_id>: <short verdict/action>` or `setup: <short description>`.
7. Push `main`.
8. If push fails because remote is ahead, pull with `--ff-only`, resolve only non-conflicting ledger/source changes, then push. If a real conflict appears, preserve both sides and ask only if it cannot be resolved from local context.

Context economy:

- Use `rg` and targeted reads.
- Do not read huge generated files wholesale.
- Prefer source snapshots and ledgers over re-discovering known facts.
- Re-read `GOAL.md` and `insights.md` periodically.

## 10. Mandatory Topic Spine

The book must cover:

- Early language modeling and classical ML context where necessary.
- Word embeddings, seq2seq, attention, Transformer.
- Scaling laws.
- GPT-1, GPT-2, GPT-3, and the road to ChatGPT.
- A major ChatGPT chapter.
- Instruction tuning and RLHF.
- OpenAI/Microsoft.
- Google, DeepMind, Gemini.
- Anthropic and Claude.
- A major Claude Code/coding agents chapter.
- Meta, Llama, open weights.
- Alibaba/Qwen, including Qwen 2, Qwen 3, Qwen 3.5, and Qwen 3.6 family where supported.
- DeepSeek, including V3/R1/V4-era systems where supported by cutoff sources.
- GLM/Z.ai, Kimi/Moonshot, Mistral, MiniMax, xAI, Baidu, Tencent, Xiaomi MiMo, StepFun, NVIDIA Nemotron, and other top labs/models as supported.
- Top open-source and proprietary model-rankings landscape as of cutoff, with source snapshots.
- Coding agents, harnesses, evaluation, tool use, SWE automation.
- GPUs, CPUs where relevant, CUDA, H100/B200/GB200, Vera Rubin as announced/roadmap if cutoff-supported.
- Datacenters, power, networking, gas turbines where they explain LLM scaling.
- A major NVIDIA GTC 2026 chapter, using `GTC-2026-Keynote.pdf` if valuable.
- Datasets, tokenization, inference economics, reasoning/test-time compute.
- Architecture deep dives throughout.

## 11. Priorities When They Conflict

1. Truth, safety, and invariants.
2. Source integrity and provenance.
3. Primary BookScore gains past the improvement floor.
4. Narrative addiction and prose beauty.
5. Technical depth.
6. Visual beauty and data usefulness.
7. Novelty and archive diversity.
8. Simplicity: at equal score, choose the clearer, truer, more vivid, less self-indulgent version.

## 12. Done-Enough And Never-Stop

The loop is now in a 15-pass private-edition finish sprint. It may mark the private edition done-enough only when:

- Hard constraints pass.
- Unsupported factual claims are zero or explicitly quarantined.
- Full-book PDF render passes.
- Source and asset ledgers are auditable for private use.
- The requested private visual targets are either met or explicitly reported as the only remaining shortfall after the fifteenth sprint pass.
- The final report states the remaining weaknesses honestly.

Do not ask the user routine research questions. Find sources and files yourself. Ask only if blocked by missing permissions, inaccessible files, or a genuine objective contradiction.

## First-Pass Command

From this workspace, run:

```text
/goal Read GOAL.md fully, then run the loop forever per its protocol.
```
