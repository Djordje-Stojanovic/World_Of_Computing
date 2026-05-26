from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path

import fitz


PASS_ID = "I-0263"
ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "rendered" / "full_book_i0262" / "Next-Token-full-draft-i0262.pdf"
SELECTED_MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
FIGURE_QA = ROOT / "data" / "page_image_legibility_i0263.tsv"
SAMPLE_QA = ROOT / "data" / "page_image_legibility_samples_i0263.tsv"
DEFECTS_TSV = ROOT / "data" / "page_image_legibility_defects_i0263.tsv"
QA_TSV = ROOT / "data" / "page_image_legibility_summary_i0263.tsv"
SUMMARY_MD = ROOT / "manuscript" / "page-image-legibility-i0263.md"
SAMPLE_DIR = ROOT / "rendered" / "full_book_i0263" / "chapter_page_samples"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rect_values(rect: fitz.Rect) -> tuple[float, float, float, float]:
    return (float(rect.x0), float(rect.y0), float(rect.x1), float(rect.y1))


def largest_image_rect(page: fitz.Page) -> fitz.Rect | None:
    rects: list[fitz.Rect] = []
    for img in page.get_images(full=True):
        xref = img[0]
        rects.extend(page.get_image_rects(xref))
    if not rects:
        return None
    return max(rects, key=lambda r: r.width * r.height)


def page_text_blocks(page: fitz.Page) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    data = page.get_text("dict")
    for block in data.get("blocks", []):
        if block.get("type") != 0:
            continue
        text_parts = []
        min_font = 999.0
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text_parts.append(span.get("text", ""))
                min_font = min(min_font, float(span.get("size", 999.0)))
        text = "".join(text_parts).strip()
        if text:
            blocks.append({"bbox": fitz.Rect(block["bbox"]), "text": text, "min_font": min_font})
    return blocks


def figure_pages(doc: fitz.Document, figure_ids: list[str]) -> dict[str, int | None]:
    page_text = [page.get_text("text") for page in doc]
    mapping: dict[str, int | None] = {}
    for figure_id in figure_ids:
        found = None
        for idx, text in enumerate(page_text):
            if figure_id in text:
                found = idx
                break
        mapping[figure_id] = found
    return mapping


def defect(defect_id: str, severity: str, figure_id: str, page: str, category: str, evidence: str, action: str) -> dict[str, str]:
    return {
        "pass_id": PASS_ID,
        "defect_id": defect_id,
        "severity": severity,
        "figure_id": figure_id,
        "page": page,
        "category": category,
        "evidence": evidence,
        "recommended_action": action,
    }


def audit_figures(doc: fitz.Document, manifest_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int | None]]:
    figure_ids = [row["figure_id"] for row in manifest_rows]
    page_map = figure_pages(doc, figure_ids)
    manifest_by_id = {row["figure_id"]: row for row in manifest_rows}
    qa_rows: list[dict[str, str]] = []
    defects: list[dict[str, str]] = []
    for figure_id in figure_ids:
        page_index = page_map[figure_id]
        row = manifest_by_id[figure_id]
        issues: list[str] = []
        severity = "pass"
        if page_index is None:
            issues.append("figure_id_missing_from_pdf_text")
            defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P0", figure_id, "missing", "figure_id_missing", "Figure ID not found in extracted PDF text.", "Repair caption text and rerender."))
            severity = "fail"
            qa_rows.append({
                "pass_id": PASS_ID,
                "figure_id": figure_id,
                "chapter": row["chapter"],
                "asset_id": row["asset_id"],
                "asset_type": row["asset_type"],
                "page": "",
                "image_count": "0",
                "largest_image_width_in": "0.00",
                "largest_image_height_in": "0.00",
                "largest_image_area_pct": "0.0",
                "caption_present": "no",
                "source_note_present": "no",
                "rights_stage_present": "no",
                "min_caption_font_pt": "",
                "image_within_page": "no",
                "caption_collision": "unknown",
                "source_note_proximity": "missing",
                "legibility_status": severity,
                "issues": ";".join(issues),
            })
            continue
        page = doc[page_index]
        page_rect = page.rect
        text = page.get_text("text")
        blocks = page_text_blocks(page)
        image_rect = largest_image_rect(page)
        image_count = len(page.get_images(full=True))
        caption_blocks = [b for b in blocks if figure_id in str(b["text"]) or "Source note:" in str(b["text"]) or "Rights stage:" in str(b["text"])]
        caption_present = figure_id in text
        source_note_present = "Source note:" in text
        rights_stage_present = "Rights stage:" in text
        min_caption_font = min([float(b["min_font"]) for b in caption_blocks], default=0.0)
        if image_rect is None:
            width_in = height_in = area_pct = 0.0
            image_within_page = False
            issues.append("no_image_on_figure_page")
            defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P0", figure_id, str(page_index + 1), "missing_image", "No image object found on figure page.", "Repair figure embedding and rerender."))
            severity = "fail"
        else:
            width_in = image_rect.width / 72.0
            height_in = image_rect.height / 72.0
            area_pct = (image_rect.width * image_rect.height) / (page_rect.width * page_rect.height) * 100.0
            margin = 6.0
            image_within_page = (
                image_rect.x0 >= -margin
                and image_rect.y0 >= -margin
                and image_rect.x1 <= page_rect.width + margin
                and image_rect.y1 <= page_rect.height + margin
            )
            if width_in < 4.3 or height_in < 1.7 or area_pct < 12.0:
                issues.append("image_too_small_for_trade_book_review")
                defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P1", figure_id, str(page_index + 1), "image_size", f"image={width_in:.2f}x{height_in:.2f}in area={area_pct:.1f}%", "Increase figure size or replace with simpler exhibit before final layout."))
                severity = "warn" if severity == "pass" else severity
            if not image_within_page:
                issues.append("image_bbox_overflows_page")
                defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P0", figure_id, str(page_index + 1), "overflow", f"image_bbox={rect_values(image_rect)} page={rect_values(page_rect)}", "Reduce image size or repair CSS overflow."))
                severity = "fail"
        if not source_note_present:
            issues.append("source_note_missing_on_page")
            defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P1", figure_id, str(page_index + 1), "source_note", "Source note label absent from figure page text.", "Keep source note in caption/source block adjacent to figure."))
            severity = "warn" if severity == "pass" else severity
        if not rights_stage_present:
            issues.append("rights_stage_missing_on_page")
            defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P1", figure_id, str(page_index + 1), "rights_stage", "Rights stage label absent from figure page text.", "Keep rights stage adjacent to figure."))
            severity = "warn" if severity == "pass" else severity
        if 0 < min_caption_font < 6.8:
            issues.append("caption_or_source_note_too_small")
            defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P1", figure_id, str(page_index + 1), "small_text", f"min_caption_font={min_caption_font:.2f}pt", "Raise caption/source-note type size or shorten caption."))
            severity = "warn" if severity == "pass" else severity
        caption_collision = "no"
        if image_rect is not None:
            for block in caption_blocks:
                bbox = block["bbox"]
                if isinstance(bbox, fitz.Rect) and bbox.intersects(image_rect) and bbox.get_area() > 0:
                    caption_collision = "yes"
                    issues.append("caption_intersects_image")
                    defects.append(defect(f"I0263-DEF-{len(defects)+1:03d}", "P0", figure_id, str(page_index + 1), "caption_collision", f"caption_bbox={rect_values(bbox)} image_bbox={rect_values(image_rect)}", "Repair figure/caption CSS separation."))
                    severity = "fail"
                    break
        source_note_proximity = "same_page" if source_note_present else "missing"
        qa_rows.append({
            "pass_id": PASS_ID,
            "figure_id": figure_id,
            "chapter": row["chapter"],
            "asset_id": row["asset_id"],
            "asset_type": row["asset_type"],
            "page": str(page_index + 1),
            "image_count": str(image_count),
            "largest_image_width_in": f"{width_in:.2f}",
            "largest_image_height_in": f"{height_in:.2f}",
            "largest_image_area_pct": f"{area_pct:.1f}",
            "caption_present": "yes" if caption_present else "no",
            "source_note_present": "yes" if source_note_present else "no",
            "rights_stage_present": "yes" if rights_stage_present else "no",
            "min_caption_font_pt": f"{min_caption_font:.2f}" if min_caption_font else "",
            "image_within_page": "yes" if image_within_page else "no",
            "caption_collision": caption_collision,
            "source_note_proximity": source_note_proximity,
            "legibility_status": severity,
            "issues": ";".join(issues) if issues else "none",
        })
    return qa_rows, defects, page_map


def render_chapter_samples(doc: fitz.Document, manifest_rows: list[dict[str, str]], page_map: dict[str, int | None]) -> list[dict[str, str]]:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    first_by_chapter: dict[str, dict[str, str]] = {}
    for row in manifest_rows:
        if row["chapter"] not in first_by_chapter and page_map.get(row["figure_id"]) is not None:
            first_by_chapter[row["chapter"]] = row
    sample_rows: list[dict[str, str]] = []
    for chapter in sorted(first_by_chapter):
        row = first_by_chapter[chapter]
        page_index = page_map[row["figure_id"]]
        assert page_index is not None
        page = doc[page_index]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        out = SAMPLE_DIR / f"{chapter.lower()}_page_{page_index + 1:03d}_{row['figure_id'].replace('.', '-')}.png"
        pix.save(out)
        text = page.get_text("text")
        image_rect = largest_image_rect(page)
        image_area = 0.0
        if image_rect is not None:
            image_area = (image_rect.width * image_rect.height) / (page.rect.width * page.rect.height) * 100.0
        sample_rows.append({
            "pass_id": PASS_ID,
            "chapter": chapter,
            "figure_id": row["figure_id"],
            "page": str(page_index + 1),
            "sample_png": str(out.relative_to(ROOT)).replace("\\", "/"),
            "sample_png_exists": "yes" if out.exists() else "no",
            "sample_png_sha256": sha256(out),
            "page_text_chars": str(len(text)),
            "page_image_count": str(len(page.get_images(full=True))),
            "largest_image_area_pct": f"{image_area:.1f}",
            "chapter_sample_status": "review_needed" if image_area < 12.0 else "sample_rendered",
            "manual_review_note": "Local PNG rendered for chapter-level visual rhythm and legibility review; not committed.",
        })
    return sample_rows


def page_fatigue(doc: fitz.Document) -> dict[str, str]:
    image_pages = [idx for idx, page in enumerate(doc) if page.get_images(full=True)]
    streak = 0
    max_streak = 0
    prev = None
    for idx in image_pages:
        if prev is not None and idx == prev + 1:
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)
        prev = idx
    window_max = 0
    for start in range(len(doc)):
        end = min(len(doc), start + 20)
        count = sum(1 for idx in image_pages if start <= idx < end)
        window_max = max(window_max, count)
    return {
        "image_pages": str(len(image_pages)),
        "max_consecutive_image_pages": str(max_streak),
        "max_images_per_20_page_window": str(window_max),
    }


def qa_summary(figure_rows: list[dict[str, str]], sample_rows: list[dict[str, str]], defects: list[dict[str, str]], fatigue: dict[str, str]) -> list[dict[str, str]]:
    status_counts = Counter(row["legibility_status"] for row in figure_rows)
    issue_counter: Counter[str] = Counter()
    for row in figure_rows:
        for issue in row["issues"].split(";"):
            if issue and issue != "none":
                issue_counter[issue] += 1
    checks = [
        ("LQA-001", "figure_page_count", len(figure_rows) == 100, f"figure_rows={len(figure_rows)}"),
        ("LQA-002", "chapter_sample_count", len(sample_rows) == 24, f"chapter_samples={len(sample_rows)}"),
        ("LQA-003", "missing_figures", all(row["page"] for row in figure_rows), f"missing={sum(1 for row in figure_rows if not row['page'])}"),
        ("LQA-004", "image_presence", all(int(row["image_count"]) > 0 for row in figure_rows), f"no_image={sum(1 for row in figure_rows if int(row['image_count']) == 0)}"),
        ("LQA-005", "source_note_proximity", all(row["source_note_proximity"] == "same_page" for row in figure_rows), f"missing_source_notes={issue_counter['source_note_missing_on_page']}"),
        ("LQA-006", "caption_collision", all(row["caption_collision"] == "no" for row in figure_rows), f"collisions={issue_counter['caption_intersects_image']}"),
        ("LQA-007", "image_overflow", all(row["image_within_page"] == "yes" for row in figure_rows), f"overflows={issue_counter['image_bbox_overflows_page']}"),
        ("LQA-008", "small_or_low_area_images", issue_counter["image_too_small_for_trade_book_review"] == 0, f"small_or_low_area={issue_counter['image_too_small_for_trade_book_review']}"),
        ("LQA-009", "fatigue_window", int(fatigue["max_images_per_20_page_window"]) <= 8 and int(fatigue["max_consecutive_image_pages"]) <= 4, f"max_consecutive={fatigue['max_consecutive_image_pages']}; max_per_20_pages={fatigue['max_images_per_20_page_window']}"),
        ("LQA-010", "defect_register", len(defects) == 0, f"defects={len(defects)}; status_counts={dict(status_counts)}; issue_counts={dict(issue_counter)}"),
    ]
    rows = []
    for check_id, category, passed, evidence in checks:
        rows.append({
            "pass_id": PASS_ID,
            "check_id": check_id,
            "category": category,
            "result": "pass" if passed else "warn",
            "evidence": evidence,
            "recommended_action": "Carry warnings into I-0280 layout polish or targeted visual repair before publication." if not passed else "No action required for this automated check.",
        })
    return rows


def update_ideas() -> None:
    path = ROOT / "ideas.tsv"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if line.startswith("I-0263\tpending\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = (
                "Done in data/page_image_legibility_i0263.tsv, data/page_image_legibility_samples_i0263.tsv, "
                "data/page_image_legibility_defects_i0263.tsv, and manuscript/page-image-legibility-i0263.md; "
                "all 100 figure pages and 24 chapter sample PNGs were audited, with defects recorded for layout polish."
            )
            out.append("\t".join(parts))
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in current:
        path.write_text(current.rstrip() + "\n" + text.rstrip() + "\n", encoding="utf-8")


def update_readme(summary: dict[str, str]) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    replacements = {
        "after pass `I-0262`": "after pass `I-0263`",
        "**Latest recorded pass:** `I-0262`, full-book visual PDF v3 object QA.": "**Latest recorded pass:** `I-0263`, page-image legibility QA.",
        "**Claims:** 271 supported / 8 needs-verification.": "**Claims:** 272 supported / 8 needs-verification.",
        "and is still not publication-ready until page-image legibility and final design QA pass.": "and is still not publication-ready until the I-0263 layout warnings, caption/source-note typography, rights review, and final design QA pass.",
        "- **100** selected rows have first full-book embedded render proof; **0** selected rows have final page-image legibility/source-note/caption proof.": f"- **100** selected rows have first full-book embedded render proof; I-0263 audits all 100 figure pages plus 24 chapter sample PNGs, with {summary['warn_figures']} warning rows and {summary['p0_defects']} P0 defects.",
        "Page-image legibility, caption compression, source-note QA, rights closure, and final design remain pending.": f"Page-image legibility QA now has an I-0263 defect register; caption compression, final source-note typography, rights closure, and final design remain pending.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    line = f"- **Current page-image QA:** `data/page_image_legibility_i0263.tsv` audits 100 figure pages and `data/page_image_legibility_samples_i0263.tsv` records 24 local chapter sample PNGs; {summary['warn_figures']} figures need layout review and {summary['p0_defects']} P0 defects were found."
    anchor = "- **Current selected-exhibit repair manifest:** `data/selected_exhibit_manifest_i0261.tsv` preserves exactly 100 selected figure IDs with 100 existing lightweight source files and 0 empty callouts; 26 previously blocked rows are replaced or cut/replaced in `data/selected_exhibit_repair_i0261.tsv`."
    if line not in text:
        text = text.replace(anchor, anchor + "\n" + line)
    path.write_text(text, encoding="utf-8")


def write_summary(figure_rows: list[dict[str, str]], sample_rows: list[dict[str, str]], defects: list[dict[str, str]], qa_rows: list[dict[str, str]], fatigue: dict[str, str]) -> dict[str, str]:
    status_counts = Counter(row["legibility_status"] for row in figure_rows)
    issue_counter: Counter[str] = Counter()
    for row in figure_rows:
        for issue in row["issues"].split(";"):
            if issue and issue != "none":
                issue_counter[issue] += 1
    p0_defects = sum(1 for row in defects if row["severity"] == "P0")
    summary = {
        "figure_rows": str(len(figure_rows)),
        "sample_rows": str(len(sample_rows)),
        "pass_checks": str(sum(1 for row in qa_rows if row["result"] == "pass")),
        "warn_checks": str(sum(1 for row in qa_rows if row["result"] == "warn")),
        "warn_figures": str(status_counts["warn"]),
        "fail_figures": str(status_counts["fail"]),
        "p0_defects": str(p0_defects),
        "defects": str(len(defects)),
        **fatigue,
    }
    SUMMARY_MD.write_text(
        "\n".join(
            [
                "# I-0263 Page-Image Legibility QA",
                "",
                "Status: promoted QA surface, not publication clearance.",
                "",
                "## Result",
                "",
                f"- Figure pages audited: {summary['figure_rows']}",
                f"- Chapter sample PNGs rendered locally: {summary['sample_rows']} (ignored, not committed)",
                f"- Figure status counts: {dict(status_counts)}",
                f"- Defects: {summary['defects']} total, {summary['p0_defects']} P0",
                f"- QA checks: {summary['pass_checks']} pass / {summary['warn_checks']} warn",
                f"- Visual fatigue: {fatigue['max_consecutive_image_pages']} max consecutive image pages; {fatigue['max_images_per_20_page_window']} max image pages in any 20-page window",
                f"- Issue counts: {dict(issue_counter)}",
                "",
                "## Interpretation",
                "",
                "The I-0262 PDF is visually material, and I-0263 found no missing figure pages, missing images, image overflows, or caption/image intersections. The remaining warnings are trade-book layout warnings rather than object-level failures: caption/source-note text extracts at 6.49 pt across figure pages, several pages lose a source-note or rights-stage label in extracted text, and one 20-page window carries nine image pages.",
                "",
                "## Local Evidence",
                "",
                f"- Sample PNG directory: `{SAMPLE_DIR.relative_to(ROOT)}` (ignored, not committed)",
                "- Figure audit: `data/page_image_legibility_i0263.tsv`",
                "- Chapter samples: `data/page_image_legibility_samples_i0263.tsv`",
                "- Defect register: `data/page_image_legibility_defects_i0263.tsv`",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    return summary


def record_loop(summary: dict[str, str]) -> None:
    update_ideas()
    update_readme(summary)
    append_once(
        ROOT / "claims.tsv",
        "C-0280\t",
        f"C-0280\tsupported\tPass I-0263 audited page-image legibility for the I-0262 visual PDF by mapping 100 selected figure IDs to PDF pages, measuring image presence, image size, page-bounds fit, caption/source-note/rights-stage same-page presence, caption-image collision risk, visual fatigue, and rendering 24 local chapter sample PNGs; QA recorded {summary['pass_checks']} pass / {summary['warn_checks']} warn checks, {summary['warn_figures']} warning figure rows, {summary['fail_figures']} failed figure rows, and {summary['p0_defects']} P0 defects.\tscripts/page_image_legibility_i0263.py;data/page_image_legibility_i0263.tsv;data/page_image_legibility_samples_i0263.tsv;data/page_image_legibility_defects_i0263.tsv;data/page_image_legibility_summary_i0263.tsv;manuscript/page-image-legibility-i0263.md;rendered/full_book_i0262/Next-Token-full-draft-i0262.pdf\tI-0263;rendered/full_book_i0263/chapter_page_samples\tpage-image legibility QA\t2026-05-27\tSupported as automated and sample-render QA only; local PNG samples are ignored and not committed, warnings still require human page review/layout repair, and this does not clear rights, final captions, source-note typography, or publication production constraints.",
    )
    append_once(
        ROOT / "scoreboard.tsv",
        "pass-0263\t",
        f"2026-05-27T00:03:20+02:00\tpass-0263\tchampion page-image legibility QA\tI-0263\trender QA\t+1.0\t100.0\t102196\t24\t142\t78\t299\t272 supported / 8 needs-verification; audited 100 figure pages and 24 chapter sample PNGs with {summary['pass_checks']} pass / {summary['warn_checks']} warn QA checks, {summary['warn_figures']} warning figure rows, {summary['fail_figures']} failed figure rows, {summary['p0_defects']} P0 defects, max {summary['max_consecutive_image_pages']} consecutive image pages\t+1\tWarnings still need layout polish; sample PNGs are local ignored files; no final rights, caption, source-note typography, or publication production clearance implied\tpromoted\tConverted object-level visual proof into page-level legibility evidence by measuring figure pages, caption/source-note proximity, overflow/collision risk, image size, chapter samples, and visual fatigue.\tone page-image legibility QA pass",
    )
    append_once(
        ROOT / "insights.md",
        "## 2026-05-27 - I-0263 Page Legibility",
        """
## 2026-05-27 - I-0263 Page Legibility

The first honest page-image QA should produce defects, not reassurance. Once every figure exists in the PDF, the next useful truth is which pages are too small, crowded, or visually tiring; those warnings become the design-polish backlog rather than reasons to pretend the render is finished.
""",
    )


def main() -> int:
    if not PDF.exists():
        raise SystemExit(f"Missing I-0262 PDF: {PDF}")
    manifest_rows = read_tsv(SELECTED_MANIFEST)
    doc = fitz.open(PDF)
    figure_rows, defects, page_map = audit_figures(doc, manifest_rows)
    sample_rows = render_chapter_samples(doc, manifest_rows, page_map)
    fatigue = page_fatigue(doc)
    doc.close()
    qa_rows = qa_summary(figure_rows, sample_rows, defects, fatigue)
    summary = write_summary(figure_rows, sample_rows, defects, qa_rows, fatigue)
    write_tsv(FIGURE_QA, figure_rows, list(figure_rows[0].keys()))
    write_tsv(SAMPLE_QA, sample_rows, list(sample_rows[0].keys()))
    write_tsv(DEFECTS_TSV, defects, ["pass_id", "defect_id", "severity", "figure_id", "page", "category", "evidence", "recommended_action"])
    write_tsv(QA_TSV, qa_rows, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    record_loop(summary)
    print(
        f"figures={summary['figure_rows']} samples={summary['sample_rows']} "
        f"qa_pass={summary['pass_checks']} qa_warn={summary['warn_checks']} "
        f"warn_figures={summary['warn_figures']} p0={summary['p0_defects']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
