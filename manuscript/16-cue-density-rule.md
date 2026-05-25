# Chapter 16 Cue-Density Rule

Pass I-0057 converts the I-0053 readability audit into a stable rule for final Chapter 16 layout. The companion table is `data/chapter16_cue_density_rule_i0057.tsv`.

The rule is conservative: CH16Q row IDs stay inline whenever the sentence contains an exact measured value, forecast/scenario value, advisory estimate, operator-survey signal, blocked NVIDIA/GTC company claim, or explicit energy-per-token exclusion. Source-only brackets may be combined or moved to a paragraph note, but a bracket containing a CH16Q ID is not source-only clutter.

The only current candidate for a cleaner final-note treatment is the dense U.S. LBNL/DOE paragraph containing CH16Q-003 through CH16Q-006. A sidenote or endnote may replace the inline cluster only if it preserves all four mappings separately: TWh measured, TWh scenario, percentage measured, and percentage scenario.

This rule does not change `manuscript/16-speed-to-power.md`. It gives I-0058 a test harness: build a final-note prototype that makes the chapter cleaner while proving that CH16Q-017 and CH16Q-018 remain visible blockers and that scenarios cannot be mistaken for happened history.
