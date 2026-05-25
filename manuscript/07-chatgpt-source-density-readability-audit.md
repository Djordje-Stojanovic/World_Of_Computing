# Chapter 7 Source-Density And Readability Audit

Pass: I-0087
Date: 2026-05-25
Surface: `manuscript/07-chatgpt-interface-event.md`
Parent: champion Chapter 7 after I-0082 and I-0086

## Result

Chapter 7's paragraph-level source density is healthy after the adoption and institutional-reception integrations: 2,837 body words, 18 source-cue brackets, and about 157.6 words per cue before the verification-task tail. The cues are not too sparse. The main readability problem is instead control text concentration: the opening source note has become a miniature ledger, and two Enterprise sentences still describe S-0079 as blocked even though I-0075 later made it locally text-rendered and quote-ready for narrow OpenAI-attributed rows.

The live prose should not be broadly polished yet. The adoption paragraph and reception paragraph are doing the right kind of work: their source cues sit close to the claims, and their caveats prevent metric merging, fastest-growing-app shorthand, and fake public-reception generalization. Moving those caveats into notes now would make the chapter prettier but weaker.

## Findings

See `data/chatgpt_ch7_readability_audit_i0087.tsv` for row-level results.

- Keep the current paragraph source-cue density; it is inside the 150-250 words-per-cue target.
- Split the opening source note in a later cleanup pass into a compact global note plus paragraph-level notes. Keep only global prohibitions in the opener.
- Modernize S-0079 wording before or during the next Enterprise integration pass: S-0079 is quote-ready only for narrow OpenAI-attributed original-post rows, while C-0010 still blocks paid Enterprise adoption, neutral named-customer deployment, and measured productivity outcomes.
- Keep the adoption metric firewall inline until a note prototype proves paragraph-level visibility.
- Keep the reception negative-control sentence inline; it is a claim-control sentence, not clutter.
- Treat I-0090 as the natural next prose pass: a single PwC sentence can cite S-0100 and S-0103 together only if pricing, revenue, active usage, paid seats, global rollout, client adoption, and productivity blockers remain visible.

## Gate

Verdict: promoted audit, no live prose change. This pass improves the evaluator by preventing an attractive but unsafe cleanup: collapsing all C-0010 caveats into the opening note would reduce friction for readers but would also hide the exact metric and source-role boundaries that make Chapter 7 honest.
