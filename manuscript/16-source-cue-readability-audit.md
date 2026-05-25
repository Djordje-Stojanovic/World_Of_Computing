# Chapter 16 Source-Cue Readability Audit

Status: promoted prose-audit pass I-0053 on 2026-05-25.

This audit checks the Chapter 16 opening after the CH16Q source-cue merge. The companion table is `data/chapter16_source_cue_readability_i0053.tsv`.

## Finding

The CH16Q cue system is readable enough to keep. The only obvious clutter came from adjacent source-only brackets in the opening and closing paragraphs. Those were compacted in `manuscript/16-speed-to-power.md` without moving or deleting any CH16Q row ID.

The heavier cue clusters in the IEA, LBNL/DOE, EPRI, DOE-SEAB, and Uptime paragraphs should stay for now because each cluster protects exact TWh, MW, percentage, lead-time, PUE, rack-density, NVIDIA/GTC, or energy-per-token-exclusion language. Removing those cues before a final note system exists would make the prose prettier but less inspectable.

## Current Rule

- Combine adjacent source-only brackets when they interrupt cadence.
- Keep CH16Q row IDs inline when the paragraph contains exact quantitative, scenario, advisory, operator-survey, NVIDIA/GTC-blocker, or explicit-exclusion language.
- Do not collapse CH16Q IDs into a paragraph-level note until a later cue-density rule proves the row mapping remains auditable.

