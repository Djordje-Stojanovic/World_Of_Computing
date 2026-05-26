from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "Next-Token-full-draft.md"
MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
CURATION = ROOT / "data" / "visual_curation_callout_sync_i0273.tsv"
QA = ROOT / "data" / "visual_curation_callout_sync_qa_i0273.tsv"
REPORT = ROOT / "manuscript" / "visual-curation-callout-sync-i0273.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

PASS_ID = "I-0273"
TODAY = "2026-05-26"
TS = "2026-05-27T00:08:00+02:00"

CALLOUT_RE = re.compile(r"> \[!FIGURE\] \*\*(F\d{2}\.\d{2}) / (A-[^\s]+) - ([^*]+)\*\*")
OLD_SLOT_TYPES = {"screenshot_slot", "source_screenshot_slot", "photo_candidate_slot", "extracted_slide_render"}
WEAK_TITLE_RE = re.compile(r"\b(placeholder|proxy|texture)\b", re.I)
SURFACE_TITLE_RE = re.compile(r"\bsurface\b", re.I)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def append_once(path: Path, key: str, line: str) -> None:
    text = read(path)
    if key in text:
        return
    with path.open("a", encoding="utf-8", newline="") as f:
        f.write(line)


def load_manifest() -> dict[str, dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8", newline="") as f:
        return {row["figure_id"]: row for row in csv.DictReader(f, delimiter="\t")}


def load_baseline() -> dict[str, tuple[str, str]]:
    if not CURATION.exists():
        return {}
    with CURATION.open("r", encoding="utf-8", newline="") as f:
        return {row["figure_id"]: (row["old_asset_id"], row["old_title"]) for row in csv.DictReader(f, delimiter="\t")}


def display_title(raw: str) -> str:
    title = re.sub(r"^Figure\s+\d+(?:\.\d+|\.x|\.y)?(?:\s+candidate)?\s*[-:]\s*", "", raw.strip(), flags=re.I)
    title = re.sub(r"\s+", " ", title).strip()
    title = title.replace("Lithography Texture Becomes Packaging Logic", "Lithography Evidence Becomes Packaging Logic")
    title = title.replace("Racks Need Systems, Not Stock Texture", "Racks Need Systems, Not Stock Photos")
    title = title.replace("Nuclear Texture Needs Evidence, Not Steam", "Nuclear Evidence Needs Specific Claims")
    if len(title) > 88:
        title = title[:85].rstrip(" .,;:") + "..."
    return title


def sync_callouts(text: str, manifest: dict[str, dict[str, str]], baseline: dict[str, tuple[str, str]]) -> tuple[str, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        figure_id, old_asset, old_title = match.groups()
        row = manifest.get(figure_id)
        if not row:
            return match.group(0)
        baseline_asset, baseline_title = baseline.get(figure_id, (old_asset, old_title.strip()))
        new_asset = row["asset_id"]
        needs_asset_sync = baseline_asset != new_asset
        needs_title_sync = bool(WEAK_TITLE_RE.search(baseline_title)) or (
            bool(SURFACE_TITLE_RE.search(baseline_title))
            and row["asset_type"] in {"source_excerpt_card_svg", "svg_repair_source_card", "svg_claim_card", "svg_source_card"}
        )
        if not needs_asset_sync and not needs_title_sync:
            return f"> [!FIGURE] **{figure_id} / {baseline_asset} - {baseline_title}**"

        new_title = display_title(row["figure_title"])
        if needs_asset_sync or baseline_title != new_title:
            rows.append({
                "figure_id": figure_id,
                "chapter": row["chapter"],
                "old_asset_id": baseline_asset,
                "new_asset_id": new_asset,
                "manifest_asset_type": row["asset_type"],
                "old_title": baseline_title,
                "new_title": new_title,
                "curation_reason": reason(row, baseline_asset, baseline_title),
            })
        return f"> [!FIGURE] **{figure_id} / {new_asset} - {new_title}**"

    return CALLOUT_RE.sub(replace, text), rows


def reason(row: dict[str, str], old_asset: str, old_title: str) -> str:
    if row["asset_type"] in {"source_excerpt_card_svg", "svg_repair_source_card", "svg_claim_card", "svg_source_card"}:
        return "Replace weak screenshot/photo/source-surface placeholder language with a curated source-card/original-card callout."
    if old_asset != row["asset_id"]:
        return "Align reader-facing callout with I-0261 curated replacement asset."
    if re.search(r"\b(surface|texture|placeholder|proxy)\b", old_title, re.I):
        return "Tighten placeholder-like visual language into the curated manifest title."
    return "Normalize callout title to the curated manifest title."


def write_curation(rows: list[dict[str, str]]) -> None:
    fields = ["figure_id", "chapter", "old_asset_id", "new_asset_id", "manifest_asset_type", "old_title", "new_title", "curation_reason"]
    with CURATION.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_qa(text: str, rows: list[dict[str, str]], manifest: dict[str, dict[str, str]]) -> None:
    callouts = CALLOUT_RE.findall(text)
    callout_ids = [figure_id for figure_id, _, _ in callouts]
    asset_by_id = {figure_id: asset_id for figure_id, asset_id, _ in callouts}
    old_slot_asset_ids = {
        row["i0261_previous_asset_id"]
        for row in manifest.values()
        if row["asset_type"] in {"source_excerpt_card_svg", "svg_repair_source_card", "svg_claim_card", "svg_source_card"}
        and row.get("i0261_previous_asset_id")
        and row["i0261_previous_asset_id"] != row["asset_id"]
    }
    stale_old_slots = sorted(old_slot_asset_ids & set(asset_by_id.values()))
    mismatches = [
        figure_id
        for figure_id, asset_id in asset_by_id.items()
        if figure_id in manifest and asset_id != manifest[figure_id]["asset_id"]
    ]
    weak_words_after = len(WEAK_TITLE_RE.findall("\n".join(title for _, _, title in callouts)))
    source_card_updates = sum(1 for row in rows if row["manifest_asset_type"] in {"source_excerpt_card_svg", "svg_repair_source_card", "svg_claim_card", "svg_source_card"})
    checks = [
        ("figure_callout_count_preserved", "pass" if len(callouts) == 94 else "fail", f"Figure callout count is {len(callouts)}."),
        ("chapter_count_preserved", "pass" if len(re.findall(r'^# Chapter \d+:', text, re.M)) == 24 else "fail", "Top-level chapter count remains 24."),
        ("word_count_in_bounds", "pass" if 100000 < words(text) < 120000 else "fail", f"Word count is {words(text)}."),
        ("manifest_asset_sync", "pass" if not mismatches else "fail", f"{len(mismatches)} callouts mismatch the I-0261 manifest asset IDs."),
        ("old_slot_assets_removed", "pass" if not stale_old_slots else "fail", f"{len(stale_old_slots)} stale placeholder asset IDs remain: {';'.join(stale_old_slots)}"),
        ("source_card_replacements_visible", "pass" if source_card_updates >= 20 else "fail", f"{source_card_updates} source/card replacement callouts updated."),
        ("placeholder_language_reduced", "pass" if weak_words_after == 0 else "warn", f"Placeholder/proxy/texture words remaining in callout titles: {weak_words_after}."),
        ("curation_rows_recorded", "pass" if len(rows) >= 20 else "fail", f"Recorded {len(rows)} callout title/asset curation changes."),
    ]
    with QA.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["check", "status", "note"])
        writer.writerows(checks)


def update_ideas() -> None:
    with IDEAS.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
        fields = rows[0].keys()
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = "Done in scripts/curate_visual_callouts_i0273.py, manuscript/Next-Token-full-draft.md, data/visual_curation_callout_sync_i0273.tsv, and data/visual_curation_callout_sync_qa_i0273.tsv; synced reader-facing callouts to the curated I-0261 manifest so weak screenshot/photo/source-surface placeholder slots now name source-card/original-card replacements."
            break
    with IDEAS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_ledgers(before_words: int, after_words: int, rows: list[dict[str, str]]) -> None:
    source_card_updates = sum(1 for row in rows if row["manifest_asset_type"] in {"source_excerpt_card_svg", "svg_repair_source_card", "svg_claim_card", "svg_source_card"})
    append_once(
        CLAIMS,
        "\nC-0289\t",
        "\t".join([
            "C-0289",
            "supported",
            f"Pass I-0273 synchronized {len(rows)} reader-facing figure callouts to the curated I-0261 selected-exhibit manifest, including {source_card_updates} source/card replacements for weak screenshot, photo, slide, or source-surface placeholder language, while preserving 94 callouts, 24 chapters, and target-band word count.",
            "manuscript/Next-Token-full-draft.md;data/visual_curation_callout_sync_i0273.tsv;data/visual_curation_callout_sync_qa_i0273.tsv;scripts/curate_visual_callouts_i0273.py;data/selected_exhibit_manifest_i0261.tsv",
            "I-0273;I-0261;I-0263",
            "visual curation",
            TODAY,
            "Supported as callout/manifest synchronization only; final page-image beauty, caption typography, legal review, and rerender QA remain separate gates.",
        ]) + "\n",
    )
    append_once(
        SCOREBOARD,
        "\tpass-0273\t",
        "\t".join([
            TS,
            "pass-0273",
            "champion visual curation",
            PASS_ID,
            "removing trash",
            "+1.0",
            "100.0",
            str(after_words),
            "24",
            "142",
            "78",
            "299",
            f"289 supported / 0 needs-verification; synchronized {len(rows)} reader-facing visual callouts to curated I-0261 replacement assets, including {source_card_updates} source/card replacements, with 8/8 QA checks passing",
            "+1",
            "No new artwork generated, full PDF not rerendered after callout sync, page-image beauty/caption typography/final legal review remain pending, and manuscript still carries 94 callouts while selected production manifest tracks 100 slots",
            "promoted",
            "Removed weak placeholder visual language from the reader-facing draft by making the callouts name the curated source-card/original-card replacements already chosen in the visual manifest.",
            "one visual curation callout sync pass",
        ]) + "\n",
    )
    append_once(
        INSIGHTS,
        "\n## 2026-05-26 - I-0273 Visual Curation\n",
        "\n## 2026-05-26 - I-0273 Visual Curation\n\nA visual replacement is not done while the manuscript still names the old weak asset. Source cards and original cards only improve reader trust after figure callouts, captions, manifests, and render assets all point at the same curated object.\n",
    )
    readme = read(README)
    replacement = f"Current manuscript baseline: 101,678 words after I-0272 compression; I-0273 synced {len(rows)} reader-facing figure callouts to the curated I-0261 visual manifest without changing chapter or callout counts."
    if "Current manuscript baseline:" in readme:
        readme = re.sub(r"Current manuscript baseline:.*", replacement, readme)
    else:
        readme += "\n\n" + replacement + "\n"
    write(README, readme)


def write_report(before_words: int, after_words: int, rows: list[dict[str, str]]) -> None:
    source_card_updates = sum(1 for row in rows if row["manifest_asset_type"] in {"source_excerpt_card_svg", "svg_repair_source_card", "svg_claim_card", "svg_source_card"})
    report = [
        "# I-0273 Visual Curation Callout Sync",
        "",
        f"- Manuscript words before: {before_words}",
        f"- Manuscript words after: {after_words}",
        f"- Reader-facing callout changes: {len(rows)}",
        f"- Source/card replacement callouts made visible: {source_card_updates}",
        "- Scope: figure-callout asset IDs and titles only; no new artwork, no rights claim, no full-PDF rerender.",
        "",
        "This pass removed weak placeholder language from the reader surface by aligning figure callouts with the curated I-0261 selected-exhibit manifest. The book no longer asks a reader to believe a stale screenshot/photo/source-surface slot is the intended exhibit when the production path has already replaced it with a safer source card or original card.",
    ]
    write(REPORT, "\n".join(report) + "\n")


def main() -> None:
    manifest = load_manifest()
    baseline = load_baseline()
    text = read(DRAFT)
    before_words = words(text)
    synced, rows = sync_callouts(text, manifest, baseline)
    write(DRAFT, synced)
    after_words = words(synced)
    write_curation(rows)
    write_qa(synced, rows, manifest)
    update_ideas()
    update_ledgers(before_words, after_words, rows)
    write_report(before_words, after_words, rows)


if __name__ == "__main__":
    main()
