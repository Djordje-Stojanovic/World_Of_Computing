# Insights: Next Token Project

## Final State (I-0337)

- **Word Count**: 104,416
- **Chapter Count**: 24
- **SHA-256**: fb52c3e6a4f701d97b8b8f4f0b11641d109171f5df59b26cc84bb61783c20195
- **Pass Count**: ~337 (I-0001 through I-0337)
- **Completion Date**: 2026-05-27
- **PDF**: rendered/final_i0337/Next-Token-final-i0337.pdf

## What Worked

1. **FIFO Queue Discipline**: The ideas.tsv FIFO queue kept work organized and traceable across 300+ passes
2. **Scripted Reproducibility**: All major edits were scripted in Python for auditability and rollback
3. **Hard Gates as Guardrails**: Explicit QA checks (forbidden strings, word count, chapter count) prevented drift
4. **Manifest-Driven Visuals**: The exhibit manifest system kept image assignments consistent and provenance-tracked
5. **Chronological Design**: Starting with Transformer prehistory rather than ChatGPT gave the book proper historical depth
6. **Ledger System**: Separate TSV files for claims, sources, assets, and scoreboard created a full audit trail
7. **Champion/Archive Pattern**: Never overwriting champion/ without backup prevented data loss

## What Required Multiple Passes

1. **Process Language Purge**: Required dedicated passes (I-0322, I-0323, I-0325) to fully remove editorial language
2. **Chapter Order Fix**: Required explicit work (I-0330) to move ChatGPT from Chapter 1 to Chapter 6
3. **Timeline Accuracy**: Required dedicated pass (I-0332) for Blackwell dates, Hormuz crisis, financial data
4. **Visual Placement**: Multiple passes (I-0318, I-0319, I-0324) to get images in correct chapter context

## Key Content Covered

- Transformer prehistory through Bahdanau attention
- GPT-1 through GPT-5.5 and the o-series reasoning models
- ChatGPT launch ecosystem and productization
- DeepSeek V3, V3.2, V4, R1, DSA, NSA, DFlash
- Meta Llama open-weight family through Llama 4
- NVIDIA H100/Blackwell/DGX Spark and CUDA moat
- AMD MI300X/MI350X/Ryzen AI alternative path
- xAI Colossus 1 (200K GPU, 300MW, 122 days) and Colossus 2
- Anthropic Claude through Opus 4.7
- vLLM and SGLang inference engines
- OpenAI $110B raise, Anthropic economics
- GPU rental price index, Hormuz Strait crisis
- Benchmarks, LMArena, coding agents, test-time compute

## Lessons for Future Projects

1. **Start with the manifest**: Define image assignments before writing prose
2. **Script everything**: All edits should be reproducible Python
3. **Hard gates early**: Forbidden string checks should run after every pass
4. **Chronological first**: Always start with historical depth, not the shock moment
5. **FIFO discipline**: One pass, one task, commit immediately
6. **Prose/manifest separation**: Keep clean publication prose separate from image-embedding drafts
7. **Ledger-backed claims**: Every factual claim needs a source row before it enters prose

## Final Verdict

The book "Next Token" is complete. All 24 chapters written, all hard gates passed, zero forbidden strings in reader-facing prose, sources tracked, and the publication candidate cleanly rendered. The project moved from an initial ChatGPT-centric opening through chronological reconstruction to a final text that reads like a serious nonfiction book about the LLM era.
