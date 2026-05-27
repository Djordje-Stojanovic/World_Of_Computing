"""
I-0321: Fix script for reader-facing residue found during hostile page QA.

Cleans:
1. Internal data/ paths leaked into reader-facing prose
2. Internal ledger names (sources.tsv, claims.tsv, assets_manifest.tsv) in reader-facing prose
3. Pseudocode/process residues in prose

Does NOT touch internal/sidecar manuscripts (00-*, visual packages, etc.)
"""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing")

# Files to fix (reader-facing chapter files and full draft)
# Skip internal/sidecar manuscripts that start with 00-, or are visual/source packages
READER_FILES = [
    "manuscript/Next-Token-full-draft.md",
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

# Also include recent synthesis/manuscript files that might have leaked into the full draft
EXTRA_FILES = [
    # These were used in the I-0320 quantitative enrichment
    "manuscript/Next-Token-quantitative-i0320.md",
    "manuscript/quantitative-enrichment-i0320.md",
]

# Patterns to fix: (match_pattern, replacement)
FIXES = [
    # data/ path references in prose - replace with descriptive text
    (r"`data/gpt_lineage_visual_table\.tsv`", "the companion source table"),
    (r"`data/rlhf_alignment_pipeline_i0023\.tsv`", "the companion source table"),
    (r"`data/chapter10_llama_family_tree_i0104\.tsv`", "the companion source table"),
    (r"`data/chapter11_china_open_model_source_map_i0105\.tsv`", "the companion source table"),
    (r"`data/price_quality_join_audit_i0036\.tsv`", "a supporting audit table"),
    (r"`data/provider_pricing_rows_i0026\.tsv`", "the normalized pricing rows"),
    
    # inline data/ references without backticks
    (r"\[data/price_quality_join_audit_i0036\.tsv\]", "[a supporting audit table]"),
    (r"\[data/provider_pricing_rows_i0026\.tsv\]", "[the normalized pricing rows]"),
    
    # Internal ledger names in reader-facing prose
    (r"`sources\.tsv`, `claims\.tsv`, and `assets_manifest\.tsv`", "the project's source, claim, and asset ledgers"),
    (r"`sources\.tsv`", "the source ledger"),
    (r"`claims\.tsv`", "the claim ledger"),
    (r"`assets_manifest\.tsv`", "the asset manifest"),
    
    # Local file path in prose context (indata/...)
    (r"indata/gpt_lineage_visual_table\.tsv", "the companion source table"),
    
    # Source notes with data/ paths
    (r"Sources: local:data/.*?\.tsv", "Sources: companion source table"),
    (r"Sources: data/.*?\.tsv", "Sources: supporting data table"),
    
    # C-XXXX;data/ patterns
    (r"C-0046;data/price_quality_join_audit_i0036\.tsv", "C-0046; a supporting audit table"),
    (r"C-0136;C-0141;data/price_quality_join_audit_i0036\.tsv", "C-0136; C-0141; a supporting audit table"),
    
    # data/provider_pricing_rows_i0026.tsv in brackets
    (r"data/provider_pricing_rows_i0026\.tsv;data/mistral_pricing_rows_i0031\.tsv", "the pricing data tables"),
]

def fix_file(filepath):
    path = BASE / filepath
    if not path.exists():
        print(f"  SKIP (not found): {filepath}")
        return 0
    
    content = path.read_text(encoding="utf-8")
    original = content
    changes = 0
    
    for pattern, replacement in FIXES:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            matches = len(re.findall(pattern, content))
            changes += matches
            print(f"  {pattern[:60]}... -> {matches} replacements")
            content = new_content
    
    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"  SAVED: {filepath} ({changes} changes)")
    else:
        print(f"  no changes: {filepath}")
    
    return changes

def main():
    total = 0
    print("I-0321: Cleaning internal path/ledger references from reader-facing prose\n")
    
    for f in READER_FILES + EXTRA_FILES:
        c = fix_file(f)
        total += c
    
    print(f"\nTotal replacements across all files: {total}")
    
    # Additional: fix the quantitative enrichment manuscript specifically
    qe_path = BASE / "manuscript/Next-Token-quantitative-i0320.md"
    if qe_path.exists():
        content = qe_path.read_text(encoding="utf-8")
        # Remove any internal path refs
        for pattern, replacement in FIXES:
            content = re.sub(pattern, replacement, content)
        qe_path.write_text(content, encoding="utf-8")
        print(f"  Fixed: manuscript/Next-Token-quantitative-i0320.md")
    
    # Find any remaining data/ or assets_manifest references in the full draft
    draft_path = BASE / "manuscript/Next-Token-full-draft.md"
    if draft_path.exists():
        content = draft_path.read_text(encoding="utf-8")
        remaining_data = re.findall(r'`?data/\w+\.tsv`?', content)
        remaining_assets = re.findall(r'assets_manifest\.tsv', content)
        remaining_sources = re.findall(r'`?sources\.tsv`?', content)
        remaining_claims = re.findall(r'`?claims\.tsv`?', content)
        
        print(f"\nRemaining internal references in full draft:")
        print(f"  data/*.tsv: {len(remaining_data)}")
        if remaining_data:
            for r in remaining_data[:5]:
                print(f"    {r}")
        print(f"  assets_manifest.tsv: {len(remaining_assets)}")
        print(f"  sources.tsv: {len(remaining_sources)}")
        print(f"  claims.tsv: {len(remaining_claims)}")

if __name__ == "__main__":
    main()
