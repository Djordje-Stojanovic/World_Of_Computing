# Chapter 16 Final-Note Prototype

Pass I-0058 tests the I-0057 cue-density rule against the current Chapter 16 opening. The companion table is `data/chapter16_final_note_prototype_i0058.tsv`.

## Accepted Test Case

The only current paragraph that should move CH16Q row IDs out of inline brackets is the dense U.S. LBNL/DOE paragraph. A prototype final layout may replace the two inline CH16Q clusters with one note anchor:

> The United States made the compression visible. Lawrence Berkeley National Laboratory and the Department of Energy reported about 176 terawatt-hours of U.S. data-centre electricity use in 2023, then modeled 2028 scenarios ranging from 325 to 580 terawatt-hours. In share terms, the report put U.S. data centres at about 4.4 percent of electricity use in 2023 and projected a possible 6.7 to 12 percent by 2028. [N16-1] Those were scenarios, not prophecy.

Prototype note:

> N16-1: LBNL/DOE U.S. data-centre paragraph. CH16Q-003 = reported 176 TWh 2023 estimate; CH16Q-004 = modeled 325-580 TWh 2028 scenario range; CH16Q-005 = reported 4.4 percent 2023 share; CH16Q-006 = projected 6.7 to 12 percent 2028 scenario share. Keep reported/modeled/projected/scenario labels; do not collapse all four rows into one "LBNL/DOE data" claim.

## Rejected Moves

Do not move CH16Q-017 or CH16Q-018 out of inline prose. CH16Q-017 is the NVIDIA/GTC company-claim blocker, and CH16Q-018 is the energy-per-token exclusion. They are guardrails, not ordinary citations. A final layout may duplicate them in sidenotes, but the row IDs must remain visible in the sentence where the tempting claim or exclusion appears.

## Deferred Moves

CH16Q-001/CH16Q-002 and CH16Q-015/CH16Q-016 can stay inline for now. They are readable enough, and moving them would add design complexity before the page system proves it can preserve measured-versus-forecast and operator-survey labels.

This pass does not edit `manuscript/16-speed-to-power.md`. It defines the first safe note prototype and the two non-negotiable inline blockers for the eventual PDF/layout pass.
