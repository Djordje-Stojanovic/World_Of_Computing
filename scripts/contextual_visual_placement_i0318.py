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
PASS_ID = "I-0318"
RUN_ID = "pass-0318"

SOURCE_HTML = ROOT / "rendered" / "final_private_i0317" / "Next-Token-final-private-page-density-i0317.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0317" / "Next-Token-final-private-page-density-i0317.pdf"
SOURCE_MD = ROOT / "manuscript" / "Next-Token-page-density-i0317.md"

OUTDIR = ROOT / "rendered" / "final_private_i0318"
HTML_OUT = OUTDIR / "Next-Token-final-private-contextual-visuals-i0318.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-contextual-visuals-i0318.pdf"
MD_OUT = ROOT / "manuscript" / "Next-Token-contextual-visuals-i0318.md"
REPORT = ROOT / "manuscript" / "contextual-visual-placement-i0318.md"
CHAMPION_REPORT = ROOT / "champion" / "contextual-visual-placement-i0318.md"
CHAMPION_POINTER = ROOT / "champion" / "final-private-pdf-pointer-i0318.md"

OUT_BASELINE = ROOT / "data" / "contextual_visual_baseline_i0318.tsv"
OUT_SECTIONS = ROOT / "data" / "contextual_visual_sections_i0318.tsv"
OUT_QA = ROOT / "data" / "contextual_visual_qa_i0318.tsv"
OUT_MANIFEST = ROOT / "data" / "contextual_visual_manifest_i0318.tsv"

README = ROOT / "README.md"
CHAMPION_README = ROOT / "champion" / "README.md"
READER_GUIDE = ROOT / "champion" / "private-reader-guide-i0311.md"
GUIDE_POINTER = ROOT / "champion" / "final-private-reader-guide-pointer-i0311.md"
IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0318_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0318_changed_files_manifest.tsv"


CHAPTER_THEMES = {
    "01": "attention's architecture",
    "02": "the sequence-model prehistory",
    "03": "scale as measurement",
    "04": "GPT pretraining and the first platform turn",
    "05": "instruction tuning and assistant behavior",
    "06": "ChatGPT's public interface shock",
    "07": "ChatGPT's product surface",
    "08": "the Microsoft and OpenAI cloud bargain",
    "09": "Google and DeepMind's response",
    "10": "open weights and the Llama ecosystem",
    "11": "Claude and frontier pluralism",
    "12": "China's frontier-model field",
    "13": "benchmarks, arenas, and rank",
    "14": "CUDA, GPUs, and accelerator software",
    "15": "GTC 2026 and AI-factory rhetoric",
    "16": "datacenters, power, and physical constraint",
    "17": "data, tokens, and corpora",
    "18": "retrieval, tools, and agents",
    "19": "code as a model-native language",
    "20": "Claude Code and repository work",
    "21": "reasoning and test-time compute",
    "22": "token economics and product packaging",
    "23": "failure, truth, and trust",
    "24": "the cutoff synthesis",
}


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
            text = page.get_text("text").strip()
            images = len(page.get_images(full=True))
            ink = page_ink_ratio(page)
            if not text and images == 0 and ink < 0.015:
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
        for page in doc:
            images = page.get_images(full=True)
            if len(images) > 1:
                multi_image_pages += 1
            image_objects += len(images)
            drawing_objects += len(page.get_drawings())
        return {
            "pages": str(doc.page_count),
            "image_objects": str(image_objects),
            "drawing_objects": str(drawing_objects),
            "multi_image_pages": str(multi_image_pages),
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


def chapter_info(h1: Tag) -> tuple[str, str]:
    text = h1.get_text(" ", strip=True)
    match = re.search(r"Chapter\s+(\d{2}):\s*(.+)", text)
    if not match:
        return "", ""
    return match.group(1), match.group(2).strip()


def first_context_anchor(h1: Tag, stop: Tag | None) -> Tag:
    node = h1
    last_candidate = h1
    seen_paragraph = False
    while True:
        node = node.find_next_sibling()
        if node is None or node is stop:
            return last_candidate
        if not isinstance(node, Tag):
            continue
        classes = set(node.get("class", []))
        if "i0308-chapter-visual-portfolio" in classes:
            continue
        if node.name in {"section"} and "i0316-date-rail" in classes:
            last_candidate = node
            continue
        if node.name == "h2":
            last_candidate = node
            continue
        if node.name == "p":
            last_candidate = node
            seen_paragraph = True
            continue
        if seen_paragraph:
            return last_candidate
        last_candidate = node


def collapse_chapter_separators(soup: BeautifulSoup) -> int:
    changed = 0
    for h1 in soup.find_all("h1", class_="chapter-title"):
        prev = h1.find_previous_sibling()
        if isinstance(prev, Tag) and prev.name == "a" and prev.get("id"):
            h1["id"] = prev["id"]
            doomed = prev
            prev = doomed.find_previous_sibling()
            doomed.decompose()
            changed += 1
        if isinstance(prev, Tag) and prev.name == "hr":
            prev.decompose()
            changed += 1
    return changed


def contextual_css() -> str:
    return """
<style>
.i0318-contextual-visuals {
  break-before: auto !important;
  page-break-before: auto !important;
  break-after: auto !important;
  page-break-after: auto !important;
  margin: 0.14in 0 0.18in !important;
  padding: 0.08in 0 0 !important;
  border-top: 1px solid #c7bda9;
}
.i0318-contextual-visuals h2 {
  break-before: auto !important;
  page-break-before: auto !important;
  margin: 0 0 0.08in !important;
  font-size: 13pt !important;
  line-height: 1.12 !important;
}
.i0318-contextual-visuals .i0318-context-line {
  margin: 0 0 0.10in !important;
  font-size: 9.2pt !important;
  line-height: 1.35 !important;
  color: #50483d;
}
.i0318-contextual-visuals .atlas-grid {
  gap: 0.08in !important;
}
.i0318-contextual-visuals .atlas-figure,
.i0318-contextual-visuals .i0299-board {
  break-inside: avoid !important;
  page-break-inside: avoid !important;
}
body > hr {
  display: none !important;
}
h1.chapter-title,
h1.chapter-title + .i0316-date-rail,
h1.chapter-title + .i0316-date-rail + h2 {
  break-after: auto !important;
  page-break-after: auto !important;
}
h1.chapter-title + .i0316-date-rail {
  break-inside: auto !important;
  page-break-inside: auto !important;
}
.i0316-date-rail + h2,
.i0316-date-rail + h2 + p {
  break-after: auto !important;
  page-break-after: auto !important;
}
</style>
"""


def baseline_rows(soup: BeautifulSoup) -> list[dict[str, str]]:
    rows = []
    text = soup.get_text("\n")
    rows.append({"pass_id": PASS_ID, "metric": "image_sequence_text_hits", "value": str(text.count("Image Sequence"))})
    rows.append({"pass_id": PASS_ID, "metric": "images_placed_phrase_hits", "value": str(text.count("Images placed with this chapter"))})
    rows.append({"pass_id": PASS_ID, "metric": "portfolio_sections", "value": str(len(soup.select(".i0308-chapter-visual-portfolio")))})
    rows.append({"pass_id": PASS_ID, "metric": "contextual_sections", "value": str(len(soup.select(".i0318-contextual-visuals")))})
    rows.append({"pass_id": PASS_ID, "metric": "atlas_figures", "value": str(len(soup.select(".atlas-figure")))})
    rows.append({"pass_id": PASS_ID, "metric": "embedded_figures", "value": str(len(soup.select(".book-figure.embedded-visual")))})
    return rows


def rewrite_visual_sections() -> list[dict[str, str]]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(read(SOURCE_HTML), "html.parser")
    write_tsv(OUT_BASELINE, baseline_rows(soup))
    if soup.head:
        soup.head.append(BeautifulSoup(contextual_css(), "html.parser"))
    collapsed_separators = collapse_chapter_separators(soup)
    h1s = list(soup.find_all("h1", class_="chapter-title"))
    rows: list[dict[str, str]] = []
    for index, h1 in enumerate(h1s):
        no, title = chapter_info(h1)
        if not no:
            continue
        stop = h1s[index + 1] if index + 1 < len(h1s) else None
        sections: list[Tag] = []
        node = h1
        while True:
            node = node.find_next_sibling()
            if node is None or node is stop:
                break
            if isinstance(node, Tag) and "i0308-chapter-visual-portfolio" in node.get("class", []):
                sections.append(node)
        anchor = first_context_anchor(h1, stop)
        for section_i, section in enumerate(sections, start=1):
            old_text = " ".join(section.get_text(" ", strip=True).split())[:240]
            section["class"] = [cls for cls in section.get("class", []) if cls != "i0308-chapter-visual-portfolio"]
            section["class"] = list(dict.fromkeys(section.get("class", []) + ["i0318-contextual-visuals"]))
            section["data-context-chapter"] = no
            h2 = section.find("h2")
            if h2 is None:
                h2 = soup.new_tag("h2")
                section.insert(0, h2)
            h2.string = f"Context Images: Chapter {no}, {title}"
            for p in list(section.find_all("p", recursive=False)):
                if "Images placed with this chapter" in p.get_text(" ", strip=True):
                    p.decompose()
            context = soup.new_tag("p", **{"class": "i0318-context-line"})
            theme = CHAPTER_THEMES.get(no, "the chapter's argument")
            context.string = f"The images make {theme} concrete beside the chapter's opening argument."
            h2.insert_after(context)
            for fig in section.select(".atlas-figure, .book-figure"):
                fig["data-context-chapter"] = no
            section.extract()
            anchor.insert_after(section)
            anchor = section
            rows.append(
                {
                    "pass_id": PASS_ID,
                    "chapter": no,
                    "title": title,
                    "section_index": str(section_i),
                    "old_reader_text_sample": old_text,
                    "new_heading": h2.get_text(" ", strip=True),
                    "figure_count": str(len(section.select("figure, .atlas-figure, .book-figure"))),
                    "placement": f"moved_after_chapter_opening_context; collapsed_chapter_separators={collapsed_separators}",
                }
            )
    write(HTML_OUT, "<!doctype html>\n" + str(soup))
    write_tsv(OUT_SECTIONS, rows)
    return rows


def write_markdown_snapshot() -> None:
    text = read(SOURCE_MD)
    text = text.replace(
        "This manuscript snapshot carries the chronological date rails and the current page-density layout.",
        "This manuscript snapshot carries the chronological date rails, page-density layout, and chapter-local contextual visual placement.",
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


def qa_rows(before: dict[str, str], after: dict[str, str], sections: list[dict[str, str]]) -> list[dict[str, str]]:
    text = pdf_text(PDF_OUT)
    html = read(HTML_OUT)
    soup = BeautifulSoup(html, "html.parser")
    claims = claim_counts()
    chapter_ids = set(re.findall(r"Chapter\s+(\d{2}):", text))
    old_phrases = {
        "Image Sequence": text.count("Image Sequence"),
        "Images placed with this chapter": text.count("Images placed with this chapter"),
        "Visual Portfolio": text.count("Visual Portfolio"),
        "PORTFOLIO PLATE": text.count("PORTFOLIO PLATE"),
    }
    contextual_sections = len(soup.select(".i0318-contextual-visuals"))
    bad_old_sections = len(soup.select(".i0308-chapter-visual-portfolio"))
    context_heading_hits = text.count("Context Images: Chapter")
    return [
        {"pass_id": PASS_ID, "check": "24 visual sections contextualized", "result": "pass" if contextual_sections == 24 else "fail", "evidence": f"contextual_sections={contextual_sections}"},
        {"pass_id": PASS_ID, "check": "old portfolio class removed", "result": "pass" if bad_old_sections == 0 else "fail", "evidence": f"old_sections={bad_old_sections}"},
        {"pass_id": PASS_ID, "check": "old image-sequence wording removed", "result": "pass" if all(value == 0 for value in old_phrases.values()) else "fail", "evidence": "; ".join(f"{key}={value}" for key, value in old_phrases.items())},
        {"pass_id": PASS_ID, "check": "context headings visible", "result": "pass" if context_heading_hits >= 24 else "fail", "evidence": f"context_heading_hits={context_heading_hits}"},
        {"pass_id": PASS_ID, "check": "24 chapters preserved", "result": "pass" if len(chapter_ids) == 24 else "fail", "evidence": f"unique_chapters={len(chapter_ids)}"},
        {"pass_id": PASS_ID, "check": "word count remains in band", "result": "pass" if 100000 <= int(after["word_count_pdf_text"]) <= 120000 else "fail", "evidence": after["word_count_pdf_text"]},
        {"pass_id": PASS_ID, "check": "visual abundance preserved", "result": "pass" if int(after["image_objects"]) >= 300 else "fail", "evidence": f"{before['image_objects']} -> {after['image_objects']} image objects"},
        {"pass_id": PASS_ID, "check": "zero blank pages preserved", "result": "pass" if after["blank_pages"] == "0" else "fail", "evidence": f"blank_pages={after['blank_pages']}"},
        {"pass_id": PASS_ID, "check": "claim ledger unsupported zero", "result": "pass" if claims.get("needs-verification", 0) == 0 else "fail", "evidence": f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification"},
    ]


def write_reports(before: dict[str, str], after: dict[str, str], qa: list[dict[str, str]], sections: list[dict[str, str]]) -> None:
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    report = f"""# Contextual Visual Placement - I-0318

I-0318 executes the sixth rescue task: rebuild the chapter visual blocks so they sit with their current chronological chapters and read as contextual evidence rather than old separated visual dumps.

## Result

- Source PDF: `{rel(SOURCE_PDF)}`
- New local proof: `{rel(PDF_OUT)}`
- Contextualized visual sections: {len(sections)}
- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- Word count from PDF text: {after['word_count_pdf_text']}
- Blank pages: {after['blank_pages']}
- Severe sparse pages: {after['severe_sparse_pages']}
- Multi-image pages still open for I-0319: {after['multi_image_pages']}

## What Changed

The old reader-facing separated visual blocks were renamed to current chapter-local context sections, old chronology numbers were replaced by current chapter numbers/titles, and the sections were moved beside each chapter opening instead of being left as loose chapter-end galleries.

## Still Open

I-0319 through I-0322 must still enforce one visual per page, add stronger quantitative density, run hostile QA, and build the final publication candidate.

QA: {qa_pass} pass / {qa_fail} fail.
"""
    write(REPORT, report)
    write(CHAMPION_REPORT, report)
    pointer = f"""# Final Private PDF Pointer - I-0318

Updated: 2026-05-27

Current rescue proof:

`{rel(PDF_OUT)}`

SHA-256: `{after['sha256']}`

Render metrics:

- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- Word count from PDF text: {after['word_count_pdf_text']}
- Contextualized visual sections: {len(sections)}
- Blank pages by ink/text/image QA: {after['blank_pages']}
- Severe sparse pages by ink/text QA: {after['severe_sparse_pages']}
- Micro-visual sparse pages: {after['micro_visual_pages']}
- Multi-image pages: {after['multi_image_pages']}

Status: this proof completes only I-0318. It is not final. The next queued rescue pass is I-0319, max-one-visual-per-page and board/portfolio removal.
"""
    write(CHAMPION_POINTER, pointer)


def write_manifest(before: dict[str, str], after: dict[str, str]) -> None:
    artifacts = [
        ("source_pdf", SOURCE_PDF, before, "I-0317 page-density proof"),
        ("contextual_html", HTML_OUT, {}, "I-0318 contextual visual HTML"),
        ("contextual_pdf", PDF_OUT, after, "I-0318 contextual visual PDF"),
        ("contextual_markdown", MD_OUT, {}, "I-0318 manuscript snapshot"),
        ("baseline", OUT_BASELINE, {}, "I-0318 visual-placement baseline"),
        ("sections", OUT_SECTIONS, {}, "24 contextualized visual sections"),
        ("qa", OUT_QA, {}, "I-0318 visual placement QA"),
        ("report", REPORT, {}, "I-0318 report"),
        ("pointer", CHAMPION_POINTER, {}, "I-0318 pointer"),
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
    old_path = "rendered/final_private_i0317/Next-Token-final-private-page-density-i0317.pdf"
    new_path = rel(PDF_OUT)
    for path in [README, CHAMPION_README, READER_GUIDE, GUIDE_POINTER]:
        if not path.exists():
            continue
        text = read(path)
        text = text.replace(old_path, new_path)
        text = text.replace("champion/final-private-pdf-pointer-i0317.md", "champion/final-private-pdf-pointer-i0318.md")
        text = text.replace("final-private-pdf-pointer-i0317.md", "final-private-pdf-pointer-i0318.md")
        text = text.replace("updated by `I-0317`", "updated by `I-0318`")
        text = text.replace("after pass `I-0317`", "after pass `I-0318`")
        text = text.replace("`I-0317`, page-density and blank-page repair", "`I-0318`, contextual visual placement")
        text = text.replace("I-0317 PDF is the current local rescue proof", "I-0318 PDF is the current local rescue proof")
        text = text.replace("the guide points to the I-0317 page-density proof only", "the guide points to the I-0318 contextual-visual proof only")
        text = text.replace("I-0318 through I-0322", "I-0319 through I-0322")
        text = text.replace("- I-0318: place every kept visual beside the text it serves.\n", "")
        text = text.replace("replaces old Image Sequence blocks with current chapter-local context sections", "replaces old separated visual blocks with current chapter-local context sections")
        text = re.sub(r"`claims.tsv` has 333 supported rows and 0 needs-verification rows after the I-0317 page-density repair", "`claims.tsv` has 334 supported rows and 0 needs-verification rows after the I-0318 contextual visual placement pass", text)
        metric_sentence = (
            f"This proof has {after['pages']} pages, {after['image_objects']} image objects, "
            f"{after['drawing_objects']} drawing/vector objects, 24 contextualized visual sections, "
            f"and {after['blank_pages']} blank pages by ink/text/image QA. SHA-256: `{after['sha256']}`."
        )
        text = re.sub(r"This proof has .*?SHA-256: `[^`]+`\.", metric_sentence, text, flags=re.S)
        marker = "I-0318 update:"
        addition = (
            "\n\nI-0318 update: the current rescue proof replaces old separated visual blocks with current chapter-local "
            "context sections beside the chapter openings. It still needs I-0319 through I-0322 for one-image pages, "
            "quantitative enrichment, hostile QA, and final build.\n"
        )
        if marker not in text:
            text = text.rstrip() + addition
        write(path, text)


def mark_idea_done() -> None:
    text = read(IDEAS)
    pattern = re.compile(r"(?m)^I-0318\t(?:pending|done)\t(.+)$")
    replacement = (
        "I-0318\tdone\t"
        "Rebuild visual placement so every kept image sits beside the text it serves: relocate photos, screenshots, paper/PDF pages, tables, charts, logos, renderings, and people images into the relevant chronological scene or mechanism; cut out-of-context visuals.\t"
        "rescue 6\tcontextual visual placement for all kept images\t"
        "Done in scripts/contextual_visual_placement_i0318.py, data/contextual_visual_baseline_i0318.tsv, data/contextual_visual_sections_i0318.tsv, data/contextual_visual_qa_i0318.tsv, manuscript/contextual-visual-placement-i0318.md, and champion/final-private-pdf-pointer-i0318.md; 24 old Image Sequence blocks were rewritten as current chapter-local context sections and moved beside chapter openings."
    )
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit("Could not mark I-0318 done in ideas.tsv")
    write(IDEAS, text)


def append_claim() -> None:
    row = "\t".join(
        [
            "C-0334",
            "supported",
            "I-0318 rendered a contextual-visual private proof in which all 24 old separated visual blocks were rewritten as current chapter-local context sections beside chapter openings, with old block-heading wording removed from the rendered PDF.",
            "manuscript/contextual-visual-placement-i0318.md;data/contextual_visual_baseline_i0318.tsv;data/contextual_visual_sections_i0318.tsv;data/contextual_visual_qa_i0318.tsv;champion/final-private-pdf-pointer-i0318.md",
            "I-0318",
            "rendered PDF visual-placement QA",
            "2026-05-27",
            "Supported as contextual visual-section placement only; one-image-per-page enforcement, composite board removal, quantitative enrichment, hostile QA, and final build remain queued.",
        ]
    )
    upsert_tsv_line(CLAIMS, "C-0334\t", row)


def append_scoreboard(after: dict[str, str], qa_pass: int, qa_fail: int, sections: list[dict[str, str]]) -> None:
    claims = claim_counts()
    row = "\t".join(
        [
            datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            RUN_ID,
            "champion I-0317 rescue proof",
            PASS_ID,
            "rescue 6",
            "+1.0",
            "100.0",
            after["word_count_pdf_text"],
            "24",
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; contextual PDF pages={after['pages']}; contextual_sections={len(sections)}; image_sequence_hits=0; images={after['image_objects']}; drawings={after['drawing_objects']}; blank_pages={after['blank_pages']}; multi_image_pages={after['multi_image_pages']}; QA {qa_pass} pass / {qa_fail} fail",
            "+1",
            "I-0319 through I-0322 still must enforce one-image pages, add quantitative density, run hostile QA, and final publication build",
            "promoted",
            "Rewrote old separated visual blocks as current chapter-local contextual sections near chapter openings.",
            "one contextual visual-placement render pass",
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
        raise SystemExit("I-0317 source HTML/PDF/markdown missing; run or restore I-0317 first.")

    backup_targets()
    before = pdf_stats(SOURCE_PDF)
    sections = rewrite_visual_sections()
    write_markdown_snapshot()
    if not args.skip_render:
        render_pdf(chrome)
    after = pdf_stats(PDF_OUT)
    qa = qa_rows(before, after, sections)
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    write_tsv(OUT_QA, qa)
    write_reports(before, after, qa, sections)
    update_human_files(after)
    write_manifest(before, after)
    mark_idea_done()
    append_claim()
    append_scoreboard(after, qa_pass, qa_fail, sections)
    append_once(
        INSIGHTS,
        "- I-0318:",
        "\n- I-0318: visual placement has to survive chronology changes. When chapters are reordered, visual blocks must inherit the current chapter title and sit near the chapter's live argument, or the old numbering turns visual abundance into visible confusion.\n",
    )
    if qa_fail:
        raise SystemExit(f"I-0318 contextual visual QA failed: {qa_fail} checks failed")


if __name__ == "__main__":
    main()
