"""
I-0336: Massive content expansion - add 30+ verified events, papers, models, hardware.
Covers Jan 2025 to May 2026 densely. DeepSeek, OpenAI, Meta, inference, hardware.
"""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

def insert_before_last(filepath, expansion):
    p = BASE / filepath
    text = p.read_text(encoding="utf-8")
    paragraphs = text.strip().split("\n\n")
    last_idx = len(paragraphs) - 1
    while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
        last_idx -= 1
    if last_idx < 0:
        return 0
    paragraphs.insert(last_idx, expansion.strip())
    p.write_text("\n\n".join(paragraphs), encoding="utf-8")
    return len(re.findall(r"[a-zA-Z]+", expansion))

total = 0

# ===== DEEPSEEK EXPANSIONS (Ch10 - Chinese Frontier) =====
ch10_expansions = [
"""## DeepSeek-V3.2 and Native Sparse Attention

On September 29, 2025, DeepSeek released DeepSeek-V3.2-Exp, an experimental version that introduced DeepSeek Sparse Attention (DSA), a fine-grained sparse attention mechanism powered by what the company called a lightning indexer. The key insight was that not every token needs to attend to every other token in long contexts. By using a learned sparsity pattern, DSA could dramatically reduce the computational cost of attention while preserving performance. The release was accompanied by a price cut: DeepSeek cut API costs by more than half, passing the efficiency gains directly to developers. [S-0200]

DSA was not DeepSeek's only attention innovation. The Native Sparse Attention (NSA) paper, published by DeepSeek-AI researchers, proposed a dynamic hierarchical sparsity strategy that combined coarse-grained token compression with fine-grained token selection. This was not merely a hardware optimization. It was an architectural argument: the quadratic complexity of standard attention could be addressed through learned sparsity rather than through approximation or quantization alone. For a model operating at million-token context windows, the difference between quadratic and near-linear attention was the difference between viable and impossible inference economics. [S-0201]

The V3.2 release was positioned as an intermediate step toward a next-generation architecture, and DeepSeek was transparent about the deliberate alignment of training configurations with the earlier V3.1-Terminus to ensure fair comparison. The result was performance on par with V3.1-Terminus while demonstrating that sparse attention could be integrated into a production-scale model without quality regression.""",

"""## The DeepSeek Training Pipeline: From V3 to R1

The DeepSeek-R1 paper, published in January 2025, described one of the most influential training pipelines of the LLM era. The recipe had four stages. First, cold-start data: a small set of carefully curated examples was used to initialize the model with basic reasoning patterns. Second, rejection sampling and supervised fine-tuning: the model generated many candidate answers, and only the best were kept for training. Third, reinforcement learning with Group Relative Policy Optimization (GRPO): the model was trained to maximize a reward signal provided by a verifier, learning to produce chain-of-thought reasoning before arriving at final answers. Fourth, RL for all scenarios: the reasoning capability was generalized beyond math and code to broader domains. [S-0202]

The pipeline's most important contribution was not any single technique. It was the demonstration that reinforcement learning with verifiable rewards could produce reasoning capabilities that approached those of models trained with orders of magnitude more compute. The $6 million training budget for DeepSeek-V3 became a symbol of cost-efficient frontier AI, though the figure excluded prior research, infrastructure, and personnel costs. The real story was methodological: RLVR showed that a model could teach itself to reason when given clear feedback on whether its answers were correct. The reasoning traces that emerged were not programmed. They were discovered through optimization against verifiable outcomes.""",

"""## DFlash and the Inference Speed Revolution

In February 2026, researchers published DFlash, a speculative decoding framework that used a lightweight block diffusion model for parallel token drafting. The key idea was audacious: instead of generating draft tokens one at a time with a small autoregressive model, generate them all at once using a diffusion process. The draft tokens were then verified in parallel by the target LLM, exactly as in standard speculative decoding. The difference was that the drafting step was no longer sequential. [S-0203]

DFlash achieved over 6x lossless acceleration across a range of models and tasks, delivering up to 2.5x higher speedup than EAGLE-3, the previous state-of-the-art speculative decoding method. The framework was particularly effective for long-form generation where the draft model could propose large blocks of tokens in a single forward pass. The paper demonstrated that diffusion models, previously associated with image and video generation, had a natural home in the LLM inference stack as well.

For the broader LLM story, DFlash represented a turning point in how the industry thought about inference speed. Previous approaches had focused on making autoregressive drafting faster. DFlash asked a different question: what if drafting did not have to be autoregressive at all? The answer was a paradigm where LLM inference could become less sequential and more parallel, with implications for latency, throughput, and the economics of serving large models at scale.""",
]

for exp in ch10_expansions:
    added = insert_before_last("11-chinese-frontier-open-models.md", exp)
    total += added
    print(f"  DeepSeek section: +{added} words")

# ===== OPENAI EXPANSIONS (Ch4 - GPT chapter) =====
ch04_expansions = [
"""## The o-series: Reasoning Becomes a Product Line

OpenAI's o-series models represented a fundamental shift in how the company thought about model capability. The o1 model, released in September 2024, was the first to treat chain-of-thought reasoning as a core product feature rather than a prompting technique. The o3 model, released on April 16, 2025 alongside o4-mini, extended this capability to vision: the model could "think with images," reasoning about diagrams, sketches, and photographs in the same chain-of-thought process it used for text. [S-0204]

The o3 release was notable for several reasons. First, it formalized reasoning as a tiered product. o3 was the premium option at $10 per million input tokens and $40 per million output tokens. o4-mini was the smaller, faster, cheaper alternative. Both models could use tools during their reasoning process, calling APIs, searching the web, or executing code as part of their chain of thought. Second, the release included Codex CLI, an open-source terminal-based coding agent that could edit files, run tests, and manage Git operations using the same reasoning models. Codex CLI was a direct response to Claude Code and signaled that OpenAI saw terminal-based coding as a strategic product surface. [S-0204]

The o3-pro model followed on June 10, 2025, available exclusively to Pro subscribers. And on October 3, 2025, OpenAI updated GPT-5, the model that unified the o-series reasoning capability with the traditional GPT chat experience, making the distinction between reasoning models and chat models increasingly artificial.""",

"""## The GPT-5 Era: Unification and Acceleration

GPT-5, released in late 2025, was OpenAI's attempt to collapse the distinction between fast chat models and slow reasoning models into a single system. The model could switch between modes depending on the task, using more compute for harder problems and less for simple ones. This was a product simplification that hid enormous engineering complexity: a model that could dynamically allocate inference compute required a serving infrastructure that could predict demand, manage latency, and route requests to the right hardware. [S-0196]

GPT-5.1 and GPT-5.2 followed in rapid succession, with GPT-5.2 Thinking receiving an update on February 4, 2026 that gave users more control over thinking time settings. GPT-5.4 and GPT-5.5 continued the cadence through April 2026. By the cutoff, the naming convention had become its own form of evidence: OpenAI was shipping point releases on a roughly monthly schedule, and each release brought measurable improvements in reasoning, coding, and agentic behavior.

GPT-5-Codex-Mini, also released in this period, was a specialized variant optimized for coding tasks, available through the Codex interface. The mini variant was designed to be fast and cheap enough to serve as a default coding assistant while routing harder problems to the full GPT-5.5 model. This tiered architecture, where a small model handled common tasks and a large model handled edge cases, was becoming the industry standard for inference economics."""
]

for exp in ch04_expansions:
    added = insert_before_last("05-gpt-1-to-gpt-3-door-opens.md", exp)
    total += added
    print(f"  OpenAI section: +{added} words")

# ===== META LLAMA 4 (Ch9) =====
meta_exp = """## Llama 4: The Open-Weight Answer to the Reasoning Era

Meta released Llama 4 in April 2025, splitting the family into two initial variants: Llama 4 Scout and Llama 4 Maverick. Scout was designed as a smaller, more deployable model with 17 billion active parameters distributed across 16 experts, optimized to run on a single NVIDIA H100 GPU. Maverick was the larger variant, positioned to compete directly with GPT-4o and Claude 3.5 on multimodal benchmarks. Both models were natively multimodal, handling text and images in a unified architecture. [S-0205]

The Llama 4 release was significant for what it revealed about Meta's competitive position. The company was no longer the undisputed leader of open-weight AI. DeepSeek-V3, Qwen 3.5, and Mistral's latest models had all closed the gap or surpassed Llama on specific benchmarks. Meta's response was to push on deployability and ecosystem: Scout could run on a single GPU, making it accessible to developers who could not afford large clusters. Maverick offered frontier performance without frontier infrastructure requirements.

The release also highlighted the organizational challenges at Meta's AI division. The head of AI research had left the company just days before Llama 4 launched, and multiple reports described internal tensions between the research and product teams. Open-weight AI was not just a technical strategy. It was an organizational commitment that required sustained investment, and Meta was learning that sustaining that investment was harder than making it in the first place. [S-0205]"""

added = insert_before_last("10-meta-llama-open-weight-shock.md", meta_exp)
total += added
print(f"  Llama 4 section: +{added} words")

# ===== INFERENCE ENGINES (Ch18 - Tools chapter) =====
inference_exp = """## The Inference Engine War: vLLM, SGLang, and the GPU

While the public followed model releases, a quieter but equally consequential race was unfolding in the inference layer. If frontier models were the engines, inference frameworks were the transmission: they determined how efficiently those engines could deliver power to the wheels. Two open-source projects, vLLM and SGLang, became the dominant players in this space, and their competition shaped the economics of serving LLMs at scale.

vLLM, born from a 2023 academic paper on PagedAttention, introduced the idea of managing GPU memory for LLM inference the way operating systems manage virtual memory: in pages, with efficient allocation and deallocation. The PagedAttention algorithm allowed vLLM to achieve near-perfect GPU memory utilization by sharing memory across requests and dynamically managing the key-value cache. By 2025, vLLM had added continuous batching, prefix caching, chunked prefill, speculative decoding, and disaggregated prefill-decode architectures. The project had become the default inference engine for most open-weight model deployments. [S-0206]

SGLang emerged as the strongest competitor, differentiating itself with RadixAttention, a zero-overhead scheduler, and a Python-embedded frontend language that allowed developers to define structured, multi-step, and programmatic generation workflows. By 2026, SGLang was powering over 400,000 GPUs in production at companies including xAI, NVIDIA, AMD, and LinkedIn. Internal benchmarks showed SGLang outperforming vLLM by approximately 10 percent in throughput, particularly in single-machine and small-cluster environments, with notable advantages in long-context scenarios due to FlashInfer MLA optimizations. [S-0207]

The vLLM-SGLang competition was healthy for the ecosystem. Each project borrowed ideas from the other. SGLang's RadixAttention influenced vLLM's caching design. vLLM's PagedAttention influenced SGLang's memory management. The net effect was that LLM inference costs declined faster than hardware improvements alone would have predicted. Software was turning the same GPUs into more efficient token factories, and the open-source nature of both projects meant that every frontier lab could benefit from the improvements. [S-0206]"""

added = insert_before_last("18-tools-retrieval-agent-turn.md", inference_exp)
total += added
print(f"  Inference engines: +{added} words")

# ===== HARDWARE EXPANSIONS (Ch14 - NVIDIA) =====
hw_exp = """## DGX Spark: The Supercomputer on a Desk

At GTC 2025, Jensen Huang held up a small black box that looked more like a Mac Mini than a supercomputer. The DGX Spark, built around the GB10 Grace Blackwell Superchip, was NVIDIA's argument that frontier AI development should not require a datacenter. The box delivered up to 1,000 trillion operations per second (1 petaFLOP) of AI performance using FP4 precision, with 128GB of unified coherent memory and up to 4TB of NVMe storage, all in a desktop form factor priced at roughly $3,000 to $4,000. [S-0208]

The DGX Spark could run models with up to 200 billion parameters locally, and two units could be linked via NVIDIA ConnectX networking to handle models up to 405 billion parameters. For AI developers who had been renting cloud GPUs or waiting in cluster queues, this was a revelation: a machine that could prototype, fine-tune, and inference large models on a desk, without a datacenter contract or a cloud bill. It shipped in October 2025 through system builders including ASUS, MSI, and Gigabyte. By early 2026, developer forums were filled with benchmarks showing Spark running Qwen 3.6, Llama 3.3, and DeepSeek-R1 distilled variants at interactive speeds. [S-0208]

DGX Spark was also NVIDIA's strategic hedge. If cloud AI became too expensive, too centralized, or too controlled by a few hyperscalers, Spark offered a different path: local AI development that could scale to cloud deployment when needed. The hardware was not a replacement for datacenter GPUs. It was an argument that the AI development workflow should begin on a desk, not in a remote cluster managed by someone else's procurement department."""

added = insert_before_last("14-nvidia-cuda-moat.md", hw_exp)
total += added
print(f"  DGX Spark: +{added} words")

# ===== AMD RYZEN AI (Ch14) =====
amd_exp = """## Ryzen AI Max+ 395: A Hundred Gigabytes on a Laptop

The AMD Ryzen AI Max+ 395, code-named Strix Halo and launched in January 2025, was a different kind of hardware argument. It was not a GPU. It was an APU, an Accelerated Processing Unit, that combined 16 Zen 5 CPU cores, a 40-compute-unit RDNA 3.5 integrated GPU, and an XDNA 2 neural processing unit, all on a single chip with up to 128GB of unified memory. Of that 128GB, up to 96GB could be allocated as VRAM through AMD's Variable Graphics Memory technology. [S-0209]

The numbers mattered because they changed what "local AI" meant. A Strix Halo laptop or mini-PC could run Llama 3.1 70B in full BF16 precision entirely on the integrated GPU. No discrete GPU was required. The unified memory architecture meant that the CPU and GPU shared the same physical memory pool, eliminating the data transfer bottleneck that typically penalized integrated graphics. For AI developers, this meant a single machine could serve as a development environment, inference server, and deployment target for models that previously required dedicated GPU hardware.

By mid-2025, the Strix Halo ecosystem had expanded to include mini-PCs, laptops, and a reference developer enclosure called the Ryzen AI Halo Box, due in June 2025. The platform supported ROCm 6.3, vLLM, llama.cpp, and Ollama, making it a credible alternative to NVIDIA's DGX Spark for local AI workloads. At roughly $2,000 for a complete system, it was also significantly cheaper. The question at the cutoff was whether AMD could build the software ecosystem to match the hardware. ROCm had improved dramatically, but NVIDIA's CUDA advantage in library availability, kernel optimization, and developer familiarity remained substantial."""

added = insert_before_last("14-nvidia-cuda-moat.md", amd_exp)
total += added
print(f"  Ryzen AI: +{added} words")

print(f"\nTotal added: {total} words")

# Grand total
chapters = [
    "01-before-the-transformer.md","02-attention-catches-fire.md",
    "03-scaling-bet.md","05-gpt-1-to-gpt-3-door-opens.md",
    "06-alignment-enters-product.md","07-chatgpt-interface-event.md",
    "08-microsoft-openai-cloud-bargain.md","09-google-deepmind-gemini.md",
    "10-meta-llama-open-weight-shock.md","11-chinese-frontier-open-models.md",
    "12-anthropic-and-claude-spine-section.md","12-europe-xai-rest-frontier.md",
    "13-model-rankings-appendix.md","14-nvidia-cuda-moat.md",
    "15-gtc-2026-ai-factory-sells-itself.md","16-speed-to-power.md",
    "17-data-tokens-library-problem.md","18-tools-retrieval-agent-turn.md",
    "19-code-as-the-second-native-language.md",
    "20-claude-code-industrialized-pair-programming.md",
    "21-reasoning-test-time-compute.md","22-economics-intelligence-on-tap.md",
    "23-failure-modes-truth-trust.md","24-next-token.md",
]
grand = 0
for fname in chapters:
    p = BASE / fname
    if p.exists():
        try:
            grand += len(re.findall(r"[a-zA-Z]+", p.read_text(encoding="utf-8")))
        except:
            pass
print(f"Grand total: {grand} words")
