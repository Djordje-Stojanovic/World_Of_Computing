"""
I-0322: Purge ALL process/scaffolding language from reader-facing chapter files.

Handles 54 patterns across 452 instances found in I-0321 audit:
- "the chapter should", "the book should", "the reader should"
- "Date span:", "Cutoff guard:", category labels in chapter openers
- "notes ledger", "Place Figure", "visual integration:", "visual anchor:"
- "this pass", "later pass", "future pass", "queued by pass"
- "should not", "should stay", "should feel", "should use", "should resist", etc.
- "live in", "lives in" (for data/file references)
- "the chapter must", "this chapter must", "What This Chapter Must Not Claim"
- "the chapter does not", "the chapter cannot"

Strategy: Rewrite or remove each instance, preserving factual content
while eliminating editorial/scaffolding voice.
"""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing")

# All reader-facing chapter files (the canonical source chapters)
CHAPTER_FILES = [
    "manuscript/01-the-shock.md",
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

# Also fix the assembled full draft
ASSEMBLED_FILES = [
    "manuscript/Next-Token-full-draft.md",
    "manuscript/Next-Token-chronological-spine-i0315.md",
    "manuscript/Next-Token-contextual-visuals-i0318.md",
    "manuscript/Next-Token-one-visual-page-i0319.md",
    "manuscript/Next-Token-page-density-i0317.md",
    "manuscript/Next-Token-quantitative-i0320.md",
    "manuscript/Next-Token-timeline-date-rails-i0316.md",
]

ALL_FILES = CHAPTER_FILES + ASSEMBLED_FILES

def clean_text(text, filename):
    """Apply all cleanup transformations. Returns (new_text, change_count)."""
    changes = 0
    original = text
    
    # ---- BLOCK 1: Remove Date span / Cutoff guard / category labels from chapter openers ----
    # Pattern: "Date span: ..." line followed by "CATEGORY" and "Cutoff guard: ..."
    # Remove the entire metadata block from chapter openers
    text, c = re.subn(
        r'\nDate span:.*?\n',
        '\n',
        text
    )
    changes += c
    
    text, c = re.subn(
        r'\nCutoff guard:.*?\n',
        '\n',
        text
    )
    changes += c
    
    # Remove standalone category labels at chapter openers
    for label in ['ARCHITECTURE', 'PREHISTORY', 'MEASUREMENT', 'PRETRAINING',
                  'ASSISTANT BEHAVIOR', 'PUBLIC INTERFACE', 'PRODUCTIZATION',
                  'CLOUD AND CAPITAL', 'INCUMBENT RESPONSE', 'OPEN WEIGHTS',
                  'FRONTIER PLURALISM', 'CHINA AND OPEN MODELS', 'EVALUATION',
                  'HARDWARE STACK', 'INFRASTRUCTURE STAGE', 'PHYSICAL CONSTRAINT',
                  'DATA SUPPLY', 'TOOL USE', 'CODE MODELS', 'REPOSITORY WORK',
                  'REASONING', 'ECONOMICS', 'TRUST', 'CUTOFF SYNTHESIS']:
        text, c = re.subn(
            rf'\n{label}\n',
            '\n',
            text
        )
        changes += c
    
    # ---- BLOCK 2: Remove notes ledger references ----
    text, c = re.subn(r',?\s*notes ledger,?\s*', ' ', text)
    changes += c
    text, c = re.subn(r'notes ledger', '', text)
    changes += c
    
    # ---- BLOCK 3: Remove visual integration/anchor notes ----
    text, c = re.subn(r'Visual integration:.*?(?=\n\n|\n[#A-Z]|\Z)', '', text, flags=re.DOTALL)
    changes += c
    text, c = re.subn(r'Visual anchor:.*?(?=\n\n|\n[#A-Z]|\Z)', '', text, flags=re.DOTALL)
    changes += c
    
    # ---- BLOCK 4: Remove Place Figure instructions ----
    text, c = re.subn(r'Place Figure[\s\d\.x,;]*.*?(?=\n\n|\n[#A-Z]|\Z)', '', text, flags=re.DOTALL)
    changes += c
    
    # ---- BLOCK 5: Remove "the chapter should" / "the book should" patterns ----
    # Rewrite to remove the scaffolding voice
    
    # "The chapter should be careful here too." -> remove
    text, c = re.subn(
        r'\n?The chapter should be careful here too\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "The prose should not claim that..." -> rewrite
    text, c = re.subn(
        r'The prose should not claim that ',
        '',
        text
    )
    changes += c
    
    # "the chapter should avoid" -> remove the instruction, keep what follows if factual
    text, c = re.subn(
        r'\n?[Tt]he chapter should (avoid|not|resist|keep|treat|preserve|use|show|carry|make|leave|let|end|sit|help|explain|lean|phrase|speak|distinguish|be careful|begin|stay|feel) ',
        ' ',
        text
    )
    changes += c
    
    # "the book should avoid/not/resist/keep..." -> remove instruction
    text, c = re.subn(
        r'\n?[Tt]he book should (avoid|not|resist|keep|treat|preserve|use|show|carry|make|leave|let|end|be careful|call it|distinguish) ',
        ' ',
        text
    )
    changes += c
    
    # "the reader should feel/understand/see/leave/enter/ask..." -> rewrite as direct statement
    text, c = re.subn(
        r'\n?[Tt]he reader should (feel|understand|see|leave|enter|ask|finish|carry) ',
        ' ',
        text
    )
    changes += c
    
    # "should not" in editorial context - more surgical
    # Keep factual "should not" (e.g., technical constraints) but remove editorial ones
    # "the chapter should not X" -> remove
    text, c = re.subn(
        r'\n?[Tt]he chapter should not [^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "the chapter should therefore..." -> remove
    text, c = re.subn(
        r'\n?[Tt]he chapter should therefore[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # ---- BLOCK 6: Remove "this pass" / "later pass" / "future pass" ----
    text, c = re.subn(
        r'\n?[Tt]his pass does not[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    text, c = re.subn(
        r'\n?[Tt]his pass is[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    text, c = re.subn(
        r'\n?in a later pass,?[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    text, c = re.subn(
        r'\n?[Ff]uture pass[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    text, c = re.subn(
        r',? queued by pass[^,.]*',
        '',
        text
    )
    changes += c
    
    # ---- BLOCK 7: Remove "What This Chapter Must Not Claim" sections ----
    text, c = re.subn(
        r'\n?#+\s*What This Chapter (Must Not|Cannot|Does Not|Still Refuses|Still|Will Not)[^\n]*\n',
        '\n',
        text
    )
    changes += c
    
    # ---- BLOCK 8: Remove "live in" / "lives in" for data references ----
    text, c = re.subn(
        r'\n?[Tt]he (companion |row )?data lives? in[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # ---- BLOCK 9: Remove standalone editorial instruction sentences ----
    # "That is why the chapter should..." -> remove the whole sentence
    text, c = re.subn(
        r'\n?That is why the chapter should[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "This is why the chapter should..." -> remove
    text, c = re.subn(
        r'\n?This is why the chapter should[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "This is also where the book should..." -> remove
    text, c = re.subn(
        r'\n?This is also where the book should[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "That is the notes opening for this chapter, provided..." -> remove
    text, c = re.subn(
        r'\n?That is the notes opening for this chapter[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "Every architecture chapter needs a humility section." -> rewrite
    text, c = re.subn(
        r'\n?Every architecture chapter needs a humility section\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "The chapter should therefore use three lanes Measured lane" -> remove
    text, c = re.subn(
        r'\n?[Tt]he chapter should therefore use three lanes[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "the chapter has to live in that tension:" -> rewrite as "This creates a tension:"
    text, c = re.subn(
        r'\n?[Tt]he chapter has to live in that tension[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "The book should keep its LLM focus, so this chapter does not need" -> remove 
    text, c = re.subn(
        r'\n?The book should keep its LLM focus[^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # "This chapter should therefore avoid myth." / "This chapter should resist" -> remove
    text, c = re.subn(
        r'\n?[Tt]his chapter should (therefore avoid|therefore be|also keep|keep|speak|stay|preserve|belong|end|lean|treat|resist|phrase|use|show|carry|make|leave|let|help|explain) [^.]*\.\s*',
        ' ',
        text
    )
    changes += c
    
    # ---- BLOCK 10: Source note / Continuity note removal ----
    text, c = re.subn(
        r'\n?Source note:.*?\n',
        '\n',
        text
    )
    changes += c
    text, c = re.subn(
        r'\n?Continuity note:.*?\n',
        '\n',
        text
    )
    changes += c
    
    # ---- Clean up: remove double spaces, triple newlines ----
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # ---- Clean up: remove lines that are just "should" remnants ----
    text = re.sub(r'\n+should [a-z].*\n', '\n', text)
    text = re.sub(r'\n+[Tt]he chapter [a-z].*\n', '\n', text)
    
    if text != original:
        # Final clean
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text, changes

def main():
    print("I-0322: Purging ALL process/scaffolding language from reader-facing prose\n")
    
    total_changes = 0
    files_changed = 0
    
    for rel_path in ALL_FILES:
        path = BASE / rel_path
        if not path.exists():
            continue
        
        content = path.read_text(encoding="utf-8")
        cleaned, changes = clean_text(content, rel_path)
        
        if changes > 0:
            path.write_text(cleaned, encoding="utf-8")
            print(f"  {rel_path}: {changes} changes")
            total_changes += changes
            files_changed += 1
    
    print(f"\nFiles changed: {files_changed}")
    print(f"Total changes: {total_changes}")
    
    # Verify: scan for remaining process patterns
    print("\n--- Residual pattern scan ---")
    residual_patterns = [
        r'Date span:',
        r'Cutoff guard:',
        r'notes ledger',
        r'Place Figure',
        r'Visual integration:',
        r'Visual anchor:',
        r'the chapter should',
        r'the book should',
        r'this pass does not',
        r'later pass',
        r'future pass',
        r'queued by pass',
        r'What This Chapter Must Not',
        r'This Chapter Still Refuses',
        r'lives? in data/',
        r'Source note:',
        r'Continuity note:',
        r'Every architecture chapter needs',
    ]
    
    remaining = 0
    for rel_path in CHAPTER_FILES:
        path = BASE / rel_path
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for pat in residual_patterns:
            matches = re.findall(pat, content, re.IGNORECASE)
            if matches:
                for m in matches[:3]:
                    print(f"  RESIDUAL in {rel_path}: '{m}'")
                remaining += len(matches)
    
    print(f"\nTotal residual hits in chapter files: {remaining}")
    
    if remaining > 0:
        print("⚠ Some patterns still remain. Manual cleanup may be needed.")
    else:
        print("✅ All targeted patterns removed from chapter files.")

if __name__ == "__main__":
    main()
