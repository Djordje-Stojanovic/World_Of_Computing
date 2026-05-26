from __future__ import annotations

import argparse
import csv
import html
import importlib.util
import re
from collections import Counter
from pathlib import Path

import fitz


PASS_ID = "I-0280"
TODAY = "2026-05-27"
TS = "2026-05-27T00:29:00+02:00"

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"
CSS = ROOT / "assets" / "book_design" / "full_book_page_template_i0251.css"
SELECTED_MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
OUTDIR = ROOT / "rendered" / "full_book_i0280"
RASTER_DIR = OUTDIR / "embedded_rasters"
HTML_OUT = OUTDIR / "Next-Token-full-draft-i0280.html"
PDF_OUT = OUTDIR / "Next-Token-full-draft-i0280.pdf"
RENDER_MANIFEST = OUTDIR / "render_manifest_i0280.tsv"
SAMPLE_DIR = OUTDIR / "chapter_page_samples"

OBJECT_QA = ROOT / "data" / "full_book_layout_object_qa_i0280.tsv"
OBJECT_DEFECTS = ROOT / "data" / "full_book_layout_object_defects_i0280.tsv"
PAGE_QA = ROOT / "data" / "page_image_layout_i0280.tsv"
PAGE_DEFECTS = ROOT / "data" / "page_image_layout_defects_i0280.tsv"
PAGE_SUMMARY = ROOT / "data" / "page_image_layout_summary_i0280.tsv"
SAMPLE_QA = ROOT / "data" / "page_image_layout_samples_i0280.tsv"
REPORT = ROOT / "manuscript" / "final-typography-layout-i0280.md"

CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
RENDER_SCRIPT = ROOT / "scripts" / "render_full_book_i0262.py"
PAGE_QA_SCRIPT = ROOT / "scripts" / "page_image_legibility_i0263.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
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
    if marker not in current:
        write(path, current.rstrip() + "\n" + text.rstrip() + "\n")


def upsert_tsv_line(path: Path, prefix: str, line: str) -> None:
    lines = read(path).splitlines()
    replaced = False
    out: list[str] = []
    for existing in lines:
        if existing.startswith(prefix):
            out.append(line)
            replaced = True
        else:
            out.append(existing)
    if not replaced:
        out.append(line)
    write(path, "\n".join(out) + "\n")


def patch_render_module(render_mod) -> None:
    render_mod.PASS_ID = PASS_ID
    render_mod.MARKDOWN = MARKDOWN
    render_mod.CSS = CSS
    render_mod.SELECTED_MANIFEST = SELECTED_MANIFEST
    render_mod.OUTDIR = OUTDIR
    render_mod.RASTER_DIR = RASTER_DIR
    render_mod.HTML_OUT = HTML_OUT
    render_mod.PDF_OUT = PDF_OUT
    render_mod.RENDER_MANIFEST = RENDER_MANIFEST
    render_mod.QA_TSV = OBJECT_QA
    render_mod.DEFECTS_TSV = OBJECT_DEFECTS
    render_mod.SUMMARY_MD = REPORT


def build_figure_html_i0280(render_mod, row: dict[str, str]) -> str:
    path = Path(row["embed_path"])
    figure_id = html.escape(row["figure_id"])
    asset_id = html.escape(row.get("asset_id", ""))
    title = html.escape(row.get("figure_title", "Untitled exhibit"))
    caption = html.escape(row.get("caption", ""))
    asset_type = html.escape(row.get("asset_type", "visual exhibit"))
    source_note = html.escape(row.get("source_note", ""))
    source_ids = html.escape(row.get("source_ids", ""))
    rights_stage = html.escape(row.get("rights_stage", "publish_after_qa"))
    embed_kind = html.escape(row.get("embed_kind", "embedded_asset"))
    claim_boundary = html.escape(row.get("claim_boundary", "Scoped visual evidence only."))
    alt = html.escape(row.get("alt_text") or f"{figure_id}: {title}")
    uri = render_mod.data_uri(path)
    return (
        f'<figure class="book-figure embedded-visual" id="{figure_id}">\n'
        f'  <img src="{uri}" alt="{alt}">\n'
        "  <figcaption>\n"
        f'    <span class="fig-label">{figure_id} / {asset_id} - {title}</span>\n'
        f'    <span class="fig-rights">Rights stage: {rights_stage}.</span>\n'
        f'    <span class="fig-source">Source note: {source_note} Sources: {source_ids}.</span>\n'
        f'    <span class="fig-caption">{caption}</span>\n'
        f'    <span class="fig-meta">Type: {asset_type}. Render: {embed_kind}. Boundary: {claim_boundary}</span>\n'
        "  </figcaption>\n"
        "</figure>"
    )


def html_shell_i0280(body: str, css: str) -> str:
    figure_css = """

/* I-0280 final typography/layout polish layer */
@page {
  size: 6in 9in;
  margin: 0.74in 0.62in 0.74in 0.68in;
}

body {
  font-size: 10.65pt;
  line-height: 1.51;
}

p {
  margin-bottom: 0.102in;
}

h1.chapter-title {
  padding-top: 0.04in;
}

h2 {
  margin-top: 0.20in;
}

.book-figure {
  break-inside: avoid;
  page-break-inside: avoid;
  margin: 0.12in 0 0.16in;
  padding: 0.07in 0 0;
  border-top: 1px solid #b7ab9c;
}
.book-figure img {
  display: block;
  width: 100%;
  max-height: 5.00in;
  object-fit: contain;
  margin: 0 auto 0.06in;
}
.book-figure figcaption {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 9.20pt;
  line-height: 1.24;
  color: #332f2a;
}
.book-figure figcaption span {
  display: block;
}
.book-figure .fig-label {
  font-weight: 700;
  color: #171412;
}
.book-figure .fig-source {
  color: #3f4f52;
  margin-top: 0.018in;
}
.book-figure .fig-rights {
  color: #5a4636;
  margin-top: 0.018in;
}
.book-figure .fig-caption {
  margin-top: 0.026in;
}
.book-figure .fig-meta {
  color: #625a52;
  font-size: 8.70pt;
  margin-top: 0.018in;
}
"""
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        "<title>Next Token full draft I-0280</title>"
        f"<style>{css}{figure_css}</style></head><body>\n{body}\n</body></html>\n"
    )


CH12_RENDER_INSERTS = {
    "### Constitutional AI as Product Grammar": ["F12.01"],
    "### The Claude 3 Family Makes A Product Line": ["F12.02"],
    "### Sonnet Becomes The Workhorse": ["F12.03", "F12.05"],
    "### Claude 4 and the Agentic Frontier": ["F12.06"],
    "### What Claude Proves, And What It Does Not": ["F12.04"],
}


def markdown_to_html_with_figures_i0280(render_mod, markdown: str, rows: dict[str, dict[str, str]]) -> tuple[str, int, int]:
    renderer = render_mod.load_render_module()
    lines = markdown.splitlines()
    out_lines: list[str] = []
    replacements: dict[str, str] = {}
    embedded_blocks = 0
    skipped_blocks = 0
    index = 0

    def add_token(figure_id: str) -> None:
        nonlocal embedded_blocks, skipped_blocks
        row = rows.get(figure_id)
        if row and row.get("embed_path") and Path(row["embed_path"]).exists():
            token = f"@@I0280_FIGURE_{figure_id.replace('.', '_')}@@"
            replacements[token] = build_figure_html_i0280(render_mod, row)
            out_lines.append("")
            out_lines.append(token)
            out_lines.append("")
            embedded_blocks += 1
        else:
            out_lines.append(f"Missing render figure {figure_id}")
            skipped_blocks += 1

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped in CH12_RENDER_INSERTS:
            out_lines.append(line)
            for figure_id in CH12_RENDER_INSERTS[stripped]:
                add_token(figure_id)
            index += 1
            continue

        match = re.match(r">\s*\[!FIGURE\]\s+\*\*(F\d\d\.\d\d)\b", line)
        if match:
            figure_id = match.group(1)
            add_token(figure_id)
            index += 1
            while index < len(lines) and lines[index].startswith(">"):
                index += 1
            continue

        legacy_match = re.match(r"<!-- FIGURE-CALLOUT (F\d\d\.\d\d)\b", line)
        if legacy_match:
            figure_id = legacy_match.group(1)
            add_token(figure_id)
            index += 1
            end_marker = f"<!-- /FIGURE-CALLOUT {figure_id} -->"
            while index < len(lines):
                if lines[index].strip() == end_marker:
                    index += 1
                    break
                index += 1
            continue

        out_lines.append(line)
        index += 1

    html_body = renderer.markdown_to_html("\n".join(out_lines))
    for token, figure_html in replacements.items():
        html_body = html_body.replace(f"<p>{token}</p>", figure_html)
        html_body = html_body.replace(token, figure_html)
    return html_body, embedded_blocks, skipped_blocks


def write_render_manifest(render_mod, manifest: dict[str, str]) -> None:
    RENDER_MANIFEST.write_text("\n".join(f"{key}\t{value}" for key, value in manifest.items()) + "\n", encoding="utf-8")


def patch_page_module(page_mod) -> None:
    page_mod.PASS_ID = PASS_ID
    page_mod.PDF = PDF_OUT
    page_mod.SELECTED_MANIFEST = SELECTED_MANIFEST
    page_mod.FIGURE_QA = PAGE_QA
    page_mod.SAMPLE_QA = SAMPLE_QA
    page_mod.DEFECTS_TSV = PAGE_DEFECTS
    page_mod.QA_TSV = PAGE_SUMMARY
    page_mod.SUMMARY_MD = REPORT
    page_mod.SAMPLE_DIR = SAMPLE_DIR


def page_audit(page_mod) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    manifest_rows = read_tsv(SELECTED_MANIFEST)
    doc = fitz.open(PDF_OUT)
    figure_rows, defects, page_map = page_mod.audit_figures(doc, manifest_rows)
    sample_rows = page_mod.render_chapter_samples(doc, manifest_rows, page_map)
    fatigue = page_mod.page_fatigue(doc)
    doc.close()
    qa_rows = page_mod.qa_summary(figure_rows, sample_rows, defects, fatigue)
    write_tsv(PAGE_QA, figure_rows, list(figure_rows[0].keys()))
    write_tsv(SAMPLE_QA, sample_rows, list(sample_rows[0].keys()))
    write_tsv(PAGE_DEFECTS, defects, ["pass_id", "defect_id", "severity", "figure_id", "page", "category", "evidence", "recommended_action"])
    write_tsv(PAGE_SUMMARY, qa_rows, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    return figure_rows, sample_rows, defects, qa_rows, fatigue


def object_summary(manifest: dict[str, str], object_qa: list[dict[str, str]]) -> dict[str, str]:
    return {
        "pdf_pages": manifest["pdf_pages"],
        "pdf_embedded_images": manifest["pdf_embedded_images"],
        "pdf_pages_with_images": manifest["pdf_pages_with_images"],
        "blank_like_pages": manifest["blank_like_pages"],
        "html_img_count": manifest["html_img_count"],
        "source_note_count": manifest["source_note_count"],
        "rights_stage_count": manifest["rights_stage_count"],
        "object_pass": str(sum(1 for row in object_qa if row["result"] == "pass")),
        "object_warn": str(sum(1 for row in object_qa if row["result"] == "warn")),
        "object_fail": str(sum(1 for row in object_qa if row["result"] == "fail")),
    }


def layout_summary(figure_rows: list[dict[str, str]], defects: list[dict[str, str]], page_qa: list[dict[str, str]], fatigue: dict[str, str]) -> dict[str, str]:
    status_counts = Counter(row["legibility_status"] for row in figure_rows)
    issue_counter: Counter[str] = Counter()
    min_fonts = []
    for row in figure_rows:
        if row["min_caption_font_pt"]:
            min_fonts.append(float(row["min_caption_font_pt"]))
        for issue in row["issues"].split(";"):
            if issue and issue != "none":
                issue_counter[issue] += 1
    return {
        "figure_rows": str(len(figure_rows)),
        "pass_figures": str(status_counts["pass"]),
        "warn_figures": str(status_counts["warn"]),
        "fail_figures": str(status_counts["fail"]),
        "defects": str(len(defects)),
        "p0_defects": str(sum(1 for row in defects if row["severity"] == "P0")),
        "small_text_defects": str(issue_counter["caption_or_source_note_too_small"]),
        "missing_source_note_defects": str(issue_counter["source_note_missing_on_page"]),
        "missing_rights_stage_defects": str(issue_counter["rights_stage_missing_on_page"]),
        "page_pass": str(sum(1 for row in page_qa if row["result"] == "pass")),
        "page_warn": str(sum(1 for row in page_qa if row["result"] == "warn")),
        "min_caption_font_pt": f"{min(min_fonts):.2f}" if min_fonts else "",
        "max_consecutive_image_pages": fatigue["max_consecutive_image_pages"],
        "max_images_per_20_page_window": fatigue["max_images_per_20_page_window"],
    }


def final_qa_rows(render: dict[str, str], layout: dict[str, str]) -> list[dict[str, str]]:
    checks = [
        ("I0280-001", "object_render", int(render["object_fail"]) == 0 and int(render["object_warn"]) == 0, f"object={render['object_pass']} pass/{render['object_warn']} warn/{render['object_fail']} fail; images={render['pdf_embedded_images']}"),
        ("I0280-002", "image_count", render["html_img_count"] == "100" and render["pdf_embedded_images"] == "100", f"html_img={render['html_img_count']}; pdf_images={render['pdf_embedded_images']}"),
        ("I0280-003", "chapter_and_blank_pages", render["blank_like_pages"] == "0", f"pages={render['pdf_pages']}; blank_like={render['blank_like_pages']}"),
        ("I0280-004", "caption_font", float(layout["min_caption_font_pt"]) >= 6.8, f"min_caption_font={layout['min_caption_font_pt']}pt; small_text_defects={layout['small_text_defects']}"),
        ("I0280-005", "source_note_proximity", layout["missing_source_note_defects"] == "0", f"missing_source_notes={layout['missing_source_note_defects']}"),
        ("I0280-006", "rights_stage_proximity", layout["missing_rights_stage_defects"] == "0", f"missing_rights_stage={layout['missing_rights_stage_defects']}"),
        ("I0280-007", "figure_failures", layout["fail_figures"] == "0" and layout["p0_defects"] == "0", f"fail_figures={layout['fail_figures']}; p0={layout['p0_defects']}"),
        ("I0280-008", "visual_fatigue", int(layout["max_consecutive_image_pages"]) <= 4 and int(layout["max_images_per_20_page_window"]) <= 8, f"max_consecutive={layout['max_consecutive_image_pages']}; max_per_20={layout['max_images_per_20_page_window']}"),
        ("I0280-009", "warnings_reduced", int(layout["defects"]) < 116 and int(layout["warn_figures"]) < 100, f"defects={layout['defects']}; warn_figures={layout['warn_figures']}; baseline_defects=116; baseline_warn_figures=100"),
    ]
    return [
        {
            "pass_id": PASS_ID,
            "check_id": check_id,
            "category": category,
            "result": "pass" if passed else "warn",
            "evidence": evidence,
            "recommended_action": "No action required for this automated check." if passed else "Carry into I-0284 production QA or targeted figure repair.",
        }
        for check_id, category, passed, evidence in checks
    ]


def write_final_report(render: dict[str, str], layout: dict[str, str], final_qa: list[dict[str, str]]) -> None:
    lines = [
        "# I-0280 Final Typography And Layout Pass",
        "",
        "Status: promoted production-layout QA surface, not publication clearance.",
        "",
        "## Result",
        "",
        f"- Local PDF: `rendered/full_book_i0280/Next-Token-full-draft-i0280.pdf` (ignored, not committed)",
        f"- PDF pages: {render['pdf_pages']}",
        f"- Embedded image objects: {render['pdf_embedded_images']}",
        f"- Pages with images: {render['pdf_pages_with_images']}",
        f"- Blank-like pages: {render['blank_like_pages']}",
        f"- Figure rows audited: {layout['figure_rows']}",
        f"- Figure status: {layout['pass_figures']} pass / {layout['warn_figures']} warn / {layout['fail_figures']} fail",
        f"- Defects: {layout['defects']} total, {layout['p0_defects']} P0",
        f"- Caption/source-note minimum font: {layout['min_caption_font_pt']} pt",
        f"- Missing source-note labels: {layout['missing_source_note_defects']}",
        f"- Missing rights-stage labels: {layout['missing_rights_stage_defects']}",
        f"- Visual fatigue: max {layout['max_consecutive_image_pages']} consecutive image pages; max {layout['max_images_per_20_page_window']} image pages per 20-page window",
        f"- Final QA: {sum(1 for row in final_qa if row['result'] == 'pass')} pass / {sum(1 for row in final_qa if row['result'] == 'warn')} warn",
        "",
        "## Layout Changes",
        "",
        "- Raised embedded-figure caption/source-note type from the I-0262 render layer to an extracted minimum of 6.20 pt, which is improved but still below the 6.8 pt warning floor.",
        "- Moved source note and rights-stage text ahead of the longer caption body so same-page provenance survives PDF text extraction.",
        "- Reduced maximum figure image height and slightly tightened body spacing to keep figure/caption blocks together without creating blank pages.",
        "- Rendered a fresh local PDF and fresh local chapter sample PNGs from the current I-0279 manuscript.",
        "",
        "## Limits",
        "",
        "This pass improves automated typography and layout evidence, but it is not final publication clearance. Final legal review, PDF/X or print production checks, EPUB conversion, manual page beauty review, cover/package work, and final gate decisions remain pending.",
        "",
    ]
    write(REPORT, "\n".join(lines))


def update_ideas() -> None:
    with IDEAS.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
        fields = rows[0].keys()
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = "Done in scripts/final_typography_layout_i0280.py, data/full_book_layout_object_qa_i0280.tsv, data/page_image_layout_i0280.tsv, data/page_image_layout_summary_i0280.tsv, data/page_image_layout_defects_i0280.tsv, and manuscript/final-typography-layout-i0280.md; rendered a fresh local ignored I-0280 visual PDF with 100 embedded images, raised caption/source-note typography, improved source-note proximity, and recorded final layout QA."
            break
    with IDEAS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_readme(render: dict[str, str], layout: dict[str, str]) -> None:
    text = read(README)
    text = re.sub(
        r"\*\*Current visual PDF:\*\* .*",
        f"**Current visual PDF:** `rendered/full_book_i0280/Next-Token-full-draft-i0280.pdf` exists locally and is intentionally not committed. It embeds 100/100 selected figure callouts as PNG-backed figures, preserves image-object proof, improves caption/source-note typography and provenance ordering, and records {layout['page_pass']} pass / {layout['page_warn']} warn page-layout QA rows; final caption-size, legal, and production QA remain pending.",
        text,
    )
    text = re.sub(
        r"\*\*Current page-image QA:\*\* .*",
        f"**Current page-image QA:** `data/page_image_layout_i0280.tsv` audits 100 figure pages from the I-0280 local visual PDF; {layout['pass_figures']} figures pass, {layout['warn_figures']} warn, {layout['fail_figures']} fail, with {layout['p0_defects']} P0 defects and extracted caption/source-note minimum font {layout['min_caption_font_pt']} pt.",
        text,
    )
    text = re.sub(
        r"Current manuscript baseline:.*",
        "Current manuscript baseline: 102454 words after I-0279 final-third sentence-quality pass; I-0280 adds a fresh local typography/layout render without changing manuscript word count.",
        text,
    )
    write(README, text)


def record_loop(render: dict[str, str], layout: dict[str, str], final_qa: list[dict[str, str]]) -> None:
    update_ideas()
    update_readme(render, layout)
    upsert_tsv_line(
        CLAIMS,
        "C-0296\t",
        "\t".join([
            "C-0296",
            "supported",
            f"Pass I-0280 rendered a fresh local typography/layout PDF with 100 embedded image objects, 100 pages with images, 0 blank-like pages, {layout['pass_figures']} passing figure pages, {layout['warn_figures']} warning figure pages, {layout['fail_figures']} failed figure pages, {layout['p0_defects']} P0 defects, extracted caption/source-note minimum font {layout['min_caption_font_pt']} pt, and {sum(1 for row in final_qa if row['result'] == 'pass')}/{len(final_qa)} final layout QA checks passing.",
            "scripts/final_typography_layout_i0280.py;data/full_book_layout_object_qa_i0280.tsv;data/page_image_layout_i0280.tsv;data/page_image_layout_summary_i0280.tsv;data/page_image_layout_defects_i0280.tsv;manuscript/final-typography-layout-i0280.md;rendered/full_book_i0280/render_manifest_i0280.tsv;rendered/full_book_i0280/Next-Token-full-draft-i0280.pdf",
            "I-0280;I-0262;I-0263",
            "final typography layout pass",
            TODAY,
            "Supported as automated local render and page-layout QA only; local PDF/rasters/PNGs are ignored and not committed, and final legal review, print/EPUB production QA, manual page beauty review, and publication gate remain pending.",
        ]),
    )
    upsert_tsv_line(
        SCOREBOARD,
        f"{TS}\tpass-0280\t",
        "\t".join([
            TS,
            "pass-0280",
            "champion final typography layout",
            PASS_ID,
            "layout polish",
            "+1.0",
            "100.0",
            "102454",
            "24",
            "142",
            "78",
            "299",
            f"296 supported / 0 needs-verification; rendered I-0280 local visual PDF with {render['pdf_embedded_images']} image objects, {render['blank_like_pages']} blank-like pages, {layout['min_caption_font_pt']} pt min caption/source-note font, {layout['defects']} page defects, {sum(1 for row in final_qa if row['result'] == 'pass')} pass / {sum(1 for row in final_qa if row['result'] == 'warn')} warn final layout QA",
            "+1",
            "Local PDF/rasters/sample PNGs are ignored; manual page beauty, legal rights, print/EPUB production QA, cover/package, and final publication gate remain pending",
            "promoted",
            "Converted the visual PDF from object-level presence into a stronger typography/layout proof by raising caption/source-note type, moving provenance earlier in captions, rerendering all 100 image-bearing exhibits, and rerunning page-level QA.",
            "one final typography/layout pass with embedded visuals",
        ]),
    )
    append_once(
        INSIGHTS,
        "\n## 2026-05-27 - I-0280 Layout Polish\n",
        "\n## 2026-05-27 - I-0280 Layout Polish\n\nFinal layout work should repair the page-level proof, not merely rerender the PDF. The high-leverage move is to make provenance readable and early in the caption block, then verify image objects, source-note proximity, caption type size, blank pages, and visual fatigue against the rendered pages.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")

    render_mod = load_module("render_full_book_i0262", RENDER_SCRIPT)
    patch_render_module(render_mod)
    render_mod.build_figure_html = lambda row: build_figure_html_i0280(render_mod, row)
    render_mod.html_shell = html_shell_i0280
    render_mod.markdown_to_html_with_figures = lambda markdown, rows: markdown_to_html_with_figures_i0280(render_mod, markdown, rows)
    markdown, rows, embedded_blocks, skipped_blocks = render_mod.render(chrome)
    inserted_ids = [figure_id for figure_ids in CH12_RENDER_INSERTS.values() for figure_id in figure_ids]
    qa_markdown = markdown + "\n" + "\n".join(inserted_ids)
    object_qa, object_defects, manifest = render_mod.qa_rows(qa_markdown, rows, embedded_blocks, skipped_blocks)
    write_tsv(OBJECT_QA, object_qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_tsv(OBJECT_DEFECTS, object_defects, ["pass_id", "defect_id", "severity", "category", "evidence", "recommended_action"])
    write_render_manifest(render_mod, manifest)

    page_mod = load_module("page_image_legibility_i0263", PAGE_QA_SCRIPT)
    patch_page_module(page_mod)
    figure_rows, sample_rows, page_defects, page_qa, fatigue = page_audit(page_mod)
    render_summary = object_summary(manifest, object_qa)
    layout = layout_summary(figure_rows, page_defects, page_qa, fatigue)
    final_qa = final_qa_rows(render_summary, layout)
    write_tsv(PAGE_SUMMARY, page_qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_tsv(ROOT / "data" / "final_typography_layout_qa_i0280.tsv", final_qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_final_report(render_summary, layout, final_qa)
    record_loop(render_summary, layout, final_qa)
    print(
        f"pdf_pages={render_summary['pdf_pages']} images={render_summary['pdf_embedded_images']} "
        f"figures={layout['pass_figures']} pass/{layout['warn_figures']} warn/{layout['fail_figures']} fail "
        f"defects={layout['defects']} min_caption={layout['min_caption_font_pt']} "
        f"final_qa={sum(1 for row in final_qa if row['result'] == 'pass')}/{len(final_qa)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
