from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_ID = "I-0268"
DATE = "2026-05-26"

SOURCE_RE = re.compile(r"S-\d{4}")
CLAIM_RE = re.compile(r"C-\d{4}|CH[0-9A-Z-]+")


AUDITS = [
    ("02-03", "architecture", "data/chapter2_transformer_claim_audit_i0093.tsv", "claim_id", "claim", "source_ids", "support_quality", "prose_permission", "blockers"),
    ("04", "scaling", "data/chapter3_scaling_claim_audit_i0094.tsv", "claim_id", "claim", "source_ids", "support_quality", "prose_permission", "blockers"),
    ("05", "gpt_lineage", "data/chapter5_gpt_lineage_claim_audit_i0095.tsv", "row_id", "claim_family", "source_ids", "status", "allowed_use", "blocked_use"),
    ("06", "alignment", "data/chapter6_alignment_claim_audit_i0096.tsv", "row_id", "claim_family", "source_ids", "status", "allowed_use", "blocked_use"),
    ("13", "benchmarks", "data/chapter13_rankings_expansion_claim_audit_i0098.tsv", "claim_id", "claim", "source_ids", "status", "allowed_language", "blocked_language"),
    ("14", "gpu_cuda", "data/chapter14_nvidia_cuda_claim_audit_i0116.tsv", "id", "claim", "source_ids", "status", "permission", "blocked_leaps"),
    ("16", "datacenter_power", "data/chapter16_quant_claim_audit_i0043.tsv", "claim_row_id", "quantity_or_phrase", "source_ids", "claim_type", "prose_permission", "caveat"),
    ("17", "data_tokens", "data/chapter17_data_tokens_claim_audit_i0121.tsv", "claim_id", "claim", "support", "status", "chapter_use", "blocker_or_note"),
    ("18", "tools_agents", "data/chapter18_tools_agents_claim_audit_i0115.tsv", "id", "claim", "source_ids", "status", "permission", "blocked_leaps"),
    ("19", "code", "data/chapter19_code_second_native_language_claim_audit_i0125.tsv", "claim_id", "claim", "source_ids", "status", "support_quality", "notes"),
    ("20", "coding_agents", "data/chapter20_coding_agents_claim_audit_i0107.tsv", "claim_id", "claim", "source_ids", "status", "support_quality", "notes"),
    ("21", "reasoning", "data/chapter21_reasoning_claim_audit_i0122.tsv", "id", "claim", "source_ids", "status", "evidence_note", "blocked_leap"),
    ("22", "economics", "data/chapter22_economics_claim_audit_i0127.tsv", "claim_id", "claim", "support", "status", "chapter_use", "blocker_or_note"),
    ("23", "trust", "data/chapter23_trust_claim_audit_i0128.tsv", "id", "claim", "source_ids", "status", "evidence_note", "blocked_leap"),
]

REQUESTED_CHAPTERS = {"02", "03", "04", "05", "06", "13", "14", "17", "18", "19", "20", "21", "22", "23"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_status(raw: str, allowed: str, blocked: str) -> str:
    text = " ".join([raw or "", allowed or "", blocked or ""]).lower()
    if "needs-verification" in text or "active" == (raw or "").lower() or "blocker" == (raw or "").lower():
        return "blocked_not_promoted"
    if "caveat" in text or "forecast" in text or "vendor" in text or "attribution" in text:
        return "supported_with_caveat"
    return "supported"


def decision_for(verdict: str) -> str:
    if verdict == "blocked_not_promoted":
        return "keep_as_guardrail_or_followup; do not promote into neutral prose/chart/caption"
    if verdict == "supported_with_caveat":
        return "allowed only with attribution/scope/date/harness/source-role caveat"
    return "allowed as bounded technical prose with source cue"


def split_chapters(chapter_field: str) -> list[str]:
    return re.findall(r"\d{2}", chapter_field)


def main() -> None:
    sources = {row["source_id"] for row in read_tsv(ROOT / "sources.tsv")}
    claims = {row["claim_id"] for row in read_tsv(ROOT / "claims.tsv")}
    rows: list[dict[str, str]] = []
    missing_sources: set[str] = set()
    missing_claim_refs: set[str] = set()

    for chapter, category, path_str, id_col, claim_col, source_col, status_col, allowed_col, blocked_col in AUDITS:
        path = ROOT / path_str
        for item in read_tsv(path):
            source_text = item.get(source_col, "")
            source_ids = SOURCE_RE.findall(source_text)
            claim_refs = [ref for ref in re.findall(r"C-\d{4}", source_text) if ref in claims]
            for sid in source_ids:
                if sid not in sources:
                    missing_sources.add(sid)
            for ref in re.findall(r"C-\d{4}", source_text):
                if ref not in claims:
                    missing_claim_refs.add(ref)
            raw_status = item.get(status_col, "")
            allowed = item.get(allowed_col, "")
            blocked = item.get(blocked_col, "")
            verdict = normalize_status(raw_status, allowed, blocked)
            rows.append(
                {
                    "pass_id": PASS_ID,
                    "chapter": chapter,
                    "technical_category": category,
                    "source_audit_file": path_str,
                    "audit_row_id": item.get(id_col, ""),
                    "raw_status": raw_status,
                    "technical_claim": item.get(claim_col, ""),
                    "source_ids": ";".join(source_ids),
                    "claim_guardrail_refs": ";".join(claim_refs),
                    "evidence_field": allowed,
                    "blocked_or_caveat_field": blocked,
                    "fact_check_verdict": verdict,
                    "i0268_decision": decision_for(verdict),
                }
            )

    write_tsv(
        ROOT / "data" / "technical_fact_check_i0268.tsv",
        rows,
        [
            "pass_id",
            "chapter",
            "technical_category",
            "source_audit_file",
            "audit_row_id",
            "raw_status",
            "technical_claim",
            "source_ids",
            "claim_guardrail_refs",
            "evidence_field",
            "blocked_or_caveat_field",
            "fact_check_verdict",
            "i0268_decision",
        ],
    )

    chapter_rows: list[dict[str, str]] = []
    for chapter in sorted({chapter for row in rows for chapter in split_chapters(row["chapter"])}):
        scoped = [row for row in rows if chapter in split_chapters(row["chapter"])]
        verdicts = {name: sum(1 for row in scoped if row["fact_check_verdict"] == name) for name in ["supported", "supported_with_caveat", "blocked_not_promoted"]}
        chapter_rows.append(
            {
                "pass_id": PASS_ID,
                "chapter": chapter,
                "rows": str(len(scoped)),
                "supported": str(verdicts["supported"]),
                "supported_with_caveat": str(verdicts["supported_with_caveat"]),
                "blocked_not_promoted": str(verdicts["blocked_not_promoted"]),
                "fact_check_status": "pass_with_guardrails" if scoped and not missing_sources else "fail",
            }
        )
    write_tsv(
        ROOT / "data" / "technical_fact_check_by_chapter_i0268.tsv",
        chapter_rows,
        ["pass_id", "chapter", "rows", "supported", "supported_with_caveat", "blocked_not_promoted", "fact_check_status"],
    )

    target_covered = REQUESTED_CHAPTERS.issubset({row["chapter"] for row in chapter_rows})
    qa_rows = [
        qa("I0268-QA-001", "requested_chapter_coverage", target_covered, f"covered={';'.join(row['chapter'] for row in chapter_rows)}"),
        qa("I0268-QA-002", "fact_check_rows_created", len(rows) >= 100, str(len(rows))),
        qa("I0268-QA-003", "all_source_ids_resolve", not missing_sources, ",".join(sorted(missing_sources))),
        qa("I0268-QA-004", "all_claim_guardrails_resolve", not missing_claim_refs, ",".join(sorted(missing_claim_refs))),
        qa("I0268-QA-005", "blocked_rows_not_promoted", all(row["i0268_decision"].startswith("keep_as_guardrail") for row in rows if row["fact_check_verdict"] == "blocked_not_promoted"), str(sum(1 for row in rows if row["fact_check_verdict"] == "blocked_not_promoted"))),
        qa("I0268-QA-006", "caveated_rows_preserve_caveats", all("caveat" in row["i0268_decision"] or "attribution" in row["i0268_decision"] for row in rows if row["fact_check_verdict"] == "supported_with_caveat"), str(sum(1 for row in rows if row["fact_check_verdict"] == "supported_with_caveat"))),
    ]
    write_tsv(ROOT / "data" / "technical_fact_check_qa_i0268.tsv", qa_rows, ["check_id", "check", "status", "detail"])
    write_summary(rows, chapter_rows, qa_rows)


def qa(check_id: str, check: str, ok: bool, detail: str) -> dict[str, str]:
    return {"check_id": check_id, "check": check, "status": "pass" if ok else "fail", "detail": detail}


def write_summary(rows: list[dict[str, str]], chapter_rows: list[dict[str, str]], qa_rows: list[dict[str, str]]) -> None:
    counts = {name: sum(1 for row in rows if row["fact_check_verdict"] == name) for name in ["supported", "supported_with_caveat", "blocked_not_promoted"]}
    qa_pass = sum(1 for row in qa_rows if row["status"] == "pass")
    qa_fail = sum(1 for row in qa_rows if row["status"] == "fail")
    lines = [
        "# I-0268 Technical Fact-Check",
        "",
        "Pass I-0268 consolidates existing chapter-level technical claim audits into one full technical fact-check register for Chapters 2-6, 13-14, and 17-23. It does not promote blocked claims; it records which claims are allowed, caveated, or explicitly not promoted.",
        "",
        "## Result",
        "",
        f"- Consolidated fact-check rows: {len(rows)}.",
        f"- Supported rows: {counts['supported']}.",
        f"- Supported-with-caveat rows: {counts['supported_with_caveat']}.",
        f"- Blocked/not-promoted guardrail rows: {counts['blocked_not_promoted']}.",
        f"- Covered requested chapters: {', '.join(row['chapter'] for row in chapter_rows)}.",
        f"- QA: {qa_pass} pass / {qa_fail} fail in `data/technical_fact_check_qa_i0268.tsv`.",
        "",
        "## Remaining Gates",
        "",
        "- Chapter 14 still needs independent non-NVIDIA corroboration before market-power, lock-in, or switching-cost prose becomes final.",
        "- Chapter 18 prompt-injection detail needs stronger security sources before taxonomy, prevalence, or incident claims.",
        "- Chapter 20 Claude 4 benchmark numbers remain vendor/harness gated; no exact comparative scores should be charted yet.",
        "- Chapter 22 still blocks revenue, gross margin, ROI, utilization, and final price-quality frontier claims.",
        "- The next technical pass should line-edit any prose that drifts beyond the allowed/caveated language in this register.",
    ]
    (ROOT / "manuscript" / "technical-fact-check-i0268.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
