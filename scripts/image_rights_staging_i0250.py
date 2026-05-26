from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PASS_ID = "I-0250"
ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "data" / "full_book_figure_list_i0229.tsv"
REAL_WORLD = ROOT / "data" / "real_world_image_placement_i0243.tsv"
MANIFEST = ROOT / "assets_manifest.tsv"
OUT_TSV = ROOT / "data" / "image_rights_staging_i0250.tsv"
SUMMARY_TSV = ROOT / "data" / "image_rights_staging_summary_i0250.tsv"
BRIEF_MD = ROOT / "manuscript" / "image-rights-staging-i0250.md"


FIELDS = [
    "pass_id",
    "figure_id",
    "chapter",
    "asset_id",
    "asset_type",
    "figure_title",
    "rights_status",
    "rights_stage",
    "publication_decision",
    "replacement_path",
    "required_next_action",
    "source_ids",
    "manifest_file_path",
    "manifest_status",
    "real_world_candidate",
    "claim_boundary",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_manifest() -> dict[str, dict[str, str]]:
    return {row["asset_id"]: row for row in read_tsv(MANIFEST)}


def load_real_world() -> set[str]:
    if not REAL_WORLD.exists():
        return set()
    return {row["figure_id"] for row in read_tsv(REAL_WORLD)}


def classify(row: dict[str, str], manifest_status: str) -> tuple[str, str, str, str, str]:
    asset_type = row["asset_type"]
    rights_status = row["rights_status"]
    figure_id = row["figure_id"]
    asset_id = row["asset_id"]

    if rights_status == "ready_svg":
        return (
            "publish",
            "publish_after_render_caption_source_note_qa",
            "Keep current original SVG/lightweight chart; no external raster rights path required.",
            "Render-proof at final size, compress any long caption, keep source IDs and blocked-claim note adjacent.",
            "Original workspace visual may support only its scoped data/mechanism claim; no outcome, rank, productivity, safety, or market conclusion without matching evidence.",
        )

    if rights_status == "local_ignored_hash_available":
        replacement = "Use nearby original SVG claim card/redraw as publication path; keep raw slide/source render as private-use verification texture."
        if figure_id == "F15.06":
            replacement = "Prefer A-0024/A-0027/A-0028/A-0029 SVG claim-card family for publication; keep GTC slide raster local-only unless permission/fair-use review clears it."
        if figure_id == "F15.07":
            replacement = "Treat as local-only source surface; replace in publication with a cropped, attributed source-card redraw unless permission/fair-use review clears the page render."
        return (
            "local-only",
            "local_only_until_permission_or_fair_use_review",
            replacement,
            "Do not ship raster/page render yet; record page crop, attribution, legibility, and source-actor review before any publication use.",
            "Raw source surfaces support source texture and attribution only; vendor stagecraft, roadmap, performance, and future-availability claims remain bounded.",
        )

    if asset_type == "source_screenshot_slot":
        return (
            "redraw",
            "redraw_or_source_card_before_publication",
            "Replace source-page screenshot with a house-style source card or paper/report first-page excerpt card after page-anchor proof.",
            "Capture or verify source page locally, extract page/title metadata, then build an original source-card/redraw with quote limits and attribution.",
            "Source-page visuals may prove provenance and chronology only; they do not authorize benchmark, superiority, adoption, safety, or company-result claims.",
        )

    if asset_type == "photo_candidate_slot":
        return (
            "permission-needed",
            "photo_rights_review_required",
            "Use only if license/credit/permission is verified; otherwise replace with public-domain/Wikimedia/company-permitted image or an original infrastructure diagram.",
            "Resolve creator, license, credit line, publication permission, and exact file hash before layout; cut or replace if any link is ambiguous.",
            "Photos provide physical texture only; they do not prove AI workload, site capacity, fuel mix, exact GPU inventory, or deployment outcomes.",
        )

    if asset_type == "screenshot_slot":
        return (
            "permission-needed",
            "screenshot_capture_and_use_review_required",
            "Capture official source surface with date/provenance, then choose fair-use/local-only/permission path; if unresolved, replace with a self-made facsimile or source-card redraw.",
            "Capture viewport, URL, access date, account/private-data state, crop, hash, rights note, attribution, and blocker language before publication layout.",
            "Product screenshots may show interface/source texture only; they do not prove current UI, endorsement, adoption, revenue, productivity, safety, or market impact.",
        )

    return (
        "replace",
        "unclassified_replace_by_default",
        "Replace with an original SVG, source card, or permission-cleared image because this asset type lacks a safe publication route.",
        "Create a new rights-safe asset or remove the figure from the selected list.",
        "No unsupported claim may rely on an unclassified visual.",
    )


def build_rows() -> list[dict[str, str]]:
    manifest = load_manifest()
    real_world = load_real_world()
    rows: list[dict[str, str]] = []
    for row in read_tsv(FIGURES):
        manifest_row = manifest.get(row["asset_id"], {})
        decision, stage, replacement, action, boundary = classify(row, manifest_row.get("status", "missing_manifest_row"))
        rows.append(
            {
                "pass_id": PASS_ID,
                "figure_id": row["figure_id"],
                "chapter": row["chapter"],
                "asset_id": row["asset_id"],
                "asset_type": row["asset_type"],
                "figure_title": row["figure_title"],
                "rights_status": row["rights_status"],
                "rights_stage": stage,
                "publication_decision": decision,
                "replacement_path": replacement,
                "required_next_action": action,
                "source_ids": row["source_ids"],
                "manifest_file_path": row["manifest_file_path"],
                "manifest_status": manifest_row.get("status", "missing_manifest_row"),
                "real_world_candidate": "yes" if row["figure_id"] in real_world else "no",
                "claim_boundary": boundary,
            }
        )
    return rows


def write_brief(rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    decision_counts = Counter(row["publication_decision"] for row in rows)
    lines = [
        "# I-0250 Image Rights Staging",
        "",
        "Status: promoted rights-staging board, not legal clearance.",
        "",
        "## Result",
        "",
        f"- Figure callouts classified: {len(rows)}",
        f"- Publish path rows: {decision_counts.get('publish', 0)}",
        f"- Local-only rows: {decision_counts.get('local-only', 0)}",
        f"- Redraw rows: {decision_counts.get('redraw', 0)}",
        f"- Permission-needed rows: {decision_counts.get('permission-needed', 0)}",
        f"- Replace rows: {decision_counts.get('replace', 0)}",
        f"- Drop rows: {decision_counts.get('drop', 0)}",
        "",
        "## Decision Rule",
        "",
        "Original SVG/chart/card assets are staged as `publish` only after render, caption, and source-note QA. Raw slide/page renders are `local-only`. Source screenshots should become source cards or redraws. Product screenshots and photos remain `permission-needed` until capture, license, attribution, and blocker gates close.",
        "",
        "## Deliverables",
        "",
        "- `data/image_rights_staging_i0250.tsv` - one row per selected figure callout.",
        "- `data/image_rights_staging_summary_i0250.tsv` - count summary and unresolved-risk totals.",
        "",
        "## Next",
        "",
        "Work the permission-needed rows first if the book needs real-world texture, or convert the redraw rows into original source cards if publication risk needs to fall fastest.",
        "",
    ]
    BRIEF_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    rows = build_rows()
    if len(rows) != 100:
        raise RuntimeError(f"Expected 100 selected figure rows, found {len(rows)}")
    decisions = Counter(row["publication_decision"] for row in rows)
    stages = Counter(row["rights_stage"] for row in rows)
    high_risk = sum(1 for row in rows if row["publication_decision"] != "publish")
    real_world_high_risk = sum(1 for row in rows if row["real_world_candidate"] == "yes" and row["publication_decision"] != "publish")
    summary = {
        "pass_id": PASS_ID,
        "figure_rows": str(len(rows)),
        "publish": str(decisions.get("publish", 0)),
        "local_only": str(decisions.get("local-only", 0)),
        "redraw": str(decisions.get("redraw", 0)),
        "permission_needed": str(decisions.get("permission-needed", 0)),
        "replace": str(decisions.get("replace", 0)),
        "drop": str(decisions.get("drop", 0)),
        "non_publish_rows": str(high_risk),
        "real_world_candidates_non_publish": str(real_world_high_risk),
        "stage_families": ";".join(f"{name}={count}" for name, count in sorted(stages.items())),
        "status": "full_selected_figure_rights_staged_fail_closed",
    }
    write_tsv(OUT_TSV, rows, FIELDS)
    write_tsv(SUMMARY_TSV, [summary], list(summary.keys()))
    write_brief(rows, summary)
    print(
        "figures={figure_rows} publish={publish} local_only={local_only} redraw={redraw} "
        "permission_needed={permission_needed} replace={replace} drop={drop}".format(**summary)
    )


if __name__ == "__main__":
    main()
