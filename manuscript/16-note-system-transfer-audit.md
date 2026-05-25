# Chapter 16 Note-System Transfer Audit

Pass: I-0088
Date: 2026-05-25
Surface: `manuscript/16-speed-to-power.md`
Parent: live Chapter 16 after N16-1 integration and render gate I-0083

## Result

N16-1 is a reusable pattern only in a narrow sense. It proves that a dense measured/scenario cluster can move from inline CH16Q row IDs into a nearby note when the rendered page keeps the note on the same page, preserves the row mapping in text extraction, and leaves unrelated blocker rows visible in live prose.

It does not prove that all Chapter 16 row IDs can move into notes. CH16Q-015 and CH16Q-016 are weaker operator-survey signals and need a separate N16-3 prototype that labels them as such. CH16Q-017 and CH16Q-018 are guardrails, not ordinary citations: the NVIDIA/GTC company-framing blocker and the energy-per-token exclusion must remain inline unless a later pass both duplicates and visibly preserves them at sentence level.

## Transfer Rule

The pattern is not "replace inline claim IDs with notes." The pattern is:

1. Move only one claim family at a time.
2. Preserve source role and claim type in the note text.
3. Prove same-page proximity and text extraction in a render gate.
4. Keep hard blockers inline when the reader could otherwise infer an unsupported claim.
5. Treat operator-survey rows as a different family from measured/scenario rows.

## Verdict

Promoted audit, no live prose change. The next safe Chapter 16 note experiment is an N16-3 operator-survey prototype for CH16Q-015 and CH16Q-016, but only if it says "operator-survey signal" in the note and passes the same render checks. N16-1 should not be generalized to CH16Q-017 or CH16Q-018.
