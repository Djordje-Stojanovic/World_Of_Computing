"""Final push to 100k with H200/memory and Huawei/SMIC content."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

ch14 = BASE / "14-nvidia-cuda-moat.md"
text = ch14.read_text(encoding="utf-8")

expansion = """The H200, announced in late 2023 and shipping in 2024, was an important intermediate step that demonstrated NVIDIA's ability to upgrade memory bandwidth without changing the core architecture. With 141GB of HBM3e at 4.8 terabytes per second -- nearly double the H100's memory bandwidth -- the H200 showed that the inference bottleneck was shifting from compute throughput to memory bandwidth and capacity. A model that could fit entirely in HBM could be served faster, and a model that needed to spill to host memory would be penalized by orders of magnitude. This memory-first thinking carried into the Blackwell design philosophy and explained why each successive GPU generation devoted more silicon and packaging complexity to memory rather than just compute."""

expansion2 = """The technical story behind Huawei's chip progress was as revealing as the geopolitical story. SMIC, China's leading foundry, reportedly achieved 5nm-class transistor density using deep ultraviolet (DUV) lithography with multi-patterning -- a technique that exposes the same wafer layer multiple times with different masks to achieve finer features than a single DUV exposure allows. This was a triumph of process engineering and a demonstration of the limits of export controls. But multi-patterning carries costs: lower yield, higher defect density, longer cycle times, and increased complexity that compounds with each patterning step. A 5nm chip made with multi-patterning was more expensive per functioning die than one made with EUV, and the cost gap widened as transistor densities increased. Huawei's achievement was therefore a qualified one: it proved that Chinese chip fabrication could stay in the game, but it did not prove that the game was now equal."""

paragraphs = text.strip().split("\n\n")
last_idx = len(paragraphs) - 1
while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
    last_idx -= 1
paragraphs.insert(last_idx, expansion.strip())
paragraphs.insert(last_idx + 1, expansion2.strip())
ch14.write_text("\n\n".join(paragraphs), encoding="utf-8")

added1 = len(re.findall(r"[a-zA-Z]+", expansion))
added2 = len(re.findall(r"[a-zA-Z]+", expansion2))
print(f"H200/Huawei content: +{added1 + added2} words")

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
        grand += len(re.findall(r"[a-zA-Z]+", p.read_text(encoding="utf-8")))
print(f"Grand total: {grand} words (need 100000, gap: {100000-grand})")
