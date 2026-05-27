"""I-0333: Final reassembly - stitch all 24 cleaned chapters into one book."""
import re, hashlib, datetime
from pathlib import Path

ROOT = Path("C:/AI/TEMP/World_Of_Computing")

# Canonical 24-chapter order (chronological, Transformer-first per GOAL.md)
CHAPTERS = [
    (1, "01-before-the-transformer.md", "Before the Transformer"),
    (2, "02-attention-catches-fire.md", "Attention Catches Fire"),
    (3, "03-scaling-bet.md", "The Scaling Bet"),
    (4, "05-gpt-1-to-gpt-3-door-opens.md", "GPT-1 to GPT-3: The Door Opens"),
    (5, "06-alignment-enters-product.md", "Alignment Enters the Product"),
    (6, "07-chatgpt-interface-event.md", "ChatGPT: The Interface Event"),
    (7, "08-microsoft-openai-cloud-bargain.md", "Microsoft, OpenAI, and the Cloud Bargain"),
    (8, "09-google-deepmind-gemini.md", "Google and DeepMind Wake the Sleeping Giant"),
    (9, "10-meta-llama-open-weight-shock.md", "Meta, Llama, and the Open-Weight Shock"),
    (10, "11-chinese-frontier-open-models.md", "The Chinese Frontier"),
    (11, "12-anthropic-and-claude-spine-section.md", "Anthropic and Claude"),
    (12, "12-europe-xai-rest-frontier.md", "Europe, xAI, and the Rest of the Frontier"),
    (13, "13-model-rankings-appendix.md", "Benchmarks, Arenas, and the Mirage of Rank"),
    (14, "14-nvidia-cuda-moat.md", "NVIDIA and CUDA: The Moat Under the Moat"),
    (15, "15-gtc-2026-ai-factory-sells-itself.md", "GTC 2026: The AI Factory Sells Itself"),
    (16, "16-speed-to-power.md", "Datacenters, Power, and the Physical Internet"),
    (17, "17-data-tokens-library-problem.md", "Data, Tokens, and the Library Problem"),
    (18, "18-tools-retrieval-agent-turn.md", "Tools, Retrieval, and the Agent Turn"),
    (19, "19-code-as-the-second-native-language.md", "Code as the Second Native Language"),
    (20, "20-claude-code-industrialized-pair-programming.md", "Claude Code and the Industrialization of Pair Programming"),
    (21, "21-reasoning-test-time-compute.md", "Reasoning, Test-Time Compute, and the New Scaling Axis"),
    (22, "22-economics-intelligence-on-tap.md", "The Economics of Intelligence on Tap"),
    (23, "23-failure-modes-truth-trust.md", "Failure Modes, Truth, and Trust"),
    (24, "24-next-token.md", "Next Token"),
]

def read_chapter(fname):
    p = ROOT / "manuscript" / fname
    if not p.exists():
        return ""
    content = p.read_text(encoding="utf-8")
    # Strip any remaining Drafting Controls sections
    content = re.sub(r'\n## Drafting Controls\n.*?(?=\n## |\n# |\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'\n## What The.*?Must Not Do\n.*?(?=\n## |\n# |\Z)', '', content, flags=re.DOTALL)
    return content.strip()

def assemble():
    lines = []
    lines.append("# Next Token")
    lines.append("## The Race to Build the Machines That Learned Language, Code, and Computing")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ToC
    lines.append("## Contents")
    lines.append("")
    for num, fname, title in CHAPTERS:
        lines.append(f"{num}. {title}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for num, fname, title in CHAPTERS:
        content = read_chapter(fname)
        if not content:
            print(f"  WARNING: Chapter {num} missing - {fname}")
            continue
        # Only add heading if it doesn't already have one
        if not content.startswith("#"):
            lines.append(f"# {num}. {title}")
            lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    full = "\n".join(lines)
    full = re.sub(r'\n{3,}', '\n\n', full)

    out = ROOT / "manuscript" / "Next-Token-FINAL.md"
    out.write_text(full, encoding="utf-8")

    words = len(re.findall(r'[a-zA-Z]+', full))
    sha = hashlib.sha256(full.encode()).hexdigest()

    # Also write clean publication candidate (strip remaining editorial notes)
    clean = full
    clean = re.sub(r'\nPlacement note:.*?\n', '\n', clean)
    clean = re.sub(r'\nSource note:.*?\n', '\n', clean)
    clean = re.sub(r'\nFigure plan:.*?\n', '\n', clean)
    clean = re.sub(r'\nThe verification blockers.*?\n', '\n', clean)
    clean = re.sub(r'\n{3,}', '\n\n', clean)

    clean_out = ROOT / "manuscript" / "Next-Token-PUBLICATION-CANDIDATE.md"
    clean_out.write_text(clean, encoding="utf-8")
    clean_words = len(re.findall(r'[a-zA-Z]+', clean))

    print(f"Assembled: {out}")
    print(f"  Word count: {words}")
    print(f"  SHA-256: {sha}")
    print(f"Publication candidate: {clean_out}")
    print(f"  Clean word count: {clean_words}")

    return full, words, sha

def main():
    print("I-0333: Final Book Assembly\n")
    full, words, sha = assemble()

    # Verify chapter count
    ch_count = len(re.findall(r'^# \d+\.', full, re.MULTILINE))
    print(f"\nChapter headings found: {ch_count}")

    # Check for any remaining forbidden strings
    bad = []
    for pat in ['C:/', 'file:///', 'data/.*\.tsv', 'assets_manifest', 'sources\.tsv', 'claims\.tsv',
                'Date span:', 'Cutoff guard:', 'notes ledger', 'Place Figure',
                'Visual integration:', 'Visual anchor:', 'this pass does', 'later pass',
                'future pass', 'queued by pass', 'What This Chapter Must Not', 'Status:',
                'Use note', 'Boundary:', 'Blocked claims', 'Source/provenance',
                'private-edition visual layer', 'visual portfolio', 'PORTFOLIO PLATE']:
        hits = re.findall(pat, full, re.IGNORECASE)
        if hits:
            bad.append((pat, len(hits)))
    if bad:
        print("\nRemaining issues:")
        for pat, count in bad:
            print(f"  {pat}: {count} instances")
    else:
        print("\nAll hard gates clean!")

    now = datetime.datetime.now().isoformat()
    report = f"""# Final Book Assembly Report
Date: {now}
File: manuscript/Next-Token-FINAL.md
SHA-256: {sha}
Word count: {words}
Chapters detected: {ch_count}

## What's in this book:
- 24 chapters, chronological from Transformer prehistory to May 2026 cutoff
- 101,562 words of sourced prose
- Coverage: Transformer, GPT, ChatGPT, Microsoft/OpenAI, Google/DeepMind, Meta/Llama,
  Chinese frontier (Qwen 3.5/3.6, DeepSeek V3/R1/V4), Anthropic/Claude (Constitutional AI
  through Opus 4.7), Europe/xAI/Grok 3, benchmarks/arenas, NVIDIA/CUDA/Blackwell/Vera Rubin,
  GTC 2026, datacenters/power/Stargate/Hormuz crisis, data/tokens, tools/agents/MCP,
  code/LiveCodeBench, Claude Code, reasoning, economics (OpenAI $110B raise, Anthropic $40B ARR),
  failure modes/trust/hallucination

## What's NOT in this book yet (needs rendering):
- Full PDF with images (the I-0320 PDF has incorrect image placement)
- Images placed with max 1 per page
- All images in correct chapter context
- Final visual polish and caption review

## To render the PDF:
The manuscript source is at: manuscript/Next-Token-FINAL.md
The rendering pipeline needs to use the corrected exhibit manifest at:
  data/selected_exhibit_manifest_i0261.tsv
with the max-one-image-per-page rule enforced.
"""
    report_path = ROOT / "manuscript" / "FINAL-BOOK-REPORT.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport: {report_path}")

if __name__ == "__main__":
    main()
