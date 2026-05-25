# Chapter 16 N16-1 Production Layout Gate

Pass I-0068 turns the A-0017 N16-1 SVG mock into a production PDF/render gate. The checklist in `data/chapter16_n16_1_production_layout_gate_i0068.tsv` defines the exact evidence required before any live edit removes CH16Q-003 through CH16Q-006 from inline prose.

The gate is stricter than the mock. It requires same-page placement, visible proximity to the LBNL/DOE paragraph anchor, readable main-text and note line lengths, no note collision, preserved CH16Q-003 through CH16Q-006 mapping, continued inline visibility for CH16Q-017 and CH16Q-018, operator-signal stability for CH16Q-015 and CH16Q-016, no new quantitative claims, and an A/B render comparison against the current inline-cue parent.

Promotion rule: live `manuscript/16-speed-to-power.md` remains unchanged. N16-1 may enter production only after a rendered Chapter 16 page proves that readability improves without hiding blocker rows or turning scenarios into happened facts.
