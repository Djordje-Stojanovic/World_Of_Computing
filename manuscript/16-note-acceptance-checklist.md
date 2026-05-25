# Chapter 16 Note Acceptance Checklist

Status: promoted design-control pass I-0062 on 2026-05-25.

Companion table: `data/chapter16_note_acceptance_checklist_i0062.tsv`.

This pass defines the acceptance gate for moving any CH16Q row IDs out of `manuscript/16-speed-to-power.md`. It does not move the row IDs. The first eligible test remains only the LBNL/DOE U.S. paragraph, where N16-1 may replace the inline CH16Q-003 through CH16Q-006 clusters if the note preserves all four mappings separately.

Acceptance summary:

- N16-1 may move only CH16Q-003, CH16Q-004, CH16Q-005, and CH16Q-006.
- The note must keep measured rows separate from modeled/projected scenario rows.
- The note must stay close to the paragraph as a same-page sidenote, footnote, or immediate note block.
- CH16Q-017 must remain inline beside NVIDIA/GTC "AI factory" company framing.
- CH16Q-018 must remain inline beside the energy-per-token exclusion.
- CH16Q-015 and CH16Q-016 stay inline until a later operator-survey note test labels them as survey signals.
- No new exact quantity, Wh/token estimate, or NVIDIA/GTC performance claim may enter a mock or layout without a successor CH16Q row.

Gate for I-0063: a single-page mock may proceed only if it can show a visible N16-1 note near the LBNL/DOE paragraph while leaving CH16Q-017 and CH16Q-018 inline in the live text. If the mock cannot pass proximity, mapping, and blocker-visibility checks, keep all CH16Q IDs inline.
