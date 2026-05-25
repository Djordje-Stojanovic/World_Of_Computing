# I-0038 Instruction-Following Alternate Capture Notes

Pass date: 2026-05-25

Purpose: resolve the S-0074 local-capture gap for OpenAI's "Aligning language models to follow instructions" post after direct shell HTML capture returned HTTP 403 in I-0028.

## Result

Direct shell capture of `https://openai.com/index/instruction-following/` remained blocked in prior pass `SNAP-20260525-004`. In this pass, the canonical official URL was captured through a text-render path:

- `SNAP-20260525-016`
- Local path: `data/source_snapshots/2026-05-25/2026-05-25__S-0074__product-post__instruction-following__text-render.md`
- SHA256: `FA7160D04B855079197A5D3E13A2AD370B8A5A798DFD50611221DA3F97F7419F`

## Useful Lines

- Line 38: publication date.
- Line 50: InstructGPT framing and API default deployment.
- Lines 192-194: GPT-3 next-word prediction contrast and RLHF/labeler demonstration/ranking process.
- Lines 284-288: demonstration/comparison/reward-model/PPO pipeline and "alignment tax" discussion.
- Lines 292-298: labeler/researcher/customer/policy influence and limitations.

## Use Rules

S-0074 may now move from paraphrase-only to short-quote-ready for the product-post points listed in `data/alignment_quote_safe_table_i0033.tsv`.

C-0044 should remain active, but narrowed. The remaining blocker is no longer S-0074's missing capture; it is final quote extraction and context review for red-team examples, exact model-policy wording, and any longer system-card passages that might enter final Chapter 6 prose.
