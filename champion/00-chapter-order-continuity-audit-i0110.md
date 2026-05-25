# Chapter-Order Continuity Audit

Status: pass I-0110, promoted structural audit.

## Executive Read

The current book is making real progress, but the structural risk is now visible: strong local chapters are not yet a clean book. Fresh measurement after the Chapter 20 expansion shows about 53,318 mapped or near-mapped main-chapter words if the unplaced Anthropic/Claude section is counted as material, but only 12 of 24 outline chapters have substantial chapter-like drafts. The book still has no true Chapter 1, no Microsoft/OpenAI chapter, no Google/DeepMind chapter, no Europe/xAI/Mistral chapter, no CUDA foundation chapter, and no final-act chapters on reasoning, economics, trust, or synthesis.

The largest continuity hazard is `manuscript/12-anthropic-and-claude-spine-section.md`. It is valuable Anthropic/Claude material, but it does not match the official Chapter 12 slot, which is "Europe, xAI, and the Rest of the Frontier." It should stay visible as a high-value spine section, but future passes must not let it silently erase the Mistral/xAI/rest-of-frontier chapter.

## Main Findings

1. The official outline still has exactly 24 chapters, but the manuscript filenames no longer line up cleanly with the outline. Files `01`, `02`, and `03` currently map to outline Chapters 2, 3, and 4 because the true opening "The Shock" is missing.
2. Chapters 8 and 9 are major business/history gaps. Without Microsoft/OpenAI and Google/DeepMind/Gemini, the book cannot credibly reach the `Chip War`/business-book benchmark.
3. Chapters 14-16 have an inverted hardware buildup. GTC 2026 and infrastructure are drafted, but the CUDA/GPU moat chapter that should teach the reader why NVIDIA mattered is still absent.
4. Chapters 18-20 need boundary discipline. Chapter 20 is now strong as a Claude Code case study, but it should not absorb the general tool/RAG/agent turn of Chapter 18 or the broader code-history arc of Chapter 19.
5. The visual system is too concentrated. The manifest has useful SVGs and GTC-derived cards, but the book still lacks a broad non-NVIDIA screenshot/photo layer.
6. The late book does not yet exist. Reasoning/test-time compute, economics, trust/failure, and final synthesis remain all-missing.

## Promotion Rationale

This pass improves the book by turning structural drift into auditable steering data. It does not add prose volume, but it prevents the next prose and asset passes from optimizing local chapters while leaving the official spine broken. The audit is promoted because it fixes a hard planning defect with no content regression.

## Deliverables

- `data/chapter_order_continuity_audit_i0110.tsv` - chapter-by-chapter continuity table for all 24 outline slots.
- `data/spine_gap_and_overlap_i0110.tsv` - cross-chapter gap, overlap, and sequencing risks.

## Immediate Queue Implications

The existing pending queue is well aimed. I-0111, I-0112, I-0113, and I-0115 directly attack the biggest gaps identified here: Google/DeepMind, non-NVIDIA visuals, Microsoft/OpenAI, and the tools/agent turn. The one caution is sequencing: the Anthropic/Claude sidecar should remain unfinalized until the Chapter 12 placement question is resolved.
