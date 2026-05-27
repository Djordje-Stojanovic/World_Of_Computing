"""
I-0327/I-0328: Final proper assembly with correct chapter mapping,
include Anthropic supplemental in Chapter 12, reach 100k word target.
"""
import re, hashlib, datetime
from pathlib import Path

ROOT = Path("C:/AI/TEMP/World_Of_Computing")
OUTDIR = ROOT / "rendered" / "final_private_i0328"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Canonical order from I-0238 canonical_chapter_order_map.tsv
CHAPTER_MAP = [
    (1, "manuscript/01-the-shock.md", "The Shock"),
    (2, "manuscript/01-before-the-transformer.md", "Before the Transformer"),
    (3, "manuscript/02-attention-catches-fire.md", "Attention Catches Fire"),
    (4, "manuscript/03-scaling-bet.md", "The Scaling Bet"),
    (5, "manuscript/05-gpt-1-to-gpt-3-door-opens.md", "GPT-1 to GPT-3: The Door Opens"),
    (6, "manuscript/06-alignment-enters-product.md", "Alignment Enters the Product"),
    (7, "manuscript/07-chatgpt-interface-event.md", "ChatGPT: The Interface Event"),
    (8, "manuscript/08-microsoft-openai-cloud-bargain.md", "Microsoft, OpenAI, and the Cloud Bargain"),
    (9, "manuscript/09-google-deepmind-gemini.md", "Google and DeepMind Wake the Sleeping Giant"),
    (10, "manuscript/10-meta-llama-open-weight-shock.md", "Meta, Llama, and the Open-Weight Shock"),
    (11, "manuscript/11-chinese-frontier-open-models.md", "The Chinese Frontier"),
]

# Chapter 12: Europe/xAI primary + Anthropic supplemental (from canonical map)
# 12-europe-xai-rest-frontier.md is primary; 12-anthropic-and-claude-spine-section.md is supplemental
CHAPTER_MAP += [
    (12, [("manuscript/12-anthropic-and-claude-spine-section.md", "Anthropic and Claude: The Assistant as a Safety Argument"),
          ("manuscript/12-europe-xai-rest-frontier.md", "Europe, xAI, and the Rest of the Frontier")],
     "Anthropic, Europe, xAI, and the Plural Frontier"),
]

CHAPTER_MAP += [
    (13, "manuscript/13-model-rankings-appendix.md", "Benchmarks, Arenas, and the Mirage of Rank"),
    (14, "manuscript/14-nvidia-cuda-moat.md", "NVIDIA and CUDA: The Moat Under the Moat"),
    (15, "manuscript/15-gtc-2026-ai-factory-sells-itself.md", "GTC 2026: The AI Factory Sells Itself"),
    (16, "manuscript/16-speed-to-power.md", "Datacenters, Power, and the Physical Internet"),
    (17, "manuscript/17-data-tokens-library-problem.md", "Data, Tokens, and the Library Problem"),
    (18, "manuscript/18-tools-retrieval-agent-turn.md", "Tools, Retrieval, and the Agent Turn"),
    (19, "manuscript/19-code-as-the-second-native-language.md", "Code as the Second Native Language"),
    (20, "manuscript/20-claude-code-industrialized-pair-programming.md", "Claude Code and the Industrialization of Pair Programming"),
    (21, "manuscript/21-reasoning-test-time-compute.md", "Reasoning, Test-Time Compute, and the New Scaling Axis"),
    (22, "manuscript/22-economics-intelligence-on-tap.md", "The Economics of Intelligence on Tap"),
    (23, "manuscript/23-failure-modes-truth-trust.md", "Failure Modes, Truth, and Trust"),
    (24, "manuscript/24-next-token.md", "Next Token"),
]

def read_chapter(path):
    """Read chapter content, strip 'Drafting Controls' section if present."""
    p = ROOT / path
    if not p.exists():
        print(f"  WARNING: {path} not found")
        return ""
    content = p.read_text(encoding="utf-8")
    # Remove any Drafting Controls section
    content = re.sub(r'\n## Drafting Controls\n.*?(?=\n## |\n# |\Z)', '', content, flags=re.DOTALL)
    return content.strip()

def assemble_final():
    """Stitch all 24 chapters into one final draft with proper headings."""
    lines = []
    lines.append("# Next Token")
    lines.append("## The Race to Build the Machines That Learned Language, Code, and Computing")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table of Contents
    lines.append("## Contents")
    lines.append("")
    for num, paths, title in CHAPTER_MAP:
        if isinstance(paths, list):
            lines.append(f"{num}. {title}")
        else:
            lines.append(f"{num}. {title}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for entry in CHAPTER_MAP:
        if len(entry) == 3:
            num, fileinfo, title = entry
            if isinstance(fileinfo, list):
                # Multi-section chapter (Chapter 12)
                lines.append(f"# Chapter {num}: {title}")
                lines.append("")
                for subpath, sublabel in fileinfo:
                    subcontent = read_chapter(subpath)
                    if subcontent:
                        # If the content already has its own heading, use it
                        if subcontent.startswith("#"):
                            lines.append(subcontent)
                        else:
                            lines.append(f"## {sublabel}")
                            lines.append("")
                            lines.append(subcontent)
                        lines.append("")
                lines.append("")
            else:
                # Single-file chapter
                content = read_chapter(fileinfo)
                if not content:
                    continue
                # If content doesn't start with #, add chapter heading
                if not content.startswith("#"):
                    lines.append(f"# Chapter {num}: {title}")
                    lines.append("")
                lines.append(content)
                lines.append("")
        lines.append("---")
        lines.append("")

    full_draft = "\n".join(lines)
    # Clean up
    full_draft = re.sub(r'\n{3,}', '\n\n', full_draft)
    full_draft = re.sub(r'  +', ' ', full_draft)

    out_path = ROOT / "manuscript" / "Next-Token-final-i0328.md"
    out_path.write_text(full_draft, encoding="utf-8")

    words = len(re.findall(r'[a-zA-Z]+', full_draft))

    # Also write a clean version that's the "publication candidate"
    # Remove any remaining process language
    clean = full_draft
    for pat in ['Data span:', 'Cutoff guard:', 'Status:', 'Source note:', 'Placement note:',
                'Figure plan:', 'Claim blocker:', 'Blocked claim:']:
        clean = re.sub(rf'\n{re.escape(pat)}.*?\n', '\n', clean)
    clean = re.sub(r'\n{3,}', '\n\n', clean)

    clean_path = ROOT / "manuscript" / "Next-Token-publication-candidate-i0328.md"
    clean_path.write_text(clean, encoding="utf-8")
    clean_words = len(re.findall(r'[a-zA-Z]+', clean))

    print(f"Full draft: {out_path} ({words} words)")
    print(f"Publication candidate: {clean_path} ({clean_words} words)")

    return full_draft, words

def run_qa(full_draft):
    """Hard gate QA."""
    print("\n--- HARD GATE QA ---")
    results = []

    words = len(re.findall(r'[a-zA-Z]+', full_draft))
    wc_ok = 100000 <= words <= 120000
    results.append(("Word count 100k-120k", words, "PASS" if wc_ok else "FAIL"))

    ch_count = len(re.findall(r'^# \d+\.', full_draft, re.MULTILINE))
    ch_ok = ch_count == 24
    results.append(("24 chapters", ch_count, "PASS" if ch_ok else "FAIL"))

    # Forbidden strings
    forbidden = [
        r'C:/', r'file:///', r'Use note', r'Boundary:', r'Blocked claims',
        r'Source/provenance', r'private-edition visual layer', r'source boundaries',
        r'visual portfolio', r'PORTFOLIO PLATE', r'sha256',
        r'generated by an AI', r'AI-generated',
    ]
    fb_hits = 0
    for f in forbidden:
        fb_hits += len(re.findall(f, full_draft, re.IGNORECASE))
    results.append(("Forbidden strings", fb_hits, "PASS" if fb_hits == 0 else "FAIL"))

    # Process language
    process = [
        r'Date span:', r'Cutoff guard:', r'notes ledger',
        r'Place Figure', r'Visual integration:', r'Visual anchor:',
        r'this pass does not', r'later pass', r'future pass', r'queued by pass',
        r'What This Chapter Must Not',
        r'Status:.*promoted.*pass I-',
    ]
    proc_hits = 0
    for p in process:
        proc_hits += len(re.findall(p, full_draft, re.IGNORECASE))
    results.append(("Process language", proc_hits, "PASS" if proc_hits == 0 else "FAIL"))

    # data/ paths
    data_hits = len(re.findall(r'data/\w+\.tsv', full_draft))
    results.append(("data/*.tsv paths", data_hits, "PASS" if data_hits == 0 else "FAIL"))

    # ledger references
    ledger_hits = len(re.findall(r'(assets_manifest|sources|claims)\.tsv', full_draft))
    results.append(("ledger .tsv references", ledger_hits, "PASS" if ledger_hits == 0 else "FAIL"))

    for name, value, status in results:
        print(f"  {name}: {value} -> {status}")

    all_pass = all(s == "PASS" for _, _, s in results)
    print(f"\nOVERALL: {'ALL GATES PASS' if all_pass else 'SOME GATES FAIL'}")

    return results, all_pass

def main():
    print("I-0327/0328: Final proper assembly with corrected chapter map\n")

    full_draft, words = assemble_final()
    results, all_pass = run_qa(full_draft)

    # If word count fails, show what's needed
    if words < 100000:
        needed = 100000 - words
        print(f"\n  WORD COUNT GAP: {needed} more words needed (currently {words})")

    # Write completion report
    sha = hashlib.sha256(full_draft.encode()).hexdigest()
    report = f"""# I-0327/0328: Final Assembly Report

Date: {datetime.datetime.now().isoformat()}
SHA-256: `{sha}`

## Metrics
- Word count: {words}
- Chapters: 24 (including Anthropic supplemental in Chapter 12)

## Hard Gates
"""
    for name, value, status in results:
        report += f"- {name}: {value} → **{status}**\n"

    report += f"""
## Overall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAIL'}

## Chapter 12 Structure
Anthropic/Claude section + Europe/xAI/Rest-of-Frontier section combined into Chapter 12:
"The Plural Frontier." This resolves the long-standing Chapter 12 conflict.
"""
    report_path = ROOT / "manuscript" / "assembly-report-i0328.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport: {report_path}")

if __name__ == "__main__":
    main()
