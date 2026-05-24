# Next Token Master Outline

Status: promoted structure pass I-0001 on 2026-05-24.

Working title: **Next Token: The Race to Build the Machines That Learned Language, Code, and Computing**

## Book Architecture

This outline fixes the first durable shape for a 24-chapter, 100,000-120,000 word nonfiction book about large language models through the factual cutoff of May 24, 2026. It is not a prose draft. It is the spine against which future chapter drafts, source packs, visual packages, and claim audits should be judged.

Design rule: every chapter must braid three strands when possible: the technical mechanism, the institutional race, and the reader-visible consequence. Hardware, datacenters, power, chips, code, benchmarks, and companies appear only where they explain LLM progress.

Target average chapter length: 4,200-4,800 words, with shorter interstitially paced chapters allowed if the full book remains above 100,000 and below 120,000 words.

## Part I: The Machine Learns Sequence

### 1. The Shock

Opening beat: the public collision with ChatGPT, treated as a product shock rather than a magic trick. The chapter should establish the central question: how did next-token prediction become a general-purpose interface to language, code, work, and computing?

Core machinery: tokens, pretraining, prompting, chat interfaces, and why fluency is not the same as truth.

Source spine: OpenAI ChatGPT launch materials, GPT-3 and GPT-4 papers, contemporary reporting, early user and developer evidence.

Visual candidates: ChatGPT launch timeline; token-to-answer schematic; first-week adoption/source chronology.

### 2. Before the Transformer

Opening beat: language modeling before the modern LLM age: n-grams, statistical NLP, neural nets, embeddings, sequence-to-sequence, and the stubborn problem of long-range context.

Core machinery: distributed representations, word embeddings, recurrent networks, LSTMs/GRUs, encoder-decoder translation, attention as a pressure building inside older systems.

Source spine: Bengio-style neural language modeling, word2vec, seq2seq, early attention papers.

Visual candidates: lineage diagram from n-grams to embeddings to seq2seq; recurrent bottleneck schematic.

### 3. Attention Catches Fire

Opening beat: the Transformer as a practical engineering rupture: less recurrence, more parallelism, and a model that could scale with accelerators.

Core machinery: self-attention, positional encodings, multi-head attention, feed-forward blocks, parallel training, why the architecture matched GPU-era compute.

Source spine: "Attention Is All You Need" and Google Research commentary.

Visual candidates: annotated Transformer block; attention heatmap; recurrence vs parallel attention comparison.

### 4. The Scaling Bet

Opening beat: labs begin treating language models as a scaling problem with measurable laws rather than only clever architecture.

Core machinery: loss curves, parameters, data, compute, Chinchilla-style compute/data balance, emergent capabilities debates, benchmark fragility.

Source spine: OpenAI scaling laws, DeepMind Chinchilla, GPT-2/GPT-3, benchmark papers.

Visual candidates: scaling-law curve; compute/data/parameter triangle; benchmark saturation timeline.

## Part II: The Product Becomes the Platform

### 5. GPT-1 to GPT-3: The Door Opens

Opening beat: OpenAI's sequence from representation learning to few-shot prompting, culminating in GPT-3 as a platform primitive.

Core machinery: unsupervised pretraining, transfer, in-context learning, API distribution, model cards, risks of capability without interpretability.

Source spine: GPT-1, GPT-2, GPT-3 papers; OpenAI API materials.

Visual candidates: GPT family growth table; prompt-as-program diagram; API ecosystem map.

### 6. Alignment Enters the Product

Opening beat: the shift from raw completion engines to assistants that follow instructions.

Core machinery: instruction tuning, supervised fine-tuning, RLHF, preference models, constitutional AI, red teaming, refusal behavior, evaluation gaps.

Source spine: InstructGPT/RLHF papers, Anthropic constitutional AI, OpenAI system card/reporting.

Visual candidates: RLHF pipeline; preference model flow; failure-mode matrix.

### 7. ChatGPT: The Interface Event

Opening beat: November 2022 as the moment the public learned to talk to an LLM and the industry learned it had been underestimating interface risk.

Core machinery: chat formatting, safety layers, latency, memory illusions, plugins/tools as early agent scaffolding.

Source spine: OpenAI ChatGPT post, GPT-3.5/GPT-4 sources, product telemetry where supportable, reporting with primary-source checks.

Visual candidates: product timeline; interaction transcript anatomy; launch-to-platform roadmap.

### 8. Microsoft, OpenAI, and the Cloud Bargain

Opening beat: the alliance between frontier model research and hyperscale compute.

Core machinery: Azure supercomputing, inference serving, capital needs, enterprise distribution, Copilot as a route from chat to work.

Source spine: Microsoft/OpenAI partnership posts, Azure AI infrastructure materials, earnings and public filings where relevant.

Visual candidates: cloud/model/platform flywheel; partnership timeline; inference cost stack.

### 9. Google and DeepMind Wake the Sleeping Giant

Opening beat: the company that incubated the Transformer finds itself racing to convert research depth into product urgency.

Core machinery: PaLM, Bard, Gemini, multimodality where it matters to LLMs, TPU/GPU strategy, search integration, model cards.

Source spine: PaLM/Gemini technical reports, DeepMind model cards, Google product posts.

Visual candidates: Google model lineage; TPU vs GPU infrastructure map; Gemini product surface timeline.

## Part III: The Open Race

### 10. Meta, Llama, and the Open-Weight Shock

Opening beat: LLaMA turns frontier-adjacent capability into a downloadable object and changes the politics of access.

Core machinery: open weights vs open source, fine-tuning, quantization, local inference, Llama 2/3/4 families where cutoff-supported.

Source spine: Meta LLaMA/Llama 2/3/4 announcements, model cards, license texts, ecosystem repos.

Visual candidates: open-weight diffusion map; model-size/capability table; license comparison.

### 11. The Chinese Frontier

Opening beat: China's model ecosystem becomes too technically important to treat as a footnote.

Core machinery: Qwen, DeepSeek, GLM/Z.ai, Kimi/Moonshot, Baidu, Tencent, Xiaomi MiMo, StepFun, MiniMax; mixture-of-experts, reasoning models, long context, open releases, inference efficiency.

Source spine: Qwen technical reports and repos, DeepSeek V3/R1/V4-era sources where cutoff-supported, GLM/Kimi/MiniMax/Baidu/Tencent/Xiaomi/StepFun primary materials.

Visual candidates: China model-family tree; open/proprietary matrix; reasoning-model timeline.

### 12. Europe, xAI, and the Rest of the Frontier

Opening beat: Mistral, xAI, and other non-Big-Tech labs test whether speed, focus, distribution, or openness can substitute for hyperscaler depth.

Core machinery: efficient training, mixture-of-experts, small frontier-grade models, data access, product distribution, benchmark positioning.

Source spine: Mistral papers/posts, xAI model cards/posts, relevant primary model releases and benchmark snapshots.

Visual candidates: lab strategy quadrant; model release calendar; benchmark caveat chart.

### 13. Benchmarks, Arenas, and the Mirage of Rank

Opening beat: the public scoreboard becomes part instrument, part theater, part market signal.

Core machinery: static benchmarks, contamination, Chatbot Arena, SWE-bench, LiveCodeBench, MMLU/HLE-style suites, price/performance leaderboards, eval harnesses.

Source spine: LMSYS/Chatbot Arena, SWE-bench, benchmark papers, provider pricing snapshots.

Visual candidates: leaderboard anatomy; contamination risk diagram; price-quality frontier.

## Part IV: The Factory Beneath the Model

### 14. NVIDIA and CUDA: The Moat Under the Moat

Opening beat: the LLM boom as the moment CUDA, GPUs, libraries, and developer habits compound into strategic infrastructure.

Core machinery: GPU parallelism, CUDA software ecosystem, H100/B200/GB200, NVLink, networking, memory bandwidth, inference vs training.

Source spine: NVIDIA architecture materials, GTC talks, technical docs, public filings.

Visual candidates: GPU memory hierarchy; CUDA stack; training cluster topology.

### 15. GTC 2026: The AI Factory Sells Itself

Opening beat: the GTC 2026 keynote as a staged argument that the next industrial unit is the AI factory.

Core machinery: Vera Rubin announcements and roadmaps as cutoff-known claims, GB200/B200 context, racks, networking, power, software stack, announced vs shipped distinction.

Source spine: local `GTC-2026-Keynote.pdf` with page-level provenance, NVIDIA GTC 2026 newsroom/investor materials.

Visual candidates: keynote claim map; roadmap vs shipping status table; AI factory block diagram.

### 16. Datacenters, Power, and the Physical Internet

Opening beat: LLMs turn abstract computation into land, transformers, turbines, cooling, fiber, and utility queues.

Core machinery: training clusters, inference regions, power density, grid interconnection, gas turbines, cooling, capex, supply constraints.

Source spine: hyperscaler filings, datacenter power reporting, grid/operator sources, NVIDIA/AMD/cloud infrastructure materials.

Visual candidates: AI datacenter anatomy; power-to-token flow; capex stack.

### 17. Data, Tokens, and the Library Problem

Opening beat: the raw material of LLMs is not "the internet" but a contested, filtered, duplicated, multilingual, licensed, synthetic, and increasingly exhausted token supply.

Core machinery: tokenization, web corpora, code data, books, synthetic data, deduplication, data mixtures, contamination, copyright only as needed for the LLM story.

Source spine: dataset papers, tokenizer docs, Common Crawl/materials, model reports, selective legal/regulatory context.

Visual candidates: token pipeline; tokenizer demo; data-mixture map.

## Part V: Machines That Use Machines

### 18. Tools, Retrieval, and the Agent Turn

Opening beat: the LLM stops being only a text generator and becomes a controller for tools, memory, search, code execution, and external systems.

Core machinery: function calling, RAG, tool-use policies, MCP-style connectors, computer use, planner/executor loops, prompt injection.

Source spine: OpenAI/Anthropic/Google tool-use docs and papers, RAG papers, security white papers.

Visual candidates: agent loop schematic; RAG pipeline; prompt-injection threat model.

### 19. Code as the Second Native Language

Opening beat: code is where LLM capability becomes measurable, economically legible, and personally unsettling to builders.

Core machinery: Codex, Copilot, AlphaCode, Code Llama, SWE-bench, repo editing, test loops, terminal use, bug fixing, code review.

Source spine: OpenAI Codex/Copilot materials, AlphaCode papers, SWE-bench, provider model cards.

Visual candidates: coding-agent harness; benchmark-to-workflow map; repository edit loop.

### 20. Claude Code and the Industrialization of Pair Programming

Opening beat: coding agents move from autocomplete to long-horizon repository work, with Claude Code as a central case study.

Core machinery: terminal agents, tool permissions, context management, memory, planning, test execution, MCP, failure modes, human-in-the-loop control.

Source spine: Anthropic Claude Code and Claude 4 materials, developer docs, benchmark reports, careful firsthand workflow notes.

Visual candidates: agent permission model; repo-task lifecycle; failure taxonomy.

### 21. Reasoning, Test-Time Compute, and the New Scaling Axis

Opening beat: inference itself becomes a place to spend compute, not merely a delivery cost after training.

Core machinery: chain-of-thought secrecy, reasoning models, search, verification, self-consistency, tool-augmented solving, latency and cost tradeoffs.

Source spine: reasoning-model papers/posts, DeepSeek R1, OpenAI/Google/Anthropic reasoning materials where available by cutoff.

Visual candidates: train-time vs test-time compute chart; verifier loop; latency/cost frontier.

## Part VI: The Race Becomes a World

### 22. The Economics of Intelligence on Tap

Opening beat: model labs discover that intelligence can be sold by token, seat, cloud commitment, API margin, ad surface, and enterprise bundle.

Core machinery: API pricing, inference optimization, caching, distillation, enterprise contracts, consumer subscriptions, open-weight pressure.

Source spine: provider pricing snapshots, public filings, cloud announcements, model cards.

Visual candidates: token price curve; gross-margin pressure stack; open vs closed economics matrix.

### 23. Failure Modes, Truth, and Trust

Opening beat: the same systems that feel general also hallucinate, flatter, leak, overfit, and fail in ways that are hard to see from demos.

Core machinery: hallucination, calibration, sycophancy, jailbreaks, prompt injection, eval blind spots, provenance, auditability, safety only where it affects LLM reliability and deployment.

Source spine: model system cards, eval papers, security reports, major incident records with primary confirmation.

Visual candidates: failure-mode map; trust stack; claim-support workflow.

### 24. Next Token

Opening beat: return to the act of prediction, now revealed as an industrial, scientific, and cultural system.

Core machinery: what changed by May 24, 2026; what remained unsolved; why the next-token objective became a new computing interface without becoming magic.

Source spine: cross-book synthesis, latest cutoff-bounded model/source snapshots, no post-cutoff history.

Visual candidates: full timeline; final system map; open questions grid.

## Coverage Audit

- Exactly 24 main chapters: yes.
- Mandatory ChatGPT chapter: chapter 7, with chapter 1 as public shock prologue.
- Mandatory Claude Code/coding agents chapter: chapters 19 and 20.
- Mandatory GTC 2026/NVIDIA chapter: chapters 14 and 15.
- Mandatory Google/DeepMind, Anthropic, Meta, Chinese labs, Mistral/xAI, hardware, datacenters, datasets, evaluations, inference economics, and reasoning/test-time compute: represented.
- Explicit exclusions: no robotics chapter; no image/video diffusion history except contrast/context; no regulation/copyright chapter except as needed for data and deployment truth.

## First Source Clusters To Build

1. Transformer and scaling primary papers.
2. OpenAI GPT-1 through ChatGPT/GPT-4 primary materials.
3. Anthropic Claude/Claude Code primary materials.
4. Meta Llama open-weight release materials.
5. Qwen, DeepSeek, GLM/Z.ai, Kimi/Moonshot, Mistral, MiniMax, xAI, Baidu, Tencent, Xiaomi MiMo, StepFun, and NVIDIA Nemotron primary materials.
6. NVIDIA GTC 2026 local PDF and official newsroom/investor sources.
7. Benchmark and provider-pricing snapshots with access dates.

## Promotion Rationale

The previous champion contained no book structure beyond directory instructions. This outline improves the hard chapter-count invariant from absent to exactly 24 planned chapters, maps every mandatory topic in `GOAL.md`, and creates a concrete surface for source packs, chapter drafts, visual planning, and claim audits. It is promoted as the current structural champion, not as a finished manuscript.
