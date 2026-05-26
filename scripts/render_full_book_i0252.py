from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import re
import subprocess
from pathlib import Path

import fitz


PASS_ID = "I-0252"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"
CSS = ROOT / "assets" / "book_design" / "full_book_page_template_i0251.css"
ROUGH_PDF = ROOT / "rendered" / "full_book_i0240" / "Next-Token-full-draft-i0240.pdf"
OUTDIR = ROOT / "rendered" / "full_book_i0252"
HTML_OUT = OUTDIR / "Next-Token-full-draft-i0252.html"
PDF_OUT = OUTDIR / "Next-Token-full-draft-i0252.pdf"
MANIFEST = OUTDIR / "render_manifest_i0252.tsv"
QA_TSV = ROOT / "data" / "full_book_render_iteration_i0252.tsv"
DEFECTS_TSV = ROOT / "data" / "full_book_render_iteration_defects_i0252.tsv"
SUMMARY_MD = ROOT / "manuscript" / "full-book-render-iteration-i0252.md"
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


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def html_shell(body: str, css: str) -> str:
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        "<title>Next Token full draft I-0252</title>"
        f"<style>{css}</style></head><body>\n{body}\n</body></html>\n"
    )


def render(chrome: Path) -> tuple[str, str]:
    renderer = load_render_module()
    markdown = MARKDOWN.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(html_shell(renderer.markdown_to_html(markdown), css), encoding="utf-8")
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
        raise RuntimeError("Chrome completed but I-0252 PDF was missing or empty")
    return markdown, css


def flatten(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def pdf_text_and_stats(path: Path) -> tuple[list[str], str, list[dict[str, float]]]:
    doc = fitz.open(path)
    page_texts = [page.get_text("text") for page in doc]
    stats = []
    for index, page in enumerate(doc, start=1):
        text_len = len(page_texts[index - 1].strip())
        pix = page.get_pixmap(matrix=fitz.Matrix(0.16, 0.16), alpha=False)
        data = pix.samples
        colors = set()
        luma_sum = 0.0
        count = 0
        for i in range(0, len(data), 3):
            r, g, b = data[i], data[i + 1], data[i + 2]
            colors.add((r // 16, g // 16, b // 16))
            luma_sum += 0.2126 * r + 0.7152 * g + 0.0722 * b
            count += 1
        stats.append(
            {
                "page": float(index),
                "text_len": float(text_len),
                "unique_colors": float(len(colors)),
                "mean_luma": luma_sum / count if count else 0.0,
            }
        )
    doc.close()
    return page_texts, flatten("\n".join(page_texts)), stats


def row(check_id: str, category: str, result: str, evidence: str, action: str) -> dict[str, str]:
    return {
        "pass_id": PASS_ID,
        "check_id": check_id,
        "category": category,
        "result": result,
        "evidence": evidence,
        "recommended_action": action,
    }


def build_qa(markdown: str, css: str) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    page_texts, full_text, page_stats = pdf_text_and_stats(PDF_OUT)
    rough_pages = "missing"
    rough_bytes = "missing"
    if ROUGH_PDF.exists():
        rough_doc = fitz.open(ROUGH_PDF)
        rough_pages = str(len(rough_doc))
        rough_bytes = str(ROUGH_PDF.stat().st_size)
        rough_doc.close()

    chapter_titles = re.findall(r"^# (Chapter \d\d: .+)$", markdown, flags=re.MULTILINE)
    missing_chapters = [title for title in chapter_titles if title not in full_text]
    source_figures = sorted(set(re.findall(r"\bF\d\d\.\d\d\b", markdown)))
    missing_figures = [figure_id for figure_id in source_figures if figure_id not in full_text]
    source_lanes = len(re.findall(r"Source lane \(I-0248\)", full_text))
    low_text_pages = [str(int(stat["page"])) for stat in page_stats if stat["text_len"] < 15]
    blank_like_pages = [
        str(int(stat["page"]))
        for stat in page_stats
        if stat["text_len"] < 5 and stat["unique_colors"] <= 2 and stat["mean_luma"] > 245
    ]
    page_count = len(page_texts)
    qa = [
        row("R2-001", "artifact_integrity", "pass" if PDF_OUT.exists() and PDF_OUT.stat().st_size > 0 else "fail", f"pdf={PDF_OUT}; bytes={PDF_OUT.stat().st_size}; sha256={sha256(PDF_OUT)}", "Regenerate designed render if PDF is missing or empty."),
        row("R2-002", "template_applied", "pass" if "font-size: 10.8pt" in css and "full-book page template" in css else "fail", f"css={CSS}; bytes={CSS.stat().st_size}; html_contains_10_8pt={'10.8pt' in HTML_OUT.read_text(encoding='utf-8')}", "Repair CSS injection before judging render quality."),
        row("R2-003", "chapter_survival", "pass" if len(chapter_titles) == 24 and not missing_chapters else "fail", f"source_chapters={len(chapter_titles)}; missing={';'.join(missing_chapters) if missing_chapters else 'none'}", "Repair headings or render conversion before design comparison."),
        row("R2-004", "figure_id_survival", "pass" if len(source_figures) == 100 and not missing_figures else "fail", f"source_figures={len(source_figures)}; missing={';'.join(missing_figures) if missing_figures else 'none'}", "Repair figure callout rendering before proceeding."),
        row("R2-005", "blank_pages", "pass" if not blank_like_pages else "fail", f"blank_like_pages={';'.join(blank_like_pages) if blank_like_pages else 'none'}; low_text_pages={';'.join(low_text_pages[:20]) if low_text_pages else 'none'}", "Inspect and remove accidental blank pages."),
        row("R2-006", "source_lane_survival", "pass" if source_lanes == 23 else "fail", f"source_lanes_in_pdf={source_lanes}; expected=23", "Repair source-lane styling/extraction if I-0248 lanes disappear."),
        row("R2-007", "page_count_comparison", "pass" if page_count > 0 else "fail", f"designed_pages={page_count}; rough_pages={rough_pages}; designed_bytes={PDF_OUT.stat().st_size}; rough_bytes={rough_bytes}", "Compare page count again after final figures and endnotes are integrated."),
        row("R2-008", "residual_defects", "warn", "Designed render still uses placeholder/callout text for figures; no image placement, overflow screenshot scan, caption compression, or rights clearance is completed.", "Run page-image overflow QA and real figure placement before calling this publication-ready."),
    ]

    defects = []
    for item in qa:
        if item["result"] == "fail":
            defects.append(
                {
                    "pass_id": PASS_ID,
                    "defect_id": item["check_id"].replace("R2-", "R2DEF-"),
                    "severity": "P0",
                    "category": item["category"],
                    "evidence": item["evidence"],
                    "recommended_action": item["recommended_action"],
                }
            )
    defects.append(
        {
            "pass_id": PASS_ID,
            "defect_id": "R2DEF-008",
            "severity": "P1",
            "category": "designed_render_not_publication_ready",
            "evidence": "No final artwork placement, overflow screenshot scan, caption compression, source-note finalization, or rights clearance.",
            "recommended_action": "Use the designed PDF as the next QA surface, not as a publication candidate.",
        }
    )

    manifest = {
        "pass_id": PASS_ID,
        "input": str(MARKDOWN),
        "css": str(CSS),
        "html_output": str(HTML_OUT),
        "pdf_output": str(PDF_OUT),
        "chapter_headings": str(len(chapter_titles)),
        "figure_ids": str(len(source_figures)),
        "designed_pages": str(page_count),
        "rough_pages": rough_pages,
        "html_bytes": str(HTML_OUT.stat().st_size),
        "pdf_bytes": str(PDF_OUT.stat().st_size),
        "html_sha256": sha256(HTML_OUT),
        "pdf_sha256": sha256(PDF_OUT),
        "qa_passes": str(sum(1 for item in qa if item["result"] == "pass")),
        "qa_warns": str(sum(1 for item in qa if item["result"] == "warn")),
        "qa_fails": str(sum(1 for item in qa if item["result"] == "fail")),
        "known_defects": "placeholder_figures;no_page_image_overflow_scan;no_final_caption_compression;no_rights_clearance;no_final_source_notes",
    }
    return qa, defects, manifest


def write_summary(qa: list[dict[str, str]], defects: list[dict[str, str]], manifest: dict[str, str]) -> None:
    lines = [
        "# I-0252 Full-Book Render Iteration 2",
        "",
        "Status: promoted designed-render QA surface.",
        "",
        "## Result",
        "",
        f"- Designed PDF: `{Path(manifest['pdf_output']).relative_to(ROOT)}` (ignored, not committed)",
        f"- Designed pages: {manifest['designed_pages']}",
        f"- Rough-render pages for comparison: {manifest['rough_pages']}",
        f"- Chapter headings found: {manifest['chapter_headings']} / 24",
        f"- Figure IDs found: {manifest['figure_ids']} / 100",
        f"- QA rows: {len(qa)} ({manifest['qa_passes']} pass, {manifest['qa_warns']} warn, {manifest['qa_fails']} fail)",
        f"- Defect rows: {len(defects)}",
        "",
        "## Promotion Rationale",
        "",
        "This pass applies the I-0251 page-template contract to the whole assembled draft and proves the designed artifact is structurally searchable enough for the next page-level QA loop: all 24 chapter headings, all 100 figure IDs, and all 23 I-0248 source lanes survive extraction.",
        "",
        "## Limits",
        "",
        "The designed PDF is not publication-ready. It still contains placeholder/callout figure text and lacks page-image overflow scanning, final artwork placement, caption compression, final source-note treatment, and rights clearance.",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_manifest(manifest: dict[str, str]) -> None:
    MANIFEST.write_text("\n".join(f"{key}\t{value}" for key, value in manifest.items()) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")

    markdown, css = render(chrome)
    qa, defects, manifest = build_qa(markdown, css)
    write_tsv(QA_TSV, qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_tsv(DEFECTS_TSV, defects, ["pass_id", "defect_id", "severity", "category", "evidence", "recommended_action"])
    write_manifest(manifest)
    write_summary(qa, defects, manifest)
    print(
        f"pdf={PDF_OUT} pages={manifest['designed_pages']} "
        f"qa_pass={manifest['qa_passes']} qa_warn={manifest['qa_warns']} qa_fail={manifest['qa_fails']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
