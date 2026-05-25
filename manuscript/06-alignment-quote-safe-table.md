# Chapter 6 Quote-Safe Alignment Table

Pass: I-0033  
Purpose: convert captured OpenAI alignment artifacts into controlled quote candidates before Chapter 6 uses exact policy or system-card wording.

## Result

The working table lives in `data/alignment_quote_safe_table_i0033.tsv`. It separates three states:

- S-0074 / SNAP-20260525-004 remains paraphrase-only because shell capture returned HTTP 403.
- S-0075 / SNAP-20260525-005 is captured HTML, so short Model Spec phrases can be used after context review.
- S-0076 and S-0077 are captured official PDFs with hash-recorded local media, so short system-card phrases can be used, but red-team examples and detailed mitigation wording still need context checks.

## Usable Chapter Moves

Chapter 6 can now quote or near-quote only very small phrases from captured artifacts:

- Model Spec: behavior became a specification surface, organized around objectives, rules, defaults, and a command hierarchy.
- GPT-4 System Card: deployment safety was presented as a combination of measurements, model-level changes, product/system interventions, and external expert engagement, while the document itself warned that mitigations remained limited and brittle.
- GPT-4o System Card: the system-card pattern continued into multimodal assistant deployment, with larger external red teaming and named risk-evaluation frameworks.

## Still Blocked

C-0044 remains open. The highest-risk missing piece is still S-0074: no exact OpenAI instruction-following product-post wording, detailed labeler-process claims, API-default language, or direct quotation from that page should enter final prose until a browser capture, archive capture, or official alternate exists.

## Drafting Rule

The chapter should prefer paraphrase unless exact wording changes the reader's understanding. When exact wording is useful, use the table's short excerpts only and preserve first-party attribution: these documents show how OpenAI described its safety and behavior-shaping work, not independent proof that the resulting systems were safe or aligned.
