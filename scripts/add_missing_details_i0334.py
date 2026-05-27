"""I-0334: Add all remaining missing details - Micron, Colossus, GPU timeline, SSD, memory constraints.
Then reassemble and attempt PDF render."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

# Add the chronological infrastructure constraint timeline to Ch16
ch16 = BASE / "16-speed-to-power.md"
text16 = ch16.read_text(encoding="utf-8")

constraint_timeline = """## The Constraint Cascade: From GPUs to Gas to Memory to Oil

The physical story of the AI boom was not a single bottleneck. It was a cascade of constraints, each one becoming visible as the previous one was partially addressed, each one revealing a deeper dependency in the supply chain.

The first constraint was GPU availability. Through 2023 and early 2024, the limiting factor was simply getting enough H100 GPUs. NVIDIA's manufacturing pipeline, constrained by TSMC's CoWoS advanced packaging capacity and SK Hynix's HBM production, could not keep pace with demand from every cloud provider, frontier lab, and nation-state simultaneously. H100 rental prices on the spot market reflected the scarcity, and allocation became a strategic function at the CEO level. Companies that had reserved capacity early had a multi-month head start. Companies that had not were forced to buy from resellers at 36-to-52-week lead times. [S-0198]

The second constraint was power. As GPU clusters grew from thousands to tens of thousands to hundreds of thousands of accelerators, the electricity required to run them exceeded what local grids could deliver. Datacenter operators turned to on-site gas turbines as a stopgap, ordering industrial generators that could provide tens of megawatts of power without waiting for grid interconnection. The gas generator became the ugly but necessary workaround: a box that burned fossil fuel to feed GPUs that trained models that might someday reduce energy consumption elsewhere. The contradiction was visible but the alternative was slower training runs, and nobody in the race was choosing slower. [S-0193]

The third constraint was memory. By October 2025, the HBM supply chain had become the rate-limiting step for GPU production. SK Hynix, Samsung, and Micron were all racing to expand HBM3E capacity, but the advanced packaging required for high-bandwidth memory could not be scaled overnight. On December 3, 2025, Micron Technology announced it would exit the consumer memory business entirely, discontinuing its Crucial brand of SSDs and RAM by February 2026 to focus exclusively on HBM and datacenter memory products. [S-0199] The decision was a market signal disguised as a corporate restructuring: the most profitable use of advanced memory fabrication capacity was no longer consumer electronics. It was AI accelerators. Consumer SSD and RAM prices rose accordingly, and the consumer electronics industry absorbed the cost of being a lower-priority customer in a market dominated by AI demand.

The fourth constraint was geopolitical. When the Strait of Hormuz closed in March 2026, the AI supply chain discovered that its physical dependencies extended into the world's most contested waterways. The diesel that powered backup generators, the bunker fuel that moved components across oceans, and the oil that underpinned energy prices everywhere all transited through a 21-mile-wide strait that had become an active war zone. Shipping insurance premiums for Gulf transit increased by orders of magnitude. Major carriers suspended service. The abstraction of cloud compute had met the reality of maritime geography. [S-0193]

By the cutoff, the constraint cascade had begun to affect storage prices as well. SSD costs, which had been declining for years, began to rise as NAND flash production capacity was diverted to meet the storage demands of AI training clusters. The same fabs that produced consumer SSDs were being retooled for enterprise drives destined for datacenter racks. A consumer buying a laptop in 2026 was competing for silicon against a Stargate campus demanding petabytes of high-speed storage.

The lesson of the constraint cascade was not that any single bottleneck would stop the AI boom. It was that the boom was built on a physical substrate whose fragility became more apparent the larger the boom grew. Each constraint was addressed at enormous cost, but each solution revealed the next constraint, and the chain extended further than any single-industry analysis could capture."""

paragraphs = text16.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, constraint_timeline.strip())
ch16.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", constraint_timeline))
print(f"Constraint cascade: +{added} words")

# Add Colossus section to Chapter 12 (Europe/xAI)
ch12 = BASE / "12-europe-xai-rest-frontier.md"
text12 = ch12.read_text(encoding="utf-8")

colossus = """## Colossus: Speed As Infrastructure

The physical expression of xAI's speed strategy was the Colossus supercomputer in Memphis, Tennessee. Construction began in 2024, and the first cluster became operational in July 2024 after what the company described as a 122-day buildout. Colossus 1 housed approximately 200,000 GPUs with an estimated hardware cost of $7 billion, drawing roughly 300 megawatts of power. Satellite imagery analysis published by SemiAnalysis and other industry observers tracked the construction progress in near-real-time, documenting a build pace that had no precedent in datacenter construction. [S-0149]

Colossus 2, which entered planning as Colossus 1 was still ramping, was designed to be the world's first gigawatt-scale AI datacenter. SemiAnalysis reported that the expansion included on-site gas turbines for primary power, a Mississippi River water supply for cooling, and additional acreage acquired for future phases. By early 2026, xAI had signed an agreement giving Anthropic access to Colossus capacity, an arrangement that would have been unthinkable between competing frontier labs just two years earlier. The deal reflected the strange economics of the AI infrastructure race: even competitors needed each other's compute.

Colossus mattered for this book not because it was the largest datacenter, but because it made the speed of infrastructure assembly a visible competitive variable. Satellite photos showed the site transforming from empty land to operational supercomputer in months, not years. The images were a different kind of evidence than benchmark tables or press releases. They showed concrete, steel, generators, cooling equipment, and transmission lines appearing at a pace that made traditional datacenter construction look like a different industry. Whether the speed was sustainable, whether the power infrastructure was reliable, and whether the cooling design would prove adequate over time were questions that only operational experience could answer. What the images proved was that xAI was willing to compress the construction timeline to its physical limit, and that changed the expectations for every other lab's infrastructure planning."""

paragraphs = text12.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, colossus.strip())
ch12.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", colossus))
print(f"Colossus section: +{added} words")

# Add GPU rental price data to Ch14
ch14 = BASE / "14-nvidia-cuda-moat.md"
text14 = ch14.read_text(encoding="utf-8")

gpu_prices = """## The Rental Market and the Price of Scarcity

The GPU allocation problem created a secondary market that was as revealing as any benchmark table. H100 one-year rental contract pricing, tracked by SemiAnalysis and other industry analysts, dropped to a low of $1.70 per GPU-hour in October 2025 as supply finally caught up with the initial wave of demand. But by March 2026, prices had surged nearly 40 percent to $2.35 per GPU-hour as a new wave of inference demand, combined with Blackwell production ramps that were slower than expected, tightened supply again. On-demand GPU rental capacity was effectively sold out across all GPU types, and organizations that had not locked in long-term contracts found themselves with few options at any price. [S-0198]

The rental market dynamics revealed something structural about the AI economy. GPU prices were not falling along a smooth learning curve. They were oscillating with supply shocks, architectural transitions, and demand waves. A lab that had budgeted for declining compute costs could find itself facing rising costs at the worst possible moment. A startup that had built its business model on abundant cheap inference could discover that abundance was not guaranteed. The GPU had become a commodity with the price volatility of a commodity, and the entire AI industry was learning to manage that volatility in real time.

The root causes of the scarcity were not primarily about GPU die production. TSMC's advanced packaging capacity, particularly CoWoS (Chip-on-Wafer-on-Substrate), was the binding constraint. HBM production from SK Hynix, Samsung, and Micron was the second constraint. The substrates and interposers that connected GPU dies to memory were the third. Each layer of the manufacturing stack had its own lead time, its own capital requirements, and its own exposure to geopolitical risk. The AI boom had outrun the semiconductor supply chain's ability to expand, and closing that gap would take years of factory construction, equipment installation, and process qualification."""

paragraphs = text14.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, gpu_prices.strip())
ch14.write_text("\n\n".join(paragraphs))
added = len(re.findall(r"[a-zA-Z]+", gpu_prices))
print(f"GPU rental market: +{added} words")

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
