from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_ID = "I-0267"
DATE = "2026-05-26"

SOURCE_RE = re.compile(r"S-\d{4}")
CLAIM_RE = re.compile(r"C-\d{4}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def clean(text: str, limit: int = 360) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "..."


def source_ref(source: dict[str, str]) -> str:
    title = source["title"]
    org = source["creator_or_org"]
    typ = source["source_type"]
    accessed = source["accessed_date"]
    path = source["url_or_path"]
    role = source["primary_or_secondary"]
    return f"{source['source_id']} - {title} ({org}; {typ}; {role}; accessed {accessed}; {path})"


def claim_ref(claim: dict[str, str]) -> str:
    return f"{claim['claim_id']} - {clean(claim['claim'], 220)}"


def note_text(source_ids: list[str], claim_ids: list[str], sources: dict[str, dict[str, str]], claims: dict[str, dict[str, str]], boundary: str) -> str:
    pieces = [source_ref(sources[sid]) for sid in source_ids]
    pieces.extend(claim_ref(claims[cid]) for cid in claim_ids)
    if boundary:
        pieces.append("Boundary: " + boundary)
    return " | ".join(pieces)


def main() -> None:
    sources = {row["source_id"]: row for row in read_tsv(ROOT / "sources.tsv")}
    claims = {row["claim_id"]: row for row in read_tsv(ROOT / "claims.tsv")}
    placeholders = read_tsv(ROOT / "data" / "endnote_placeholders_i0249.tsv")
    repairs = read_tsv(ROOT / "data" / "source_density_repair_i0266.tsv")

    final_rows: list[dict[str, str]] = []
    missing_sources: set[str] = set()
    missing_claims: set[str] = set()
    source_counter: Counter[str] = Counter()
    cluster_counter: Counter[str] = Counter()

    for placeholder in placeholders:
        source_ids = SOURCE_RE.findall(placeholder["source_ids"])
        claim_ids = CLAIM_RE.findall(placeholder["source_ids"])
        for sid in source_ids:
            if sid not in sources:
                missing_sources.add(sid)
        for cid in claim_ids:
            if cid not in claims:
                missing_claims.add(cid)
        source_counter.update(source_ids)
        cluster_key = ";".join(sorted(source_ids + claim_ids))
        cluster_counter[cluster_key] += 1
        final_rows.append(
            {
                "pass_id": PASS_ID,
                "note_id": placeholder["note_id"],
                "chapter": placeholder["chapter"],
                "chapter_title": placeholder["chapter_title"],
                "anchor_type": placeholder["origin"],
                "manuscript_anchor": clean(placeholder["anchor_excerpt"], 240),
                "source_ids": ";".join(source_ids),
                "claim_ids": ";".join(claim_ids),
                "source_count": str(len(source_ids)),
                "claim_count": str(len(claim_ids)),
                "compressed_cluster_id": cluster_id(cluster_key),
                "expanded_note": note_text(source_ids, claim_ids, sources, claims, "Placeholder expanded from I-0249; final page number awaits render pagination."),
                "page_anchor_status": "manuscript_anchor_ready__render_page_number_pending",
                "final_note_status": "expanded_from_placeholder",
            }
        )

    for index, repair in enumerate(repairs, start=1):
        source_ids = SOURCE_RE.findall(repair["inserted_sources"])
        claim_ids = CLAIM_RE.findall(repair["inserted_sources"])
        for sid in source_ids:
            if sid not in sources:
                missing_sources.add(sid)
        for cid in claim_ids:
            if cid not in claims:
                missing_claims.add(cid)
        source_counter.update(source_ids)
        cluster_key = ";".join(sorted(source_ids + claim_ids))
        cluster_counter[cluster_key] += 1
        final_rows.append(
            {
                "pass_id": PASS_ID,
                "note_id": f"SL{index:03d}",
                "chapter": chapter_from_line(repair["heading_line_before"]),
                "chapter_title": "Source-density bridge lane",
                "anchor_type": "source_density_lane_i0266",
                "manuscript_anchor": repair["heading"],
                "source_ids": ";".join(source_ids),
                "claim_ids": ";".join(claim_ids),
                "source_count": str(len(source_ids)),
                "claim_count": str(len(claim_ids)),
                "compressed_cluster_id": cluster_id(cluster_key),
                "expanded_note": note_text(source_ids, claim_ids, sources, claims, repair["boundary"]),
                "page_anchor_status": "heading_anchor_ready__render_page_number_pending",
                "final_note_status": "expanded_from_source_lane",
            }
        )

    if missing_sources or missing_claims:
        raise SystemExit(f"Missing refs: sources={sorted(missing_sources)} claims={sorted(missing_claims)}")

    write_tsv(
        ROOT / "data" / "final_endnotes_i0267.tsv",
        final_rows,
        [
            "pass_id",
            "note_id",
            "chapter",
            "chapter_title",
            "anchor_type",
            "manuscript_anchor",
            "source_ids",
            "claim_ids",
            "source_count",
            "claim_count",
            "compressed_cluster_id",
            "expanded_note",
            "page_anchor_status",
            "final_note_status",
        ],
    )

    bibliography_rows = []
    for sid, count in sorted(source_counter.items()):
        src = sources[sid]
        bibliography_rows.append(
            {
                "pass_id": PASS_ID,
                "source_id": sid,
                "note_ref_count": str(count),
                "title": src["title"],
                "creator_or_org": src["creator_or_org"],
                "source_type": src["source_type"],
                "primary_or_secondary": src["primary_or_secondary"],
                "accessed_date": src["accessed_date"],
                "url_or_path": src["url_or_path"],
                "cutoff_relevance": src["cutoff_relevance"],
                "used_in": src["used_in"],
                "bibliography_entry": source_ref(src),
                "caveat": clean(src["notes"], 260),
            }
        )
    write_tsv(
        ROOT / "data" / "bibliography_i0267.tsv",
        bibliography_rows,
        [
            "pass_id",
            "source_id",
            "note_ref_count",
            "title",
            "creator_or_org",
            "source_type",
            "primary_or_secondary",
            "accessed_date",
            "url_or_path",
            "cutoff_relevance",
            "used_in",
            "bibliography_entry",
            "caveat",
        ],
    )

    cluster_rows = []
    for key, count in sorted(cluster_counter.items(), key=lambda item: (-item[1], item[0])):
        source_ids = SOURCE_RE.findall(key)
        claim_ids = CLAIM_RE.findall(key)
        cluster_rows.append(
            {
                "pass_id": PASS_ID,
                "compressed_cluster_id": cluster_id(key),
                "use_count": str(count),
                "source_ids": ";".join(source_ids),
                "claim_ids": ";".join(claim_ids),
                "cluster_note": note_text(source_ids, claim_ids, sources, claims, "Compressed repeated cluster; do not remove local claim caveats where prose needs them."),
            }
        )
    write_tsv(
        ROOT / "data" / "compressed_note_clusters_i0267.tsv",
        cluster_rows,
        ["pass_id", "compressed_cluster_id", "use_count", "source_ids", "claim_ids", "cluster_note"],
    )

    qa_rows = [
        row("I0267-QA-001", "placeholder_notes_expanded", len(placeholders) > 0 and all(r["final_note_status"] != "" for r in final_rows), f"placeholders={len(placeholders)}; final_notes={len(final_rows)}"),
        row("I0267-QA-002", "source_lane_notes_expanded", len(repairs) == 63 and sum(1 for r in final_rows if r["anchor_type"] == "source_density_lane_i0266") == 63, f"source_lanes={len(repairs)}"),
        row("I0267-QA-003", "all_source_refs_resolve", not missing_sources, "missing=" + ",".join(sorted(missing_sources))),
        row("I0267-QA-004", "all_claim_refs_resolve", not missing_claims, "missing=" + ",".join(sorted(missing_claims))),
        row("I0267-QA-005", "bibliography_has_access_dates", all(r["accessed_date"] for r in bibliography_rows), f"sources={len(bibliography_rows)}"),
        row("I0267-QA-006", "bibliography_has_source_roles", all(r["primary_or_secondary"] for r in bibliography_rows), f"sources={len(bibliography_rows)}"),
        row("I0267-QA-007", "clusters_created", len(cluster_rows) > 0 and any(int(r["use_count"]) > 1 for r in cluster_rows), f"clusters={len(cluster_rows)}"),
        row("I0267-QA-008", "no_placeholder_phrase_in_expanded_notes", all("Placeholder only" not in r["expanded_note"] for r in final_rows), "expanded notes do not carry I-0249 placeholder wording"),
    ]
    write_tsv(
        ROOT / "data" / "final_endnotes_qa_i0267.tsv",
        qa_rows,
        ["check_id", "check", "status", "detail"],
    )

    write_summary(final_rows, bibliography_rows, cluster_rows, qa_rows)


def row(check_id: str, check: str, ok: bool, detail: str) -> dict[str, str]:
    return {"check_id": check_id, "check": check, "status": "pass" if ok else "fail", "detail": detail}


def cluster_id(key: str) -> str:
    if not key:
        return "CL-EMPTY"
    checksum = sum(ord(ch) for ch in key) % 100000
    return f"CL-{checksum:05d}"


def chapter_from_line(line: str) -> str:
    try:
        value = int(line)
    except ValueError:
        return "unknown"
    # Approximate chapter anchor from assembled full-draft line ranges. Exact page numbers wait for render.
    ranges = [
        (43, "01"), (225, "02"), (381, "03"), (549, "04"), (729, "05"), (931, "06"),
        (1157, "07"), (1368, "08"), (1574, "09"), (1765, "10"), (1951, "11"), (2138, "12"),
        (2418, "13"), (2655, "14"), (2850, "15"), (3099, "16"), (3344, "17"), (3532, "18"),
        (3722, "19"), (3913, "20"), (4111, "21"), (4249, "22"), (4423, "23"), (4545, "24"),
    ]
    current = "unknown"
    for start, chapter in ranges:
        if value >= start:
            current = chapter
    return current


def write_summary(final_rows: list[dict[str, str]], bibliography_rows: list[dict[str, str]], cluster_rows: list[dict[str, str]], qa_rows: list[dict[str, str]]) -> None:
    qa_pass = sum(1 for r in qa_rows if r["status"] == "pass")
    qa_fail = sum(1 for r in qa_rows if r["status"] == "fail")
    source_lane_rows = sum(1 for r in final_rows if r["anchor_type"] == "source_density_lane_i0266")
    placeholder_rows = len(final_rows) - source_lane_rows
    top_clusters = sorted(cluster_rows, key=lambda r: int(r["use_count"]), reverse=True)[:5]
    lines = [
        "# I-0267 Final Endnote And Bibliography Pass",
        "",
        "Pass I-0267 expands the I-0249 source-ID placeholders and the I-0266 source-density lanes into a readable source apparatus. It records manuscript anchors now and leaves rendered page numbers for the next render/page-proof cycle.",
        "",
        "## Result",
        "",
        f"- Expanded final note rows: {len(final_rows)}.",
        f"- I-0249 placeholder-derived rows: {placeholder_rows}.",
        f"- I-0266 source-lane-derived rows: {source_lane_rows}.",
        f"- Bibliography source rows: {len(bibliography_rows)}.",
        f"- Compressed repeated source clusters: {len(cluster_rows)}.",
        f"- QA: {qa_pass} pass / {qa_fail} fail in `data/final_endnotes_qa_i0267.tsv`.",
        "",
        "## Strongest Repeated Clusters",
        "",
    ]
    for cluster in top_clusters:
        lines.append(f"- `{cluster['compressed_cluster_id']}` used {cluster['use_count']} times: {cluster['source_ids'] or cluster['claim_ids']}.")
    lines.extend(
        [
            "",
            "## Remaining Gates",
            "",
            "- Render pagination must convert manuscript anchors into page numbers.",
            "- Page design must decide whether notes appear as back notes, sidenotes, footnotes, or compressed chapter source notes.",
            "- Some caveats must remain inline where moving them to notes would weaken truth controls, especially GTC/NVIDIA, benchmark, price-quality, and infrastructure scenario claims.",
        ]
    )
    (ROOT / "manuscript" / "final-endnotes-bibliography-i0267.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
