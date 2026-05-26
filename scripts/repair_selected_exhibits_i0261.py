from __future__ import annotations

import csv
import hashlib
import html
import textwrap
from collections import Counter
from pathlib import Path


PASS_ID = "I-0261"
ROOT = Path(__file__).resolve().parents[1]
OLD_MANIFEST = ROOT / "data" / "visual_embedding_manifest_i0258.tsv"
ASSETS_MANIFEST = ROOT / "assets_manifest.tsv"
REPAIR_TSV = ROOT / "data" / "selected_exhibit_repair_i0261.tsv"
NEW_MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
QA_TSV = ROOT / "data" / "selected_exhibit_repair_qa_i0261.tsv"
BRIEF_MD = ROOT / "manuscript" / "selected-exhibit-repair-i0261.md"
CARD_DIR = ROOT / "assets" / "visual_system" / "i0261"


EXISTING_REPLACEMENTS = {
    "F06.02": ("A-0260-004", "replace_with_source_card", "OpenAI behavior-spec source card replaces the unresolved ChatGPT product screenshot slot."),
    "F06.03": ("A-0260-001", "replace_with_source_card", "ChatGPT Plus source card replaces the unresolved Plus product-surface screenshot slot."),
    "F07.02": ("A-0208", "replace_with_existing_source_card", "Existing ChatGPT waiting-room card replaces the unresolved launch-page screenshot."),
    "F07.03": ("A-0260-001", "replace_with_source_card", "ChatGPT Plus card replaces the unresolved conversion-page screenshot."),
    "F07.04": ("A-0260-002", "replace_with_source_card", "Enterprise controls card replaces the unresolved Enterprise launch screenshot."),
    "F07.05": ("A-0260-003", "replace_with_source_card", "Release-note archaeology card replaces the unresolved plugins/tool screenshot."),
    "F09.05": ("A-0260-009", "replace_with_source_card", "Gemini product-launch card replaces the unresolved Google product screenshot."),
    "F10.04": ("A-0260-012", "replace_with_source_card", "LLaMA release card replaces the unresolved Meta launch screenshot."),
    "F10.05": ("A-0260-013", "replace_with_source_card", "Repository-infrastructure card replaces the unresolved Llama GitHub screenshot."),
    "F11.03": ("A-0260-014", "replace_with_source_card", "Qwen2 paper card replaces the unresolved Qwen2 source screenshot."),
    "F11.04": ("A-0260-015", "replace_with_source_card", "Qwen3 paper card replaces the unresolved Qwen3 source screenshot."),
    "F11.05": ("A-0260-016", "replace_with_source_card", "DeepSeek-R1 paper card replaces the unresolved DeepSeek source screenshot."),
    "F12.05": ("A-0260-017", "replace_with_source_card", "Computer-use announcement card replaces the unresolved Anthropic screenshot."),
    "F12.06": ("A-0260-018", "replace_with_source_card", "Claude product-family card replaces the unresolved Claude product screenshot."),
    "F15.06": ("A-0260-021", "replace_with_source_card", "AI-factory source-actor card replaces the local-only raw GTC slide slot."),
    "F15.07": ("A-0260-022", "replace_with_source_card", "Inference-compute roadmap card replaces the unresolved GTC source-surface slot."),
    "F16.06": ("A-0260-025", "replace_with_source_card", "DSX reference-design card replaces the unresolved data-center hall photo slot."),
    "F18.05": ("A-0260-003", "replace_with_source_card", "Release-note product archaeology card replaces the unresolved ChatGPT tool-surface screenshot."),
    "F19.05": ("A-0260-020", "replace_with_source_card", "Copilot launch-positioning card replaces the unresolved coding-surface screenshot."),
    "F20.05": ("A-0260-019", "replace_with_source_card", "Claude Code product card replaces the unresolved Claude Code screenshot."),
}


NEW_PHYSICAL_CARDS = {
    "F14.04": {
        "asset_id": "A-0261-001",
        "title": "Lithography Texture Becomes Packaging Logic",
        "chapter": "CH14",
        "source_ids": "S-0001;A-0159",
        "story": "Cut the unresolved ASML/photo placeholder and use an original advanced-packaging stack card instead.",
        "claim_boundary": "No photo, fab-access, lithography-performance, shipment, yield, or supplier-capacity claim.",
        "file": "assets/visual_system/i0261/i0261-f14-04-packaging-logic-card.svg",
    },
    "F14.05": {
        "asset_id": "A-0261-002",
        "title": "Cleanrooms Are Too Weak Without Rights",
        "chapter": "CH14",
        "source_ids": "S-0001;A-0159",
        "story": "Cut the unresolved cleanroom-photo placeholder and replace it with an original manufacturing-stack caution card.",
        "claim_boundary": "No facility, vendor, cleanliness, process-node, yield, or site-specific manufacturing claim.",
        "file": "assets/visual_system/i0261/i0261-f14-05-cleanroom-rights-card.svg",
    },
    "F14.06": {
        "asset_id": "A-0261-003",
        "title": "Racks Need Systems, Not Stock Texture",
        "chapter": "CH14",
        "source_ids": "A-0223;A-0012",
        "story": "Cut the unresolved generic rack-photo slot and replace it with an original AI-factory system-layer card.",
        "claim_boundary": "No data-center-photo, customer-deployment, installed-capacity, location, or performance claim.",
        "file": "assets/visual_system/i0261/i0261-f14-06-rack-system-card.svg",
    },
    "F16.07": {
        "asset_id": "A-0261-004",
        "title": "Interconnection Is A Queue, Not Atmosphere",
        "chapter": "CH16",
        "source_ids": "A-0156;A-0021",
        "story": "Cut the unresolved grid-photo placeholder and replace it with a transmission/interconnection process card.",
        "claim_boundary": "No project approval, utility queue total, regional capacity, or named-grid outcome claim.",
        "file": "assets/visual_system/i0261/i0261-f16-07-interconnection-queue-card.svg",
    },
    "F16.08": {
        "asset_id": "A-0261-005",
        "title": "Fast Power Is A Constraint Stack",
        "chapter": "CH16",
        "source_ids": "A-0157",
        "story": "Cut the unresolved gas-turbine photo placeholder and replace it with an original speed-to-power constraint card.",
        "claim_boundary": "No vendor, turbine order, emissions, project schedule, or guaranteed power-availability claim.",
        "file": "assets/visual_system/i0261/i0261-f16-08-speed-to-power-card.svg",
    },
    "F16.09": {
        "asset_id": "A-0261-006",
        "title": "Nuclear Texture Needs Evidence, Not Steam",
        "chapter": "CH16",
        "source_ids": "A-0023;A-0156",
        "story": "Cut the unresolved nuclear/cooling-tower photo placeholder and replace it with a clean-supply evidence card.",
        "claim_boundary": "No reactor deal, grid mix, emissions, power-purchase, site, or generation-capacity claim.",
        "file": "assets/visual_system/i0261/i0261-f16-09-clean-supply-card.svg",
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rel_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wrap(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False) or [""]


def render_physical_card(card: dict[str, str]) -> str:
    title = html.escape(card["title"])
    desc = html.escape(card["story"])
    story = "\n".join(
        f'<text class="body" x="92" y="{266 + i * 34}">{html.escape(line)}</text>'
        for i, line in enumerate(wrap(card["story"], 66)[:4])
    )
    boundary = "\n".join(
        f'<text class="small" x="92" y="{512 + i * 27}">{html.escape(line)}</text>'
        for i, line in enumerate(wrap(card["claim_boundary"], 88)[:3])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <style>
    .bg{{fill:#f5f4ee}}.ink{{fill:#1f2933}}.muted{{fill:#637083}}.band{{fill:#263238}}
    .panel{{fill:#fffefa;stroke:#d8d0c1;stroke-width:2}}.cut{{fill:#eef5f7;stroke:#336b7a;stroke-width:2}}
    .warn{{fill:#fff1ed;stroke:#c2412d;stroke-width:2}}.line{{stroke:#c7bfae;stroke-width:2}}
    .eyebrow{{font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;letter-spacing:0}}
    .title{{font-family:Arial,Helvetica,sans-serif;font-size:37px;font-weight:700}}
    .label{{font-family:Arial,Helvetica,sans-serif;font-size:20px;font-weight:700}}
    .body{{font-family:Arial,Helvetica,sans-serif;font-size:25px}}
    .small{{font-family:Arial,Helvetica,sans-serif;font-size:19px}}
    .tiny{{font-family:Arial,Helvetica,sans-serif;font-size:15px}}
  </style>
  <rect class="bg" width="1200" height="760"/>
  <rect class="band" width="1200" height="48"/>
  <text class="eyebrow" x="64" y="31" fill="#ffffff">I-0261 REPAIR CARD / {html.escape(card["chapter"])} / PHOTO PLACEHOLDER CUT</text>
  <text class="title ink" x="64" y="104">{title}</text>
  <text class="tiny muted" x="66" y="139">Replacement asset: {html.escape(card["asset_id"])} / Source IDs: {html.escape(card["source_ids"])}</text>
  <rect class="panel" x="64" y="188" width="1072" height="206" rx="8"/>
  <text class="label muted" x="92" y="234">WHY THIS REPLACES THE EMPTY SLOT</text>
  {story}
  <rect class="warn" x="64" y="454" width="1072" height="118" rx="8"/>
  <text class="label muted" x="92" y="492">BLOCKED CLAIMS</text>
  {boundary}
  <line class="line" x1="64" y1="626" x2="1136" y2="626"/>
  <text class="label muted" x="64" y="656">PUBLICATION PATH</text>
  <text class="small ink" x="64" y="688">Use this original card now; replace later only if a rights-cleared, source-noted photo is stronger.</text>
</svg>
'''


def asset_lookup() -> dict[str, dict[str, str]]:
    return {row["asset_id"]: row for row in read_tsv(ASSETS_MANIFEST)}


def append_new_assets(new_cards: list[dict[str, str]]) -> None:
    lines = ASSETS_MANIFEST.read_text(encoding="utf-8").splitlines()
    header = lines[0]
    existing = [line for line in lines[1:] if not line.startswith("A-0261-")]
    appended = []
    for card in new_cards:
        appended.append(
            "\t".join(
                [
                    card["asset_id"],
                    "available",
                    card["file"],
                    "svg_repair_source_card",
                    card["title"],
                    "local:data/selected_exhibit_repair_i0261.tsv",
                    card["chapter"],
                    "Codex",
                    "2026-05-27",
                    card["title"],
                    card["story"],
                    "Original lightweight SVG replacement card generated to cut an unresolved photo placeholder; no external raster or found photograph copied; final page/caption/source-note QA still required.",
                    "data/selected_exhibit_manifest_i0261.tsv",
                ]
            )
        )
    ASSETS_MANIFEST.write_text("\n".join([header, *existing, *appended]) + "\n", encoding="utf-8")


def update_ideas() -> None:
    path = ROOT / "ideas.tsv"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if line.startswith("I-0261\tpending\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = (
                "Done in data/selected_exhibit_manifest_i0261.tsv and data/selected_exhibit_repair_i0261.tsv; "
                "the successor 100-row exhibit manifest has 0 missing source files and 0 empty callouts by replacing "
                "20 blocked rows with existing source cards and cutting/replacing 6 photo placeholders with original repair cards."
            )
            out.append("\t".join(parts))
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in current:
        path.write_text(current.rstrip() + "\n" + text.rstrip() + "\n", encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    replacements = {
        "after pass `I-0260`": "after pass `I-0261`",
        "**Latest recorded pass:** `I-0260`, quote-safe source-card excerpt pack.": "**Latest recorded pass:** `I-0261`, selected-exhibit repair manifest.",
        "**Claims:** 269 supported / 8 needs-verification.": "**Claims:** 270 supported / 8 needs-verification.",
        "**Asset/provenance rows:** 261.": "**Asset/provenance rows:** 267.",
        "The remaining visual risk is no longer \"zero visuals\"; it is the 26 unresolved figure slots plus page-level legibility, caption, source-note, rights, and final design QA.": "The remaining visual risk is no longer \"zero visuals\" or empty selected slots; it is page-level legibility, caption/source-note quality, rights review, and final design QA.",
        "- **0** selected rows should be called publication-ready yet.": "- **0** selected rows should be called publication-ready yet.\n- **100** selected rows now have an I-0261 no-empty-callout successor manifest with existing lightweight source files.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    source_line = "- **Current source-card excerpt pack:** `data/source_card_excerpt_i0260.tsv` records 25 quote-safe SVG source cards derived from the I-0259 surfaces. Its QA ledger has 8 pass / 0 fail rows; the cards are committed as lightweight SVGs, but they still require final page placement, caption/source-note proof, and rights review before publication."
    repair_line = "- **Current selected-exhibit repair manifest:** `data/selected_exhibit_manifest_i0261.tsv` preserves exactly 100 selected figure IDs with 100 existing lightweight source files and 0 empty callouts; 26 previously blocked rows are replaced or cut/replaced in `data/selected_exhibit_repair_i0261.tsv`."
    if repair_line not in text:
        text = text.replace(source_line, source_line + "\n" + repair_line)
    text = text.replace(
        "- **Critical visual defect now narrowed:** the current visual PDF has 74 embedded raster image XObjects across 74 pages, but 26 selected figure slots remain blocked: 24 are missing source/acquisition files and 2 are local-only rows. Page-image legibility, caption compression, source-note QA, rights closure, capture/redraw/replacement, and final design remain pending.",
        "- **Critical visual defect now narrowed:** the current visual PDF has 74 embedded raster image XObjects across 74 pages; I-0261 repairs the selected-exhibit manifest to 100 existing lightweight source files, but the PDF has not yet been rerendered from that successor manifest. Page-image legibility, caption compression, source-note QA, rights closure, and final design remain pending.",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    for card in NEW_PHYSICAL_CARDS.values():
        path = ROOT / card["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_physical_card(card), encoding="utf-8")

    new_cards = list(NEW_PHYSICAL_CARDS.values())
    append_new_assets(new_cards)
    assets = asset_lookup()

    old_rows = read_tsv(OLD_MANIFEST)
    repair_rows: list[dict[str, str]] = []
    new_rows: list[dict[str, str]] = []
    for old in old_rows:
        fig = old["figure_id"]
        new = dict(old)
        new["pass_id"] = PASS_ID
        new["previous_manifest_status"] = old["manifest_status"]
        new["previous_fail_closed_status"] = old["fail_closed_status"]
        if fig in EXISTING_REPLACEMENTS:
            replacement_id, action, reason = EXISTING_REPLACEMENTS[fig]
        elif fig in NEW_PHYSICAL_CARDS:
            card = NEW_PHYSICAL_CARDS[fig]
            replacement_id, action, reason = card["asset_id"], "cut_photo_placeholder_replace_with_original_card", card["story"]
        else:
            replacement_id, action, reason = old["asset_id"], "keep_existing_embed_ready_asset", "Existing source file already embeds or is ready after page QA."

        replacement_asset = assets[replacement_id]
        source_file = replacement_asset["file_path"]
        source_path = ROOT / source_file
        source_exists = source_path.exists()
        new.update(
            {
                "asset_id": replacement_id,
                "asset_type": replacement_asset["asset_type"],
                "figure_title": replacement_asset["caption"] or old["figure_title"],
                "source_note": f"Source IDs: {replacement_asset['source_page_or_time']}; Asset source: {replacement_asset['source_title']}; Creator/org: {replacement_asset['creator_or_org']}",
                "source_ids": replacement_asset["source_page_or_time"] or old["source_ids"],
                "rights_status": "available_lightweight_replacement" if action != "keep_existing_embed_ready_asset" else old["rights_status"],
                "rights_stage": "publish_after_render_caption_source_note_qa",
                "publication_decision": "publish_after_repair_render_qa",
                "manifest_status": "available",
                "source_file": source_file,
                "source_file_exists": "yes" if source_exists else "no",
                "source_sha256": sha256(source_path) if source_exists else "",
                "render_embed_file": "",
                "render_embed_file_exists": "no",
                "render_embed_sha256": "",
                "i0257_render_status": "needs_i0262_render",
                "fallback_action": "Render the I-0261 replacement asset in the next full-book visual PDF; keep source-note and blocker nearby.",
                "claim_boundary": replacement_asset["rights_or_private_use_note"] if action != "keep_existing_embed_ready_asset" else old["claim_boundary"],
                "proof_gate": "I-0261 source-file proof exists; I-0262 render embedding and I-0263 page-legibility QA still required.",
                "fail_closed_status": "no_empty_callout_ready_for_i0262_render" if source_exists else "blocked_missing_replacement_file",
                "i0261_repair_action": action,
                "i0261_replacement_reason": reason,
                "i0261_previous_asset_id": old["asset_id"],
                "i0261_replacement_asset_id": replacement_id,
            }
        )
        new_rows.append(new)
        if action != "keep_existing_embed_ready_asset":
            repair_rows.append(
                {
                    "pass_id": PASS_ID,
                    "figure_id": fig,
                    "chapter": old["chapter"],
                    "old_asset_id": old["asset_id"],
                    "old_asset_type": old["asset_type"],
                    "old_fail_closed_status": old["fail_closed_status"],
                    "repair_action": action,
                    "new_asset_id": replacement_id,
                    "new_asset_type": replacement_asset["asset_type"],
                    "new_source_file": source_file,
                    "new_source_file_exists": "yes" if source_exists else "no",
                    "replacement_reason": reason,
                    "claim_boundary": new["claim_boundary"],
                    "next_gate": "I-0262 full-book render must embed this file; I-0263 must inspect page legibility.",
                }
            )

    fields = list(new_rows[0].keys())
    write_tsv(NEW_MANIFEST, new_rows, fields)
    write_tsv(
        REPAIR_TSV,
        repair_rows,
        [
            "pass_id",
            "figure_id",
            "chapter",
            "old_asset_id",
            "old_asset_type",
            "old_fail_closed_status",
            "repair_action",
            "new_asset_id",
            "new_asset_type",
            "new_source_file",
            "new_source_file_exists",
            "replacement_reason",
            "claim_boundary",
            "next_gate",
        ],
    )

    qa_rows = []
    def qa(check_id: str, check: str, ok: bool, detail: str) -> None:
        qa_rows.append({"check_id": check_id, "check": check, "status": "pass" if ok else "fail", "detail": detail})

    unique_figure_count = len({r["figure_id"] for r in new_rows})
    qa("I0261-QA-001", "selected_row_count", len(new_rows) == 100, f"{len(new_rows)} selected rows")
    qa("I0261-QA-002", "unique_figure_ids", unique_figure_count == 100, f"{unique_figure_count}/100 unique figure IDs")
    qa("I0261-QA-003", "repair_row_count", len(repair_rows) == 26, f"{len(repair_rows)} repaired/cut rows")
    missing = [r["figure_id"] for r in new_rows if r["source_file_exists"] != "yes"]
    qa("I0261-QA-004", "no_missing_source_files", not missing, f"missing={missing}")
    empty = [r["figure_id"] for r in new_rows if r["fail_closed_status"] == "blocked_missing_replacement_file"]
    qa("I0261-QA-005", "no_empty_callouts", not empty, f"blocked={empty}")
    action_counts = Counter(r["repair_action"] for r in repair_rows)
    qa("I0261-QA-006", "repair_action_mix", action_counts["replace_with_source_card"] + action_counts["replace_with_existing_source_card"] == 20 and action_counts["cut_photo_placeholder_replace_with_original_card"] == 6, f"actions={dict(action_counts)}")
    new_asset_missing = [card["asset_id"] for card in new_cards if card["asset_id"] not in assets]
    qa("I0261-QA-007", "new_assets_manifested", not new_asset_missing, f"new_asset_missing={new_asset_missing}")
    non_render_ready = [r["figure_id"] for r in new_rows if r["i0257_render_status"] != "needs_i0262_render"]
    qa("I0261-QA-008", "successor_manifest_targets_next_render", not non_render_ready, "all rows marked needs_i0262_render")
    write_tsv(QA_TSV, qa_rows, ["check_id", "check", "status", "detail"])

    if any(r["status"] != "pass" for r in qa_rows):
        raise SystemExit("I-0261 QA failed")

    BRIEF_MD.write_text(
        f"""# I-0261 Selected-Exhibit Repair Manifest

Pass I-0261 repairs the selected 100-exhibit program after I-0258/I-0260.

- Successor selected-exhibit rows: {len(new_rows)}
- Repaired/cut rows: {len(repair_rows)}
- Existing source-card replacements: {action_counts['replace_with_source_card'] + action_counts['replace_with_existing_source_card']}
- Photo placeholders cut and replaced with original repair cards: {action_counts['cut_photo_placeholder_replace_with_original_card']}
- Missing source files in successor manifest: {len(missing)}
- QA: {Counter(r['status'] for r in qa_rows)['pass']} pass / {Counter(r['status'] for r in qa_rows)['fail']} fail

This pass does not claim final rights clearance or page beauty. It closes the narrower production defect from I-0258: selected exhibit rows no longer point to missing screenshot/photo/source-surface files. The next render pass should use `data/selected_exhibit_manifest_i0261.tsv` as the visual input so every selected figure ID can resolve to an existing lightweight source file.
""",
        encoding="utf-8",
    )

    update_ideas()
    update_readme()
    append_once(
        ROOT / "claims.tsv",
        "C-0278\t",
        "C-0278\tsupported\tPass I-0261 created a successor 100-row selected-exhibit manifest with 0 missing source files and 0 empty callouts by replacing 20 previously blocked screenshot/source-surface/local-only rows with existing source cards and cutting/replacing 6 unresolved photo placeholders with original lightweight repair cards; QA passed 8/8 checks.\tscripts/repair_selected_exhibits_i0261.py;data/selected_exhibit_manifest_i0261.tsv;data/selected_exhibit_repair_i0261.tsv;data/selected_exhibit_repair_qa_i0261.tsv;manuscript/selected-exhibit-repair-i0261.md;assets/visual_system/i0261/;assets_manifest.tsv\tI-0261;F01.01-F24.04;A-0261-001-A-0261-006\tselected-exhibit repair manifest\t2026-05-27\tSupported as no-empty-callout manifest repair only; it does not prove final page legibility, final captions, final source-note proximity, legal publication rights, or an updated rendered PDF until I-0262/I-0263 rerender and inspect the book.",
    )
    append_once(
        ROOT / "scoreboard.tsv",
        "pass-0261\t",
        "2026-05-27T00:03:00+02:00\tpass-0261\tchampion selected-exhibit repair manifest\tI-0261\tvisual repair\t+1.0\t100.0\t102196\t24\t142\t78\t299\t270 supported / 8 needs-verification; successor 100-exhibit manifest has 100/100 existing source files, 26 repaired/cut rows, 20 source-card replacements, 6 photo-placeholder cuts, and 8/8 QA pass\t+1\tFull-book visual PDF has not yet been rerendered from I-0261, final page legibility and caption/source-note QA remain pending, and no legal publication clearance is implied\tpromoted\tConverted all selected blocked visual slots into existing lightweight replacement files while preserving exactly 100 selected figure IDs and fail-closing rights/page-proof gates for the next render.\tone selected-exhibit repair pass",
    )
    append_once(
        ROOT / "insights.md",
        "## 2026-05-27 - I-0261 Empty Slots",
        """
## 2026-05-27 - I-0261 Empty Slots

A selected exhibit list should never point at a missing future asset. If a screenshot or photo is not rights-ready, the honest repair is to cut it or replace it with a source card/diagram now, then let a later rights pass upgrade it only if the stronger asset clears.
""",
    )
    print(f"I-0261 complete: {len(new_rows)} selected rows, {len(repair_rows)} repaired rows, QA pass.")


if __name__ == "__main__":
    main()
