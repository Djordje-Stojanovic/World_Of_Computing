# GOAL.md - Next Token Chronological Publication Sprint

Read this file fully before acting. Then run exactly one FIFO loop pass per invocation, record what happened, commit, push, and continue forever when launched with `/goal`.

## 0. FINAL PHASE — Page-by-Page Perfection (I-0337)

The ten rescue passes are complete. The book now enters its final and ONLY remaining phase: page-by-page manual perfection of the rendered PDF.

### Current State (2026-05-27)

- **PDF:** `rendered/final_i0337/Next-Token-final-i0337.pdf` — 61.9 MB, ~710 pages, 296 images remaining (4 removed from wrong chapters, pending relocation to correct chapters)
- **HTML source:** `rendered/final_i0337/Next-Token-final-i0337.html` — 97 MB, all fixes applied via BeautifulSoup
- **Base:** I-0320 quantitative-enriched HTML (culmination of all rescue visual passes)
- **Fixes applied:** Title page, verso page, Table of Contents, 200 images relocated from chapter-start dumps into prose flow, 68 bad captions fixed, 25 process elements removed, page-break directives removed, BERT/NVIDIA/4 person images removed from Chapter 1
- **Page tracking:** `data/page_perfection_log_i0337.tsv` — one row per page
- **Pages done:** 1 (title), 2 (verso), 3 (TOC), 4 (Ch1 opening), 5 (Transformer prose), 6 (attention), 7 (positional encoding), 8 (Transformer block), 9 (GPT bridge) — all PERFECT
- **Page in progress:** 27
- **Images relocated:** BERT→Ch2, NVIDIA Blackwell→Ch14, Vinyals/Vaswani/Shazeer/Gomez→Ch1 (pending re-insertion with text context)

### What "Perfect" Means Per Page

For EACH page, verify ALL of the following before marking PERFECT:

1. **No blank pages.** If a page has <10 words and 0 images, it must be removed or filled.
2. **No sparse pages.** If a page has <50 words and 0 images, it needs more content or restructuring.
3. **Images must have text context.** No bare image pages (image + <15 words). Images must sit near relevant prose.
4. **Correct image placement.** Every image belongs in its chronologically correct chapter. No NVIDIA Blackwell in Chapter 1. No BERT page in the Transformer chapter. Person images must accompany narrative about that person.
5. **No process language.** Zero instances of: Date span, Cutoff guard, Status, notes ledger, Place Figure, Visual integration, Visual anchor, this pass, later pass, future pass, remains blocked, shown as a public web page.
6. **No editorial labels.** Zero: ARCHITECTURE, PREHISTORY, MEASUREMENT chapter category tags.
7. **Clean captions.** Every caption describes what the reader sees in plain English. No ledger IDs, no manifest paths, no internal project references.
8. **Chronological flow.** The narrative moves forward in time. The reader should feel historical momentum.
9. **Professional typography.** Good line breaks, no orphans/widows issues, proper heading hierarchy.
10. **Reads like a book, not a project artifact.** No AI/process/workflow traces visible to the reader.

### Image Placement Rules (CRITICAL — all 300 images must be placed)

Every image must be manually placed at a specific, intentional position:

1. **Correct chapter by CONTENT.** The manifest's F01.xx→Ch1 assignments are often wrong. Match by what the image depicts: Transformer paper→Ch1, BERT→Ch2, Scaling Laws→Ch3, GPUs/Blackwell→Ch14, GTC→Ch15, etc.
2. **Text context above AND below.** No bare image pages. Image sits between paragraphs that discuss it.
3. **Max 1 image per page.** Page-break before consecutive images.
4. **After the prose that introduces it, before the prose that moves on.**
5. **Clean caption.** Plain English. No ledger IDs, no "shown as a public web page."
6. **Every relocation logged.** Track which image moved from where to where.

### Process Per Page

1. Inspect the page in the rendered PDF.
2. Identify any violations of the "perfect" criteria above.
3. Edit `rendered/final_i0337/Next-Token-final-i0337.html` to fix.
4. Re-render via Chrome headless.
5. Verify the page is now perfect.
6. Log the page in `data/page_perfection_log_i0337.tsv`.
7. Commit and push.
8. Move to the next page.

**No more automated passes. No more batch edits. No more scripts that touch everything at once. One page at a time until every page is perfect, then the book is published.**

## 0. Mission (original)

Finish **Next Token: The Race to Build the Machines That Learned Language, Code, and Computing** as a 100,000-120,000 word, exactly 24-chapter, deeply sourced, visually maximal **private personal edition** about large language models through the hard factual cutoff of **May 24, 2026**.

This is now a direct 10-pass rescue sprint. The previous "clean enough" proof is not accepted as final because it opened in the wrong place, exposed internal project bureaucracy to the reader, contained blank and sparse pages, used visual portfolio dumps, allowed multi-image boards, and did not read like a professional chronological nonfiction book.

The book must read like a serious, fast, visually rich trade book: clear chronology, strong facts, real images, charts, tables, screenshots, papers, logos, people, and source surfaces placed where they serve the story. It must not read like a project ledger, audit report, AI-generated assembly, or permissions memo.

## 1. Non-Negotiable Invariants

- Factual cutoff: May 24, 2026. No post-cutoff event may be written as happened history. Announced roadmaps, expectations, and forecasts known by the cutoff may appear only with clear labels.
- Topic: LLMs specifically. Hardware, datacenters, CUDA, chips, CPUs, datasets, tools, coding agents, evaluation, companies, and power appear only where they explain LLM progress.
- Structure: exactly 24 main chapters, >100,000 and <120,000 words.
- Chronology: the reader-facing book must move historically forward. It should begin at the Transformer/attention breakthrough, with only brief necessary prehistory, then progress through GPT, scaling, instruction tuning, ChatGPT, frontier labs, open weights, China, benchmarks, NVIDIA/chips/datacenters, tools, coding agents, reasoning, economics, failure modes, and the May 24, 2026 cutoff.
- Opening: do not open the book with ChatGPT as Chapter 1. ChatGPT is a later chronological turning point.
- Final private-edition visual target remains visually maximal: at least 100 curated charts/data/SVG/visualization exhibits, at least 50 real photos/screenshots/source images, 25-30 paper/arXiv/report excerpt or figure/page exhibits, 25-30 PDF/annual-report/slide/presentation/technical-report page exhibits, 20 model-card/Hugging Face/benchmark/leaderboard/repo/documentation screenshot or excerpt exhibits, at least 50 company/lab/product logos placed with narrative purpose, at least 10 benchmarking tables with yearly coverage from GPT-1 through the cutoff, and at least 30 CEO/founder/research-leader/person photographs or public-profile images where they make the story feel real.
- Visual placement: every kept visual must sit beside or near the argument, scene, date, mechanism, person, company, benchmark, or source it serves. No terminal atlas dump. No chapter "visual portfolio" pages. No composite logo/person/source-surface boards in the reader-facing PDF.
- Visual density: no more than one visual exhibit per page. Cut, split, or relocate multi-image pages. Do not keep empty or half-empty pages unless a deliberate title/part page is specifically justified and visually polished.
- Reader-facing captions: use plain English. A caption says what the reader is seeing, when it matters, and why it belongs there. It must not contain raw ledger IDs, internal asset IDs, project notes, rights memos, blocked-claim boilerplate, or audit language.
- Endnotes-only sourcing: provenance, checksums, source IDs, rights notes, claim boundaries, and blocked-claim controls stay in ledgers and endnotes. They do not appear as visible caption boilerplate.
- Forbidden reader-facing strings include: `Use note`, `Boundary:`, `Blocked claims`, `Source/provenance`, `project ledgers`, `private-edition visual layer`, `source boundaries`, `F01.`, `A-0`, `VX`, `S-0`, `C-0`, `sha256`, local filesystem paths, `C:/`, `file:///`, and any wording that says or implies the book was generated by an AI or assembled from a workflow.
- Sourcing standard: investigative. No fabricated quotes, interviews, scenes, captions, leaked claims, or insider access.
- Unsupported factual claim count must be zero before done-enough, or any remaining uncertain material must be explicitly quarantined outside the reader-facing book.
- Truth outranks beauty; beauty outranks completeness when both versions are equally true.
- No generic "AI will change everything" futurism unless tightly grounded in sources available by the cutoff.
- No robotics. No image/video diffusion history except brief contrast or context. No regulation/copyright/bureaucracy chapters except unavoidable brief context.
- Private-use visuals may use found/company/presentation/screenshot material, including Google image results and source screenshots, without waiting for public publication permission, as long as local provenance remains in `assets_manifest.tsv` or a linked acquisition ledger.
- `GTC-2026-Keynote.pdf` is a major local source candidate for NVIDIA/GTC chapters; use it with page-level provenance where valuable.
- NVIDIA DGX Spark, GTC 2026, datacenters, power, chips, China/frontier labs, and the last six months before cutoff should be emphasized where cutoff-supported and relevant to the LLM race.
- Never overwrite `champion/` without a backup or clearly recorded replacement.
- Never use destructive git operations. Never delete user files. Never leak secrets.

## 2. State

Maintain these files and directories:

- `champion/` - current best manuscript, design files, rendered PDF pointers, and scorecards.
- `archive/` - stepping-stone variants and preserved champion backups.
- `scoreboard.tsv` - append-only experiment ledger with one row per pass.
- `ideas.tsv` - FIFO queue. Execute the first pending idea unless specific evidence rules it out.
- `insights.md` - distilled reusable lessons.
- `sources.tsv` - source ledger.
- `claims.tsv` - claim audit ledger.
- `assets/` - charts, photos, screenshots, extracted presentation images, generated diagrams, source snapshots, and data tables.
- `assets_manifest.tsv` - visual provenance ledger.
- `manuscript/` - working book files.
- `rendered/` - local PDFs and render QA outputs.
- Git repository - canonical version-control trail for source files, ledgers, lightweight charts/data, outlines, manuscripts, and loop state.

Before planning each pass, read `GOAL.md`, `insights.md`, the tail of `scoreboard.tsv`, and the first pending rows in `ideas.tsv`. Use `rg` before repeating work.

GitHub remote:

- Repository: `https://github.com/Djordje-Stojanovic/World_Of_Computing.git`
- Branch: `main`
- Never force-push. Never rewrite shared history. Never run destructive git commands.
- Keep heavyweight/private-use media out of Git by default while keeping it locally in the workspace for book production.

## 3. The Ten FIFO Rescue Passes

The active finish sprint is exactly ten passes:

1. `I-0313` - delete reader-facing bureaucracy and raw ledger language from the book.
2. `I-0314` - convert sourcing and captions to clean endnotes-only trade-book style.
3. `I-0315` - rebuild the 24-chapter chronological spine so the book begins with the Transformer/attention era, not ChatGPT.
4. `I-0316` - add chapter date ranges, visible timelines, timestamps, and cutoff controls.
5. `I-0317` - remove blank, sparse, and half-empty pages through layout repair.
6. `I-0318` - rebuild visual placement so images sit beside the text they serve.
7. `I-0319` - enforce max-one-visual-per-page and remove composite boards, portfolio plates, and visual dumps.
8. `I-0320` - add missing numbers, stats, formulas, benchmarks, comparisons, charts, and tables.
9. `I-0321` - run hostile PDF proofread and rendered-page visual QA.
10. `I-0322` - build the final publication candidate, reader guide, hashes, QA report, commit, and push.

If a pass reveals a severe defect, the next pass must repair it directly instead of doing ceremonial polishing.

## 4. Loop Protocol

One pass means one scoped rescue operation, capped by one agent invocation and one render/check cycle.

1. Re-baseline the current champion and measure the relevant defects fresh.
2. Pull latest `main` when possible.
3. Execute the first pending FIFO idea.
4. Act surgically, but do not preserve a flawed structure merely because the old sprint optimized around it.
5. Render or check the changed surface with programmatic QA.
6. Promote only if the pass improves the book or fixes a hard defect without meaningful regression.
7. Record the result in `scoreboard.tsv`, `ideas.tsv`, `claims.tsv`, `assets_manifest.tsv`, and/or `sources.tsv` as applicable.
8. Add one transferable lesson to `insights.md`.
9. Commit the completed pass and push `main`.
10. Keep the queue at the ten rescue tasks until `I-0322` completes.

## 5. Evaluator

The evaluator is the reader. The book fails if it feels like a pile of process artifacts.

Primary scalar: **Private Masterpiece BookScore**, 0-100.

Weights:

- 20% chronological narrative force and reader addiction.
- 15% visual richness that feels edited and contextual.
- 15% technical and historical correctness.
- 10% numbers, benchmarks, tables, charts, and measurable facts.
- 10% prose clarity and tension.
- 10% source integrity and claim discipline.
- 8% originality and rare insight.
- 7% page beauty, rhythm, and density.
- 5% ending force and handoff quality.

Hard render gates:

- Zero blank pages.
- Zero unintentionally half-empty body pages.
- Zero multi-visual pages.
- Zero `Visual Portfolio` or `PORTFOLIO PLATE` pages.
- Zero reader-facing bureaucracy strings listed in Section 1.
- Zero local path leaks.
- Zero visible AI/process/workflow traces.
- Exactly 24 main chapters.
- Word count remains >100,000 and <120,000.
- Final PDF has clean metadata.

## 6. Mandatory Topic Spine

The book must cover, in chronological order where possible:

- Transformer/attention breakthrough, with brief prehistory only as needed.
- GPT-1, GPT-2, GPT-3, scaling laws, instruction tuning, and RLHF.
- ChatGPT as the public interface turning point.
- OpenAI/Microsoft.
- Google, DeepMind, Gemini.
- Anthropic and Claude.
- Meta, Llama, open weights.
- Alibaba/Qwen, DeepSeek, GLM/Z.ai, Kimi/Moonshot, Mistral, MiniMax, xAI, Baidu, Tencent, Xiaomi MiMo, StepFun, NVIDIA Nemotron, and other top labs/models as supported.
- Benchmarks, model rankings, model cards, Hugging Face, leaderboards, repo/docs surfaces, and yearly model-landscape tables through May 24, 2026.
- GPUs, CPUs where relevant, CUDA, H100/B200/GB200, Vera Rubin as announced/roadmap if cutoff-supported, DGX Spark where cutoff-supported, GTC 2026, and AI factory infrastructure.
- Datacenters, power, networking, gas turbines, cooling, and inference economics where they explain LLM scaling.
- Datasets, tokenization, retrieval, tool use, agents, coding agents, SWE automation, reasoning/test-time compute, and failure/trust.
- A closing synthesis bounded by the cutoff.

## 7. Done-Enough

The private edition may be called done-enough only after `I-0322` when:

- Hard constraints pass.
- Unsupported factual claims are zero or quarantined outside reader-facing prose.
- Full-book PDF render passes all hard render gates.
- Source and asset ledgers remain auditable for private use.
- The requested private visual targets are met in a booklike way or remaining shortfalls are reported plainly.
- The final report states remaining weaknesses honestly.

Do not ask the user routine research questions. Search, inspect local files, update ledgers, render, and verify autonomously.
