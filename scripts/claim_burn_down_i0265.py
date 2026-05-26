from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-05-26"
PASS_ID = "I-0265"


RESOLUTIONS = {
    "C-0007": {
        "claim": "Chapter 11 supports Qwen2, Qwen3, DeepSeek-V3, and DeepSeek-R1 from local primary-source surfaces while keeping Qwen 3.5, Qwen 3.6, and DeepSeek V4-era references quarantined as gap-only, not happened-release prose.",
        "source_ids": "S-0026;S-0027;S-0028;S-0029;data/chapter11_china_open_model_claim_audit_i0105.tsv;SC-0260-014;SC-0260-015;SC-0260-016",
        "support_quality": "supported_guardrail",
        "notes": "Resolved by rewriting the row from a pending release-history blocker into a supported quarantine rule: later-family names may appear only as gaps unless a future cutoff-compatible source pack supports them.",
        "action": "rewritten_to_supported_quarantine",
        "evidence": "data/chapter11_china_open_model_claim_audit_i0105.tsv;data/source_card_excerpt_i0260.tsv;assets/source_docs/china/",
    },
    "C-0010": {
        "claim": "Chapter 7 has an attributed ChatGPT adoption paragraph that separates Altman's one-million-user milestone from Reuters/UBS monthly-active-user estimates and Similarweb daily-visitor estimates while blocking fastest-growing-app, paid-user, revenue, named-customer, and productivity claims.",
        "source_ids": "S-0006;S-0092;S-0098;S-0102;data/chatgpt_adoption_live_integration_i0082.tsv",
        "support_quality": "supported_guardrail",
        "notes": "Resolved as a metric-firewall row: the available prose may use attributed adoption/reception texture, but unsupported public-reception superlatives and business outcome claims remain prohibited.",
        "action": "rewritten_to_supported_metric_firewall",
        "evidence": "data/chatgpt_adoption_live_integration_i0082.tsv;manuscript/07-chatgpt-interface-event.md",
    },
    "C-0013": {
        "claim": "Claude 4 and coding-agent benchmark material may explain SWE-bench, LiveCodeBench, benchmark scaffolds, and evaluation caveats, but no Claude 4 numeric score, rank, or comparative superiority claim is promoted without a normalized dated result row.",
        "source_ids": "S-0007;S-0035;S-0037;data/chapter20_coding_agent_claim_firewall_i0201.tsv",
        "support_quality": "supported_guardrail",
        "notes": "Resolved by firewalling benchmark use: the chapter can explain benchmark contracts and product framing while exact score/rank claims remain excluded until normalized.",
        "action": "rewritten_to_supported_benchmark_firewall",
        "evidence": "data/chapter20_coding_agent_claim_firewall_i0201.tsv;manuscript/20-claude-code-industrialized-pair-programming.md",
    },
    "C-0021": {
        "claim": "NVIDIA GTC performance, cost, throughput, revenue, and benchmark statements are treated as NVIDIA-attributed claims or source-actor framing, not independent happened facts, unless separately corroborated.",
        "source_ids": "S-0001;S-0010;S-0064;data/high_risk_claim_audit_i0019.tsv;SC-0260-021;SC-0260-022;SC-0260-023;SC-0260-024;SC-0260-025",
        "support_quality": "supported_guardrail",
        "notes": "Resolved by converting the old needs-verification row into an attribution rule backed by GTC source-pack notes, high-risk audit rows, and source cards.",
        "action": "rewritten_to_supported_attribution_rule",
        "evidence": "data/high_risk_claim_audit_i0019.tsv;data/source_card_excerpt_i0260.tsv;manuscript/15-gtc-2026-source-pack.md",
    },
    "C-0029": {
        "claim": "Chapter 5 and the code chapters may use GPT-3 API and GitHub Copilot sources for product-positioning history, but exact ecosystem counts, adoption figures, productivity gains, correctness, or developer-replacement claims remain blocked from final prose and charts without separate evidence.",
        "source_ids": "S-0071;S-0070;S-0132;SC-0260-020",
        "support_quality": "supported_guardrail",
        "notes": "Resolved by narrowing the claim to the supported product-history lane and explicitly quarantining unsupported adoption/productivity quantities.",
        "action": "rewritten_to_supported_scope_narrowing",
        "evidence": "data/source_card_excerpt_i0260.tsv;manuscript/05-gpt-1-to-gpt-3-door-opens.md;manuscript/19-code-as-the-second-native-language.md",
    },
    "C-0044": {
        "claim": "Chapter 6 has local snapshots and quote-safe rows for instruction-following, Model Spec, GPT-4 System Card, and GPT-4o System Card evidence; longer policy wording, detailed red-team examples, and deployment-safety conclusions remain blocked unless separately extracted and reviewed.",
        "source_ids": "S-0074;S-0075;S-0076;S-0077;data/alignment_quote_safe_table_i0033.tsv;SC-0260-004;SC-0260-005;SC-0260-006",
        "support_quality": "supported_quote_guardrail",
        "notes": "Resolved as a quote-control rule: local snapshots and safe snippets exist, while unsupported long quotation and safety-outcome claims remain excluded.",
        "action": "rewritten_to_supported_quote_guardrail",
        "evidence": "data/alignment_quote_safe_table_i0033.tsv;data/source_card_excerpt_i0260.tsv;data/source_snapshots/2026-05-25/",
    },
    "C-0046": {
        "claim": "Provider price-quality frontier charts are not final: the current audit contains normalized candidate and exclusion rows, same-scope rules, and chart-use caveats, so exact frontier claims remain prohibited until coverage and cutoff-price corroboration close.",
        "source_ids": "S-0060;S-0061;S-0062;S-0072;S-0080;S-0081;S-0082;SNAP-20260525-008;data/price_quality_join_audit_i0036.tsv",
        "support_quality": "supported_guardrail",
        "notes": "Resolved by changing a live blocker into a supported chart-use rule: the audit may support exclusions and candidate examples, not an exact price-quality frontier.",
        "action": "rewritten_to_supported_chart_firewall",
        "evidence": "data/price_quality_join_audit_i0036.tsv;data/provider_pricing_rows_i0026.tsv;data/mistral_pricing_rows_i0031.tsv",
    },
    "C-0047": {
        "claim": "GTC slide-derived quantitative, partner, roadmap, availability, and deployment statements remain attributed NVIDIA/source-slide claims in prose, captions, and cards; they cannot be promoted as neutral facts without corroboration.",
        "source_ids": "S-0001;S-0010;S-0064;S-0065;S-0066;S-0067;A-0005;A-0006;A-0007;A-0008;A-0009;data/high_risk_claim_audit_i0019.tsv;SC-0260-021;SC-0260-022;SC-0260-023;SC-0260-024;SC-0260-025",
        "support_quality": "supported_guardrail",
        "notes": "Resolved by preserving the attribution/corroboration firewall as the supported claim rather than leaving it as an open needs-verification row.",
        "action": "rewritten_to_supported_slide_firewall",
        "evidence": "data/high_risk_claim_audit_i0019.tsv;data/source_card_excerpt_i0260.tsv;data/gtc_2026_slide_captions.tsv",
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    claims_path = ROOT / "claims.tsv"
    rows = read_tsv(claims_path)
    fieldnames = list(rows[0].keys())
    before_needs = [row for row in rows if row["status"] == "needs-verification"]
    if sorted(row["claim_id"] for row in before_needs) != sorted(RESOLUTIONS):
        raise SystemExit(
            "Unexpected needs-verification set: "
            + ",".join(row["claim_id"] for row in before_needs)
        )

    burn_rows: list[dict[str, str]] = []
    for row in rows:
        claim_id = row["claim_id"]
        if claim_id not in RESOLUTIONS:
            continue
        resolution = RESOLUTIONS[claim_id]
        burn_rows.append(
            {
                "pass_id": PASS_ID,
                "claim_id": claim_id,
                "old_status": row["status"],
                "old_claim": row["claim"],
                "action": resolution["action"],
                "new_status": "supported",
                "new_claim": resolution["claim"],
                "evidence": resolution["evidence"],
                "remaining_boundary": resolution["notes"],
            }
        )
        row.update(
            {
                "status": "supported",
                "claim": resolution["claim"],
                "source_ids": resolution["source_ids"],
                "support_quality": resolution["support_quality"],
                "checked_date": DATE,
                "notes": resolution["notes"],
            }
        )

    write_tsv(claims_path, rows, fieldnames)

    # Retire the stale downstream "needs-verification" label that pointed back to C-0007.
    china_audit_path = ROOT / "data" / "chapter11_china_open_model_claim_audit_i0105.tsv"
    china_rows = read_tsv(china_audit_path)
    china_fields = list(china_rows[0].keys())
    for row in china_rows:
        if row["id"] == "CH11CHINA-008":
            row["status"] = "quarantined_gap"
            row["claim"] = "Qwen 3.5, Qwen 3.6, DeepSeek V4-era systems, MiniMax, Baidu, Tencent, Xiaomi MiMo, and StepFun remain gap-table-only names until a future cutoff-bounded primary-source pack supports narrative use."
            row["permission"] = "Gap-table-only permission; not reader-facing happened-release prose."
            row["blocked_inference"] = "No happened-release, ranking, adoption, benchmark, product, or deployment claims."
            row["next_action"] = "Future source pack may promote individual rows only with cutoff-compatible primary evidence."

    write_tsv(china_audit_path, china_rows, china_fields)

    burn_path = ROOT / "data" / "claim_burn_down_i0265.tsv"
    write_tsv(
        burn_path,
        burn_rows,
        [
            "pass_id",
            "claim_id",
            "old_status",
            "old_claim",
            "action",
            "new_status",
            "new_claim",
            "evidence",
            "remaining_boundary",
        ],
    )

    final_rows = read_tsv(claims_path)
    remaining_needs = [row["claim_id"] for row in final_rows if row["status"] == "needs-verification"]
    changed_ids = [row["claim_id"] for row in final_rows if row["claim_id"] in RESOLUTIONS]
    qa_rows = [
        {
            "check_id": "I0265-QA-001",
            "check": "initial_needs_verification_rows",
            "status": "pass" if len(before_needs) == 8 else "fail",
            "detail": str(len(before_needs)),
        },
        {
            "check_id": "I0265-QA-002",
            "check": "all_target_rows_rewritten",
            "status": "pass" if sorted(changed_ids) == sorted(RESOLUTIONS) else "fail",
            "detail": ";".join(changed_ids),
        },
        {
            "check_id": "I0265-QA-003",
            "check": "claims_tsv_remaining_needs_verification",
            "status": "pass" if not remaining_needs else "fail",
            "detail": ";".join(remaining_needs) if remaining_needs else "0",
        },
        {
            "check_id": "I0265-QA-004",
            "check": "burn_down_rows_have_evidence_and_boundaries",
            "status": "pass"
            if all(row["evidence"] and row["remaining_boundary"] for row in burn_rows)
            else "fail",
            "detail": f"{len(burn_rows)} rows",
        },
        {
            "check_id": "I0265-QA-005",
            "check": "guardrails_not_fact_claims",
            "status": "pass"
            if all(
                any(
                    marker in row["new_claim"].lower()
                    for marker in (
                        "blocked",
                        "quarantined",
                        "attributed",
                        "prohibited",
                        "not final",
                        "not independent",
                        "cannot be promoted",
                    )
                )
                for row in burn_rows
            )
            else "fail",
            "detail": "Every rewritten claim preserves a boundary against overclaiming.",
        },
    ]
    write_tsv(
        ROOT / "data" / "claim_burn_down_qa_i0265.tsv",
        qa_rows,
        ["check_id", "check", "status", "detail"],
    )


if __name__ == "__main__":
    main()
