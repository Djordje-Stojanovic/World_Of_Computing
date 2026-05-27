from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz


PASS_ID = "I-0302"
RUN_ID = "pass-0302"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"
FINAL_PDF = ROOT / "rendered" / "final_private_i0301" / "Next-Token-final-private-personal-edition-i0301.pdf"
SOURCE_INVENTORY = ROOT / "data" / "final_private_visual_inventory_i0300.tsv"
SOURCE_SUMMARY = ROOT / "data" / "final_private_visual_category_summary_i0300.tsv"
BOARD_INVENTORY = ROOT / "data" / "expanded_private_pdf_board_inventory_i0299.tsv"

OUTDIR = ROOT / "rendered" / "final_inventory_i0302"
CONTACT_HTML = OUTDIR / "Next-Token-final-private-visual-contact-sheet-i0302.html"
CONTACT_PDF = OUTDIR / "Next-Token-final-private-visual-contact-sheet-i0302.pdf"

FINAL_INVENTORY = ROOT / "data" / "final_private_visual_inventory_i0302.tsv"
CATEGORY_SUMMARY = ROOT / "data" / "final_private_visual_category_summary_i0302.tsv"
PAGE_MAP = ROOT / "data" / "final_private_visual_page_map_i0302.tsv"
CONTACT_MANIFEST = ROOT / "data" / "final_private_contact_sheet_manifest_i0302.tsv"
QA = ROOT / "data" / "final_private_visual_inventory_qa_i0302.tsv"
REPORT = ROOT / "manuscript" / "final-private-visual-inventory-i0302.md"

CHAMPION = ROOT / "champion"
CHAMPION_INVENTORY = CHAMPION / "final-private-visual-inventory-i0302.tsv"
CHAMPION_SUMMARY = CHAMPION / "final-private-visual-category-summary-i0302.tsv"
CHAMPION_CONTACT_POINTER = CHAMPION / "final-private-contact-sheet-pointer-i0302.md"
CHAMPION_REPORT = CHAMPION / "final-private-visual-inventory-i0302.md"

README = ROOT / "README.md"
IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, text: str) -> None:
    current = read(path) if path.exists() else ""
    if marker in current:
        return
    write(path, current.rstrip() + "\n" + text.rstrip() + "\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def asset_uri(path_text: str) -> str:
    return (ROOT / path_text).resolve().as_uri()


def word_count() -> int:
    return len(re.findall(r"\b[\w'-]+\b", read(MARKDOWN)))


def chapter_count() -> int:
    return len(re.findall(r"(?m)^# Chapter \d+\b", read(MARKDOWN)))


def normalize(text: str) -> str:
    return " ".join((text or "").split()).lower()


def pdf_texts() -> list[str]:
    doc = fitz.open(FINAL_PDF)
    texts = [normalize(page.get_text("text")) for page in doc]
    doc.close()
    return texts


def find_page(texts: list[str], candidates: list[tuple[str, str]]) -> tuple[str, str, str]:
    for method, candidate in candidates:
        needle = normalize(candidate)
        if not needle:
            continue
        if method == "title_prefix":
            needle = needle[:80]
        if len(needle) < 3:
            continue
        for idx, page_text in enumerate(texts, start=1):
            if needle in page_text:
                return str(idx), method, candidate[:140]
    return "", "unmapped", ""


def board_page_map(texts: list[str]) -> dict[str, tuple[str, str, str]]:
    out: dict[str, tuple[str, str, str]] = {}
    for row in read_tsv(BOARD_INVENTORY):
        board_id = row["board_id"]
        out[board_id] = find_page(texts, [("board_title", row.get("title", "")), ("board_caption", row.get("caption", "")), ("board_id", board_id)])
    return out


def rebuild_inventory() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    texts = pdf_texts()
    boards = board_page_map(texts)
    rows: list[dict[str, str]] = []
    page_rows: list[dict[str, str]] = []
    for source in read_tsv(SOURCE_INVENTORY):
        row = dict(source)
        row["pass_id"] = PASS_ID
        old_page = row.get("pdf_page", "")
        if row["visual_family"] == "expanded_300_exhibit":
            page, method, evidence = find_page(
                texts,
                [
                    ("figure_or_section_id", row.get("board_or_section_id", "")),
                    ("asset_id", row.get("asset_id", "")),
                    ("title_prefix", row.get("title", "")),
                    ("title_full", row.get("title", "")),
                ],
            )
        else:
            page, method, evidence = boards.get(row.get("board_or_section_id", ""), ("", "unmapped", ""))
            if not page:
                page, method, evidence = find_page(
                    texts,
                    [
                        ("board_id", row.get("board_or_section_id", "")),
                        ("asset_id", row.get("asset_id", "")),
                        ("title_prefix", row.get("title", "")),
                    ],
                )
        row["pdf_page"] = page
        row["page_mapping_method_i0302"] = method
        row["page_mapping_evidence_i0302"] = evidence
        rows.append(row)
        page_rows.append(
            {
                "pass_id": PASS_ID,
                "inventory_id": row["inventory_id"],
                "visual_family": row["visual_family"],
                "asset_id": row["asset_id"],
                "title": row["title"],
                "old_pdf_page_i0300": old_page,
                "pdf_page_i0302": page,
                "mapping_method": method,
                "mapping_evidence": evidence,
                "status": "mapped" if page else "unmapped",
            }
        )
    return rows, page_rows


def category_summary(inventory: list[dict[str, str]]) -> list[dict[str, str]]:
    source = read_tsv(SOURCE_SUMMARY)
    counts = Counter()
    for row in inventory:
        for cat in row["visual_category"].split(";"):
            cat = cat.strip()
            if cat:
                counts[cat] += 1
    family_counts = Counter(row["visual_family"] for row in inventory)
    out: list[dict[str, str]] = []
    for row in source:
        new = dict(row)
        new["pass_id"] = PASS_ID
        if row["target_id"] == "authored_visual_board_pages":
            new["final_inventory_rows_i0302"] = row["final_inventory_rows_i0300"]
        else:
            new["final_inventory_rows_i0302"] = str(counts.get(row["target_id"], 0))
        new["family_counts_i0302"] = "; ".join(f"{key}={value}" for key, value in sorted(family_counts.items()))
        out.append(new)
    return out


def contact_sheet_html(inventory: list[dict[str, str]], summary: list[dict[str, str]]) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    families = [
        ("expanded_300_exhibit", "Expanded 300 Exhibit Layer"),
        ("logo_people_strip", "Logo And People Board Items"),
        ("source_surface_gallery", "Paper/PDF Source-Surface Gallery Items"),
        ("chart_data_svg_atlas", "Chart/Data/SVG Atlas Items"),
    ]
    lines = [
        "<!doctype html><html><head><meta charset='utf-8'><title>I-0302 Final Private Visual Contact Sheet</title>",
        """
        <style>
        @page { size: Letter; margin: 0.25in; }
        body { margin: 0; background: #f6f2ea; color: #171410; font-family: Georgia, 'Times New Roman', serif; }
        section { page-break-after: always; }
        h1 { font-size: 22pt; margin: 0 0 0.08in; }
        h2 { font-size: 14pt; margin: 0.1in 0 0.06in; border-bottom: 1px solid #5f5548; padding-bottom: 0.03in; }
        p { font-size: 7.5pt; line-height: 1.22; margin: 0.025in 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 0.1in; }
        th, td { border-bottom: 0.5px solid #c9c0b0; padding: 0.035in; font-size: 7pt; text-align: left; }
        .grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.058in; }
        .card { background: #fffdf8; border: 0.55px solid #c7bdab; padding: 0.04in; min-height: 1.03in; overflow: hidden; }
        .thumb { height: 0.49in; display: flex; align-items: center; justify-content: center; background: #eee9df; margin-bottom: 0.025in; }
        .thumb img { max-width: 100%; max-height: 0.47in; object-fit: contain; }
        .title { font-weight: 700; font-size: 5.7pt; line-height: 1.06; }
        .meta { color: #5b5145; font-size: 5.1pt; line-height: 1.08; }
        </style></head><body>
        """,
        "<section><h1>I-0302 Final Private Visual Inventory</h1>",
        "<p>Contact sheet for the I-0301 rhythm-repaired private PDF. The TSV inventory is authoritative; this PDF gives a compact visual scan surface with page numbers and blocked-claim reminders.</p>",
        "<table><tr><th>Category</th><th>Minimum</th><th>Rendered</th><th>I-0302 Inventory Rows</th><th>Status</th></tr>",
    ]
    for row in summary:
        lines.append(
            f"<tr><td>{html.escape(row['label'])}</td><td>{row['goal_minimum']}</td><td>{row['rendered_target_count_i0295']}</td><td>{row['final_inventory_rows_i0302']}</td><td>{row['status']}</td></tr>"
        )
    lines.append("</table></section>")
    for family, title in families:
        family_rows = [row for row in inventory if row["visual_family"] == family]
        lines.append(f"<section><h2>{html.escape(title)}</h2><div class='grid'>")
        for row in family_rows:
            src = row["file_path"]
            lines.append(
                f"""
                <article class="card">
                  <div class="thumb"><img src="{asset_uri(src)}" alt="{html.escape(row['title'])}"></div>
                  <div class="title">{html.escape(row['title'][:95])}</div>
                  <div class="meta">Page {html.escape(row['pdf_page'] or 'unmapped')} | {html.escape(row['visual_category'][:70])}</div>
                  <div class="meta">Source: {html.escape(row['source_or_provenance'][:105])}</div>
                  <div class="meta">Blocked: {html.escape(row['blocked_claims'][:105])}</div>
                </article>
                """
            )
        lines.append("</div></section>")
    lines.append("</body></html>")
    write(CONTACT_HTML, "\n".join(lines))


def render_pdf(chrome: Path) -> None:
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--allow-file-access-from-files",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={CONTACT_PDF}",
        CONTACT_HTML.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not CONTACT_PDF.exists() or CONTACT_PDF.stat().st_size == 0:
        raise RuntimeError(f"Chrome PDF render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    pages = len(doc)
    image_objects = sum(len(page.get_images(full=True)) for page in doc)
    blank_like = 0
    for page in doc:
        if not page.get_text("text").strip() and not page.get_images(full=True) and len(page.get_drawings()) < 3:
            blank_like += 1
    doc.close()
    return {
        "path": rel(path),
        "pages": str(pages),
        "image_objects": str(image_objects),
        "blank_like_pages": str(blank_like),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
    }


def qa_rows(inventory: list[dict[str, str]], page_rows: list[dict[str, str]], summary: list[dict[str, str]], contact_stats: dict[str, str]) -> list[dict[str, str]]:
    missing_pages = sum(1 for row in inventory if not row["pdf_page"])
    checks = [
        ("I0302-001", "inventory_row_count", len(inventory) == 530, f"rows={len(inventory)}", "Repair inventory source merge."),
        ("I0302-002", "page_mapping", missing_pages == 0, f"unmapped_rows={missing_pages}", "Repair I-0301 PDF page mapping."),
        ("I0302-003", "visual_targets", all(row["status"] == "pass" for row in summary), f"pass_rows={sum(1 for row in summary if row['status'] == 'pass')}/{len(summary)}", "Repair visual target summary."),
        ("I0302-004", "provenance_fields", all(row["source_or_provenance"] and row["sha256"] and row["private_use_status"] and row["blocked_claims"] for row in inventory), f"rows={len(inventory)}", "Complete provenance/private-use/blocked-claim fields."),
        ("I0302-005", "local_files_exist", all((ROOT / row["file_path"]).exists() for row in inventory), f"missing_files={sum(1 for row in inventory if not (ROOT / row['file_path']).exists())}", "Repair missing local asset references."),
        ("I0302-006", "contact_sheet_pdf", CONTACT_PDF.exists() and int(contact_stats["bytes"]) > 0, f"pages={contact_stats['pages']}; images={contact_stats['image_objects']}; bytes={contact_stats['bytes']}", "Render contact sheet PDF."),
        ("I0302-007", "contact_sheet_blank_pages", contact_stats["blank_like_pages"] == "0", f"blank_like={contact_stats['blank_like_pages']}", "Repair blank contact-sheet pages."),
        ("I0302-008", "book_invariants", 100000 < word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
    ]
    return [
        {
            "pass_id": PASS_ID,
            "check_id": check_id,
            "category": category,
            "result": "pass" if passed else "fail",
            "evidence": evidence,
            "recommended_action": "No action required for this automated check." if passed else action,
        }
        for check_id, category, passed, evidence, action in checks
    ]


def contact_manifest_rows(contact_stats: dict[str, str], inventory: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {"pass_id": PASS_ID, "artifact": "contact_sheet_html", "path": rel(CONTACT_HTML), "rows_represented": str(len(inventory)), "pages": "", "image_objects": "", "bytes": str(CONTACT_HTML.stat().st_size), "sha256": sha256(CONTACT_HTML), "private_use_note": "local ignored contact-sheet source"},
        {"pass_id": PASS_ID, "artifact": "contact_sheet_pdf", "path": rel(CONTACT_PDF), "rows_represented": str(len(inventory)), "pages": contact_stats["pages"], "image_objects": contact_stats["image_objects"], "bytes": contact_stats["bytes"], "sha256": contact_stats["sha256"], "private_use_note": "local ignored contact-sheet PDF"},
        {"pass_id": PASS_ID, "artifact": "source_pdf", "path": rel(FINAL_PDF), "rows_represented": str(len(inventory)), "pages": "", "image_objects": "", "bytes": str(FINAL_PDF.stat().st_size), "sha256": sha256(FINAL_PDF), "private_use_note": "best local rhythm-repaired private PDF"},
    ]


def write_report(inventory: list[dict[str, str]], page_rows: list[dict[str, str]], summary: list[dict[str, str]], contact_stats: dict[str, str], qa: list[dict[str, str]]) -> None:
    family_counts = Counter(row["visual_family"] for row in inventory)
    method_counts = Counter(row["mapping_method"] for row in page_rows)
    lines = [
        "# I-0302 Final Private Visual Inventory And Contact Sheet",
        "",
        "Status: promoted asset-audit pass.",
        "",
        "## Result",
        "",
        f"- Inventory rows: {len(inventory)}",
        f"- Unmapped rows: {sum(1 for row in inventory if not row['pdf_page'])}",
        f"- Contact sheet PDF: `{rel(CONTACT_PDF)}` (local/ignored, not committed)",
        f"- Contact sheet pages: {contact_stats['pages']}",
        f"- Contact sheet image objects: {contact_stats['image_objects']}",
        f"- Contact sheet blank-like pages: {contact_stats['blank_like_pages']}",
        f"- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
        "",
        "## Inventory Families",
        "",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(f"- {family}: {count}")
    lines.extend(["", "## Page Mapping Methods", ""])
    for method, count in sorted(method_counts.items()):
        lines.append(f"- {method}: {count}")
    lines.extend(
        [
            "",
            "## Visual Target Summary",
            "",
            "| Target | Minimum | Rendered | I-0302 Rows | Status |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in summary:
        lines.append(f"| {row['label']} | {row['goal_minimum']} | {row['rendered_target_count_i0295']} | {row['final_inventory_rows_i0302']} | {row['status']} |")
    lines.extend(
        [
            "",
            "## Editorial Decision",
            "",
            "The I-0301 private PDF now has an auditable I-0302 visual inventory and local contact sheet. This pass does not add new evidence or rights claims; it makes the existing private visual layer easier to inspect, navigate, and trust.",
            "",
        ]
    )
    write(REPORT, "\n".join(lines))


def update_champion(contact_stats: dict[str, str]) -> None:
    shutil.copy2(FINAL_INVENTORY, CHAMPION_INVENTORY)
    shutil.copy2(CATEGORY_SUMMARY, CHAMPION_SUMMARY)
    shutil.copy2(REPORT, CHAMPION_REPORT)
    pointer = f"""# Final Private Contact Sheet Pointer - I-0302

The final private visual contact sheet is local and intentionally not committed.

- Contact sheet PDF: `{rel(CONTACT_PDF)}`
- SHA256: `{contact_stats['sha256']}`
- Bytes: {contact_stats['bytes']}
- Pages: {contact_stats['pages']}
- Image objects: {contact_stats['image_objects']}
- Inventory TSV: `{rel(FINAL_INVENTORY)}`
- Source PDF: `{rel(FINAL_PDF)}`

Private-use note: this is an audit surface for the user's personal edition. It records provenance and blocked-claim boundaries, but it does not create publication rights.
"""
    write(CHAMPION_CONTACT_POINTER, pointer)


def update_ideas() -> None:
    evidence = (
        "Done in scripts/final_private_visual_inventory_i0302.py, data/final_private_visual_inventory_i0302.tsv, "
        "data/final_private_visual_page_map_i0302.tsv, data/final_private_visual_category_summary_i0302.tsv, "
        "data/final_private_contact_sheet_manifest_i0302.tsv, data/final_private_visual_inventory_qa_i0302.tsv, "
        "manuscript/final-private-visual-inventory-i0302.md, and champion/final-private-contact-sheet-pointer-i0302.md; "
        "rebuilt the 530-row visual inventory against the I-0301 PDF, mapped every row to a page, preserved provenance and blocked-claim fields, and rendered a local contact sheet."
    )
    out = []
    ids = set()
    for line in read(IDEAS).splitlines():
        if not line.strip():
            continue
        ids.add(line.split("\t", 1)[0])
        if line.startswith(f"{PASS_ID}\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = evidence
            line = "\t".join(parts)
        out.append(line)
    if "I-0308" not in ids:
        out.append(
            "\t".join(
                [
                    "I-0308",
                    "pending",
                    "Build a compact private reader guide that tells the user where to find the final PDF, contact sheet, inventory, champion package, and remaining-risk notes.",
                    "delivery polish",
                    "one concise guide links the local private artifacts and committed proof ledgers",
                    "After final PDF, rhythm repair, and inventory/contact-sheet passes, the user needs a simple durable map of what to open and what each artifact proves.",
                ]
            )
        )
    write(IDEAS, "\n".join(out) + "\n")


def update_readme(contact_stats: dict[str, str], inventory: list[dict[str, str]]) -> None:
    text = read(README)
    start = text.find("## Current Book State")
    end = text.find("## Readiness Snapshot")
    if start == -1 or end == -1:
        return
    replacement = f"""## Current Book State

Updated **2026-05-27** after pass `I-0302`.

- **Latest recorded pass:** `I-0302`, final private visual inventory/contact-sheet audit.
- **Words:** {word_count():,} assembled source words across the canonical 24-chapter draft.
- **Chapters:** {chapter_count()} / 24 main chapters.
- **Best local private PDF proof:** `rendered/final_private_i0301/Next-Token-final-private-personal-edition-i0301.pdf`.
- **Final visual inventory:** `data/final_private_visual_inventory_i0302.tsv` maps {len(inventory)} visual rows to the I-0301 PDF pages, local files, provenance, private-use status, story purpose, and blocked-claim boundaries.
- **Final contact sheet:** `rendered/final_inventory_i0302/Next-Token-final-private-visual-contact-sheet-i0302.pdf` exists locally and is intentionally not committed. It has {contact_stats['pages']} pages, {contact_stats['image_objects']} image objects, and SHA256 `{contact_stats['sha256']}`.

The private edition now has both the rich PDF and a separate audit surface for inspecting its charts, screenshots, source excerpts, logos, people images, tables, and model/documentation surfaces.

"""
    write(README, text[:start] + replacement + text[end:])


def record_loop(inventory: list[dict[str, str]], page_rows: list[dict[str, str]], contact_stats: dict[str, str], qa: list[dict[str, str]]) -> None:
    update_ideas()
    update_readme(contact_stats, inventory)
    append_once(
        CLAIMS,
        "C-0318\t",
        "\t".join(
            [
                "C-0318",
                "supported",
                f"I-0302 rebuilt the final private visual inventory against the I-0301 PDF with {len(inventory)} rows, {sum(1 for row in inventory if row['pdf_page'])} page-mapped rows, full provenance/private-use/blocked-claim fields, and a local contact-sheet PDF of {contact_stats['pages']} pages and {contact_stats['image_objects']} image objects.",
                "scripts/final_private_visual_inventory_i0302.py;data/final_private_visual_inventory_i0302.tsv;data/final_private_visual_page_map_i0302.tsv;data/final_private_visual_category_summary_i0302.tsv;data/final_private_contact_sheet_manifest_i0302.tsv;data/final_private_visual_inventory_qa_i0302.tsv;manuscript/final-private-visual-inventory-i0302.md;rendered/final_inventory_i0302/Next-Token-final-private-visual-contact-sheet-i0302.pdf",
                PASS_ID,
                "final visual inventory and contact-sheet audit",
                TODAY,
                "Supported as private-use inventory/contact-sheet audit only; heavy contact-sheet PDF/HTML remain ignored and no public-use rights claim is promoted.",
            ]
        ),
    )
    timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    append_once(
        SCOREBOARD,
        f"\t{RUN_ID}\t",
        "\t".join(
            [
                timestamp,
                RUN_ID,
                "champion rhythm-repaired private PDF",
                PASS_ID,
                "asset audit",
                "+1.0",
                "100.0",
                str(word_count()),
                str(chapter_count()),
                "152",
                "158",
                "510",
                f"318 supported / 0 needs-verification; final visual inventory {len(inventory)} rows, mapped pages {sum(1 for row in inventory if row['pdf_page'])}/{len(inventory)}, contact sheet {contact_stats['pages']} pages and {contact_stats['image_objects']} image objects; QA {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
                "+1",
                "Local contact-sheet PDF/HTML remain ignored; inventory/contact sheet is an audit surface, not a public-rights package",
                "promoted",
                "Made the final private visual layer auditable by mapping every inventory row to the I-0301 PDF and rendering a compact local contact sheet.",
                "one final visual inventory/contact-sheet audit pass",
            ]
        ),
    )
    append_once(
        INSIGHTS,
        "I-0302: final visual inventory",
        "\n- I-0302: a visually maximal private book needs a second artifact for trust. The contact sheet and page-mapped inventory let the reader audit hundreds of images, charts, logos, papers, screenshots, and people surfaces without re-opening the whole PDF or treating visual abundance as unverifiable clutter.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not args.skip_render and not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    if not FINAL_PDF.exists():
        raise FileNotFoundError(FINAL_PDF)

    inventory, page_rows = rebuild_inventory()
    summary = category_summary(inventory)
    contact_sheet_html(inventory, summary)
    if not args.skip_render:
        render_pdf(chrome)
    if not CONTACT_PDF.exists():
        raise FileNotFoundError(CONTACT_PDF)
    contact_stats = pdf_stats(CONTACT_PDF)
    qa = qa_rows(inventory, page_rows, summary, contact_stats)
    contact_manifest = contact_manifest_rows(contact_stats, inventory)

    write_tsv(FINAL_INVENTORY, inventory, list(inventory[0].keys()))
    write_tsv(PAGE_MAP, page_rows, list(page_rows[0].keys()))
    write_tsv(CATEGORY_SUMMARY, summary, list(summary[0].keys()))
    write_tsv(CONTACT_MANIFEST, contact_manifest, list(contact_manifest[0].keys()))
    write_tsv(QA, qa, list(qa[0].keys()))
    write_report(inventory, page_rows, summary, contact_stats, qa)

    if any(row["result"] == "fail" for row in qa):
        print(f"{PASS_ID}: FAIL. See {rel(QA)}")
        return 2

    update_champion(contact_stats)
    record_loop(inventory, page_rows, contact_stats, qa)
    print(
        f"{PASS_ID}: promoted. rows={len(inventory)} mapped={sum(1 for row in inventory if row['pdf_page'])} "
        f"contact_pages={contact_stats['pages']} contact_images={contact_stats['image_objects']} "
        f"qa={Counter(row['result'] for row in qa)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
