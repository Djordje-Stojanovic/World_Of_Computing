# I-0321: Complete Hostile QA Audit — All Defect Categories

Date: 2026-05-27
PDF: `rendered/final_private_i0320/Next-Token-final-private-quantitative-i0320.pdf`
Pages: 640 | Images: 300 | Words: 101,906

## EXECUTIVE SUMMARY

**The I-0320 PDF is not a finished book.** It is a heavily-annotated internal proof that retains
452 instances of process/scaffolding language, has images placed in wrong chapters, and opens
Chapter 1 (about the 2017 Transformer) with a NVIDIA Blackwell GPU image.

## DEFECT CATEGORIES

### CATEGORY 1: Process/Scaffolding Language (452 instances in 54 patterns)

| Pattern | Count | Example |
|---------|-------|---------|
| "should not" | 63 | "The prose should not claim..." |
| "the chapter should" | 48 | "The chapter should use one visual early" |
| "the book should" | 32 | "The book should keep its LLM focus" |
| "Date span:" | 24 | "Date span: 2017" on every chapter opener |
| "Cutoff guard:" | 24 | "Cutoff guard: The chapter stays with..." on every opener |
| "reader should" | 18 | "The reader should feel the compression" |
| "notes ledger" | 18 | ",notes ledger," embedded in prose |
| "this chapter should" | 15 | "This chapter should avoid treating..." |
| "needs a" | 14 | "the model still needs a sense of where tokens are" |
| "not yet" | 10 | "the user was not yet typing a task into a blank box" |
| "live in" | 10 | "the companion rows live in data/..." |
| "should stay" | 8 | "the phrase should stay temporary" |
| "should feel" | 8 | "the reader should feel how practical that was" |
| "should resist" | 8 | "the chapter should resist both hype and dismissal" |
| "should avoid" | 8 | "the book should avoid any claim that..." |
| "the chapter must" | 7 | "What This Chapter Must Not Claim" |
| "should use" | 7 | "the chapter should use three lanes" |
| "should keep" | 11 | "the book should keep showing the chorus" |
| "should treat" | 6 | "the book should treat those later moves with suspicion" |
| "should preserve" | 5 | "the chapter should preserve that specificity" |
| "Place Figure" | 5 | "Place Figure 16.1...near the start of the chapter" |
| "remains blocked" | 3 | "Proprietary corpus composition remains blocked" |
| "visual integration:" | 3 | "Visual integration: Figure 6.1,notes ledger, shows..." |
| "this pass does not" | 3 | "This pass does not add a dedicated synthetic-data source pack" |
| "later pass" | 2 | "in a later pass, it should enter through a sourced mechanism" |
| "future pass" | 1 | "explicit handoffs to future passes" |
| "queued by pass" | 1 | "Figure 10.2, queued by pass, should make the control stack explicit" |
| "visual anchor:" | 1 | "Visual anchor: Figure 5.1,notes ledger, compresses..." |
| "this book should" | 1 | "this book should call it the interface event" |
| "this chapter cannot" | 1 | "details this chapter cannot wave away" |
| "this chapter will" | 1 | "the strongest version of this chapter will eventually include" |
| "this chapter must" | 1 | "What This Chapter Must Not Claim" |
| "this section should" | 1 | "this section should have a practical aftertaste" |
| "this pass is" | 1 | "The most important Qwen claim for this pass is therefore structural" |
| "should show" | 9 | various |
| "should carry" | 5 | various |
| "should make" | 5 | various |
| "should leave" | 5 | various |
| "should let" | 3 | various |
| "should end" | 2 | various |
| "should sit" | 1 | various |
| "should help" | 1 | various |
| "should explain" | 1 | various |
| "should lean" | 1 | various |
| "should phrase" | 1 | various |
| "should speak" | 1 | various |
| "should distinguish" | 1 | various |

**Root cause**: The manuscript chapters were written in an "annotated proof" style where
editorial instructions, claim-control scaffolding, and visual placement notes were mixed
into the prose. The rescue passes (I-0313 through I-0320) applied structural transforms
but never performed the final prose cleanup that converts annotated draft into finished book.

### CATEGORY 2: Image Context Misplacement (CRITICAL)

**Chapter 1 (2017 Transformer) opens with WRONG images:**
- p4: "NVIDIA Blackwell, shown as a public web page" — A 2024 GPU in a 2017 chapter
- p5: "Oriol Vinyals" — Not a Transformer paper author (he was on seq2seq)

**Chapter 2 (Pre-2017 Sequence Problem) opens with WRONG images:**
- p21: "Jupyter" 
- p22: "NumPy"
- p23: "SciPy"
— These are modern Python tools, completely wrong for pre-2017 language modeling history

**Chapter 3 (2020 Scaling Laws) opens with:**
- p41: "visual grammar prototype" — Internal design mockup, not book content

**Chapter 24 (Final Synthesis) opens with:**
- p625: "xAI, shown as a public web page"
- p626: "Crusoe Cloud, shown as a public web page"
— Random company logos in the final chapter

**Visual caption format problem**: Many images have captions like "Chapter X Y" (e.g., "Chapter 19 code-as-language ladder") revealing internal chapter numbering in reader-facing captions.

### CATEGORY 3: Incomplete/Placeholder Language (18 instances)

- "pending" (8), "waiting for" (2), "should eventually" (2), 
- "still needs" (1), "needs more" (1), "still blocked" (1)
- "this chapter still" (1), "eventually include" (1), "will eventually" (1)

### CATEGORY 4: Claim-Blocker Apparatus in Reader Text (24 instances)

- "does not support" (7)
- "What This Chapter Must Not Claim" / "Still Refuses" (8)
- "claims blocked" (3), "unsupported claim" (2), "not licensed by" (2)
- These are internal permission notes that leaked into reader prose

### CATEGORY 5: Chapter-Opener Metadata Format

Every chapter opener repeats:
```
Date span: YYYY
CATEGORY LABEL
Cutoff guard: Internal instruction text
```
This is internal project infrastructure, not book design. The "Date span" and "Cutoff guard" are useful for authors but not readers. A trade book would integrate dates naturally into the opening paragraph.

### CATEGORY 6: Broken/Orphan Pages

- p76: "Generated RLHF and alignment pipeline visual" — Broken visual (0 images detected)
- p265: "What Claude Proves, And What It Does Not" — 40-char orphan section heading
- p355: Continuity note (FIXED in I-0321 source)
- p640: Weak closing line (110 chars)

## FIXES ALREADY APPLIED IN I-0321

- ✅ 33 internal path references (`data/*.tsv`, `assets_manifest.tsv`, etc.) replaced
- ✅ Internal continuity note in Chapter 14 rewritten as narrative transition
- ✅ 13 chapter source files cleaned

## HONEST ASSESSMENT

The I-0320 PDF functions as a structural proof — it proves the 24-chapter spine exists,
images are embedded, tables are placed, and hard gates (no blank pages, no multi-image pages)
pass. But it does NOT read like a finished book. The 452 process-language instances, wrong
opening images, and internal metadata labels mean a reader would perceive it as an
annotated draft, not a published work.

**The I-0322 "final publication candidate" pass must do a deep prose cleanup across
all 24 chapters before any final render.** This is the honest remaining work.
