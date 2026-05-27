"""
I-0330: Structural chapter-order fix.
GOAL.md requires: must NOT open with ChatGPT. Must begin at Transformer/attention.
Action: Merge "The Shock" into Ch6 (ChatGPT chapter), renumber Ch1-12, keep Ch13-24 same.
"""
import re
from pathlib import Path

ROOT = Path("C:/AI/TEMP/World_Of_Computing")

# Step 1: Merge "The Shock" prologue into Chapter 7 → becomes Chapter 6
shock = ROOT / "manuscript/01-the-shock.md"
chatgpt_ch = ROOT / "manuscript/07-chatgpt-interface-event.md"

shock_text = shock.read_text(encoding="utf-8")
# Extract content after the heading, remove back-referencing paragraphs
shock_text = re.sub(r'^# 1\. The Shock\n\n', '', shock_text)
# Remove: "The book begins here not because..." through "...met an interface."
shock_text = re.sub(
    r'The book begins here not because ChatGPT.*?It met an interface\.\s*\n\n',
    '',
    shock_text,
    flags=re.DOTALL
)
# Remove the final "Drafting Controls" section that talks about "This is a Chapter 1 draft"
shock_text = re.sub(r'\n## Drafting Controls\n.*', '', shock_text, flags=re.DOTALL)
shock_text = shock_text.strip()

chatgpt_text = chatgpt_ch.read_text(encoding="utf-8")
# Insert shock prologue after "# 7. ChatGPT: The Interface Event" heading line
# The heading will become "# 6." in the renumbering step
chatgpt_text = re.sub(
    r'(# 7\. ChatGPT: The Interface Event\n\n)',
    r'\1## Prologue: The Box That Was Too Easy\n\n' + shock_text + '\n\n',
    chatgpt_text
)
chatgpt_ch.write_text(chatgpt_text, encoding="utf-8")
print("Merged Shock prologue into ChatGPT chapter")

# Step 2: Renumber chapter headings - only chapters 1-12 shift
RENUMBER = [
    ("01-before-the-transformer.md", r'^# 2\.', '# 1.'),
    ("02-attention-catches-fire.md", r'^# 3\.', '# 2.'),
    ("03-scaling-bet.md", r'^# 4\.', '# 3.'),
    ("05-gpt-1-to-gpt-3-door-opens.md", r'^# 5\.', '# 4.'),
    ("06-alignment-enters-product.md", r'^# 6\.', '# 5.'),
    ("07-chatgpt-interface-event.md", r'^# 7\.', '# 6.'),
    ("08-microsoft-openai-cloud-bargain.md", r'^# 8\.', '# 7.'),
    ("09-google-deepmind-gemini.md", r'^# 9\.', '# 8.'),
    ("10-meta-llama-open-weight-shock.md", r'^# 10\.', '# 9.'),
    ("11-chinese-frontier-open-models.md", r'^# 11\.', '# 10.'),
]

for fname, old_pat, new_h in RENUMBER:
    p = ROOT / "manuscript" / fname
    if p.exists():
        text = p.read_text(encoding="utf-8")
        text = re.sub(old_pat, new_h, text, count=1, flags=re.MULTILINE)
        p.write_text(text, encoding="utf-8")
        print(f"  {fname}: {old_pat} -> {new_h}")

# Step 3: Add chapter numbers to Anthropic and Europe/xAI chapters (was unnumbered)
anthropic = ROOT / "manuscript/12-anthropic-and-claude-spine-section.md"
anth_text = anthropic.read_text(encoding="utf-8")
anth_text = re.sub(
    r'^# Anthropic and Claude: The Assistant as a Safety Argument',
    '# 11. Anthropic and Claude: The Assistant as a Safety Argument',
    anth_text
)
anthropic.write_text(anth_text)
print("  12-anthropic-and-claude: added '# 11.' heading")

europe = ROOT / "manuscript/12-europe-xai-rest-frontier.md"
eur_text = europe.read_text(encoding="utf-8")
eur_text = re.sub(
    r'^# Europe, xAI, and the Rest of the Frontier',
    '# 12. Europe, xAI, and the Rest of the Frontier',
    eur_text
)
europe.write_text(eur_text)
print("  12-europe-xai-rest-frontier: added '# 12.' heading")

# Also fix missing numbers on later chapters that have non-standard formats
fixes = [
    ("13-model-rankings-appendix.md", r'^# Chapter 13:', '# 13.'),
    ("16-speed-to-power.md", r'^# Chapter 16', '# 16.'),
]
for fname, old_p, new_h in fixes:
    p = ROOT / "manuscript" / fname
    if p.exists():
        text = p.read_text(encoding="utf-8")
        text = re.sub(old_p, new_h, text, count=1, flags=re.MULTILINE)
        p.write_text(text, encoding="utf-8")
        print(f"  {fname}: standardized heading format")

print("\n=== NEW CHAPTER ORDER (chronological, per GOAL.md) ===")
for i, label in enumerate([
    "Ch 1: Before the Transformer — The Machine Learns Sequence",
    "Ch 2: Attention Catches Fire — The Architecture That Wanted to Scale",
    "Ch 3: The Scaling Bet — When Loss Became a Map",
    "Ch 4: GPT-1 to GPT-3 — The Door Opens",
    "Ch 5: Alignment Enters the Product",
    "Ch 6: ChatGPT: The Interface Event (with Shock prologue)",
    "Ch 7: Microsoft, OpenAI, and the Cloud Bargain",
    "Ch 8: Google and DeepMind Wake the Sleeping Giant",
    "Ch 9: Meta, Llama, and the Open-Weight Shock",
    "Ch 10: The Chinese Frontier",
    "Ch 11: Anthropic and Claude: The Assistant as a Safety Argument",
    "Ch 12: Europe, xAI, and the Rest of the Frontier",
    "Ch 13: Benchmarks, Arenas, and the Mirage of Rank",
    "Ch 14: NVIDIA and CUDA: The Moat Under the Moat",
    "Ch 15: GTC 2026: The AI Factory Sells Itself",
    "Ch 16: Datacenters, Power, and the Physical Internet",
    "Ch 17: Data, Tokens, and the Library Problem",
    "Ch 18: Tools, Retrieval, and the Agent Turn",
    "Ch 19: Code as the Second Native Language",
    "Ch 20: Claude Code and the Industrialization of Pair Programming",
    "Ch 21: Reasoning, Test-Time Compute, and the New Scaling Axis",
    "Ch 22: The Economics of Intelligence on Tap",
    "Ch 23: Failure Modes, Truth, and Trust",
    "Ch 24: Next Token",
]):
    print(f"  {label}")

print("\nDone. Book now opens with Transformer prehistory, not ChatGPT.")
print("ChatGPT appears chronologically at Chapter 6.")
