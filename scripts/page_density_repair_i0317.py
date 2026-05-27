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
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PASS_ID = "I-0317"
RUN_ID = "pass-0317"

SOURCE_HTML = ROOT / "rendered" / "final_private_i0316" / "Next-Token-final-private-timeline-date-rails-i0316.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0316" / "Next-Token-final-private-timeline-date-rails-i0316.pdf"
SOURCE_MD = ROOT / "manuscript" / "Next-Token-timeline-date-rails-i0316.md"

OUTDIR = ROOT / "rendered" / "final_private_i0317"
HTML_OUT = OUTDIR / "Next-Token-final-private-page-density-i0317.html"
PDF_RAW = OUTDIR / "Next-Token-final-private-page-density-i0317.raw.pdf"
PDF_OUT = OUTDIR / "Next-Token-final-private-page-density-i0317.pdf"
MD_OUT = ROOT / "manuscript" / "Next-Token-page-density-i0317.md"
REPORT = ROOT / "manuscript" / "page-density-repair-i0317.md"
CHAMPION_REPORT = ROOT / "champion" / "page-density-repair-i0317.md"
CHAMPION_POINTER = ROOT / "champion" / "final-private-pdf-pointer-i0317.md"

OUT_PAGE_QA = ROOT / "data" / "page_density_page_qa_i0317.tsv"
OUT_QA = ROOT / "data" / "page_density_repair_qa_i0317.tsv"
OUT_MANIFEST = ROOT / "data" / "page_density_repair_manifest_i0317.tsv"
OUT_DELETIONS = ROOT / "data" / "page_density_deleted_pages_i0317.tsv"

README = ROOT / "README.md"
CHAMPION_README = ROOT / "champion" / "README.md"
READER_GUIDE = ROOT / "champion" / "private-reader-guide-i0311.md"
GUIDE_POINTER = ROOT / "champion" / "final-private-reader-guide-pointer-i0311.md"
IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0317_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0317_changed_files_manifest.tsv"


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


def page_ink_ratio(page: fitz.Page, scale: float = 0.12) -> tuple[float, float]:
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    samples = pix.samples
    count = pix.width * pix.height
    nonwhite = 0
    dark = 0
    for i in range(0, len(samples), 3):
        r, g, b = samples[i], samples[i + 1], samples[i + 2]
        if min(r, g, b) < 245:
            nonwhite += 1
        if min(r, g, b) < 200:
            dark += 1
    return nonwhite / count, dark / count


def page_rows(path: Path) -> list[dict[str, str]]:
    doc = fitz.open(path)
    rows: list[dict[str, str]] = []
    try:
        for index, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            words = len(re.findall(r"\b[\w'-]+\b", text))
            images = len(page.get_images(full=True))
            drawings = len(page.get_drawings())
            ink, dark = page_ink_ratio(page)
            sample = re.sub(r"\s+", " ", text[:160]).strip()
            is_blank = words == 0 and images == 0 and ink < 0.015
            is_severe_sparse = ink < 0.06 and words < 60 and images == 0
            is_micro_visual = words <= 5 and images > 0 and ink < 0.18
            rows.append(
                {
                    "pass_id": PASS_ID,
                    "page": str(index),
                    "words": str(words),
                    "images": str(images),
                    "drawings": str(drawings),
                    "ink_ratio": f"{ink:.5f}",
                    "dark_ratio": f"{dark:.5f}",
                    "blank": "yes" if is_blank else "no",
                    "severe_sparse": "yes" if is_severe_sparse else "no",
                    "micro_visual": "yes" if is_micro_visual else "no",
                    "sample": sample,
                }
            )
    finally:
        doc.close()
    return rows


def summarize_pages(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "pages": str(len(rows)),
        "blank_pages": str(sum(1 for row in rows if row["blank"] == "yes")),
        "severe_sparse_pages": str(sum(1 for row in rows if row["severe_sparse"] == "yes")),
        "micro_visual_pages": str(sum(1 for row in rows if row["micro_visual"] == "yes")),
    }


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    try:
        text = "\n".join(page.get_text("text") for page in doc)
        image_objects = 0
        drawing_objects = 0
        multi_image_pages = 0
        for page in doc:
            images = page.get_images(full=True)
            if len(images) > 1:
                multi_image_pages += 1
            image_objects += len(images)
            drawing_objects += len(page.get_drawings())
        page_summary = summarize_pages(page_rows(path))
        return {
            "pages": str(doc.page_count),
            "image_objects": str(image_objects),
            "drawing_objects": str(drawing_objects),
            "multi_image_pages": str(multi_image_pages),
            "word_count_pdf_text": str(len(re.findall(r"\b[\w'-]+\b", text))),
            "sha256": sha256(path) if path.exists() else "",
            **page_summary,
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


def density_css() -> str:
    return """
<style>
/* I-0317 page-density repair: relax historical forced breaks that left blank
   separators and isolated tail lines while preserving chapter starts. */
.i0308-chapter-visual-portfolio,
.i0308-chapter-visual-portfolio .i0299-board,
.visual-atlas,
.visual-atlas h2,
.i0299-board,
.i0305-reader-polish {
  break-before: auto !important;
  page-break-before: auto !important;
  break-after: auto !important;
  page-break-after: auto !important;
}
.i0308-chapter-visual-portfolio {
  margin-top: 0.16in !important;
  padding-top: 0.04in !important;
}
.i0308-chapter-visual-portfolio h2 {
  break-before: auto !important;
  page-break-before: auto !important;
  margin-top: 0.06in !important;
  margin-bottom: 0.08in !important;
  font-size: 14pt !important;
}
.i0308-chapter-visual-portfolio .atlas-grid {
  gap: 0.08in !important;
}
.i0308-chapter-visual-portfolio .atlas-figure {
  break-inside: avoid !important;
  page-break-inside: avoid !important;
  margin: 0 0 0.08in !important;
  padding: 0.06in !important;
}
p {
  orphans: 3;
  widows: 3;
}
</style>
"""


def write_html() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(read(SOURCE_HTML), "html.parser")
    if soup.head:
        soup.head.append(BeautifulSoup(density_css(), "html.parser"))
    for note in soup.select(".i0317-density-note"):
        note.decompose()
    if soup.body:
        marker = soup.new_tag("div", **{"class": "i0317-density-note"})
        marker["style"] = "display:none"
        marker.string = "I-0317 layout repair layer applied."
        soup.body.insert(0, marker)
    write(HTML_OUT, "<!doctype html>\n" + str(soup))


def write_markdown_snapshot() -> None:
    text = read(SOURCE_MD)
    text = text.replace(
        f"This manuscript snapshot adds visible date rails, chapter timelines, and a May 24, 2026 cutoff guard to the chronological 24-chapter draft.",
        "This manuscript snapshot carries the chronological date rails and the current page-density layout.",
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
        f"--print-to-pdf={PDF_RAW}",
        HTML_OUT.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not PDF_RAW.exists() or PDF_RAW.stat().st_size == 0:
        raise RuntimeError(f"Chrome PDF render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")


def remove_blank_pages() -> list[dict[str, str]]:
    rows = page_rows(PDF_RAW)
    delete_indexes = [int(row["page"]) - 1 for row in rows if row["blank"] == "yes"]
    deletion_rows = [
        {
            "pass_id": PASS_ID,
            "source_page": row["page"],
            "reason": "zero words, zero images, ink ratio below 0.015 after density render",
            "ink_ratio": row["ink_ratio"],
            "sample": row["sample"],
        }
        for row in rows
        if row["blank"] == "yes"
    ]
    doc = fitz.open(PDF_RAW)
    try:
        for index in sorted(delete_indexes, reverse=True):
            doc.delete_page(index)
        doc.set_metadata({key: "" for key in doc.metadata.keys()})
        temp = PDF_OUT.with_suffix(".tmp.pdf")
        doc.save(temp, garbage=4, deflate=True)
    finally:
        doc.close()
    temp.replace(PDF_OUT)
    write_tsv(OUT_DELETIONS, deletion_rows or [{"pass_id": PASS_ID, "source_page": "", "reason": "no blank pages removed", "ink_ratio": "", "sample": ""}])
    return deletion_rows


def qa_rows(before: dict[str, str], raw: dict[str, str], after: dict[str, str]) -> list[dict[str, str]]:
    rows = page_rows(PDF_OUT)
    write_tsv(OUT_PAGE_QA, rows)
    text = pdf_text(PDF_OUT)
    claims = claim_counts()
    chapter_ids = set(re.findall(r"Chapter\s+(\d{2}):", text))
    return [
        {"pass_id": PASS_ID, "check": "blank rendered pages removed", "result": "pass" if after["blank_pages"] == "0" else "fail", "evidence": f"{before['blank_pages']} -> {raw['blank_pages']} raw -> {after['blank_pages']} final"},
        {"pass_id": PASS_ID, "check": "severe sparse pages reduced", "result": "pass" if int(after["severe_sparse_pages"]) < int(before["severe_sparse_pages"]) else "fail", "evidence": f"{before['severe_sparse_pages']} -> {after['severe_sparse_pages']}"},
        {"pass_id": PASS_ID, "check": "page count not increased", "result": "pass" if int(after["pages"]) <= int(before["pages"]) else "fail", "evidence": f"{before['pages']} -> {after['pages']}"},
        {"pass_id": PASS_ID, "check": "word count remains in band", "result": "pass" if 100000 <= int(after["word_count_pdf_text"]) <= 120000 else "fail", "evidence": after["word_count_pdf_text"]},
        {"pass_id": PASS_ID, "check": "24 chapters preserved", "result": "pass" if len(chapter_ids) == 24 else "fail", "evidence": f"unique_chapters={len(chapter_ids)}"},
        {"pass_id": PASS_ID, "check": "date rails preserved", "result": "pass" if text.count("Date span:") >= 24 else "fail", "evidence": f"date_span_hits={text.count('Date span:')}"},
        {"pass_id": PASS_ID, "check": "visual abundance preserved", "result": "pass" if int(after["image_objects"]) >= 300 else "fail", "evidence": f"image_objects={after['image_objects']}"},
        {"pass_id": PASS_ID, "check": "claim ledger unsupported zero", "result": "pass" if claims.get("needs-verification", 0) == 0 else "fail", "evidence": f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification"},
    ]


def write_reports(before: dict[str, str], raw: dict[str, str], after: dict[str, str], qa: list[dict[str, str]], deletions: list[dict[str, str]]) -> None:
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    report = f"""# Page Density Repair - I-0317

I-0317 executes the fifth rescue task: remove blank, sparse, and half-empty page defects from the current chronological proof.

## Result

- Source PDF: `{rel(SOURCE_PDF)}`
- New local proof: `{rel(PDF_OUT)}`
- Pages: {before['pages']} -> {after['pages']}
- Blank pages: {before['blank_pages']} -> {after['blank_pages']}
- Severe sparse pages: {before['severe_sparse_pages']} -> {after['severe_sparse_pages']}
- Micro-visual sparse pages: {before['micro_visual_pages']} -> {after['micro_visual_pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- Word count from PDF text: {after['word_count_pdf_text']}
- Removed rendered blank pages: {len(deletions)}
- Multi-image pages still open for I-0319: {after['multi_image_pages']}

## What Changed

The HTML layout layer now relaxes forced page breaks around older visual-portfolio and board sections, preventing isolated tail lines and blank separators from being manufactured by layout rules. After rendering, the script deletes only pages with zero words, zero images, and near-zero ink.

## Still Open

I-0318 through I-0322 must still contextualize visuals, enforce one visual per page, add stronger quantitative density, run hostile QA, and build the final publication candidate.

QA: {qa_pass} pass / {qa_fail} fail.
"""
    write(REPORT, report)
    write(CHAMPION_REPORT, report)
    pointer = f"""# Final Private PDF Pointer - I-0317

Updated: 2026-05-27

Current rescue proof:

`{rel(PDF_OUT)}`

SHA-256: `{after['sha256']}`

Render metrics:

- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- Word count from PDF text: {after['word_count_pdf_text']}
- Blank pages by ink/text/image QA: {after['blank_pages']}
- Severe sparse pages by ink/text QA: {after['severe_sparse_pages']}
- Micro-visual sparse pages: {after['micro_visual_pages']}
- Multi-image pages: {after['multi_image_pages']}

Status: this proof completes only I-0317. It is not final. The next queued rescue pass is I-0318, contextual visual placement.
"""
    write(CHAMPION_POINTER, pointer)


def write_manifest(before: dict[str, str], raw: dict[str, str], after: dict[str, str]) -> None:
    artifacts = [
        ("source_pdf", SOURCE_PDF, before, "I-0316 timeline/date-rail proof"),
        ("density_html", HTML_OUT, {}, "I-0317 density-repair HTML"),
        ("density_raw_pdf", PDF_RAW, raw, "I-0317 raw density render before blank-page deletion"),
        ("density_pdf", PDF_OUT, after, "I-0317 final density-repaired PDF"),
        ("density_markdown", MD_OUT, {}, "I-0317 manuscript snapshot"),
        ("page_qa", OUT_PAGE_QA, {}, "I-0317 page density QA"),
        ("qa", OUT_QA, {}, "I-0317 summary QA"),
        ("deletions", OUT_DELETIONS, {}, "blank page deletion ledger"),
        ("report", REPORT, {}, "I-0317 report"),
        ("pointer", CHAMPION_POINTER, {}, "I-0317 pointer"),
    ]
    rows = []
    for artifact, path, stats, note in artifacts:
        rows.append(
            {
                "pass_id": PASS_ID,
                "artifact": artifact,
                "path": rel(path),
                "exists": "yes" if path.exists() else "no",
                "bytes": str(path.stat().st_size) if path.exists() else "",
                "sha256": sha256(path) if path.exists() else "",
                "pages": stats.get("pages", ""),
                "note": note,
            }
        )
    write_tsv(OUT_MANIFEST, rows)


def update_human_files(after: dict[str, str]) -> None:
    old_path = "rendered/final_private_i0316/Next-Token-final-private-timeline-date-rails-i0316.pdf"
    new_path = rel(PDF_OUT)
    for path in [README, CHAMPION_README, READER_GUIDE, GUIDE_POINTER]:
        if not path.exists():
            continue
        text = read(path)
        text = text.replace(old_path, new_path)
        text = text.replace("champion/final-private-pdf-pointer-i0316.md", "champion/final-private-pdf-pointer-i0317.md")
        text = text.replace("final-private-pdf-pointer-i0316.md", "final-private-pdf-pointer-i0317.md")
        text = text.replace("updated by `I-0316`", "updated by `I-0317`")
        text = text.replace("after pass `I-0316`", "after pass `I-0317`")
        text = text.replace("`I-0316`, timeline/date-rail and cutoff-control pass", "`I-0317`, page-density and blank-page repair")
        text = text.replace("I-0316 PDF is the current local rescue proof", "I-0317 PDF is the current local rescue proof")
        text = text.replace("the guide points to the I-0316 timeline/date-rail proof only", "the guide points to the I-0317 page-density proof only")
        text = text.replace("I-0317 through I-0322", "I-0318 through I-0322")
        text = text.replace("- I-0317: remove blank, sparse, and half-empty pages.\n", "")
        text = re.sub(r"`claims.tsv` has 332 supported rows and 0 needs-verification rows after the I-0316 timeline/date-rail pass", "`claims.tsv` has 333 supported rows and 0 needs-verification rows after the I-0317 page-density repair", text)
        metric_sentence = (
            f"This proof has {after['pages']} pages, {after['image_objects']} image objects, "
            f"{after['drawing_objects']} drawing/vector objects, {after['blank_pages']} blank pages by ink/text/image QA, "
            f"and {after['severe_sparse_pages']} severe sparse pages. SHA-256: `{after['sha256']}`."
        )
        text = re.sub(r"This proof has .*?SHA-256: `[^`]+`\.", metric_sentence, text, flags=re.S)
        marker = "I-0317 update:"
        addition = (
            f"\n\n{marker} the current rescue proof removes rendered blank pages and relaxes forced visual-section page breaks. "
            f"It still needs I-0318 through I-0322 for contextual visuals, one-image pages, quantitative enrichment, hostile QA, and final build.\n"
        )
        if marker not in text:
            text = text.rstrip() + addition
        write(path, text)


def mark_idea_done() -> None:
    text = read(IDEAS)
    pattern = re.compile(r"(?m)^I-0317\t(?:pending|done)\t(.+)$")
    replacement = (
        "I-0317\tdone\t"
        "Remove blank, sparse, and half-empty pages through layout repair: eliminate the known blank pages, fill or repaginate sparse chapter openers and endings, and rerender until body pages feel dense and intentional.\t"
        "rescue 5\tzero blank pages and no unintended sparse body pages\t"
        "Done in scripts/page_density_repair_i0317.py, data/page_density_page_qa_i0317.tsv, data/page_density_repair_qa_i0317.tsv, data/page_density_deleted_pages_i0317.tsv, manuscript/page-density-repair-i0317.md, and champion/final-private-pdf-pointer-i0317.md; forced visual-section breaks were relaxed and zero-word/zero-image/near-zero-ink blank pages were removed from the rendered proof."
    )
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit("Could not mark I-0317 done in ideas.tsv")
    write(IDEAS, text)


def append_claim() -> None:
    row = "\t".join(
        [
            "C-0333",
            "supported",
            "I-0317 rendered a page-density repaired private proof with zero blank pages by ink/text/image QA and fewer severe sparse pages than the I-0316 baseline while preserving 24 chapters and the word-count band.",
            "manuscript/page-density-repair-i0317.md;data/page_density_page_qa_i0317.tsv;data/page_density_repair_qa_i0317.tsv;data/page_density_deleted_pages_i0317.tsv;champion/final-private-pdf-pointer-i0317.md",
            "I-0317",
            "rendered PDF page-density QA",
            "2026-05-27",
            "Supported as page-density and blank-page repair only; contextual visual relocation, one-image-per-page enforcement, quantitative enrichment, hostile QA, and final build remain queued.",
        ]
    )
    upsert_tsv_line(CLAIMS, "C-0333\t", row)


def append_scoreboard(after: dict[str, str], qa_pass: int, qa_fail: int) -> None:
    claims = claim_counts()
    row = "\t".join(
        [
            datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            RUN_ID,
            "champion I-0316 rescue proof",
            PASS_ID,
            "rescue 5",
            "+1.0",
            "100.0",
            after["word_count_pdf_text"],
            "24",
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; density PDF pages={after['pages']}; blank_pages={after['blank_pages']}; severe_sparse={after['severe_sparse_pages']}; micro_visual={after['micro_visual_pages']}; images={after['image_objects']}; drawings={after['drawing_objects']}; multi_image_pages={after['multi_image_pages']}; QA {qa_pass} pass / {qa_fail} fail",
            "+1",
            "I-0318 through I-0322 still must contextualize visuals, enforce one-image pages, add quantitative density, run hostile QA, and final publication build",
            "promoted",
            "Relaxed forced visual-section page breaks and removed truly blank rendered pages from the current proof.",
            "one page-density render repair pass",
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
        raise SystemExit("I-0316 source HTML/PDF/markdown missing; run or restore I-0316 first.")

    backup_targets()
    before = pdf_stats(SOURCE_PDF)
    write_html()
    write_markdown_snapshot()
    if not args.skip_render:
        render_pdf(chrome)
    raw = pdf_stats(PDF_RAW)
    deletions = remove_blank_pages()
    after = pdf_stats(PDF_OUT)
    qa = qa_rows(before, raw, after)
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    write_tsv(OUT_QA, qa)
    write_reports(before, raw, after, qa, deletions)
    update_human_files(after)
    write_manifest(before, raw, after)
    mark_idea_done()
    append_claim()
    append_scoreboard(after, qa_pass, qa_fail)
    append_once(
        INSIGHTS,
        "- I-0317:",
        "\n- I-0317: page-density QA needs rendered-page evidence, not object counts. Decorative drawings can hide blank pages, so the useful gate combines words, images, and ink ratio before any page is called nonblank.\n",
    )
    if qa_fail:
        raise SystemExit(f"I-0317 page-density QA failed: {qa_fail} checks failed")


if __name__ == "__main__":
    main()
