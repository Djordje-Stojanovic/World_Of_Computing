# Chapter 16 Quantitative Claim Audit

Status: promoted claim-audit pass I-0043, 2026-05-25.

Audit table: `data/chapter16_quant_claim_audit_i0043.tsv`.

Scope: this pass audits the quantitative and scenario language in `manuscript/16-speed-to-power.md` plus the quantitative implications of `data/power_to_token_flow_i0042.tsv`.

Result: Chapter 16 now has row-level permission for TWh, MW, percentage, lead-time, PUE, rack-density, and energy-per-token language. The audit separates measured estimates, forecast/scenario ranges, advisory estimates, operator-survey signals, NVIDIA/GTC blocked claims, and explicit exclusions.

Use rule: do not add a Chapter 16 chart, caption, or prose paragraph with exact TWh, MW, percentage, lead-time, PUE, rack-density, NVIDIA performance, or energy-per-token language unless the claim maps to a row in the audit table or a later row supersedes it.
