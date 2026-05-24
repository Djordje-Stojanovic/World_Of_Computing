# Next Token Source Map

Status: promoted sourcing pass I-0002 on 2026-05-24.

Purpose: create the first book-wide source topology for **Next Token**. This is a sourcing scaffold, not a claim-complete bibliography. Each chapter draft must still verify exact wording, dates, metrics, and quoted material against the cited source before prose promotion.

Cutoff rule: sources discovered after May 24, 2026 may be used only if the underlying event, artifact, release, paper, talk, filing, or snapshot existed by the cutoff. Future passes must avoid silently importing post-cutoff changes from live pages.

## Source Priorities

1. Primary papers, model cards, system cards, technical reports, official docs, official repos, product posts, filings, and conference materials.
2. Benchmark pages and pricing pages with access dates, ideally snapshotted before use in charts.
3. Major secondary reporting only as leads, chronology cross-checks, or narrative triangulation.
4. Firsthand workflow notes only when clearly labeled as firsthand observation, not hidden insider access.

## Chapter Source Topology

### Chapters 1, 5, 7, and 8: OpenAI, ChatGPT, GPT, and Microsoft

Core primary spine:

- GPT-1, GPT-2, GPT-3, GPT-4 technical materials.
- OpenAI ChatGPT launch post and official product/system-card materials.
- InstructGPT/RLHF paper for the assistant transition.
- Microsoft/OpenAI and Azure AI infrastructure posts for the compute-platform bargain.

Next gaps:

- Capture first-party source snapshots for ChatGPT, GPT-4, GPT-4o, o-series reasoning, API/pricing, and Microsoft Copilot/Azure materials.
- Use public filings and earnings transcripts only for capital, cloud, and distribution claims.
- Do not use adoption numbers unless a primary or clearly attributable source supports the exact figure.

### Chapters 2, 3, and 4: Origins, Transformer, Scaling

Core primary spine:

- Neural language model, word2vec/embeddings, seq2seq, attention, Transformer.
- OpenAI scaling laws and DeepMind Chinchilla for compute/data scaling tension.

Next gaps:

- Add canonical early NLP sources before chapter drafting: Bengio neural probabilistic language model, Mikolov word2vec, Sutskever seq2seq, Bahdanau attention.
- Add a short source note distinguishing "scaling law" evidence from debated "emergence" interpretations.

### Chapters 6, 18, 20, and 23: Alignment, Tool Use, Agents, Safety

Core primary spine:

- InstructGPT, constitutional AI, Claude product/model releases, Claude Code docs, tool-use docs, RAG, and prompt-injection/security papers.

Next gaps:

- Snapshot Claude Code docs and Claude model cards before quoting capabilities.
- Treat agent claims as workflow claims: verify tool permissions, context management, test execution, and failure modes from docs or reproducible firsthand notes.
- Keep safety material tied to LLM reliability, deployment, and trust; do not let it become a regulation chapter.

### Chapters 9, 10, 11, and 12: Frontier Labs and Open Weights

Core primary spine:

- Google/DeepMind PaLM and Gemini reports/model cards.
- Meta LLaMA/Llama 2/Llama 3/Llama 4 materials and Code Llama.
- Qwen, DeepSeek, GLM/Z.ai, Kimi/Moonshot, Mistral, xAI, MiniMax, Baidu, Tencent, Xiaomi MiMo, StepFun, and NVIDIA Nemotron sources where cutoff-supported.

Next gaps:

- Create separate lab source sheets for Chinese labs because live pages are likely to change quickly.
- Verify Qwen 3.5 and Qwen 3.6 as cutoff-supported before writing them as happened releases. Until then, mark them as "support pending" in chapter planning.
- Treat DeepSeek V4-era claims as support pending unless a cutoff-bounded primary source is captured.
- Do not collapse open weights, open source, open data, and permissive licensing into one category.

### Chapter 13: Benchmarks and Rankings

Core primary spine:

- Chatbot Arena, SWE-bench, LiveCodeBench, MMLU/HLE-style benchmark papers, provider pricing pages, and model cards.

Next gaps:

- Build source snapshots for leaderboard state, model version, price, context window, and access date.
- Any ranking chart must show caveats: contamination, hidden prompts, sampling, judge model, release cadence, and price/performance.

### Chapters 14, 15, and 16: Compute, NVIDIA, Datacenters, Power

Core primary spine:

- NVIDIA H100/Blackwell/Vera Rubin materials, local `GTC-2026-Keynote.pdf`, CUDA docs, and hyperscaler infrastructure posts/filings.

Next gaps:

- Extract page-level provenance from the local GTC 2026 PDF before any NVIDIA chapter prose or visual.
- Distinguish shipped hardware, announced products, and roadmap claims in every caption and claim ledger row.
- Add grid/operator and datacenter power sources before writing chapter 16.

### Chapters 17, 21, 22, and 24: Data, Reasoning, Economics, Synthesis

Core primary spine:

- Dataset papers, tokenizers, RAG, reasoning-model reports, provider pricing, cloud filings, and model cards.

Next gaps:

- Snapshot tokenizer docs and data-source papers before using token diagrams.
- Build a price/source matrix separately from the prose draft because live pricing changes.
- Use chapter 24 only for cutoff-bounded synthesis; no post-cutoff hindsight.

## Immediate Ledger Gains

Pass I-0002 adds primary-source coverage for:

- early Transformer/scaling/open GPT materials,
- instruction tuning/RLHF and constitutional AI,
- Google/DeepMind, Meta/Llama, Anthropic/Claude,
- Qwen and DeepSeek,
- core benchmarks and coding-agent harnesses,
- NVIDIA/compute and Microsoft/Azure infrastructure,
- datasets/tokenization/RAG.

## Red Flags For Future Passes

- Live pages can mutate. Snapshot before charts and before model-ranking claims.
- Product posts are not neutral accounts; use them for dates, declared capabilities, and official positioning, then triangulate.
- "Frontier" is a moving label. For the cutoff book, frontier status must mean the state known by May 24, 2026.
- Secondary reporting should never carry a technical claim when a paper, model card, repo, or doc exists.
