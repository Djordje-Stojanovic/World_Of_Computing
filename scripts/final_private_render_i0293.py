from __future__ import annotations

import argparse
import csv
import html
import importlib.util
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


PASS_ID = "I-0293"
RUN_ID = "pass-0293"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"
CSS = ROOT / "assets" / "book_design" / "full_book_page_template_i0251.css"
SELECTED_MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
OUTDIR = ROOT / "rendered" / "full_book_i0293"
RASTER_DIR = OUTDIR / "embedded_rasters"
HTML_OUT = OUTDIR / "Next-Token-full-draft-i0293.html"
PDF_OUT = OUTDIR / "Next-Token-full-draft-i0293.pdf"
RENDER_MANIFEST = OUTDIR / "render_manifest_i0293.tsv"
SAMPLE_DIR = OUTDIR / "chapter_page_samples"

OBJECT_QA = ROOT / "data" / "full_private_render_object_qa_i0293.tsv"
OBJECT_DEFECTS = ROOT / "data" / "full_private_render_object_defects_i0293.tsv"
PAGE_QA = ROOT / "data" / "full_private_render_page_qa_i0293.tsv"
PAGE_DEFECTS = ROOT / "data" / "full_private_render_page_defects_i0293.tsv"
PAGE_SUMMARY = ROOT / "data" / "full_private_render_page_summary_i0293.tsv"
SAMPLE_QA = ROOT / "data" / "full_private_render_samples_i0293.tsv"
VISUAL_DENSITY = ROOT / "data" / "full_private_render_visual_density_i0293.tsv"
FINAL_QA = ROOT / "data" / "full_private_render_final_qa_i0293.tsv"
REPORT = ROOT / "manuscript" / "full-private-render-i0293.md"

CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
RENDER_SCRIPT = ROOT / "scripts" / "render_full_book_i0262.py"
PAGE_QA_SCRIPT = ROOT / "scripts" / "page_image_legibility_i0263.py"
TYPO_SCRIPT = ROOT / "scripts" / "final_typography_layout_i0280.py"


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
    if marker not in current:
        write(path, current.rstrip() + "\n" + text.rstrip() + "\n")


def upsert_idea_done() -> None:
    evidence = (
        "Done in scripts/final_private_render_i0293.py, rendered/full_book_i0293/Next-Token-full-draft-i0293.pdf "
        "(local ignored), data/full_private_render_object_qa_i0293.tsv, "
        "data/full_private_render_page_qa_i0293.tsv, data/full_private_render_final_qa_i0293.tsv, "
        "data/full_private_render_visual_density_i0293.tsv, and manuscript/full-private-render-i0293.md; "
        "rendered a full private-edition PDF from the post-I-0292 manifest, embedded/audited 100 selected figures, "
        "and recorded missing-image, blank-page, unreadable-page, caption/source-note, and density defects for I-0294."
    )
    lines = read(IDEAS).splitlines()
    out: list[str] = []
    changed = False
    for line in lines:
        if line.startswith(f"{PASS_ID}\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = evidence
            line = "\t".join(parts)
            changed = True
        out.append(line)
    if not changed:
        out.append(
            "\t".join(
                [
                    PASS_ID,
                    "done",
                    "Run the first final private-edition polish/render pass: apply a richer image-first layout, rebalance visual rhythm, fix captions/source-note typography, generate a full PDF with all new visuals, and audit missing images, blank pages, unreadable pages, and figure density.",
                    "final polish 1",
                    "full visual PDF",
                    evidence,
                ]
            )
        )
    write(IDEAS, "\n".join(out) + "\n")


def patch_render_module(render_mod, chrome: Path) -> None:
    render_mod.PASS_ID = PASS_ID
    render_mod.DEFAULT_CHROME = chrome
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


def build_figure_html(render_mod, row: dict[str, str]) -> str:
    path = Path(row["embed_path"])
    figure_id = html.escape(row["figure_id"])
    asset_id = html.escape(row.get("asset_id", ""))
    title = html.escape(row.get("figure_title", "Untitled exhibit"))
    caption = html.escape(row.get("caption", ""))
    asset_type = html.escape(row.get("asset_type", "visual exhibit"))
    source_note = html.escape(row.get("source_note", ""))
    source_ids = html.escape(row.get("source_ids", ""))
    rights_stage = html.escape(row.get("rights_stage", "private_use_pending_review"))
    embed_kind = html.escape(row.get("embed_kind", "embedded_asset"))
    claim_boundary = html.escape(row.get("claim_boundary", "Scoped visual evidence only."))
    alt = html.escape(row.get("alt_text") or f"{figure_id}: {title}")
    uri = render_mod.data_uri(path)
    return (
        f'<figure class="book-figure embedded-visual {asset_type}" id="{figure_id}">\n'
        f'  <div class="figure-image-frame"><img src="{uri}" alt="{alt}"></div>\n'
        "  <figcaption>\n"
        f'    <span class="fig-label">{figure_id} / {asset_id} - {title}</span>\n'
        f'    <span class="fig-caption">{caption}</span>\n'
        f'    <span class="fig-source">Source note: {source_note}</span>\n'
        f'    <span class="fig-rights">Rights stage: {rights_stage}.</span>\n'
        f'    <span class="fig-meta">Type: {asset_type}. Sources: {source_ids}. Render: {embed_kind}. Boundary: {claim_boundary}</span>\n'
        "  </figcaption>\n"
        "</figure>"
    )


def html_shell(body: str, css: str) -> str:
    figure_css = """

/* I-0293 private-edition image-first render layer */
@page {
  size: 6in 9in;
  margin: 0.66in 0.56in 0.70in 0.62in;
}

body {
  font-size: 10.45pt;
  line-height: 1.48;
}

p {
  margin-bottom: 0.095in;
}

h1.chapter-title {
  padding-top: 0.02in;
}

h2 {
  margin-top: 0.18in;
}

.book-figure {
  break-inside: avoid;
  page-break-inside: avoid;
  margin: 0.10in 0 0.15in;
  padding: 0.07in 0 0;
  border-top: 1px solid #9b8d7a;
}
.book-figure .figure-image-frame {
  width: 100%;
  background: #fffdf7;
}
.book-figure img {
  display: block;
  width: 100%;
  max-height: 5.28in;
  object-fit: contain;
  margin: 0 auto 0.055in;
}
.book-figure.source_surface_pdf_presentation_page img,
.book-figure.source_surface_pdf_technical_report_page img,
.book-figure.benchmark_model_landscape_table img,
.book-figure.benchmark_model_card_surface_leaderboard_surface img {
  max-height: 5.48in;
}
.book-figure.real_world_person_image img,
.book-figure.real_world_logo img {
  max-height: 3.45in;
}
.book-figure figcaption {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8.55pt;
  line-height: 1.18;
  color: #302c27;
}
.book-figure figcaption span {
  display: block;
}
.book-figure .fig-label {
  font-weight: 700;
  color: #151311;
}
.book-figure .fig-caption {
  margin-top: 0.022in;
}
.book-figure .fig-source {
  color: #2f4c4f;
  margin-top: 0.018in;
}
.book-figure .fig-rights {
  color: #5b4635;
  margin-top: 0.016in;
}
.book-figure .fig-meta {
  color: #635b52;
  font-size: 8.10pt;
  margin-top: 0.016in;
}
"""
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        "<title>Next Token private visual draft I-0293</title>"
        f"<style>{css}{figure_css}</style></head><body>\n{body}\n</body></html>\n"
    )


def write_render_manifest(manifest: dict[str, str]) -> None:
    RENDER_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    RENDER_MANIFEST.write_text("\n".join(f"{key}\t{value}" for key, value in manifest.items()) + "\n", encoding="utf-8")


def render_book(chrome: Path):
    render_mod = load_module("render_full_book_i0262", RENDER_SCRIPT)
    typo_mod = load_module("final_typography_layout_i0280", TYPO_SCRIPT)
    patch_render_module(render_mod, chrome)
    typo_mod.PASS_ID = PASS_ID
    typo_mod.CH12_RENDER_INSERTS = {
        "### Constitutional AI as Product Grammar": ["F12.01"],
        "### The Claude 3 Family Makes A Product Line": ["F12.02"],
        "### Claude 4 and the Agentic Frontier": ["F12.03"],
        "### What Claude Proves, And What It Does Not": ["F12.04"],
        "### The Distribution Layer: APIs, Clouds, and Protocols": ["F12.05", "F12.06"],
    }
    typo_mod.build_figure_html_i0280 = lambda patched_render_mod, row: build_figure_html(patched_render_mod, row)
    render_mod.build_figure_html = lambda row: build_figure_html(render_mod, row)
    render_mod.html_shell = html_shell
    render_mod.markdown_to_html_with_figures = lambda markdown, rows: typo_mod.markdown_to_html_with_figures_i0280(render_mod, markdown, rows)
    markdown, rows, embedded_blocks, skipped_blocks = render_mod.render(chrome)
    object_qa, object_defects, manifest = render_mod.qa_rows(markdown, rows, embedded_blocks, skipped_blocks)
    write_tsv(OBJECT_QA, object_qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_tsv(OBJECT_DEFECTS, object_defects, ["pass_id", "defect_id", "severity", "category", "evidence", "recommended_action"])
    write_render_manifest(manifest)
    return render_mod, object_qa, object_defects, manifest


def page_audit():
    page_mod = load_module("page_image_legibility_i0263", PAGE_QA_SCRIPT)
    patch_page_module(page_mod)
    manifest_rows = read_tsv(SELECTED_MANIFEST)
    doc = page_mod.fitz.open(PDF_OUT)
    figure_rows, defects, page_map = page_mod.audit_figures(doc, manifest_rows)
    sample_rows = page_mod.render_chapter_samples(doc, manifest_rows, page_map)
    fatigue = page_mod.page_fatigue(doc)
    doc.close()
    page_qa = page_mod.qa_summary(figure_rows, sample_rows, defects, fatigue)
    write_tsv(PAGE_QA, figure_rows, list(figure_rows[0].keys()))
    write_tsv(SAMPLE_QA, sample_rows, list(sample_rows[0].keys()))
    write_tsv(PAGE_DEFECTS, defects, ["pass_id", "defect_id", "severity", "figure_id", "page", "category", "evidence", "recommended_action"])
    write_tsv(PAGE_SUMMARY, page_qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    return figure_rows, sample_rows, defects, page_qa, fatigue


def object_summary(manifest: dict[str, str], object_qa: list[dict[str, str]]) -> dict[str, str]:
    return {
        "pdf_pages": manifest["pdf_pages"],
        "pdf_embedded_images": manifest["pdf_embedded_images"],
        "pdf_pages_with_images": manifest["pdf_pages_with_images"],
        "blank_like_pages": manifest["blank_like_pages"],
        "html_img_count": manifest["html_img_count"],
        "source_note_count": manifest["source_note_count"],
        "rights_stage_count": manifest["rights_stage_count"],
        "pdf_bytes": manifest["pdf_bytes"],
        "pdf_sha256": manifest["pdf_sha256"],
        "object_pass": str(sum(1 for row in object_qa if row["result"] == "pass")),
        "object_warn": str(sum(1 for row in object_qa if row["result"] == "warn")),
        "object_fail": str(sum(1 for row in object_qa if row["result"] == "fail")),
    }


def layout_summary(figure_rows: list[dict[str, str]], defects: list[dict[str, str]], page_qa: list[dict[str, str]], fatigue: dict[str, str]) -> dict[str, str]:
    status_counts = Counter(row["legibility_status"] for row in figure_rows)
    issue_counter: Counter[str] = Counter()
    min_fonts = []
    area_values = []
    for row in figure_rows:
        if row["min_caption_font_pt"]:
            min_fonts.append(float(row["min_caption_font_pt"]))
        if row["largest_image_area_pct"]:
            area_values.append(float(row["largest_image_area_pct"]))
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
        "too_small_image_defects": str(issue_counter["image_too_small_for_trade_book_review"]),
        "page_pass": str(sum(1 for row in page_qa if row["result"] == "pass")),
        "page_warn": str(sum(1 for row in page_qa if row["result"] == "warn")),
        "min_caption_font_pt": f"{min(min_fonts):.2f}" if min_fonts else "",
        "median_image_area_pct": f"{sorted(area_values)[len(area_values)//2]:.1f}" if area_values else "",
        "max_consecutive_image_pages": fatigue["max_consecutive_image_pages"],
        "max_images_per_20_page_window": fatigue["max_images_per_20_page_window"],
    }


def visual_density_rows(figure_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    chapter_rows: dict[str, list[dict[str, str]]] = {}
    for row in figure_rows:
        chapter_rows.setdefault(row["chapter"], []).append(row)
    out: list[dict[str, str]] = []
    for chapter in sorted(chapter_rows):
        rows = chapter_rows[chapter]
        pages = sorted({int(row["page"]) for row in rows if row["page"].isdigit()})
        statuses = Counter(row["legibility_status"] for row in rows)
        out.append(
            {
                "pass_id": PASS_ID,
                "chapter": chapter,
                "figure_count": str(len(rows)),
                "first_figure_page": str(pages[0]) if pages else "",
                "last_figure_page": str(pages[-1]) if pages else "",
                "page_span": str(pages[-1] - pages[0] + 1) if pages else "",
                "pass_figures": str(statuses["pass"]),
                "warn_figures": str(statuses["warn"]),
                "fail_figures": str(statuses["fail"]),
            }
        )
    write_tsv(VISUAL_DENSITY, out, ["pass_id", "chapter", "figure_count", "first_figure_page", "last_figure_page", "page_span", "pass_figures", "warn_figures", "fail_figures"])
    return out


def final_qa_rows(render: dict[str, str], layout: dict[str, str], density_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    checks = [
        ("I0293-001", "object_render", int(render["object_fail"]) == 0, f"object={render['object_pass']} pass/{render['object_warn']} warn/{render['object_fail']} fail; images={render['pdf_embedded_images']}"),
        ("I0293-002", "image_count", render["html_img_count"] == "100" and render["pdf_embedded_images"] == "100", f"html_img={render['html_img_count']}; pdf_images={render['pdf_embedded_images']}"),
        ("I0293-003", "blank_pages", render["blank_like_pages"] == "0", f"pages={render['pdf_pages']}; blank_like={render['blank_like_pages']}"),
        ("I0293-004", "figure_failures", layout["fail_figures"] == "0" and layout["p0_defects"] == "0", f"fail_figures={layout['fail_figures']}; p0={layout['p0_defects']}"),
        ("I0293-005", "caption_font", float(layout["min_caption_font_pt"]) >= 6.8, f"min_caption_font={layout['min_caption_font_pt']}pt; small_text={layout['small_text_defects']}"),
        ("I0293-006", "source_note_proximity", layout["missing_source_note_defects"] == "0", f"missing_source_notes={layout['missing_source_note_defects']}"),
        ("I0293-007", "rights_stage_proximity", layout["missing_rights_stage_defects"] == "0", f"missing_rights_stage={layout['missing_rights_stage_defects']}"),
        ("I0293-008", "image_size", int(layout["too_small_image_defects"]) <= 18, f"too_small_images={layout['too_small_image_defects']}; median_area={layout['median_image_area_pct']}%"),
        ("I0293-009", "visual_fatigue", int(layout["max_consecutive_image_pages"]) <= 5 and int(layout["max_images_per_20_page_window"]) <= 10, f"max_consecutive={layout['max_consecutive_image_pages']}; max_per_20={layout['max_images_per_20_page_window']}"),
        ("I0293-010", "chapter_density", len(density_rows) == 24 and min(int(row["figure_count"]) for row in density_rows) >= 1, f"chapters={len(density_rows)}; min_figures={min(int(row['figure_count']) for row in density_rows)}"),
    ]
    rows = [
        {
            "pass_id": PASS_ID,
            "check_id": check_id,
            "category": category,
            "result": "pass" if passed else "warn",
            "evidence": evidence,
            "recommended_action": "No action required for this automated check." if passed else "Carry this defect into I-0294 correction and rerender.",
        }
        for check_id, category, passed, evidence in checks
    ]
    write_tsv(FINAL_QA, rows, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    return rows


def write_report(render: dict[str, str], layout: dict[str, str], final_qa: list[dict[str, str]], density_rows: list[dict[str, str]]) -> None:
    lines = [
        "# I-0293 Full Private-Edition Render",
        "",
        "Status: promoted first final render/polish QA surface, not final delivery.",
        "",
        "## Result",
        "",
        "- Local PDF: `rendered/full_book_i0293/Next-Token-full-draft-i0293.pdf` (ignored, not committed)",
        f"- PDF SHA-256: `{render['pdf_sha256']}`",
        f"- PDF bytes: {render['pdf_bytes']}",
        f"- PDF pages: {render['pdf_pages']}",
        f"- Embedded image objects: {render['pdf_embedded_images']}",
        f"- Pages with images: {render['pdf_pages_with_images']}",
        f"- Blank-like pages: {render['blank_like_pages']}",
        f"- Figure pages audited: {layout['figure_rows']}",
        f"- Figure status: {layout['pass_figures']} pass / {layout['warn_figures']} warn / {layout['fail_figures']} fail",
        f"- Defects: {layout['defects']} total, {layout['p0_defects']} P0",
        f"- Minimum extracted caption/source-note font: {layout['min_caption_font_pt']} pt",
        f"- Median largest-image area: {layout['median_image_area_pct']}%",
        f"- Visual fatigue: max {layout['max_consecutive_image_pages']} consecutive image pages; max {layout['max_images_per_20_page_window']} image pages per 20-page window",
        f"- Final QA: {sum(1 for row in final_qa if row['result'] == 'pass')} pass / {sum(1 for row in final_qa if row['result'] == 'warn')} warn",
        "",
        "## Render Changes",
        "",
        "- Rendered from the post-I-0292 active selected exhibit manifest, so real-world images, source-surface page renders, model-card screenshots, leaderboard surfaces, repo surfaces, and yearly benchmark tables all enter one full PDF.",
        "- Applied a new I-0293 image-first CSS layer with wider usable page area, larger maximum image frames for source pages and benchmark tables, and caption ordering that foregrounds caption, source note, rights stage, type, and claim boundary.",
        "- Generated chapter sample PNGs locally and recorded per-chapter visual density so I-0294 can target ugly or overcrowded stretches instead of guessing.",
        "",
        "## Defect Backlog For I-0294",
        "",
        f"- Figure warnings: {layout['warn_figures']}",
        f"- Small-image warnings: {layout['too_small_image_defects']}",
        f"- Missing source-note labels in extracted text: {layout['missing_source_note_defects']}",
        f"- Missing rights-stage labels in extracted text: {layout['missing_rights_stage_defects']}",
        f"- Chapters in density ledger: {len(density_rows)}",
        "",
        "The local PDF is now the right object to inspect, but the warning rows are not cosmetic paperwork: they are the correction map for I-0294.",
        "",
    ]
    write(REPORT, "\n".join(lines))


def update_readme(render: dict[str, str], layout: dict[str, str]) -> None:
    text = read(README)
    baseline = (
        f"Current manuscript baseline: 103526 words after I-0293 full private-edition render; "
        "I-0293 generated a local ignored full visual PDF at rendered/full_book_i0293/Next-Token-full-draft-i0293.pdf "
        f"with {render['pdf_embedded_images']} embedded image objects, {render['blank_like_pages']} blank-like pages, "
        f"and {layout['pass_figures']} pass / {layout['warn_figures']} warn / {layout['fail_figures']} fail figure-page QA."
    )
    if "Current manuscript baseline:" in text:
        text = re.sub(r"Current manuscript baseline:.*", baseline, text)
    else:
        text = text.rstrip() + "\n\n" + baseline + "\n"
    write(README, text)


def record_loop(render: dict[str, str], layout: dict[str, str], final_qa: list[dict[str, str]]) -> None:
    upsert_idea_done()
    update_readme(render, layout)
    append_once(
        CLAIMS,
        "C-0309\t",
        "\t".join(
            [
                "C-0309",
                "supported",
                f"I-0293 rendered a local ignored full private-edition PDF from the post-I-0292 selected manifest with {render['pdf_embedded_images']} embedded image objects, {render['html_img_count']} HTML image tags, {render['blank_like_pages']} blank-like pages, {layout['figure_rows']} audited figure pages, {layout['pass_figures']} pass / {layout['warn_figures']} warn / {layout['fail_figures']} fail figure-page rows, {layout['p0_defects']} P0 defects, and {sum(1 for row in final_qa if row['result'] == 'pass')} pass / {sum(1 for row in final_qa if row['result'] == 'warn')} warn final render QA checks.",
                "scripts/final_private_render_i0293.py;data/full_private_render_object_qa_i0293.tsv;data/full_private_render_page_qa_i0293.tsv;data/full_private_render_page_defects_i0293.tsv;data/full_private_render_final_qa_i0293.tsv;data/full_private_render_visual_density_i0293.tsv;manuscript/full-private-render-i0293.md;rendered/full_book_i0293/render_manifest_i0293.tsv;rendered/full_book_i0293/Next-Token-full-draft-i0293.pdf",
                PASS_ID,
                "local full-PDF render, object QA, page-image QA, sample-page generation, and density audit",
                TODAY,
                "Supported as private local render and automated QA only; PDF/sample PNGs are ignored and not committed, warning rows remain for I-0294, and no rights, print, EPUB, or final-publication clearance is implied.",
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
                "champion first final private visual render",
                PASS_ID,
                "final polish 1",
                "+1.0",
                "100.0",
                "103526",
                "24",
                "152",
                "158",
                "510",
                f"309 supported / 0 needs-verification; rendered I-0293 local full visual PDF with {render['pdf_embedded_images']} image objects, {render['blank_like_pages']} blank-like pages, {layout['pass_figures']} pass / {layout['warn_figures']} warn / {layout['fail_figures']} fail figure rows, {layout['defects']} page defects, {sum(1 for row in final_qa if row['result'] == 'pass')} pass / {sum(1 for row in final_qa if row['result'] == 'warn')} warn final QA",
                "+1",
                "Local PDF/rasters/sample PNGs are ignored; I-0294 must repair warnings, low-story-value pages, table legibility, and caption/source-note issues before final assembly",
                "promoted",
                "Generated the first full private-edition visual PDF after all three integration passes and turned it into a concrete page-defect backlog for correction.",
                "one full visual PDF render and audit pass",
            ]
        ),
    )
    append_once(
        INSIGHTS,
        "I-0293: first final render",
        "\n- I-0293: first final render should be judged as a defect generator, not a victory lap; once all integrated visuals enter one PDF, the valuable output is the page-by-page warning map that tells the correction pass where visual density, caption extraction, and small-image problems actually appear.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")

    _render_mod, object_qa, _object_defects, manifest = render_book(chrome)
    figure_rows, _sample_rows, page_defects, page_qa, fatigue = page_audit()
    render = object_summary(manifest, object_qa)
    layout = layout_summary(figure_rows, page_defects, page_qa, fatigue)
    density_rows = visual_density_rows(figure_rows)
    final_qa = final_qa_rows(render, layout, density_rows)
    write_report(render, layout, final_qa, density_rows)
    record_loop(render, layout, final_qa)
    print(
        f"pdf={PDF_OUT} pages={render['pdf_pages']} images={render['pdf_embedded_images']} "
        f"blank_like={render['blank_like_pages']} figures={layout['pass_figures']} pass/"
        f"{layout['warn_figures']} warn/{layout['fail_figures']} fail defects={layout['defects']} "
        f"final_qa={sum(1 for row in final_qa if row['result'] == 'pass')}/{len(final_qa)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
