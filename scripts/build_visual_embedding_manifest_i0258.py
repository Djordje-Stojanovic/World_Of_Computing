from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path


PASS_ID = "I-0258"
ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "data" / "full_book_figure_list_i0229.tsv"
RIGHTS = ROOT / "data" / "image_rights_staging_i0250.tsv"
ASSETS = ROOT / "assets_manifest.tsv"
RENDER_MANIFEST = ROOT / "rendered" / "full_book_i0257" / "render_manifest_i0257.tsv"
RASTER_DIR = ROOT / "rendered" / "full_book_i0257" / "embedded_rasters"
OUT_TSV = ROOT / "data" / "visual_embedding_manifest_i0258.tsv"
QA_TSV = ROOT / "data" / "visual_embedding_manifest_qa_i0258.tsv"
SUMMARY_MD = ROOT / "manuscript" / "visual-embedding-manifest-i0258.md"


FIELDS = [
    "pass_id",
    "figure_id",
    "chapter",
    "chapter_anchor",
    "selected_rank",
    "asset_id",
    "asset_type",
    "figure_title",
    "caption",
    "alt_text",
    "source_note",
    "source_ids",
    "rights_status",
    "rights_stage",
    "publication_decision",
    "manifest_status",
    "source_file",
    "source_file_exists",
    "source_sha256",
    "render_embed_file",
    "render_embed_file_exists",
    "render_embed_sha256",
    "i0257_render_status",
    "fallback_action",
    "claim_boundary",
    "proof_gate",
    "fail_closed_status",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256_or_blank(path_text: str) -> str:
    if not path_text:
        return ""
    path = ROOT / path_text
    if not path.exists() or path.is_dir():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def exists_text(path_text: str) -> str:
    if not path_text:
        return "no"
    return "yes" if (ROOT / path_text).exists() else "no"


def render_manifest() -> dict[str, str]:
    data: dict[str, str] = {}
    if not RENDER_MANIFEST.exists():
        return data
    for line in RENDER_MANIFEST.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            key, value = line.split("\t", 1)
            data[key] = value
    return data


def raster_path_for(figure_id: str, source_file: str) -> str:
    if not source_file.lower().endswith(".svg"):
        return ""
    stem = Path(source_file).stem
    candidate = RASTER_DIR / f"{figure_id.replace('.', '-')}_{stem}.png"
    return str(candidate.relative_to(ROOT)) if candidate.exists() else ""


def source_note(fig: dict[str, str], right: dict[str, str], asset: dict[str, str]) -> str:
    source_ids = right.get("source_ids") or fig.get("source_ids", "")
    source_title = asset.get("source_title", "")
    source_page = asset.get("source_page_or_time", "")
    creator = asset.get("creator_or_org", "")
    parts = []
    if source_ids:
        parts.append(f"Source IDs: {source_ids}")
    if source_title:
        parts.append(f"Asset source: {source_title}")
    if source_page and source_page != "n/a":
        parts.append(f"Anchor: {source_page}")
    if creator:
        parts.append(f"Creator/org: {creator}")
    return "; ".join(parts) if parts else "Source note missing; fail closed before publication."


def proof_gate(right: dict[str, str], render_embed_file: str) -> str:
    decision = right.get("publication_decision", "")
    if decision == "publish" and render_embed_file:
        return "I-0257 embedded-render proof exists; still requires page-image legibility, caption compression, and final source-note QA."
    if decision == "local-only":
        return "Keep local-only unless permission/fair-use/source-actor review explicitly promotes it; otherwise replace with redraw/source card."
    if decision == "redraw":
        return "Convert to source card or original redraw before embedding; raw source screenshot is blocked."
    if decision == "permission-needed":
        return "Capture/permission/fair-use review required; if unresolved, replace with self-made facsimile, source card, or alternate original visual."
    return "Publication decision unresolved; fail closed."


def fail_closed_status(right: dict[str, str], source_file_exists: str, render_embed_file_exists: str) -> str:
    decision = right.get("publication_decision", "")
    if decision == "publish" and source_file_exists == "yes" and render_embed_file_exists == "yes":
        return "embed_ready_after_page_qa"
    if decision == "publish":
        return "blocked_missing_publish_file_or_render"
    if source_file_exists != "yes":
        return f"blocked_missing_source_file_{decision or 'unresolved'}"
    return f"blocked_{decision or 'unresolved'}"


def build_rows() -> list[dict[str, str]]:
    figures = read_tsv(FIGURES)
    rights = {row["figure_id"]: row for row in read_tsv(RIGHTS)}
    assets = {row["asset_id"]: row for row in read_tsv(ASSETS)}
    rows: list[dict[str, str]] = []
    for fig in figures:
        figure_id = fig["figure_id"]
        right = rights.get(figure_id, {})
        asset = assets.get(fig.get("asset_id", ""), {})
        source_file = right.get("manifest_file_path") or fig.get("manifest_file_path", "")
        render_embed_file = raster_path_for(figure_id, source_file)
        source_file_exists = exists_text(source_file)
        render_embed_file_exists = exists_text(render_embed_file)
        caption = asset.get("caption") or f"{figure_id}: {fig.get('figure_title', '')}. {fig.get('final_role', '')}."
        fallback = right.get("replacement_path") or right.get("required_next_action") or fig.get("next_gate", "")
        rows.append(
            {
                "pass_id": PASS_ID,
                "figure_id": figure_id,
                "chapter": fig.get("chapter", ""),
                "chapter_anchor": fig.get("chapter_anchor", ""),
                "selected_rank": fig.get("selected_rank", ""),
                "asset_id": fig.get("asset_id", ""),
                "asset_type": fig.get("asset_type", ""),
                "figure_title": fig.get("figure_title", ""),
                "caption": caption,
                "alt_text": fig.get("alt_text", ""),
                "source_note": source_note(fig, right, asset),
                "source_ids": right.get("source_ids") or fig.get("source_ids", ""),
                "rights_status": right.get("rights_status") or fig.get("rights_status", ""),
                "rights_stage": right.get("rights_stage", ""),
                "publication_decision": right.get("publication_decision", ""),
                "manifest_status": right.get("manifest_status", ""),
                "source_file": source_file,
                "source_file_exists": source_file_exists,
                "source_sha256": sha256_or_blank(source_file),
                "render_embed_file": render_embed_file,
                "render_embed_file_exists": render_embed_file_exists,
                "render_embed_sha256": sha256_or_blank(render_embed_file),
                "i0257_render_status": "embedded_in_i0257_pdf" if render_embed_file_exists == "yes" else "not_embedded_in_i0257_pdf",
                "fallback_action": fallback,
                "claim_boundary": right.get("claim_boundary", ""),
                "proof_gate": proof_gate(right, render_embed_file),
                "fail_closed_status": fail_closed_status(right, source_file_exists, render_embed_file_exists),
            }
        )
    return rows


def qa(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    render = render_manifest()
    ids = [row["figure_id"] for row in rows]
    counts = Counter(row["fail_closed_status"] for row in rows)
    missing_required = [
        row["figure_id"]
        for row in rows
        if not row["caption"]
        or not row["alt_text"]
        or not row["source_note"]
        or not row["rights_stage"]
        or not row["fallback_action"]
        or not row["proof_gate"]
    ]
    duplicate_ids = sorted([item for item, count in Counter(ids).items() if count > 1])
    embedded_ready = counts.get("embed_ready_after_page_qa", 0)
    blocked = len(rows) - embedded_ready
    missing_source_files = [row["figure_id"] for row in rows if row["source_file_exists"] != "yes"]
    missing_publish_files = [
        row["figure_id"]
        for row in rows
        if row["publication_decision"] == "publish" and row["source_file_exists"] != "yes"
    ]
    embed_hashes = [
        row["render_embed_sha256"]
        for row in rows
        if row["fail_closed_status"] == "embed_ready_after_page_qa" and row["render_embed_sha256"]
    ]
    duplicate_embed_hash_count = len(embed_hashes) - len(set(embed_hashes))
    return [
        row("VM-001", "row_count", "pass" if len(rows) == 100 else "fail", f"rows={len(rows)}; expected=100", "Repair selected-figure join."),
        row("VM-002", "unique_figure_ids", "pass" if len(set(ids)) == 100 and not duplicate_ids else "fail", f"unique={len(set(ids))}; duplicates={';'.join(duplicate_ids) if duplicate_ids else 'none'}", "Repair duplicate/missing figure IDs."),
        row("VM-003", "required_fields", "pass" if not missing_required else "fail", f"missing_required_fields={';'.join(missing_required) if missing_required else 'none'}", "Fill caption, alt text, source note, rights stage, fallback, and proof gate for every row."),
        row("VM-004", "embedded_ready_rows", "pass" if embedded_ready == 74 else "fail", f"embed_ready_after_page_qa={embedded_ready}; expected=74", "Reconcile against I-0257 render output."),
        row("VM-005", "blocked_rows", "pass" if blocked == 26 else "fail", f"blocked_rows={blocked}; expected=26; statuses={dict(counts)}", "Keep unresolved slots fail-closed until capture/redraw/permission work finishes."),
        row("VM-006", "render_join", "pass" if render.get("pdf_embedded_images") == "74" and render.get("figure_ids") == "100" else "fail", f"i0257_pdf_embedded_images={render.get('pdf_embedded_images', 'missing')}; i0257_figure_ids={render.get('figure_ids', 'missing')}", "Regenerate I-0257 or repair manifest render join."),
        row("VM-007", "source_file_missing_fail_closed", "pass" if not missing_publish_files and len(missing_source_files) == 24 else "fail", f"missing_source_files={len(missing_source_files)}; missing_publish_files={';'.join(missing_publish_files) if missing_publish_files else 'none'}", "Do not embed missing-source rows; acquire, redraw, replace, or drop them in later passes."),
        row("VM-008", "raster_uniqueness", "pass" if len(embed_hashes) == 74 and duplicate_embed_hash_count == 0 else "fail", f"embed_hashes={len(embed_hashes)}; unique_embed_hashes={len(set(embed_hashes))}; duplicate_embed_hash_count={duplicate_embed_hash_count}", "Regenerate raster cache if multiple selected figures collapse to identical PNGs."),
    ]


def row(check_id: str, category: str, result: str, evidence: str, action: str) -> dict[str, str]:
    return {
        "pass_id": PASS_ID,
        "check_id": check_id,
        "category": category,
        "result": result,
        "evidence": evidence,
        "recommended_action": action,
    }


def write_summary(rows: list[dict[str, str]], qa_rows: list[dict[str, str]]) -> None:
    counts = Counter(row["fail_closed_status"] for row in rows)
    decision_counts = Counter(row["publication_decision"] for row in rows)
    missing_source_files = sum(1 for row in rows if row["source_file_exists"] != "yes")
    lines = [
        "# I-0258 Visual Embedding Manifest",
        "",
        "Status: promoted 100-exhibit placement contract.",
        "",
        "## Result",
        "",
        f"- Manifest rows: {len(rows)} / 100",
        f"- Embed-ready after page QA: {counts.get('embed_ready_after_page_qa', 0)}",
        f"- Blocked fail-closed rows: {len(rows) - counts.get('embed_ready_after_page_qa', 0)}",
        f"- Missing source/acquisition files, all blocked: {missing_source_files}",
        f"- Publication decisions: {dict(decision_counts)}",
        f"- Raster uniqueness: {sum(1 for row in rows if row['render_embed_sha256'])} render hashes, {len(set(row['render_embed_sha256'] for row in rows if row['render_embed_sha256']))} unique",
        f"- QA rows: {len(qa_rows)} ({sum(1 for item in qa_rows if item['result'] == 'pass')} pass, {sum(1 for item in qa_rows if item['result'] == 'fail')} fail)",
        "",
        "## What The Manifest Guarantees",
        "",
        "Every selected figure ID now has a single row with its source file, caption, alt text, source note, rights stage, publication decision, render embed file where available, fallback action, claim boundary, proof gate, and fail-closed status.",
        "",
        "## Limits",
        "",
        "This does not clear the 26 unresolved slots. It makes them explicit production blockers for the next acquisition, source-card, redraw, permission, or replacement passes.",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    rows = build_rows()
    qa_rows = qa(rows)
    write_tsv(OUT_TSV, rows, FIELDS)
    write_tsv(QA_TSV, qa_rows, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_summary(rows, qa_rows)
    failures = sum(1 for item in qa_rows if item["result"] == "fail")
    print(f"rows={len(rows)} qa_fail={failures} output={OUT_TSV}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
