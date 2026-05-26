# GTC-2026 Chart Mining Pass (I-0184)

This pass inspected all 76 pages of `GTC-2026-Keynote.pdf` with local PDF text extraction and converted the deck into an explicit chart-mining artifact. The result is not another slide gallery. It is an evidence map for the NVIDIA chapter: which pages carry NVIDIA's AI-factory argument, which pages are only product/spec support, and which chart-like pages should be dropped because they invite overclaiming.

The strongest thesis surface remains page 29: "AI Factories are the Industrial Infrastructure of the AI Era." Pages 51, 49, and 50 form the best follow-on sequence: DSX platform, one-gigawatt system comparison, and roadmap cadence. This confirms the later I-0192 shortlist rather than replacing it.

The new value from the all-page scan is the economics and mechanism reserve lane. Pages 27, 32, 36, 37, 40, and 41 are the most important non-product chart candidates for token cost, throughput per megawatt, interactivity, and revenue-per-gigawatt rhetoric. They are visually valuable but unsafe as final art until exact axes, values, source context, and independent corroboration are available. Page 44 is the best mechanism diagram because it links prefill, decode, KV cache, Dynamo, Vera Rubin, and Groq 3 LPX without relying only on product glamor.

Drop logic matters. Pages 62, 64, 65, and 66 are visually tempting because they contain open-model and benchmark material, but they belong outside the GTC visual program unless independent benchmark normalization changes their role. They risk pulling the chapter into leaderboard theater, robotics/physical-AI drift, or unsupported model-superiority claims.

Deliverables:

- `data/gtc_2026_page_scan_i0184.tsv` records every page from the 76-page local PDF and its mining decision.
- `data/gtc_2026_chart_mining_i0184.tsv` ranks 18 chart/diagram candidates and records captions, blockers, treatments, and links to the later I-0192 choose/drop board.

Gate result: promote as a source+visual acquisition pass. It fixes the provenance gap behind the GTC chart program: the book can now say the deck was scanned page by page, not merely sampled around already-rendered product slides. It does not create new screenshots, clear rights, extract exact chart values, or authorize NVIDIA economics/performance claims as independent facts.
