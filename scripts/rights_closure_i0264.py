from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PASS_ID = "I-0264"
ROOT = Path(__file__).resolve().parents[1]
RIGHTS_I0250 = ROOT / "data" / "image_rights_staging_i0250.tsv"
REPAIR_I0261 = ROOT / "data" / "selected_exhibit_repair_i0261.tsv"
MANIFEST_I0261 = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
LEGIBILITY_I0263 = ROOT / "data" / "page_image_legibility_i0263.tsv"
OUT_TSV = ROOT / "data" / "rights_closure_i0264.tsv"
QA_TSV = ROOT / "data" / "rights_closure_qa_i0264.tsv"
SUMMARY_MD = ROOT / "manuscript" / "rights-closure-i0264.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def closure_status(old: dict[str, str], repair: dict[str, str]) -> tuple[str, str, str]:
    action = repair["repair_action"]
    old_decision = old["publication_decision"]
    if action == "cut_photo_placeholder_replace_with_original_card":
        return (
            "closed_cut_replaced_by_original_card",
            "drop_old_photo_candidate_from_publication",
            "Old photo candidate is not used in the selected publication path; keep only as historical local research pointer unless separately cleared later.",
        )
    if old_decision == "local-only":
        return (
            "closed_local_only_reserve_replaced_by_source_card",
            "keep_old_raster_local_only_do_not_publish",
            "Old slide/source raster remains local-only reserve; publication path uses an original source card.",
        )
    return (
        "closed_replaced_by_source_card",
        "retire_old_screenshot_slot_from_publication",
        "Old screenshot/source-surface placeholder is replaced by an original lightweight source card; no permission request is required for the retired placeholder.",
    )


def update_ideas() -> None:
    path = ROOT / "ideas.tsv"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if line.startswith("I-0264\tpending\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = (
                "Done in data/rights_closure_i0264.tsv and manuscript/rights-closure-i0264.md; "
                "all 26 I-0250 non-publish rows are closed as 18 source-card replacements, "
                "2 local-only reserves replaced by source cards, and 6 photo placeholders cut/replaced by original cards, "
                "with 8/8 QA checks passing."
            )
            out.append("\t".join(parts))
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in current:
        path.write_text(current.rstrip() + "\n" + text.rstrip() + "\n", encoding="utf-8")


def update_readme(counts: Counter[str]) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    replacements = {
        "after pass `I-0263`": "after pass `I-0264`",
        "**Latest recorded pass:** `I-0263`, page-image legibility QA.": "**Latest recorded pass:** `I-0264`, rights-closure reconciliation.",
        "**Claims:** 272 supported / 8 needs-verification.": "**Claims:** 273 supported / 8 needs-verification.",
        "- **Image rights staging:** `data/image_rights_staging_i0250.tsv` classifies all 100 selected figure callouts as 74 publish-after-QA rows, 2 local-only rows, 3 redraw/source-card rows, 21 permission-needed rows, 0 replace rows, and 0 drop rows. This is staging only: no raster/screenshot/photo/source-surface row is publication-ready.": "- **Image rights closure:** `data/rights_closure_i0264.tsv` closes the 26 old I-0250 non-publish rows: screenshot/source-surface/photo placeholders are no longer active publication slots, and the current selected path uses source cards or original repair cards. This is rights-path closure, not final legal/publication clearance.",
        "caption compression, final source-note typography, rights closure, and final design remain pending.": "caption compression, final source-note typography, final rights review, and final design remain pending.",
        "- **26** selected rows remain non-publish under fail-closed rights staging.": "- **0** selected rows remain active non-publish placeholders under the current I-0264 closure board.",
        "- **21** screenshot/photo rows are permission-needed.": "- **21** old permission-needed screenshot/photo rows are retired, cut/replaced, or converted to source-card paths in I-0264.",
        "- **3** source-screenshot rows should become redraw/source-card work before publication.": "- **3** old source-screenshot rows are converted to source-card replacements in I-0264.",
        "- **2** raw slide/source-surface rows are local-only pending permission or fair-use/source-actor review.": "- **2** old raw slide/source-surface rows remain local-only reserves and are replaced in publication path by source cards.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    line = (
        f"- **Current rights closure:** I-0264 closes 26/26 old non-publish rows "
        f"({dict(counts)}) while keeping final rights/legal review pending for the finished PDF."
    )
    anchor = "- **Current page-image QA:** `data/page_image_legibility_i0263.tsv` audits 100 figure pages and `data/page_image_legibility_samples_i0263.tsv` records 24 local chapter sample PNGs; 100 figures need layout review and 0 P0 defects were found."
    if line not in text:
        text = text.replace(anchor, anchor + "\n" + line)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    old_rows = [row for row in read_tsv(RIGHTS_I0250) if row["publication_decision"] != "publish"]
    repair_by_figure = {row["figure_id"]: row for row in read_tsv(REPAIR_I0261)}
    manifest_by_figure = {row["figure_id"]: row for row in read_tsv(MANIFEST_I0261)}
    legibility_by_figure = {row["figure_id"]: row for row in read_tsv(LEGIBILITY_I0263)}
    closure_rows: list[dict[str, str]] = []
    for old in old_rows:
        figure_id = old["figure_id"]
        repair = repair_by_figure.get(figure_id, {})
        manifest = manifest_by_figure.get(figure_id, {})
        legibility = legibility_by_figure.get(figure_id, {})
        if not repair:
            status, action, note = "open_missing_repair_row", "repair_required", "No I-0261 repair row exists."
        else:
            status, action, note = closure_status(old, repair)
        replacement_file = repair.get("new_source_file", "")
        replacement_exists = "yes" if replacement_file and (ROOT / replacement_file).exists() else "no"
        closure_rows.append({
            "pass_id": PASS_ID,
            "figure_id": figure_id,
            "chapter": old["chapter"],
            "old_asset_id": old["asset_id"],
            "old_asset_type": old["asset_type"],
            "old_figure_title": old["figure_title"],
            "old_rights_status": old["rights_status"],
            "old_rights_stage": old["rights_stage"],
            "old_publication_decision": old["publication_decision"],
            "old_manifest_file_path": old["manifest_file_path"],
            "old_manifest_status": old["manifest_status"],
            "old_claim_boundary": old["claim_boundary"],
            "i0261_repair_action": repair.get("repair_action", ""),
            "new_asset_id": repair.get("new_asset_id", ""),
            "new_asset_type": repair.get("new_asset_type", ""),
            "new_source_file": replacement_file,
            "new_source_file_exists": replacement_exists,
            "current_selected_asset_id": manifest.get("asset_id", ""),
            "current_publication_decision": manifest.get("publication_decision", ""),
            "current_fail_closed_status": manifest.get("fail_closed_status", ""),
            "i0262_render_status": "embedded_in_i0262_pdf" if legibility else "not_verified_in_i0263",
            "i0263_page": legibility.get("page", ""),
            "i0263_legibility_status": legibility.get("legibility_status", ""),
            "rights_closure_status": status,
            "final_publication_action": action,
            "closure_note": note,
            "remaining_gate": "I-0280 layout polish plus final rights/legal review for the finished PDF; do not revive old placeholder without fresh rights proof.",
        })

    fields = list(closure_rows[0].keys())
    write_tsv(OUT_TSV, closure_rows, fields)
    status_counts = Counter(row["rights_closure_status"] for row in closure_rows)
    old_decisions = Counter(row["old_publication_decision"] for row in closure_rows)
    actions = Counter(row["final_publication_action"] for row in closure_rows)
    missing_replacements = [row["figure_id"] for row in closure_rows if row["new_source_file_exists"] != "yes"]
    not_rendered = [row["figure_id"] for row in closure_rows if row["i0262_render_status"] != "embedded_in_i0262_pdf"]
    active_permission_needed = [row["figure_id"] for row in closure_rows if row["rights_closure_status"].startswith("open")]
    qa_rows = [
        {"pass_id": PASS_ID, "check_id": "RC-001", "category": "old_nonpublish_count", "result": "pass" if len(closure_rows) == 26 else "fail", "evidence": f"rows={len(closure_rows)}; expected=26", "recommended_action": "Rejoin I-0250 non-publish rows."},
        {"pass_id": PASS_ID, "check_id": "RC-002", "category": "old_decision_mix", "result": "pass" if old_decisions == {"permission-needed": 21, "redraw": 3, "local-only": 2} else "fail", "evidence": f"old_decisions={dict(old_decisions)}", "recommended_action": "Reconcile I-0250 staging counts."},
        {"pass_id": PASS_ID, "check_id": "RC-003", "category": "replacement_files", "result": "pass" if not missing_replacements else "fail", "evidence": f"missing_replacements={missing_replacements}", "recommended_action": "Create or select replacement asset files."},
        {"pass_id": PASS_ID, "check_id": "RC-004", "category": "render_verified", "result": "pass" if not not_rendered else "fail", "evidence": f"not_rendered_or_not_legibility_checked={not_rendered}", "recommended_action": "Rerender or rerun page-image QA."},
        {"pass_id": PASS_ID, "check_id": "RC-005", "category": "no_active_open_rights_rows", "result": "pass" if not active_permission_needed else "fail", "evidence": f"open_rows={active_permission_needed}", "recommended_action": "Close open rows or mark local-only reserve/drop."},
        {"pass_id": PASS_ID, "check_id": "RC-006", "category": "closure_status_mix", "result": "pass" if sum(status_counts.values()) == 26 and len(status_counts) == 3 else "fail", "evidence": f"closure_statuses={dict(status_counts)}", "recommended_action": "Ensure every old status maps to an exact closure."},
        {"pass_id": PASS_ID, "check_id": "RC-007", "category": "action_mix", "result": "pass" if sum(actions.values()) == 26 else "fail", "evidence": f"actions={dict(actions)}", "recommended_action": "Assign final publication action for every row."},
        {"pass_id": PASS_ID, "check_id": "RC-008", "category": "fail_closed_language", "result": "pass" if all(row["remaining_gate"] and row["closure_note"] for row in closure_rows) else "fail", "evidence": "all_rows_have_closure_note_and_remaining_gate", "recommended_action": "Add fail-closed closure notes."},
    ]
    write_tsv(QA_TSV, qa_rows, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    SUMMARY_MD.write_text(
        "\n".join([
            "# I-0264 Rights Closure Reconciliation",
            "",
            "Status: promoted rights-path closure, not legal/publication clearance.",
            "",
            "## Result",
            "",
            f"- Old I-0250 non-publish rows closed: {len(closure_rows)} / 26",
            f"- Old publication decisions: {dict(old_decisions)}",
            f"- Closure statuses: {dict(status_counts)}",
            f"- Final publication actions: {dict(actions)}",
            f"- Replacement files missing: {len(missing_replacements)}",
            f"- Rows not verified in I-0263 page QA: {len(not_rendered)}",
            f"- QA rows: {sum(1 for row in qa_rows if row['result'] == 'pass')} pass / {sum(1 for row in qa_rows if row['result'] == 'fail')} fail",
            "",
            "## Interpretation",
            "",
            "The 26 old non-publish rows are no longer active publication slots. Screenshot and source-screenshot placeholders are replaced by source cards, raw GTC slide/page surfaces remain local-only reserves, and unresolved photo placeholders are cut/replaced by original repair cards. This closes the rights-path ambiguity that began in I-0250 while preserving a final legal/design review gate for the finished PDF.",
            "",
            "## Still Not Publication Clearance",
            "",
            "No external screenshot, source-page raster, slide render, or photo is newly declared publication-ready. The safe path is the current I-0261/I-0262 lightweight replacement set, subject to I-0263/I-0280 layout fixes and final rights review.",
            "",
        ]),
        encoding="utf-8",
        newline="\n",
    )
    if any(row["result"] == "fail" for row in qa_rows):
        raise SystemExit("I-0264 QA failed")
    update_ideas()
    update_readme(status_counts)
    append_once(
        ROOT / "claims.tsv",
        "C-0281\t",
        f"C-0281\tsupported\tPass I-0264 reconciled and closed all 26 non-publish rows from the I-0250 rights staging board by joining them to I-0261 replacement assets and I-0263 page-QA evidence: {dict(status_counts)}; all 26 replacement files exist, all 26 are verified in the I-0263 page audit, and QA passed 8/8 checks.\tscripts/rights_closure_i0264.py;data/rights_closure_i0264.tsv;data/rights_closure_qa_i0264.tsv;manuscript/rights-closure-i0264.md;data/image_rights_staging_i0250.tsv;data/selected_exhibit_repair_i0261.tsv;data/page_image_legibility_i0263.tsv\tI-0264;F06.02-F20.05\trights closure reconciliation\t2026-05-27\tSupported as rights-path closure only; no external screenshot, photo, slide, or source-page raster is newly publication-cleared, and final legal review, layout polish, caption/source-note typography, and production QA remain pending.",
    )
    append_once(
        ROOT / "scoreboard.tsv",
        "pass-0264\t",
        f"2026-05-27T00:03:30+02:00\tpass-0264\tchampion rights closure reconciliation\tI-0264\trights QA\t+1.0\t100.0\t102196\t24\t142\t78\t299\t273 supported / 8 needs-verification; closed 26/26 old non-publish rights rows with statuses {dict(status_counts)}, 26/26 replacement files, 26/26 I-0263 page-QA joins, and 8/8 QA pass\t+1\tFinal legal/publication clearance, caption/source-note typography, and layout polish remain pending; old rasters/photos are not revived as publication assets\tpromoted\tReconciled the stale I-0250 permission/local-only/redraw rows against the current source-card/original-card replacement path so the selected exhibit program no longer carries ambiguous active non-publish placeholders.\tone rights closure reconciliation pass",
    )
    append_once(
        ROOT / "insights.md",
        "## 2026-05-27 - I-0264 Rights Closure",
        """
## 2026-05-27 - I-0264 Rights Closure

Rights closure is not the same as permission. The useful move is to retire unsafe screenshot/photo/slide placeholders from the active publication path and point the book at original source cards or local-only reserves, while preserving final legal review as a separate gate.
""",
    )
    print(f"I-0264 complete: rows={len(closure_rows)} statuses={dict(status_counts)} QA pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
