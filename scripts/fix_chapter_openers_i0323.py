"""
I-0323: Fix chapter openers - remove Status lines, fix cross-chapter refs, ensure clean openings.
"""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing")

CHAPTER_FILES = [
    "manuscript/01-before-the-transformer.md",
    "manuscript/02-attention-catches-fire.md",
    "manuscript/03-scaling-bet.md",
    "manuscript/05-gpt-1-to-gpt-3-door-opens.md",
    "manuscript/06-alignment-enters-product.md",
    "manuscript/07-chatgpt-interface-event.md",
    "manuscript/08-microsoft-openai-cloud-bargain.md",
    "manuscript/09-google-deepmind-gemini.md",
    "manuscript/10-meta-llama-open-weight-shock.md",
    "manuscript/11-chinese-frontier-open-models.md",
    "manuscript/12-europe-xai-rest-frontier.md",
    "manuscript/13-model-rankings-appendix.md",
    "manuscript/14-nvidia-cuda-moat.md",
    "manuscript/15-gtc-2026-ai-factory-sells-itself.md",
    "manuscript/16-speed-to-power.md",
    "manuscript/17-data-tokens-library-problem.md",
    "manuscript/18-tools-retrieval-agent-turn.md",
    "manuscript/19-code-as-the-second-native-language.md",
    "manuscript/20-claude-code-industrialized-pair-programming.md",
    "manuscript/21-reasoning-test-time-compute.md",
    "manuscript/22-economics-intelligence-on-tap.md",
    "manuscript/23-failure-modes-truth-trust.md",
    "manuscript/24-next-token.md",
]

# Also the assembled manuscripts
ASSEMBLED = [
    "manuscript/Next-Token-full-draft.md",
    "manuscript/Next-Token-chronological-spine-i0315.md",
    "manuscript/Next-Token-contextual-visuals-i0318.md",
    "manuscript/Next-Token-one-visual-page-i0319.md",
    "manuscript/Next-Token-page-density-i0317.md",
    "manuscript/Next-Token-quantitative-i0320.md",
    "manuscript/Next-Token-timeline-date-rails-i0316.md",
]

def clean_file(path):
    content = path.read_text(encoding="utf-8")
    original = content
    changes = 0
    
    # Remove "Status:" lines - these are internal audit metadata
    content, c = re.subn(r'\nStatus:.*?\n', '\n', content)
    changes += c
    
    # Remove lines that are just "Status:..." with nothing after
    content, c = re.subn(r'^Status:.*$(\n)?', '', content, flags=re.MULTILINE)
    changes += c
    
    # Fix "Chapter X did Y" cross-references that reference old numbering
    # These appear in chapter openers like "Chapter 3 made the architecture feel stackable"
    # Replace with natural references
    content = content.replace(
        "Chapter 2 ended with a bottleneck: language had become numerical", 
        "The previous chapter ended with a bottleneck: language had become numerical"
    )
    content = content.replace(
        "Chapter 3 made the architecture feel stackable and parallel enough",
        "The Transformer chapter made the architecture feel stackable and parallel enough"
    )
    content = content.replace(
        "Chapter 4 made scale feel measurable. Chapter 5 shows a lab turning",
        "The scaling-laws chapter made scale feel measurable. This chapter shows a lab turning"
    )
    content = content.replace(
        "Chapter 5 showed models becoming programmable through prompts, APIs,",
        "The GPT chapter showed models becoming programmable through prompts, APIs,"
    )
    
    # Clean up double newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'  +', ' ', content)
    
    if content != original:
        path.write_text(content, encoding="utf-8")
        return changes
    return 0

def main():
    print("I-0323: Fixing chapter openers\n")
    total = 0
    for rel in CHAPTER_FILES + ASSEMBLED:
        p = BASE / rel
        if p.exists():
            c = clean_file(p)
            if c > 0:
                print(f"  {rel}: {c} changes")
                total += c
    
    print(f"\nTotal changes: {total}")
    
    # Verify no Status lines remain in chapter files
    print("\n--- Verification ---")
    remaining = 0
    for rel in CHAPTER_FILES:
        p = BASE / rel
        if p.exists():
            content = p.read_text(encoding="utf-8")
            hits = re.findall(r'^Status:', content, re.MULTILINE)
            if hits:
                print(f"  RESIDUAL in {rel}: {len(hits)} Status lines")
                remaining += len(hits)
    
    if remaining == 0:
        print("  CLEAN - all Status lines removed from chapter files.")
    else:
        print(f"  {remaining} Status lines remain.")

if __name__ == "__main__":
    main()
