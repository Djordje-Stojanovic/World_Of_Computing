# I-0337: FINAL COMPREHENSIVE PASS - Complete Book Perfection

## Target
Complete the "Next Token" book to publication-ready state with:
- **Full image-embedded PDF** (not just text)
- **Correct image placement** in each chapter (per exhibit manifest)
- **Max 1 image per page** enforced
- **Zero forbidden strings** in final output
- **Perfect chronological timeline** (Jan 1, 2025 → May 20, 2026)
- **All 30+ verified events** integrated (DeepSeek, OpenAI, Meta, NVIDIA, AMD, xAI, Claude, etc.)
- **100,000-120,000 word count** (currently 104,701)
- **24 chapters** in correct order (Transformer first, ChatGPT at Ch6)

## Current State (as of I-0336)
- ✅ Prose complete: 104,701 words, 24 chapters
- ✅ Basic PDF rendered (text-only, no images)
- ✅ All content additions done (DeepSeek V3.2/DSA/NSA/DFlash, OpenAI o3/o4-mini/GPT-5, Llama 4, vLLM/SGLang, DGX Spark, Ryzen AI, Colossus, Hormuz, Micron, GPU timeline, Stargate)
- ✅ Chapter order correct (Transformer → Attention → Scaling → GPT → Alignment → ChatGPT → Microsoft → Google → Meta → China → Anthropic → Europe/xAI → Benchmarks → NVIDIA → GTC → Power → Data → Tools → Code → Claude Code → Reasoning → Economics → Trust → Next Token)
- ✅ All hard gates passed on prose (zero process language, zero placeholder language, zero claim-blocker apparatus)
- ❌ **Full image-embedded PDF NOT DONE** (basic render only, no images)
- ❌ **Final champion pointer NOT updated**
- ❌ **Final SHA-256 hash NOT computed for image-embedded PDF**
- ❌ **Visual QA on final PDF NOT done**

## Required Actions (DO ALL IN THIS PASS)

### 1. Full Image-Embedded PDF Render
**Goal**: Render PDF with all images embedded in correct chapters

**Steps**:
1.1. Use the I-0262 rendering pipeline (`scripts/render_full_book_i0262.py`)
1.2. Point to the final manuscript: `manuscript/Next-Token-PUBLICATION-CANDIDATE.md`
1.3. Use the corrected exhibit manifest: `data/selected_exhibit_manifest_i0261.tsv`
1.4. Enforce max 1 image per page rule
1.5. Output to: `rendered/final_i0337/Next-Token-final-i0337.pdf`

**Why**: The basic render (I-0335) has no images. The I-0262 pipeline embeds images from the exhibit manifest into the correct chapter context.

### 2. Hard Gate QA on Final PDF
**Goal**: Verify the final PDF meets all publication requirements

**Checks**:
2.1. **Multi-image pages**: Zero pages with more than 1 image
2.2. **Blank pages**: Zero completely blank pages
2.3. **Forbidden strings**: Zero instances of:
   - `C:/`, `file:///`
   - `data/*.tsv`, `assets_manifest`, `sources.tsv`, `claims.tsv`
   - `Date span:`, `Cutoff guard:`, `Status:`, `Use note`, `Boundary:`
   - `What This Chapter Must Not`, `notes ledger`
   - `Place Figure`, `Visual integration:`, `Visual anchor:`
   - `this pass does`, `later pass`, `future pass`, `queued by pass`
   - `What This Chapter Must Not Claim`, `does not support`, `remains blocked`
   - `private-edition visual layer`, `visual portfolio`, `PORTFOLIO PLATE`

2.4. **Visual density**: Each page has appropriate text density (not too sparse, not too dense)
2.5. **Image captions**: All images have correct captions (no "Chapter X" labels)
2.6. **Figure numbering**: Stable Fcc.nn IDs throughout
2.7. **Page count**: Verify total pages match expected count
2.8. **Word count**: Confirm 100,000-120,000 words in final PDF

**Output**: `data/final_i0337_qa.tsv` with all check results

### 3. Final SHA-256 Hash
**Goal**: Compute hash of the final PDF

**Steps**:
3.1. Calculate SHA-256 of `rendered/final_i0337/Next-Token-final-i0337.pdf`
3.2. Record in: `manuscript/FINAL-BOOK-REPORT.md`
3.3. Record in: `scoreboard.tsv`

### 4. Champion Pointer Update
**Goal**: Update the champion pointer to the new final PDF

**Steps**:
4.1. Update: `champion/final-private-pdf-pointer-i0337.md`
4.2. Include:
   - PDF filename
   - SHA-256 hash
   - Word count
   - Chapter count
   - Render date
   - Honest completion report (what's done, what's not, any known issues)

### 5. Reader Guide Update
**Goal**: Update the reader guide with final PDF link

**Steps**:
5.1. Update: `manuscript/reader-guide-final.md`
5.2. Include:
   - Link to final PDF
   - How to read the book
   - Key themes and structure
   - Note about the 24-chapter chronological design

### 6. Final Commit and Push
**Goal**: Commit all final artifacts to GitHub

**Steps**:
6.1. Stage all final files:
   - `manuscript/Next-Token-FINAL.md`
   - `manuscript/Next-Token-PUBLICATION-CANDIDATE.md`
   - `manuscript/FINAL-BOOK-REPORT.md`
   - `manuscript/reader-guide-final.md`
   - `champion/final-private-pdf-pointer-i0337.md`
   - `rendered/final_i0337/Next-Token-final-i0337.pdf` (if git-allowed, otherwise just the manifest)
   - `data/final_i0337_qa.tsv`
   - All scripts created in this pass

6.2. Commit message:
   ```
   pass I-0337: FINAL COMPREHENSIVE PASS - complete book with full image-embedded PDF, hard gate QA, SHA-256 hash, champion pointer, reader guide
   ```

6.3. Push to `main`

### 7. Scoreboard Update
**Goal**: Record this pass in the append-only ledger

**Steps**:
7.1. Update `scoreboard.tsv` with:
   - Pass ID: I-0337
   - Type: comprehensive
   - Description: Final book with image-embedded PDF, all hard gates, champion pointer
   - Verdict: DONE
   - Word count: 104,701
   - SHA-256: [computed hash]
   - Date: [current date]

### 8. Ideas TSV Update
**Goal**: Mark I-0326 and I-0337 as done

**Steps**:
8.1. Update `ideas.tsv`:
   - I-0326: change from "pending" to "done"
   - I-0337: add as new done entry

### 9. Insights Update
**Goal**: Document key learnings from the complete project

**Steps**:
9.1. Update `insights.md` with:
   - Final word count and chapter count
   - Key content additions (30+ events)
   - Timeline corrections made
   - Visual design decisions
   - What worked, what didn't
   - Recommendations for future projects

### 10. Final Verification Checklist
**Goal**: Confirm everything is complete

**Checklist**:
- [ ] Full image-embedded PDF rendered
- [ ] Max 1 image per page enforced
- [ ] All images in correct chapter context
- [ ] Zero forbidden strings in final output
- [ ] Zero process language in reader text
- [ ] Zero placeholder language in reader text
- [ ] 24 chapters in correct chronological order
- [ ] 100,000-120,000 word count achieved
- [ ] SHA-256 hash computed and recorded
- [ ] Champion pointer updated
- [ ] Reader guide updated
- [ ] Final commit and push done
- [ ] Scoreboard updated
- [ ] Insights updated
- [ ] Ideas.tsv updated (I-0326 marked done)

## Success Criteria
The pass is complete when:
1. **PDF exists**: `rendered/final_i0337/Next-Token-final-i0337.pdf` with embedded images
2. **QA passes**: All hard gates show zero failures
3. **Hash computed**: SHA-256 recorded in report and scoreboard
4. **Champion updated**: `champion/final-private-pdf-pointer-i0337.md` points to final PDF
5. **Git pushed**: All final artifacts committed and pushed to main
6. **Ledgers updated**: scoreboard.tsv, insights.md, ideas.tsv all updated

## Dependencies
- Chrome installed at `C:\Program Files\Google\Chrome\Application\chrome.exe`
- pymupdf (fitz) installed
- I-0262 render pipeline available
- Exhibit manifest at `data/selected_exhibit_manifest_i0261.tsv`

## Output Files
- `rendered/final_i0337/Next-Token-final-i0337.pdf` (final book with images)
- `rendered/final_i0337/Next-Token-final-i0337.html` (HTML source)
- `data/final_i0337_qa.tsv` (QA results)
- `manuscript/FINAL-BOOK-REPORT.md` (completion report)
- `manuscript/reader-guide-final.md` (reader guide)
- `champion/final-private-pdf-pointer-i0337.md` (champion pointer)
- `scripts/final_comprehensive_i0337.py` (orchestration script)

## Notes
- This is the FINAL pass. After this, the book is complete.
- Do not commit large binary PDFs to git (use .gitignore or store externally)
- The prose is already clean and complete (104,701 words)
- The only thing missing is the image-embedded PDF render
- After this pass, there are NO remaining FIFO tasks
