# I-0028 Alignment Source Snapshot Notes

Access date: 2026-05-25

Purpose: document local capture status for Chapter 6 alignment sources before using exact OpenAI instruction-following, behavior-specification, or system-card wording.

## Result

- S-0074 / SNAP-20260525-004: shell HTML capture of `https://openai.com/index/instruction-following/` returned HTTP 403. Local note saved at `data/source_snapshots/2026-05-25/2026-05-25__S-0074__html__capture-note.txt`.
- S-0075 / SNAP-20260525-005: Model Spec 2024-05-08 HTML captured successfully, 120,063 bytes, SHA256 `F2CDAC6E4383AD3A9EFD3B83026784F4561E78052ED5009CA1C22A0300C150A1`.
- S-0076 / SNAP-20260525-006: GPT-4 System Card PDF captured successfully, 1,014,552 bytes, SHA256 `CA3677E1B83E255AA1296D432D374378154F230F3C296B32EE67540D571B7004`. The PDF is local ignored source media under the repository heavyweight-media rule; the committed ledger records its path and hash.
- S-0077 / SNAP-20260525-007: GPT-4o System Card PDF captured successfully, 1,402,648 bytes, SHA256 `E2579ECB185CBC13BAC39F9DBF25E1917F78E1EA5A3A5023165C6614FB5DB724`. The PDF is local ignored source media under the repository heavyweight-media rule; the committed ledger records its path and hash.

## Use Rules

- Use the captured Model Spec and locally ignored system-card artifacts for structural Chapter 6 support and short quote candidates only after quote-limit review.
- Keep S-0074 as structural/paraphrase-only until a local HTML, screenshot, or archive capture exists.
- Keep C-0044 open because the highest-value product-post wording and labeler-process details remain local-capture blocked.
