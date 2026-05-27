"""I-0332: Comprehensive timeline fix and missing event coverage.
Adds: Hormuz crisis, Stargate, Anthropic/OpenAI financials, Qwen 3.5/3.6, fixed Blackwell timeline, Micron, GPU supply chain."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

# Fix 1: Correct Blackwell timeline in Ch14 (announced March 2024, shipped late 2024/early 2025)
ch14 = BASE / "14-nvidia-cuda-moat.md"
text = ch14.read_text(encoding="utf-8")
text = text.replace(
    "announced at GTC 2024 and entering production through 2024 and 2025",
    "announced at GTC in March 2024, with B200 GPUs beginning volume shipments in the fourth quarter of 2024 and GB200 NVL72 rack-scale systems ramping through the first half of 2025"
)
text = text.replace(
    "introduced a second-generation Transformer Engine",
    "introduced the second-generation Transformer Engine"
)
ch14.write_text(text, encoding="utf-8")
print("Fixed Blackwell timeline in Ch14")

# Fix 2: Add comprehensive infrastructure crisis section to Ch16
ch16 = BASE / "16-speed-to-power.md"
text16 = ch16.read_text(encoding="utf-8")

hormuz_section = """## The Hormuz Shock and the Fragile Supply Chain

On March 2, 2026, the Iranian military moved to close the Strait of Hormuz, the narrow waterway through which roughly 20 percent of the world's oil passes daily. Within days, the United States responded with a naval blockade of Iranian ports, and a zone of active military confrontation enveloped the Gulf. By the ninth week of the crisis in early May 2026, dual blockades were in effect, oil prices had spiked dramatically, and global shipping routes were being redrawn in real time. The Port of Salalah in Oman, a critical transshipment gateway, was struck by a drone on March 3 and closed indefinitely. [S-0193]

For the AI infrastructure story, the Hormuz crisis was not a sidebar. It was the moment when the physical fragility of the AI supply chain became undeniable. The same datacenters that were being planned around GPU availability and power interconnection suddenly had a new variable: the price and availability of the diesel fuel that powered backup generators, the bunker fuel that moved components across oceans, and the geopolitical risk premium that attached to every long-term infrastructure contract in a world where a single strait could paralyze global energy markets.

By late April 2026, shipping insurance premiums for Gulf transit had increased by orders of magnitude. Major carriers had suspended service through the region. Oil that normally transited Hormuz was being rerouted around the Cape of Good Hope, adding weeks of transit time and millions in additional cost per voyage. For datacenter operators, the immediate concern was diesel for backup generators. For hardware manufacturers, it was the shipping cost and timeline for every component that moved through Middle Eastern waters. For the AI industry as a whole, it was a reminder that the clean abstraction of cloud compute was built on a physical substrate that extended into the world's most contested geography.

The Hormuz crisis also exposed a deeper structural vulnerability. The AI boom had concentrated infrastructure spending in regions with access to cheap power, but it had not diversified the supply chains that fed those regions. A single geopolitical event could simultaneously stress the energy supply, the component supply, the shipping capacity, and the insurance infrastructure that kept the whole system running. The industry had planned for GPU shortages and power constraints. It had not planned for a war in the Strait of Hormuz."""

paragraphs = text16.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, hormuz_section.strip())
ch16.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", hormuz_section))
print(f"Hormuz section: +{added} words to Ch16")

# Fix 3: Add Stargate project section to Ch16
stargate = """## Stargate: Infrastructure at the Half-Trillion Scale

The Stargate project, formally announced on January 21, 2025, at a White House press conference with President Trump, Sam Altman, Larry Ellison, and Masayoshi Son, represented the most ambitious AI infrastructure commitment in history. Stargate LLC, a joint venture between OpenAI, SoftBank, Oracle, and the Abu Dhabi investment firm MGX, committed to investing up to $500 billion in U.S. AI infrastructure by 2029. [S-0194]

The first phase focused on Abilene, Texas, where ten half-million-square-foot data center buildings were under construction, with the site itself leased from Crusoe, the energy infrastructure company. The campus would eventually draw an estimated 1.4 gigawatts of power. By October 2025, Stargate had expanded to Port Washington, Wisconsin, with Vantage Data Centers committing $15 billion to a campus powered by zero-emission energy resources. Additional sites were announced or rumored in multiple states, each representing a bet that AI compute demand would continue growing at rates that justified half-trillion-dollar infrastructure commitments. [S-0194]

By April 2026, the Stargate model was showing signs of strain. OpenAI abandoned plans to rent compute capacity directly from a planned 230-megawatt data center in Narvik, Norway, built by UK AI cloud company Nscale. Instead, OpenAI said it was in discussions with Microsoft to rent the capacity. The shift was significant: OpenAI had positioned the Norway project under the Stargate umbrella as an initial offtaker, meaning the company would directly contract for compute infrastructure. Pulling back suggested that even the best-capitalized AI company in the world was reconsidering how much infrastructure risk it wanted to carry directly. [S-0194]

For this book's narrative, Stargate is the extreme expression of the AI factory concept that NVIDIA had been selling since GTC 2024. If the AI factory was the metaphor, Stargate was the literalization: half a trillion dollars committed to buildings, power lines, chips, cooling systems, and transmission infrastructure, all in service of the same next-token prediction that had begun as a research problem in a 2017 paper."""

paragraphs = Path(ch16).read_text(encoding="utf-8").strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, stargate.strip())
ch16.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", stargate))
print(f"Stargate section: +{added} words to Ch16")

# Fix 4: Add Anthropic financials to Ch11 (Anthropic chapter)
ch11a = BASE / "12-anthropic-and-claude-spine-section.md"
text11 = ch11a.read_text(encoding="utf-8")

anth_fin = """## The Revenue Explosion

Anthropic's growth trajectory was, by any historical standard, extraordinary. The company crossed $1 billion in annualized revenue in December 2024. By July 2025, that figure had reached $4 billion. By December 2025, it was $9 billion. By February 2026, just before the company closed a $30 billion Series G funding round at a $380 billion post-money valuation, annualized revenue had reached $14 billion. By May 2026, CNBC reported that Anthropic was on track for $10.9 billion in quarterly revenue -- implying an annualized run rate north of $40 billion. The growth rate was roughly 10x per year, sustained over eighteen months. [S-0195]

This was not just a startup success story. It was evidence that the commercial market for frontier AI had developed faster than almost anyone had predicted. Anthropic had passed OpenAI in revenue while reportedly spending 4x less to train its models. The company's focus on safety, reliability, and enterprise deployment had translated into a business that was growing faster than the company that had created the category. Whether this growth was sustainable, and whether it reflected genuine end-user value or a land-grab phase of enterprise AI adoption, remained open questions at the cutoff. What was not in question was the magnitude: a company that had been generating tens of millions in revenue three years earlier was now generating billions per quarter.

On February 12, 2026, Anthropic closed its $30 billion Series G at a $380 billion valuation, making it one of the most valuable private companies in the world. The round came less than two weeks before OpenAI's $110 billion raise at a valuation between $730 billion and $852 billion, depending on the source. Between them, the two leading American AI labs had raised $140 billion in a single month -- more than the entire venture capital industry had deployed in any full year before 2020. [S-0195]"""

paragraphs = text11.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, anth_fin.strip())
ch11a.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", anth_fin))
print(f"Anthropic financials: +{added} words to Ch11")

# Fix 5: Add OpenAI $110B raise to Ch4 (GPT chapter)
ch04 = BASE / "05-gpt-1-to-gpt-3-door-opens.md"
text04 = ch04.read_text(encoding="utf-8")

openai_fin = """## The $110 Billion Month

On February 27, 2026, OpenAI closed a $110 billion funding round -- the largest venture deal in history. Amazon invested $50 billion, NVIDIA invested $30 billion, and SoftBank invested $30 billion. The round valued OpenAI at $730 billion according to Bloomberg, or as high as $852 billion by other estimates, making it one of the most valuable private companies ever created. The company also disclosed that it expected to lose $14 billion in 2026, a figure that made the investment round both more impressive and more unsettling. [S-0196]

The Amazon investment was particularly significant because it came with a multiyear strategic partnership. Amazon, which competed with OpenAI through its own AI models and through Anthropic, was now OpenAI's largest financial backer. The deal illustrated the strange geometry of the AI industry: competitors were also investors, customers were also suppliers, and no single relationship captured the full picture of who depended on whom.

The OpenAI raise, combined with Anthropic's $30 billion Series G two weeks earlier, meant that $140 billion had been committed to the two leading American AI labs in February 2026 alone. For context, the entire global venture capital industry deployed roughly $350 billion in 2024. Two companies had raised nearly half that amount in one month. The numbers were so large they broke the normal vocabulary of startup finance. This was not venture capital in the traditional sense. It was industrial capital, allocated at industrial scale, to companies that had become infrastructure projects as much as software startups."""

paragraphs = text04.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, openai_fin.strip())
ch04.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", openai_fin))
print(f"OpenAI financials: +{added} words to Ch4")

# Fix 6: Add Qwen 3.5/3.6 to Ch10
ch10 = BASE / "11-chinese-frontier-open-models.md"
text10 = ch10.read_text(encoding="utf-8")

qwen_section = """## Qwen 3.5, 3.6, and the Alibaba Acceleration

While DeepSeek captured headlines with cost-efficient training, Alibaba's Qwen team was building one of the fastest release cadences in the industry. Qwen 3.5, released in early 2026, included the 35B-A3B variant that used a mixture-of-experts architecture to deliver strong performance at a fraction of the parameter count. Qwen 3.6 followed rapidly -- the 35B-A3B model appeared on Hugging Face on April 16, 2026, and the Qwen 3.6 Plus Preview had launched on OpenRouter on March 30, 2026, with a 1-million-token context window and what community testers described as roughly three times the speed of Claude Opus 4.6. Qwen 3.7-Max, described by Alibaba as designed for the agent era, was already on the horizon. [S-0197]

In between these releases, Alibaba shipped Qwen 3 Coder Next, an 80-billion-parameter model optimized specifically for code generation and agentic workflows. The model was benchmarked extensively on NVIDIA DGX Spark hardware, with developers reporting strong performance on coding benchmarks at a fraction of the cost of proprietary alternatives. The Coder Next release demonstrated that Alibaba was not just chasing general-purpose benchmarks. It was targeting specific workloads -- code, agents, translation -- where open-weight models could compete directly with closed APIs. [S-0197]

The speed of Alibaba's releases was itself a competitive signal. Western labs typically shipped new model families on six-to-twelve-month cycles. Alibaba was shipping notable new variants every four to eight weeks. The pace suggested a development infrastructure that had been optimized for rapid iteration, and it meant that any snapshot of the Chinese frontier was outdated within a month. For a book with a May 24, 2026 cutoff, the Qwen release schedule was a vivid reminder that the frontier was not waiting for anyone's publication timeline."""

paragraphs = text10.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, qwen_section.strip())
ch10.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", qwen_section))
print(f"Qwen section: +{added} words to Ch10")

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
print(f"\nGrand total: {grand} words")
