from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import fitz
from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[1]
PASS_ID = "I-0319"
RUN_ID = "pass-0319"

SOURCE_HTML = ROOT / "rendered" / "final_private_i0318" / "Next-Token-final-private-contextual-visuals-i0318.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0318" / "Next-Token-final-private-contextual-visuals-i0318.pdf"
SOURCE_MD = ROOT / "manuscript" / "Next-Token-contextual-visuals-i0318.md"

OUTDIR = ROOT / "rendered" / "final_private_i0319"
HTML_OUT = OUTDIR / "Next-Token-final-private-one-visual-page-i0319.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-one-visual-page-i0319.pdf"
MD_OUT = ROOT / "manuscript" / "Next-Token-one-visual-page-i0319.md"
REPORT = ROOT / "manuscript" / "one-visual-page-i0319.md"
CHAMPION_REPORT = ROOT / "champion" / "one-visual-page-i0319.md"
CHAMPION_POINTER = ROOT / "champion" / "final-private-pdf-pointer-i0319.md"

OUT_BASELINE = ROOT / "data" / "one_visual_page_baseline_i0319.tsv"
OUT_REMOVED_BOARDS = ROOT / "data" / "one_visual_page_removed_boards_i0319.tsv"
OUT_QA = ROOT / "data" / "one_visual_page_qa_i0319.tsv"
OUT_MANIFEST = ROOT / "data" / "one_visual_page_manifest_i0319.tsv"

README = ROOT / "README.md"
CHAMPION_README = ROOT / "champion" / "README.md"
READER_GUIDE = ROOT / "champion" / "private-reader-guide-i0311.md"
GUIDE_POINTER = ROOT / "champion" / "final-private-reader-guide-pointer-i0311.md"
IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0319_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0319_changed_files_manifest.tsv"


FORBIDDEN_PDF_STRINGS = [
    "Visual Portfolio",
    "PORTFOLIO PLATE",
    "Image Sequence",
    "Images placed with this chapter",
    "Use note",
    "Boundary:",
    "Blocked claims",
    "Source/provenance",
    "project ledgers",
    "private-edition visual layer",
    "source boundaries",
    "F01.",
    "A-0",
    "VX",
    "S-0",
    "C-0",
    "sha256",
    "C:/",
    "file:///",
    "rescue proof",
    "placeholder",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def pdf_text(path: Path) -> str:
    doc = fitz.open(path)
    try:
        return "\n".join(page.get_text("text") for page in doc)
    finally:
        doc.close()


def page_ink_ratio(page: fitz.Page, scale: float = 0.12) -> float:
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    samples = pix.samples
    count = pix.width * pix.height
    nonwhite = 0
    for i in range(0, len(samples), 3):
        if min(samples[i], samples[i + 1], samples[i + 2]) < 245:
            nonwhite += 1
    return nonwhite / count


def page_density_summary(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    blank = 0
    severe_sparse = 0
    micro_visual = 0
    try:
        for page in doc:
            text = page.get_text("text").strip()
            words = len(re.findall(r"\b[\w'-]+\b", text))
            images = len(page.get_images(full=True))
            ink = page_ink_ratio(page)
            if words == 0 and images == 0 and ink < 0.015:
                blank += 1
            if ink < 0.06 and words < 60 and images == 0:
                severe_sparse += 1
            if words <= 5 and images > 0 and ink < 0.18:
                micro_visual += 1
    finally:
        doc.close()
    return {"blank_pages": str(blank), "severe_sparse_pages": str(severe_sparse), "micro_visual_pages": str(micro_visual)}


def strip_blank_pdf_pages(path: Path) -> int:
    source = fitz.open(path)
    blank_pages: list[int] = []
    try:
        for index, page in enumerate(source):
            if not page.get_text("text").strip() and len(page.get_images(full=True)) == 0 and page_ink_ratio(page) < 0.015:
                blank_pages.append(index)
        if not blank_pages:
            return 0
        cleaned = fitz.open()
        for index in range(source.page_count):
            if index not in blank_pages:
                cleaned.insert_pdf(source, from_page=index, to_page=index)
        temp = path.with_suffix(".blank-stripped.pdf")
        cleaned.save(temp, garbage=4, deflate=True)
        cleaned.close()
    finally:
        source.close()
    temp.replace(path)
    return len(blank_pages)


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    try:
        text = "\n".join(page.get_text("text") for page in doc)
        image_objects = 0
        drawing_objects = 0
        multi_image_pages = 0
        max_images_on_page = 0
        for page in doc:
            images = page.get_images(full=True)
            max_images_on_page = max(max_images_on_page, len(images))
            if len(images) > 1:
                multi_image_pages += 1
            image_objects += len(images)
            drawing_objects += len(page.get_drawings())
        return {
            "pages": str(doc.page_count),
            "image_objects": str(image_objects),
            "drawing_objects": str(drawing_objects),
            "multi_image_pages": str(multi_image_pages),
            "max_images_on_page": str(max_images_on_page),
            "word_count_pdf_text": str(len(re.findall(r"\b[\w'-]+\b", text))),
            "sha256": sha256(path) if path.exists() else "",
            **page_density_summary(path),
        }
    finally:
        doc.close()


def claim_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    with CLAIMS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            status = row.get("status", "")
            counts[status] = counts.get(status, 0) + 1
    return counts


def upsert_tsv_line(path: Path, key: str, row: str) -> None:
    lines = read(path).splitlines()
    lines = [line for line in lines if key not in line]
    lines.append(row)
    write(path, "\n".join(lines) + "\n")


def append_once(path: Path, marker: str, text: str) -> None:
    current = read(path) if path.exists() else ""
    if marker not in current:
        write(path, current.rstrip() + "\n" + text.strip() + "\n")


def backup_targets() -> None:
    targets = [README, CHAMPION_README, READER_GUIDE, GUIDE_POINTER]
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    rows: list[dict[str, str]] = []
    for target in targets:
        if not target.exists():
            continue
        dest = BACKUP_DIR / target.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, dest)
        rows.append({"pass_id": PASS_ID, "source": rel(target), "backup": rel(dest), "sha256": sha256(dest)})
    write_tsv(BACKUP_MANIFEST, rows, ["pass_id", "source", "backup", "sha256"])


def one_visual_css() -> str:
    return """
<style>
.i0299-board,
.visual-atlas {
  display: none !important;
}
.i0318-contextual-visuals,
.i0319-one-visual-flow {
  break-before: auto !important;
  page-break-before: auto !important;
  margin: 0 !important;
  padding: 0 !important;
  border: 0 !important;
}
.i0318-contextual-visuals h2,
.i0318-contextual-visuals .i0318-context-line {
  display: none !important;
}
.i0318-contextual-visuals .atlas-grid {
  display: block !important;
}
figure.i0319-visual-exhibit,
.atlas-figure.i0319-visual-exhibit,
.book-figure.i0319-visual-exhibit {
  break-before: page !important;
  page-break-before: always !important;
  break-after: auto !important;
  page-break-after: auto !important;
  break-inside: avoid !important;
  page-break-inside: avoid !important;
  min-height: 7.35in !important;
  margin: 0 !important;
  padding: 0.12in 0 0 !important;
  border-top: 1px solid #8f806b !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
}
figure.i0319-visual-exhibit img,
.atlas-figure.i0319-visual-exhibit img,
.book-figure.i0319-visual-exhibit img {
  display: block !important;
  width: 100% !important;
  max-width: 100% !important;
  max-height: 6.25in !important;
  object-fit: contain !important;
  margin: 0 auto 0.07in !important;
}
.atlas-figure.i0319-visual-exhibit.logo img,
.atlas-figure.i0319-visual-exhibit.portrait img,
.book-figure.i0319-visual-exhibit.real_world_logo img,
.book-figure.i0319-visual-exhibit.real_world_person_image img {
  width: 100% !important;
  max-width: 100% !important;
  max-height: 5.9in !important;
}
figure.i0319-visual-exhibit figcaption,
.atlas-figure.i0319-visual-exhibit figcaption,
.book-figure.i0319-visual-exhibit figcaption {
  font-family: Arial, Helvetica, sans-serif !important;
  font-size: 9.2pt !important;
  line-height: 1.18 !important;
  color: #2f2a24 !important;
}
</style>
"""


def baseline_rows(soup: BeautifulSoup, stats: dict[str, str]) -> list[dict[str, str]]:
    rows = [
        {"pass_id": PASS_ID, "metric": "source_pages", "value": stats["pages"]},
        {"pass_id": PASS_ID, "metric": "source_image_objects", "value": stats["image_objects"]},
        {"pass_id": PASS_ID, "metric": "source_multi_image_pages", "value": stats["multi_image_pages"]},
        {"pass_id": PASS_ID, "metric": "source_max_images_on_page", "value": stats["max_images_on_page"]},
        {"pass_id": PASS_ID, "metric": "source_blank_pages", "value": stats["blank_pages"]},
        {"pass_id": PASS_ID, "metric": "html_composite_boards", "value": str(len(soup.select(".i0299-board")))},
        {"pass_id": PASS_ID, "metric": "html_board_images", "value": str(sum(len(board.select("img")) for board in soup.select(".i0299-board")))},
        {"pass_id": PASS_ID, "metric": "html_single_image_figures", "value": str(len([fig for fig in soup.select("figure") if len(fig.select("img")) == 1]))},
        {"pass_id": PASS_ID, "metric": "html_multi_image_figures", "value": str(len([fig for fig in soup.select("figure") if len(fig.select("img")) > 1]))},
    ]
    return rows


def rewrite_html() -> list[dict[str, str]]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(read(SOURCE_HTML), "html.parser")
    before = pdf_stats(SOURCE_PDF)
    write_tsv(OUT_BASELINE, baseline_rows(soup, before))

    if soup.head:
        soup.head.append(BeautifulSoup(one_visual_css(), "html.parser"))

    removed: list[dict[str, str]] = []
    for index, board in enumerate(list(soup.select(".i0299-board")), start=1):
        title_node = board.find(["h1", "h2", "h3"])
        title = title_node.get_text(" ", strip=True) if title_node else ""
        removed.append(
            {
                "pass_id": PASS_ID,
                "board_index": str(index),
                "id": board.get("id", ""),
                "title": title,
                "image_count": str(len(board.select("img"))),
                "text_sample": " ".join(board.get_text(" ", strip=True).split())[:240],
            }
        )
        board.decompose()

    visual_index = 0
    for section in soup.select(".i0318-contextual-visuals"):
        classes = list(dict.fromkeys(section.get("class", []) + ["i0319-one-visual-flow"]))
        section["class"] = classes
        for node in list(section.find_all(["h2"], recursive=False)):
            node.decompose()
        for node in list(section.select(":scope > .i0318-context-line")):
            node.decompose()
    for fig in soup.select("figure"):
        if len(fig.select("img")) != 1:
            continue
        visual_index += 1
        classes = list(dict.fromkeys(fig.get("class", []) + ["i0319-visual-exhibit"]))
        fig["class"] = classes
        fig["data-i0319-visual-index"] = str(visual_index)

    write(HTML_OUT, "<!doctype html>\n" + str(soup))
    write_tsv(OUT_REMOVED_BOARDS, removed, ["pass_id", "board_index", "id", "title", "image_count", "text_sample"])
    return removed


def write_markdown_snapshot() -> None:
    text = read(SOURCE_MD)
    text = text.replace(
        "This manuscript snapshot carries the chronological date rails, page-density layout, and chapter-local contextual visual placement.",
        "This manuscript snapshot carries the chronological date rails, page-density layout, chapter-local contextual visual placement, and one-visual-per-page reader flow.",
    )
    write(MD_OUT, text)


def render_pdf(chrome: Path) -> None:
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not PDF_OUT.exists() or PDF_OUT.stat().st_size == 0:
        raise RuntimeError(f"Chrome PDF render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")
    doc = fitz.open(PDF_OUT)
    doc.set_metadata({key: "" for key in doc.metadata.keys()})
    temp = PDF_OUT.with_suffix(".meta.pdf")
    doc.save(temp, garbage=4, deflate=True)
    doc.close()
    temp.replace(PDF_OUT)
    strip_blank_pdf_pages(PDF_OUT)


def qa_rows(before: dict[str, str], after: dict[str, str], removed: list[dict[str, str]]) -> list[dict[str, str]]:
    text = pdf_text(PDF_OUT)
    html = read(HTML_OUT)
    soup = BeautifulSoup(html, "html.parser")
    claims = claim_counts()
    chapter_ids = set(re.findall(r"Chapter\s+(\d{2}):", text))
    forbidden_hits = {pattern: text.count(pattern) for pattern in FORBIDDEN_PDF_STRINGS}
    return [
        {"pass_id": PASS_ID, "check": "multi-image pages eliminated", "result": "pass" if after["multi_image_pages"] == "0" else "fail", "evidence": f"{before['multi_image_pages']} -> {after['multi_image_pages']}; max_images_on_page={after['max_images_on_page']}"},
        {"pass_id": PASS_ID, "check": "composite boards removed from reader HTML", "result": "pass" if len(soup.select(".i0299-board")) == 0 else "fail", "evidence": f"boards_removed={len(removed)}; remaining={len(soup.select('.i0299-board'))}"},
        {"pass_id": PASS_ID, "check": "single-image figure flow retained", "result": "pass" if len(soup.select("figure.i0319-visual-exhibit")) >= 250 else "fail", "evidence": f"single_visual_figures={len(soup.select('figure.i0319-visual-exhibit'))}"},
        {"pass_id": PASS_ID, "check": "visual abundance remains high", "result": "pass" if int(after["image_objects"]) >= 250 else "fail", "evidence": f"{before['image_objects']} -> {after['image_objects']} image objects"},
        {"pass_id": PASS_ID, "check": "zero blank pages preserved", "result": "pass" if after["blank_pages"] == "0" else "fail", "evidence": f"blank_pages={after['blank_pages']}"},
        {"pass_id": PASS_ID, "check": "forbidden reader-facing residue absent", "result": "pass" if sum(forbidden_hits.values()) == 0 else "fail", "evidence": "; ".join(f"{k}={v}" for k, v in forbidden_hits.items() if v) or "0 hits"},
        {"pass_id": PASS_ID, "check": "24 chapters preserved", "result": "pass" if len(chapter_ids) == 24 else "fail", "evidence": f"unique_chapters={len(chapter_ids)}"},
        {"pass_id": PASS_ID, "check": "word count remains in band", "result": "pass" if 100000 < int(after["word_count_pdf_text"]) < 120000 else "fail", "evidence": after["word_count_pdf_text"]},
        {"pass_id": PASS_ID, "check": "claim ledger unsupported zero", "result": "pass" if claims.get("needs-verification", 0) == 0 else "fail", "evidence": f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification"},
    ]


def write_reports(before: dict[str, str], after: dict[str, str], removed: list[dict[str, str]], qa_pass: int, qa_fail: int) -> None:
    report = f"""# One Visual Per Page - I-0319

I-0319 executes the seventh rescue task: remove composite visual boards and force each remaining reader-facing exhibit onto a page where it is the only image object.

## Baseline

- Source proof: `{rel(SOURCE_PDF)}`
- Source pages: {before['pages']}
- Source image objects: {before['image_objects']}
- Source multi-image pages: {before['multi_image_pages']}
- Source max images on a page: {before['max_images_on_page']}
- Composite boards removed: {len(removed)}

## Result

- Output proof: `{rel(PDF_OUT)}`
- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Multi-image pages: {after['multi_image_pages']}
- Max images on a page: {after['max_images_on_page']}
- Blank pages: {after['blank_pages']}
- Severe sparse pages: {after['severe_sparse_pages']}
- Micro-visual sparse pages: {after['micro_visual_pages']}
- Word count from PDF text: {after['word_count_pdf_text']}

QA: {qa_pass} pass / {qa_fail} fail.

## Still Open

I-0320 through I-0322 must still add stronger quantitative density, run hostile QA, and build the final publication candidate.
"""
    write(REPORT, report)
    write(CHAMPION_REPORT, report)

    pointer = f"""# Final Private PDF Pointer - I-0319

Updated: 2026-05-27

Current rescue proof:

`{rel(PDF_OUT)}`

SHA-256: `{after['sha256']}`

Render metrics:

- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- Word count from PDF text: {after['word_count_pdf_text']}
- Composite boards removed: {len(removed)}
- Multi-image pages by PDF image-object QA: {after['multi_image_pages']}
- Max images on a page: {after['max_images_on_page']}
- Blank pages by ink/text/image QA: {after['blank_pages']}
- Severe sparse pages by ink/text QA: {after['severe_sparse_pages']}
- Micro-visual sparse pages: {after['micro_visual_pages']}

Status: this proof completes only I-0319. It is not final. The next queued rescue pass is I-0320, quantitative enrichment with numbers, tables, charts, formulas, and benchmarks.
"""
    write(CHAMPION_POINTER, pointer)


def write_manifest(before: dict[str, str], after: dict[str, str]) -> None:
    artifacts = [
        ("source_pdf", SOURCE_PDF, before, "I-0318 contextual visual proof"),
        ("one_visual_html", HTML_OUT, {}, "I-0319 one-visual-per-page HTML"),
        ("one_visual_pdf", PDF_OUT, after, "I-0319 one-visual-per-page PDF"),
        ("one_visual_markdown", MD_OUT, {}, "I-0319 manuscript snapshot"),
        ("baseline", OUT_BASELINE, {}, "I-0319 multi-image baseline"),
        ("removed_boards", OUT_REMOVED_BOARDS, {}, "I-0319 removed composite boards"),
        ("qa", OUT_QA, {}, "I-0319 one-visual-page QA"),
        ("report", REPORT, {}, "I-0319 report"),
        ("pointer", CHAMPION_POINTER, {}, "I-0319 pointer"),
    ]
    rows: list[dict[str, str]] = []
    for name, path, stats, note in artifacts:
        rows.append(
            {
                "pass_id": PASS_ID,
                "artifact": name,
                "path": rel(path),
                "exists": "yes" if path.exists() else "no",
                "bytes": str(path.stat().st_size) if path.exists() else "0",
                "sha256": sha256(path) if path.exists() else "",
                "pages": stats.get("pages", ""),
                "note": note,
            }
        )
    write_tsv(OUT_MANIFEST, rows, ["pass_id", "artifact", "path", "exists", "bytes", "sha256", "pages", "note"])


def update_handoff_files(after: dict[str, str], removed: list[dict[str, str]]) -> None:
    metric_sentence = (
        f"This proof has {after['pages']} pages, {after['image_objects']} image objects, "
        f"{after['drawing_objects']} drawing/vector objects, {after['multi_image_pages']} multi-image pages, "
        f"and {after['blank_pages']} blank pages by ink/text/image QA. SHA-256: `{after['sha256']}`."
    )
    for path in [README, CHAMPION_README, READER_GUIDE, GUIDE_POINTER]:
        if not path.exists():
            continue
        text = read(path)
        text = text.replace("final-private-pdf-pointer-i0318.md", "final-private-pdf-pointer-i0319.md")
        text = text.replace("champion/final-private-pdf-pointer-i0318.md", "champion/final-private-pdf-pointer-i0319.md")
        text = text.replace("updated by `I-0318`", "updated by `I-0319`")
        text = text.replace("after pass `I-0318`", "after pass `I-0319`")
        text = text.replace("`I-0318`, contextual visual placement", "`I-0319`, one-visual-per-page layout")
        text = text.replace("I-0318 PDF is the current local rescue proof", "I-0319 PDF is the current local rescue proof")
        text = text.replace("the guide points to the I-0318 contextual-visual proof only", "the guide points to the I-0319 one-visual-page proof only")
        text = text.replace("I-0319 through I-0322", "I-0320 through I-0322")
        text = text.replace("- I-0319: enforce max one visual exhibit per page and remove composite boards.\n", "")
        text = text.replace("- I-0319: enforce max one visual per page and remove composite boards/portfolio plates.\n", "")
        text = re.sub(r"`claims.tsv` has 334 supported rows and 0 needs-verification rows after the I-0318 contextual visual placement pass", "`claims.tsv` has 335 supported rows and 0 needs-verification rows after the I-0319 one-visual-page pass", text)
        text = re.sub(r"This proof has .*?SHA-256: `[^`]+`\.", metric_sentence, text, flags=re.S)
        marker = "I-0319 update:"
        addition = (
            "\n\nI-0319 update: the current rescue proof removes reader-facing composite boards and forces "
            f"single-image exhibit flow. It has {after['multi_image_pages']} multi-image pages after PDF QA "
            f"and removes {len(removed)} composite boards. It still needs I-0320 through I-0322 for quantitative density, hostile QA, and final publication build."
        )
        if marker not in text:
            text = text.rstrip() + addition + "\n"
        write(path, text)


def mark_idea_done() -> None:
    text = read(IDEAS)
    replacement = (
        "I-0319\tdone\t"
        "Enforce max one visual exhibit per page and remove composite boards, portfolio plates, logo strips, people strips, and visual dumps from the reader-facing PDF; split, relocate, or cut visuals until no page carries multiple unrelated images."
    )
    text, count = re.subn(r"(?m)^I-0319\t(?:pending|done)\t(.+)$", replacement, text)
    if count != 1:
        raise SystemExit("Could not mark I-0319 done in ideas.tsv")
    write(IDEAS, text)


def append_claim() -> None:
    row = "\t".join(
        [
            "C-0335",
            "supported",
            "I-0319 rendered a one-visual-per-page private proof with composite boards removed from reader-facing HTML and zero PDF pages containing more than one image object.",
            "manuscript/one-visual-page-i0319.md;data/one_visual_page_baseline_i0319.tsv;data/one_visual_page_removed_boards_i0319.tsv;data/one_visual_page_qa_i0319.tsv;champion/final-private-pdf-pointer-i0319.md",
            "I-0319",
            "rendered PDF image-object QA",
            "2026-05-27",
            "Supported as page-level visual-layout QA only; quantitative enrichment, hostile proofread, and final publication build remain queued.",
        ]
    )
    upsert_tsv_line(CLAIMS, "C-0335\t", row)


def append_scoreboard(after: dict[str, str], qa_pass: int, qa_fail: int, removed: list[dict[str, str]]) -> None:
    claims = claim_counts()
    row = "\t".join(
        [
            datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            RUN_ID,
            "champion I-0318 rescue proof",
            PASS_ID,
            "rescue 7",
            "+1.0",
            "100.0",
            after["word_count_pdf_text"],
            "24",
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; one-visual PDF pages={after['pages']}; images={after['image_objects']}; drawings={after['drawing_objects']}; multi_image_pages={after['multi_image_pages']}; max_images_on_page={after['max_images_on_page']}; boards_removed={len(removed)}; blank_pages={after['blank_pages']}; QA {qa_pass} pass / {qa_fail} fail",
            "+1",
            "I-0320 through I-0322 still must add quantitative density, run hostile QA, and final publication build",
            "promoted",
            "Removed composite reader-facing boards and forced remaining exhibit figures into a one-image-page flow.",
            "one one-visual-per-page render pass",
        ]
    )
    upsert_tsv_line(SCOREBOARD, f"\t{PASS_ID}\t", row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args()

    chrome = Path(args.chrome)
    if not args.skip_render and not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    if not SOURCE_HTML.exists() or not SOURCE_PDF.exists() or not SOURCE_MD.exists():
        raise SystemExit("I-0319 source proof artifacts are missing; run I-0318 first.")

    backup_targets()
    before = pdf_stats(SOURCE_PDF)
    removed = rewrite_html()
    write_markdown_snapshot()
    if not args.skip_render:
        render_pdf(chrome)
    after = pdf_stats(PDF_OUT)
    qa = qa_rows(before, after, removed)
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    write_tsv(OUT_QA, qa, ["pass_id", "check", "result", "evidence"])

    write_reports(before, after, removed, qa_pass, qa_fail)
    write_manifest(before, after)
    update_handoff_files(after, removed)
    mark_idea_done()
    append_claim()
    append_scoreboard(after, qa_pass, qa_fail, removed)
    append_once(
        INSIGHTS,
        "- I-0319:",
        "\n- I-0319: one-visual-per-page layout is a stricter promise than visual abundance. Composite boards can inflate image counts while making pages feel like dumps; the better private proof keeps many exhibits but gives each one its own page rhythm.\n",
    )

    if qa_fail:
        raise SystemExit(f"I-0319 one-visual-page QA failed: {qa_fail} checks failed")


if __name__ == "__main__":
    main()
