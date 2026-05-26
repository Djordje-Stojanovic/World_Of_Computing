from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import importlib.util
import re
import subprocess
from pathlib import Path

import fitz


PASS_ID = "I-0257"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"
CSS = ROOT / "assets" / "book_design" / "full_book_page_template_i0251.css"
FIGURES = ROOT / "data" / "full_book_figure_list_i0229.tsv"
RIGHTS = ROOT / "data" / "image_rights_staging_i0250.tsv"
OUTDIR = ROOT / "rendered" / "full_book_i0257"
RASTER_DIR = OUTDIR / "embedded_rasters"
HTML_OUT = OUTDIR / "Next-Token-full-draft-i0257.html"
PDF_OUT = OUTDIR / "Next-Token-full-draft-i0257.pdf"
MANIFEST = OUTDIR / "render_manifest_i0257.tsv"
QA_TSV = ROOT / "data" / "full_book_visual_embedding_i0257.tsv"
DEFECTS_TSV = ROOT / "data" / "full_book_visual_embedding_defects_i0257.tsv"
SUMMARY_MD = ROOT / "manuscript" / "full-book-visual-embedding-i0257.md"
RENDER_I0240 = ROOT / "scripts" / "render_full_book_i0240.py"


def load_render_module():
    spec = importlib.util.spec_from_file_location("render_full_book_i0240", RENDER_I0240)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load I-0240 render module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def data_uri(path: Path) -> str:
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    if path.suffix.lower() == ".svg":
        mime = "image/svg+xml"
    elif path.suffix.lower() == ".png":
        mime = "image/png"
    else:
        mime = "application/octet-stream"
    return f"data:{mime};base64,{payload}"


def rasterize_svg(source: Path, target: Path, chrome: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    html_path = target.with_suffix(".html")
    html_path.write_text(
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        "<style>html,body{margin:0;width:1400px;height:900px;background:#fffdf8;}"
        "body{display:flex;align-items:center;justify-content:center;overflow:hidden;}"
        "img{max-width:1360px;max-height:860px;width:auto;height:auto;}</style>"
        f"</head><body><img src=\"{source.resolve().as_uri()}\"></body></html>",
        encoding="utf-8",
    )
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--hide-scrollbars",
        "--window-size=1400,900",
        f"--screenshot={target}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not target.exists() or target.stat().st_size == 0:
        raise RuntimeError(
            "Chrome SVG rasterization failed\n"
            f"source={source}\ntarget={target}\nreturncode={result.returncode}\n"
            f"stdout={result.stdout}\nstderr={result.stderr}"
        )


def rasterize_rows(rows: dict[str, dict[str, str]], chrome: Path) -> None:
    RASTER_DIR.mkdir(parents=True, exist_ok=True)
    for figure_id, row in rows.items():
        source = Path(row["resolved_path"])
        if source.suffix.lower() == ".svg":
            target = RASTER_DIR / f"{figure_id.replace('.', '-')}_{source.stem}.png"
            rasterize_svg(source, target, chrome)
            row["embed_path"] = str(target)
            row["embed_kind"] = "chrome_rasterized_png_from_svg"
        else:
            row["embed_path"] = str(source)
            row["embed_kind"] = source.suffix.lower().lstrip(".") or "source_file"


def figure_maps() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    figure_rows = {row["figure_id"]: row for row in read_tsv(FIGURES)}
    rights_rows = {row["figure_id"]: row for row in read_tsv(RIGHTS)}
    return figure_rows, rights_rows


def publishable_rows() -> dict[str, dict[str, str]]:
    figures, rights = figure_maps()
    rows: dict[str, dict[str, str]] = {}
    for figure_id, right in rights.items():
        fig = figures.get(figure_id, {})
        path_text = right.get("manifest_file_path") or fig.get("manifest_file_path", "")
        path = ROOT / path_text
        if (
            right.get("publication_decision") == "publish"
            and right.get("manifest_status") == "available"
            and path.exists()
        ):
            rows[figure_id] = {**fig, **right, "resolved_path": str(path)}
    return rows


def build_figure_html(row: dict[str, str]) -> str:
    path = Path(row["embed_path"])
    figure_id = html.escape(row["figure_id"])
    asset_id = html.escape(row.get("asset_id", ""))
    title = html.escape(row.get("figure_title", "Untitled exhibit"))
    role = html.escape(row.get("final_role") or row.get("asset_type", "visual exhibit"))
    source_ids = html.escape(row.get("source_ids", ""))
    rights_stage = html.escape(row.get("rights_stage", "publish_after_qa"))
    embed_kind = html.escape(row.get("embed_kind", "embedded_asset"))
    claim_boundary = html.escape(row.get("claim_boundary", "Scoped visual evidence only."))
    alt = html.escape(row.get("alt_text") or f"{figure_id}: {title}")
    uri = data_uri(path)
    return (
        f'<figure class="book-figure embedded-visual" id="{figure_id}">\n'
        f'  <img src="{uri}" alt="{alt}">\n'
        f"  <figcaption><strong>{figure_id} / {asset_id} - {title}</strong> "
        f"{role}. Sources: {source_ids}. Rights stage: {rights_stage}. Render: {embed_kind}. "
        f"Boundary: {claim_boundary}</figcaption>\n"
        "</figure>"
    )


def markdown_to_html_with_figures(markdown: str, rows: dict[str, dict[str, str]]) -> str:
    renderer = load_render_module()
    lines = markdown.splitlines()
    out_lines: list[str] = []
    replacements: dict[str, str] = {}
    skipped_blocks = 0
    embedded_blocks = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"<!-- FIGURE-CALLOUT (F\d\d\.\d\d)\b", line)
        if not match:
            out_lines.append(line)
            index += 1
            continue
        figure_id = match.group(1)
        block = [line]
        index += 1
        end_marker = f"<!-- /FIGURE-CALLOUT {figure_id} -->"
        while index < len(lines):
            block.append(lines[index])
            if lines[index].strip() == end_marker:
                index += 1
                break
            index += 1
        if figure_id in rows:
            token = f"@@I0257_FIGURE_{figure_id.replace('.', '_')}@@"
            replacements[token] = build_figure_html(rows[figure_id])
            out_lines.append(token)
            embedded_blocks += 1
        else:
            out_lines.extend(block)
            skipped_blocks += 1
    html_body = renderer.markdown_to_html("\n".join(out_lines))
    for token, figure_html in replacements.items():
        html_body = html_body.replace(f"<p>{token}</p>", figure_html)
    return html_body, embedded_blocks, skipped_blocks


def html_shell(body: str, css: str) -> str:
    figure_css = """

/* I-0257 embedded visual layer */
.book-figure {
  break-inside: avoid;
  margin: 0.18in 0 0.2in;
  padding: 0.08in 0 0;
  border-top: 1px solid #c9c1b4;
}
.book-figure img {
  display: block;
  width: 100%;
  max-height: 5.85in;
  object-fit: contain;
  margin: 0 auto 0.075in;
}
.book-figure figcaption {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 7.6pt;
  line-height: 1.28;
  color: #37322b;
}
"""
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        "<title>Next Token full draft I-0257</title>"
        f"<style>{css}{figure_css}</style></head><body>\n{body}\n</body></html>\n"
    )


def render(chrome: Path) -> tuple[str, dict[str, dict[str, str]], int, int]:
    rows = publishable_rows()
    rasterize_rows(rows, chrome)
    markdown = MARKDOWN.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    body, embedded_blocks, skipped_blocks = markdown_to_html_with_figures(markdown, rows)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(html_shell(body, css), encoding="utf-8")
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT.as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "Chrome PDF render failed\n"
            f"returncode={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    if not PDF_OUT.exists() or PDF_OUT.stat().st_size == 0:
        raise RuntimeError("Chrome completed but I-0257 PDF was missing or empty")
    return markdown, rows, embedded_blocks, skipped_blocks


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    text = "\n".join(page.get_text("text") for page in doc)
    embedded_images = sum(len(page.get_images(full=True)) for page in doc)
    pages_with_images = sum(1 for page in doc if page.get_images(full=True))
    pages_with_drawings = sum(1 for page in doc if len(page.get_drawings()) > 20)
    page_count = len(doc)
    doc.close()
    return {
        "pages": str(page_count),
        "text": text,
        "embedded_images": str(embedded_images),
        "pages_with_images": str(pages_with_images),
        "pages_with_many_drawings": str(pages_with_drawings),
    }


def qa_rows(markdown: str, rows: dict[str, dict[str, str]], embedded_blocks: int, skipped_blocks: int) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    stats = pdf_stats(PDF_OUT)
    text = stats.pop("text")
    html_text = HTML_OUT.read_text(encoding="utf-8")
    source_figures = sorted(set(re.findall(r"\bF\d\d\.\d\d\b", markdown)))
    pdf_figures = sorted(set(re.findall(r"\bF\d\d\.\d\d\b", text)))
    missing_pdf_figures = [figure_id for figure_id in source_figures if figure_id not in pdf_figures]
    html_png_img_count = html_text.count("<img src=\"data:image/png;base64,")
    html_svg_img_count = html_text.count("<img src=\"data:image/svg+xml;base64,")
    html_img_count = html_png_img_count + html_svg_img_count
    file_missing = [figure_id for figure_id, row in rows.items() if not Path(row["resolved_path"]).exists()]
    checks = [
        check("VE-001", "publishable_asset_selection", "pass" if len(rows) == 74 else "fail", f"publishable_available_assets={len(rows)}; expected=74", "Repair rights/file join before rendering."),
        check("VE-002", "html_embedding", "pass" if html_img_count == 74 and embedded_blocks == 74 else "fail", f"html_img_count={html_img_count}; html_png_img_count={html_png_img_count}; html_svg_img_count={html_svg_img_count}; embedded_callout_blocks={embedded_blocks}; blocked_callout_blocks={skipped_blocks}", "Repair callout replacement if HTML lacks the 74 selected visual images."),
        check("VE-003", "file_existence", "pass" if not file_missing else "fail", f"missing_files={';'.join(file_missing) if file_missing else 'none'}", "Resolve or de-select missing assets."),
        check("VE-004", "pdf_artifact", "pass" if PDF_OUT.exists() and PDF_OUT.stat().st_size > 0 else "fail", f"pdf={PDF_OUT}; bytes={PDF_OUT.stat().st_size}; sha256={sha256(PDF_OUT)}", "Regenerate PDF."),
        check("VE-005", "figure_id_survival", "pass" if len(source_figures) == 100 and not missing_pdf_figures else "fail", f"source_figures={len(source_figures)}; pdf_figures={len(pdf_figures)}; missing={';'.join(missing_pdf_figures) if missing_pdf_figures else 'none'}", "Repair caption/source-note extraction for embedded figures."),
        check("VE-006", "pdf_visual_objects", "pass" if int(stats["embedded_images"]) >= 74 else "warn", f"embedded_images={stats['embedded_images']}; pages_with_images={stats['pages_with_images']}; pages_with_many_drawings={stats['pages_with_many_drawings']}", "Inspect page images before publication; raster objects alone do not prove legibility."),
        check("VE-007", "known_limits", "warn", "74 original SVG/chart/card assets embedded; 26 local-only, permission-needed, or redraw rows remain blocked callouts.", "Continue with I-0258/I-0259/I-0260/I-0261 to close file-level manifest, source surfaces, source cards, and remaining slots."),
    ]
    defects = [
        {
            "pass_id": PASS_ID,
            "defect_id": item["check_id"].replace("VE-", "VEDEF-"),
            "severity": "P0" if item["result"] == "fail" else "P1",
            "category": item["category"],
            "evidence": item["evidence"],
            "recommended_action": item["recommended_action"],
        }
        for item in checks
        if item["result"] != "pass"
    ]
    manifest = {
        "pass_id": PASS_ID,
        "input": str(MARKDOWN),
        "css": str(CSS),
        "html_output": str(HTML_OUT),
        "pdf_output": str(PDF_OUT),
        "publishable_assets": str(len(rows)),
        "embedded_callout_blocks": str(embedded_blocks),
        "blocked_callout_blocks": str(skipped_blocks),
        "html_img_count": str(html_img_count),
        "html_png_img_count": str(html_png_img_count),
        "html_svg_img_count": str(html_svg_img_count),
        "raster_dir": str(RASTER_DIR),
        "chapter_headings": str(len(re.findall(r"^# Chapter \d\d:", markdown, flags=re.MULTILINE))),
        "figure_ids": str(len(source_figures)),
        "pdf_pages": stats["pages"],
        "pdf_embedded_images": stats["embedded_images"],
        "pdf_pages_with_images": stats["pages_with_images"],
        "pdf_pages_with_many_drawings": stats["pages_with_many_drawings"],
        "html_bytes": str(HTML_OUT.stat().st_size),
        "pdf_bytes": str(PDF_OUT.stat().st_size),
        "html_sha256": sha256(HTML_OUT),
        "pdf_sha256": sha256(PDF_OUT),
        "qa_passes": str(sum(1 for item in checks if item["result"] == "pass")),
        "qa_warns": str(sum(1 for item in checks if item["result"] == "warn")),
        "qa_fails": str(sum(1 for item in checks if item["result"] == "fail")),
        "known_defects": "26_unembedded_non_publish_rows;no_page_image_legibility_scan;no_final_caption_compression;no_rights_clearance_for_screenshot_photo_source_surface_rows",
    }
    return checks, defects, manifest


def check(check_id: str, category: str, result: str, evidence: str, action: str) -> dict[str, str]:
    return {
        "pass_id": PASS_ID,
        "check_id": check_id,
        "category": category,
        "result": result,
        "evidence": evidence,
        "recommended_action": action,
    }


def write_manifest(manifest: dict[str, str]) -> None:
    MANIFEST.write_text("\n".join(f"{key}\t{value}" for key, value in manifest.items()) + "\n", encoding="utf-8")


def write_summary(qa: list[dict[str, str]], defects: list[dict[str, str]], manifest: dict[str, str]) -> None:
    SUMMARY_MD.write_text(
        "\n".join(
            [
                "# I-0257 Full-Book Visual Embedding",
                "",
                "Status: promoted visual-embedding render surface.",
                "",
                "## Result",
                "",
                f"- Local PDF: `{Path(manifest['pdf_output']).relative_to(ROOT)}` (ignored, not committed)",
                f"- PDF pages: {manifest['pdf_pages']}",
                f"- Publishable SVG/chart/card assets embedded: {manifest['embedded_callout_blocks']} / 74",
                f"- Remaining blocked callout blocks: {manifest['blocked_callout_blocks']}",
        f"- HTML image tags: {manifest['html_img_count']} ({manifest['html_png_img_count']} raster PNG, {manifest['html_svg_img_count']} SVG)",
        f"- Local raster staging: `{Path(manifest['raster_dir']).relative_to(ROOT)}` (ignored, not committed)",
        f"- PDF visual-object evidence: {manifest['pdf_embedded_images']} raster image XObjects, {manifest['pdf_pages_with_images']} pages with raster images",
                f"- QA rows: {len(qa)} ({manifest['qa_passes']} pass, {manifest['qa_warns']} warn, {manifest['qa_fails']} fail)",
                f"- Defect rows: {len(defects)}",
                "",
                "## Promotion Rationale",
                "",
                "The previous designed render preserved figure IDs as text only. This pass changes the render pipeline so every selected figure row that is both marked `publish` and has an available local SVG/chart/card file is rasterized to a local PNG and inserted as an actual image-bearing figure with caption, sources, rights stage, and claim boundary.",
                "",
                "## Limits",
                "",
                "This is still not publication-ready. Twenty-six selected slots remain blocked as local-only, permission-needed, or redraw rows. The SVGs still need page-image legibility QA, caption compression, final source-note treatment, and the next file-level manifest pass.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    markdown, rows, embedded_blocks, skipped_blocks = render(chrome)
    qa, defects, manifest = qa_rows(markdown, rows, embedded_blocks, skipped_blocks)
    write_tsv(QA_TSV, qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_tsv(DEFECTS_TSV, defects, ["pass_id", "defect_id", "severity", "category", "evidence", "recommended_action"])
    write_manifest(manifest)
    write_summary(qa, defects, manifest)
    print(
        f"pdf={PDF_OUT} pages={manifest['pdf_pages']} embedded={manifest['embedded_callout_blocks']} "
        f"blocked={manifest['blocked_callout_blocks']} qa_pass={manifest['qa_passes']} "
        f"qa_warn={manifest['qa_warns']} qa_fail={manifest['qa_fails']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
